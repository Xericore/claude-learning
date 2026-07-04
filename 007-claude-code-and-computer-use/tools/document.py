import os
from markitdown import MarkItDown, StreamInfo
from io import BytesIO
from pydantic import Field


def binary_document_to_markdown(binary_data: bytes, file_type: str) -> str:
    """Converts binary document data to markdown-formatted text."""
    md = MarkItDown()
    file_obj = BytesIO(binary_data)
    stream_info = StreamInfo(extension=file_type)
    result = md.convert(file_obj, stream_info=stream_info)
    return result.text_content


def document_path_to_markdown(
    file_path: str = Field(
        description="Path to the PDF or DOCX file to read and convert to markdown"
    ),
) -> str:
    """Reads a PDF or DOCX file from disk and converts its content to markdown-formatted text.

    Detects the document type from the file path's extension (case-insensitive),
    reads the file's contents, and converts it to markdown.

    When to use:
    - When you have a path to a PDF or DOCX file on disk and want its content as markdown.

    When not to use:
    - When you already have the document's binary contents in memory; use
      binary_document_to_markdown instead.

    Examples:
    >>> document_path_to_markdown("/path/to/document.pdf")
    '# Document Title\\n\\nDocument content...'
    >>> document_path_to_markdown("/path/to/document.docx")
    '# Document Title\\n\\nDocument content...'
    """
    file_type = os.path.splitext(file_path)[1].lstrip(".").lower()
    with open(file_path, "rb") as f:
        binary_data = f.read()
    return binary_document_to_markdown(binary_data, file_type)
