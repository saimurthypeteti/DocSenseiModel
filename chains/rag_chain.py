"""RAG and grounded generation chains."""

from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI

from config import get_settings
from models.schemas import Citation, DocumentChunk
from prompts.templates import EXPLAIN_TEMPLATE, RAG_TEMPLATE, SUMMARY_TEMPLATE, SYSTEM_PROMPT
from utils.errors import MissingApiKeyError

UNKNOWN_ANSWER = "I do not know. The answer is not available in the uploaded document."


class LLMFactory:
    """Create OpenAI-compatible chat clients."""

    @staticmethod
    def create() -> ChatOpenAI:
        settings = get_settings()
        if not settings.llm_api_key:
            raise MissingApiKeyError("Missing LLM_API_KEY in environment.")
        return ChatOpenAI(
            api_key=settings.llm_api_key,
            base_url=settings.llm_base_url,
            model=settings.llm_model,
            temperature=settings.llm_temperature,
        )


class GroundedGenerationChain:
    """Generate answers from retrieved document context only."""

    def __init__(self) -> None:
        self.llm = LLMFactory.create()

    def answer(self, question: str, chunks: list[DocumentChunk]) -> str:
        """Answer a question from retrieved chunks."""
        if not chunks:
            return UNKNOWN_ANSWER
        context = self._format_context(chunks)
        prompt = ChatPromptTemplate.from_template(RAG_TEMPLATE)
        response = (prompt | self.llm).invoke(
            {
                "system_prompt": SYSTEM_PROMPT,
                "context": context,
                "question": question,
            }
        )
        text = str(response.content).strip()
        return text or UNKNOWN_ANSWER

    def summarize(self, summary_type: str, chunks: list[DocumentChunk]) -> str:
        """Create a document, page, or chapter summary."""
        if not chunks:
            return UNKNOWN_ANSWER
        prompt = ChatPromptTemplate.from_template(SUMMARY_TEMPLATE)
        response = (prompt | self.llm).invoke(
            {
                "system_prompt": SYSTEM_PROMPT,
                "summary_type": summary_type,
                "context": self._format_context(chunks),
            }
        )
        return str(response.content).strip() or UNKNOWN_ANSWER

    def explain(self, level: str, chunks: list[DocumentChunk]) -> str:
        """Explain selected retrieved chunks at a requested level."""
        if not chunks:
            return UNKNOWN_ANSWER
        prompt = ChatPromptTemplate.from_template(EXPLAIN_TEMPLATE)
        response = (prompt | self.llm).invoke(
            {
                "system_prompt": SYSTEM_PROMPT,
                "level": level,
                "context": self._format_context(chunks),
            }
        )
        return str(response.content).strip() or UNKNOWN_ANSWER

    @staticmethod
    def citations_for(chunks: list[DocumentChunk]) -> list[Citation]:
        """Convert chunks to unique citations."""
        seen: set[tuple[str, int, str]] = set()
        citations: list[Citation] = []
        for chunk in chunks:
            key = (chunk.document_name, chunk.page_number, chunk.chunk_id)
            if key in seen:
                continue
            seen.add(key)
            citations.append(Citation(*key))
        return citations

    @staticmethod
    def _format_context(chunks: list[DocumentChunk]) -> str:
        return "\n\n".join(
            (
                f"Document: {chunk.document_name}\n"
                f"Page: {chunk.page_number}\n"
                f"Chunk ID: {chunk.chunk_id}\n"
                f"Text: {chunk.text}"
            )
            for chunk in chunks
        )
