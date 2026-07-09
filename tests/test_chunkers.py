from models.schemas import LoadedPage
from preprocessing.chunkers import ChunkStrategy, DocumentChunker


def test_fixed_chunking_adds_metadata():
    page = LoadedPage("sample.pdf", 2, "A" * 700, "uploads/sample.pdf")
    chunks = DocumentChunker(chunk_size=500, overlap=100).chunk_pages(
        [page],
        ChunkStrategy.FIXED,
    )

    assert len(chunks) == 2
    assert chunks[0].document_name == "sample.pdf"
    assert chunks[0].page_number == 2
    assert chunks[0].chunk_id == "sample.pdf:p2:c1"


def test_recursive_chunking_returns_content():
    page = LoadedPage("sample.docx", 1, "Heading\n\n" + "Body text. " * 80, "x")
    chunks = DocumentChunker().chunk_pages([page], ChunkStrategy.RECURSIVE)

    assert chunks
    assert all(chunk.text for chunk in chunks)
