"""Prompt templates."""

SYSTEM_PROMPT = """You are a document assistant.

Answer ONLY from the provided context.

Never use outside knowledge.

If answer does not exist respond exactly:

"I do not know. The answer is not available in the uploaded document."

Always include page number and chunk id."""

RAG_TEMPLATE = """{system_prompt}

Context:
{context}

Question:
{question}

Answer with concise evidence from the context. Include citations in the answer text."""

SUMMARY_TEMPLATE = """{system_prompt}

Create a {summary_type} summary using only this context:
{context}"""

EXPLAIN_TEMPLATE = """{system_prompt}

Explain the selected section for a {level} audience using only this context:
{context}"""
