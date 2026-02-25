import pymupdf


def extract_text_from_pdf(pdf_bytes: bytes) -> str:
    """Extract text from PDF bytes using PyMuPDF.

    Args:
        pdf_bytes: PDF file content as bytes.

    Returns:
        Extracted text from all pages of the PDF.
    """
    doc = pymupdf.open(stream=pdf_bytes, filetype="pdf")

    try:
        text = ""
        for page in doc:
            # sort=True sorts text blocks by position (layout preservation)
            text += page.get_text("text", sort=True) + "\n"
        return text
    finally:
        doc.close()
