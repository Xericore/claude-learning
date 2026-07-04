import os
import shutil
import pytest
from tools.document import binary_document_to_markdown, document_path_to_markdown


class TestBinaryDocumentToMarkdown:
    # Define fixture paths
    FIXTURES_DIR = os.path.join(os.path.dirname(__file__), "fixtures")
    DOCX_FIXTURE = os.path.join(FIXTURES_DIR, "mcp_docs.docx")
    PDF_FIXTURE = os.path.join(FIXTURES_DIR, "mcp_docs.pdf")

    def test_fixture_files_exist(self):
        """Verify test fixtures exist."""
        assert os.path.exists(self.DOCX_FIXTURE), (
            f"DOCX fixture not found at {self.DOCX_FIXTURE}"
        )
        assert os.path.exists(self.PDF_FIXTURE), (
            f"PDF fixture not found at {self.PDF_FIXTURE}"
        )

    def test_binary_document_to_markdown_with_docx(self):
        """Test converting a DOCX document to markdown."""
        # Read binary content from the fixture
        with open(self.DOCX_FIXTURE, "rb") as f:
            docx_data = f.read()

        # Call function
        result = binary_document_to_markdown(docx_data, "docx")

        # Basic assertions to check the conversion was successful
        assert isinstance(result, str)
        assert len(result) > 0
        # Check for typical markdown formatting - this will depend on your actual test file
        assert "#" in result or "-" in result or "*" in result

    def test_binary_document_to_markdown_with_pdf(self):
        """Test converting a PDF document to markdown."""
        # Read binary content from the fixture
        with open(self.PDF_FIXTURE, "rb") as f:
            pdf_data = f.read()

        # Call function
        result = binary_document_to_markdown(pdf_data, "pdf")

        # Basic assertions to check the conversion was successful
        assert isinstance(result, str)
        assert len(result) > 0
        # Check for typical markdown formatting - this will depend on your actual test file
        assert "#" in result or "-" in result or "*" in result


class TestDocumentPathToMarkdown:
    # Define fixture paths
    FIXTURES_DIR = os.path.join(os.path.dirname(__file__), "fixtures")
    DOCX_FIXTURE = os.path.join(FIXTURES_DIR, "mcp_docs.docx")
    PDF_FIXTURE = os.path.join(FIXTURES_DIR, "mcp_docs.pdf")

    def test_document_path_to_markdown_with_docx(self):
        """Test converting a DOCX document to markdown from a file path."""
        result = document_path_to_markdown(self.DOCX_FIXTURE)

        assert isinstance(result, str)
        assert len(result) > 0
        assert "#" in result or "-" in result or "*" in result

    def test_document_path_to_markdown_with_pdf(self):
        """Test converting a PDF document to markdown from a file path."""
        result = document_path_to_markdown(self.PDF_FIXTURE)

        assert isinstance(result, str)
        assert len(result) > 0
        assert "#" in result or "-" in result or "*" in result

    @pytest.mark.parametrize(
        "fixture_path, file_type",
        [(DOCX_FIXTURE, "docx"), (PDF_FIXTURE, "pdf")],
    )
    def test_document_path_to_markdown_matches_binary_conversion(
        self, fixture_path, file_type
    ):
        """Path-based conversion should match converting the same bytes directly."""
        with open(fixture_path, "rb") as f:
            data = f.read()
        expected = binary_document_to_markdown(data, file_type)

        result = document_path_to_markdown(fixture_path)

        assert result == expected

    @pytest.mark.parametrize("fixture_path", [DOCX_FIXTURE, PDF_FIXTURE])
    def test_document_path_to_markdown_infers_file_type_from_extension(
        self, fixture_path
    ):
        """Should determine the document type from the path's extension alone,
        without requiring a separate file_type argument."""
        result = document_path_to_markdown(fixture_path)

        assert isinstance(result, str)
        assert len(result) > 0

    @pytest.mark.parametrize(
        "fixture_path, uppercase_name",
        [(DOCX_FIXTURE, "mcp_docs.DOCX"), (PDF_FIXTURE, "mcp_docs.PDF")],
    )
    def test_document_path_to_markdown_with_uppercase_extension(
        self, tmp_path, fixture_path, uppercase_name
    ):
        """Extension matching should be case-insensitive."""
        uppercase_path = tmp_path / uppercase_name
        shutil.copyfile(fixture_path, uppercase_path)

        result = document_path_to_markdown(str(uppercase_path))

        assert isinstance(result, str)
        assert len(result) > 0
