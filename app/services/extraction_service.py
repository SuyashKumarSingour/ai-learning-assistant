from pypdf import PdfReader


def extract_pdf(file_path: str) -> str:
    reader = PdfReader(file_path)

    text_parts = []

    for page in reader.pages:
        page_text = page.extract_text()

        if page_text:
            text_parts.append(page_text)

    text = "\n".join(text_parts).strip()

    if not text:
        raise ValueError("The PDF does not contain extractable text.")

    return text