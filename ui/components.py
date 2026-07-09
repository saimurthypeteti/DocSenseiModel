"""Reusable Streamlit UI components."""

from pathlib import Path

import streamlit as st

from models.schemas import AnswerResult, Citation, DocumentChunk


def render_logo() -> None:
    """Render project logo text."""
    st.image("assets/logo.svg", use_container_width=True)
    st.caption("Grounded document intelligence")


def render_answer(result: AnswerResult) -> None:
    """Render answer, citations, and retrieval details."""
    st.subheader("Answer")
    st.write(result.answer)
    st.caption(f"Response time: {result.response_time_seconds:.2f}s")

    st.subheader("Citations")
    if not result.citations:
        st.info("No citations returned.")
    for citation in result.citations:
        chunk = _find_chunk_for_citation(citation, result.retrieved_chunks)
        with st.container(border=True):
            st.markdown(f"**Document:** {citation.document_name}")
            st.markdown(f"**Page:** {citation.page_number}")
            st.markdown(f"**Chunk ID:** `{citation.chunk_id}`")
            if chunk:
                with st.expander("Show cited text"):
                    st.write(chunk.text)
                _render_source_download(chunk)

    render_retrieved_chunks(result.retrieved_chunks)


def render_retrieved_chunks(chunks: list[DocumentChunk]) -> None:
    """Render expandable retrieved chunks."""
    st.subheader("Retrieved Chunks")
    for chunk in chunks:
        label = f"{chunk.document_name} | Page {chunk.page_number} | {chunk.chunk_id}"
        with st.expander(label):
            st.write(chunk.text)


def render_search_results(chunks: list[DocumentChunk]) -> None:
    """Render semantic search results."""
    if not chunks:
        st.info("No matching chunks found.")
    for chunk in chunks:
        with st.expander(f"{chunk.document_name} | Page {chunk.page_number}"):
            st.caption(f"Chunk ID: {chunk.chunk_id}")
            st.write(chunk.text)


def _find_chunk_for_citation(
    citation: Citation,
    chunks: list[DocumentChunk],
) -> DocumentChunk | None:
    """Find the retrieved chunk that produced a citation."""
    for chunk in chunks:
        if (
            chunk.document_name == citation.document_name
            and chunk.page_number == citation.page_number
            and chunk.chunk_id == citation.chunk_id
        ):
            return chunk
    return None


def _render_source_download(chunk: DocumentChunk) -> None:
    """Render a download button for the cited source document."""
    source = Path(chunk.source)
    if not source.exists() or not source.is_file():
        st.caption("Source file is not available for download in this session.")
        return

    st.download_button(
        label="Download source document",
        data=source.read_bytes(),
        file_name=chunk.document_name,
        mime=_mime_type(source.suffix),
        key=f"download-{chunk.chunk_id}",
    )


def _mime_type(suffix: str) -> str:
    """Return a browser-friendly MIME type."""
    if suffix.lower() == ".pdf":
        return "application/pdf"
    if suffix.lower() == ".docx":
        return (
            "application/vnd.openxmlformats-officedocument."
            "wordprocessingml.document"
        )
    return "application/octet-stream"
