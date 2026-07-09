"""Streamlit entry point for DocSensei."""

import logging

import streamlit as st

from config import get_settings
from preprocessing.chunkers import ChunkStrategy
from services.document_service import DocumentService
from services.explain_service import ExplainService
from services.qa_service import QAService
from services.search_service import SearchService
from services.summary_service import SummaryService
from ui.components import render_answer, render_logo, render_search_results
from utils.errors import DocSenseiError, MissingApiKeyError
from utils.logging_config import configure_logging

configure_logging()
logger = logging.getLogger(__name__)
settings = get_settings()

st.set_page_config(page_title="DocSensei", page_icon="DS", layout="wide")

if "messages" not in st.session_state:
    st.session_state.messages = []

with st.sidebar:
    render_logo()
    uploaded_files = st.file_uploader(
        "Upload PDF or DOCX files",
        type=["pdf", "docx"],
        accept_multiple_files=True,
    )
    strategy = st.selectbox(
        "Chunk strategy",
        options=[ChunkStrategy.FIXED, ChunkStrategy.RECURSIVE],
        format_func=lambda item: item.value,
    )

    document_service = DocumentService()
    if st.button("Create Index", type="primary", use_container_width=True):
        if not uploaded_files:
            st.warning("Upload at least one PDF or DOCX file.")
        else:
            try:
                progress = st.progress(0)
                progress.progress(25)
                count = document_service.index_uploads(uploaded_files, strategy)
                progress.progress(100)
                st.success(f"Indexed {count} chunks.")
            except DocSenseiError as exc:
                logger.exception("Indexing failed")
                st.error(str(exc))

    if st.button("Clear Database", use_container_width=True):
        document_service.clear_database()
        st.success("Vector database cleared.")

    try:
        st.metric("Indexed vectors", document_service.indexed_count())
    except DocSenseiError:
        st.metric("Indexed vectors", 0)

st.title("DocSensei")
st.caption("Ask questions and receive answers grounded only in uploaded documents.")

tab_chat, tab_search, tab_summary, tab_explain = st.tabs(
    ["Chat", "Semantic Search", "Summary", "Explain"]
)

with tab_chat:
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.write(message["content"])

    question = st.chat_input("Ask a question about the uploaded documents")
    if question:
        st.session_state.messages.append({"role": "user", "content": question})
        with st.chat_message("user"):
            st.write(question)
        with st.chat_message("assistant"):
            try:
                with st.spinner("Retrieving evidence and generating answer..."):
                    result = QAService().answer(question)
                render_answer(result)
                st.session_state.messages.append(
                    {"role": "assistant", "content": result.answer}
                )
            except MissingApiKeyError as exc:
                st.error(str(exc))
            except Exception as exc:
                logger.exception("Question answering failed")
                st.error(f"Unable to answer: {exc}")

with tab_search:
    search_query = st.text_input("Semantic search query")
    if st.button("Search", use_container_width=False) and search_query:
        try:
            render_search_results(SearchService().search(search_query))
        except Exception as exc:
            logger.exception("Search failed")
            st.error(f"Unable to search: {exc}")

with tab_summary:
    summary_type = st.selectbox(
        "Summary type",
        ["Document Summary", "Page Summary", "Chapter Summary"],
    )
    summary_query = st.text_input(
        "Summary focus",
        value="Summarize the uploaded document",
    )
    if st.button("Generate Summary") and summary_query:
        try:
            with st.spinner("Generating grounded summary..."):
                st.write(SummaryService().summarize(summary_query, summary_type))
        except Exception as exc:
            logger.exception("Summary failed")
            st.error(f"Unable to summarize: {exc}")

with tab_explain:
    section_query = st.text_input("Section to explain")
    level = st.segmented_control(
        "Level",
        options=["Beginner", "Intermediate", "Advanced"],
        default="Beginner",
    )
    if st.button("Explain Section") and section_query:
        try:
            with st.spinner("Preparing explanation..."):
                st.write(ExplainService().explain(section_query, level))
        except Exception as exc:
            logger.exception("Explanation failed")
            st.error(f"Unable to explain: {exc}")

