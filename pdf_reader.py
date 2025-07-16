import PyPDF2
from io import BytesIO

def extract_text_from_pdf(pdf_file_object):
    """
    Extracts text from a given PDF file object (BytesIO or file path).
    """
    text = ""
    try:
        # Check if the input is a BytesIO object (from Streamlit upload)
        if isinstance(pdf_file_object, BytesIO):
            pdf_file_object.seek(0) # Ensure the buffer is at the beginning
            reader = PyPDF2.PdfReader(pdf_file_object)
        else: # Assume it's a file path if not BytesIO (less common in this app's flow but good for robustness)
            with open(pdf_file_object, "rb") as file:
                reader = PyPDF2.PdfReader(file)

        for page_num in range(len(reader.pages)):
            page = reader.pages[page_num]
            page_text = page.extract_text()
            if page_text:
                text += page_text + "\n" # Add a newline for better readability between pages

        if not text.strip(): # If text is empty or just whitespace after extraction
            return "Could not extract text from PDF or PDF is image-only."
        return text

    except Exception as e:
        print(f"Error extracting text from PDF: {e}")
        # Provide a more specific message if it's likely an image-only PDF
        if "PDF object is not a file object" in str(e) or "Illegal character in XREF table" in str(e):
             return "Failed to extract text from the PDF. It might be image-only, corrupted, or password-protected."
        return "Could not extract text from PDF."