import streamlit as st
from pdf_reader import extract_text_from_pdf
from summarizer import summarize_text, ask_question_about_text
from io import BytesIO
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.enums import TA_JUSTIFY

# ---------------------- #
# Streamlit Page Config
# ---------------------- #
st.set_page_config(page_title="AI Research Paper Summarizer", layout="centered")

# ---------------------- #
# Title and Intro
# ---------------------- #
st.title("🧠 AI Research Paper Summarizer")
st.markdown("""
Welcome to the AI-powered research paper summarization tool.
Upload a PDF, choose how you'd like the summary to be presented, and get an instant, clean summary.
""")

# Initialize session state for text if not already present
if 'extracted_text' not in st.session_state:
    st.session_state.extracted_text = ""

# ---------------------- #
# Step 1 – Upload
# ---------------------- #
st.header("📄 1. Upload Research Paper")
uploaded_file = st.file_uploader("Upload a research paper PDF", type="pdf")

# ---------------------- #
# Step 2 – Choose Style
# ---------------------- #
st.header("🎯 2. Select Summary Style")
style = st.selectbox("Choose summary style:", [
    "Simple Summary",
    "Bullet Points",
    "Section-wise Summary"
])

# ---------------------- #
# Step 3 – Choose Length
# ---------------------- #
st.header("📏 3. Select Summary Length")
length = st.selectbox("Choose summary length:", [
    "Short (~100 words)",
    "Medium (~300 words)",
    "Long (~500+ words)"
])

# ---------------------- #
# Step 4 – Process PDF
# ---------------------- #
if uploaded_file:
    # Use BytesIO to handle the uploaded file directly without saving to disk
    # This is generally cleaner for Streamlit apps
    pdf_buffer = BytesIO(uploaded_file.read())
    st.success("✅ PDF uploaded successfully!")

    # Button: Summarize
    if st.button("🚀 Summarize"):
        with st.spinner("⏳ Extracting text and generating summary..."):
            st.session_state.extracted_text = extract_text_from_pdf(pdf_buffer)

            if st.session_state.extracted_text == "Could not extract text from PDF.":
                st.error("❗ Failed to extract text from the PDF. Please try another file or ensure it's not an image-only PDF.")
            else:
                # Truncate text for summarization as per original logic for efficiency
                summary = summarize_text(st.session_state.extracted_text[:3000], style, length)

                # Display the summary
                st.header("📋 4. Summary")
                st.write(summary)

                # Download as TXT
                txt_bytes = summary.encode('utf-8')
                st.download_button(
                    label="📄 Download Summary as TXT",
                    data=txt_bytes,
                    file_name="summary.txt",
                    mime="text/plain"
                )

                # Download as PDF using ReportLab
                # Create a BytesIO object to hold the PDF
                pdf_output_buffer = BytesIO()
                doc = SimpleDocTemplate(pdf_output_buffer, pagesize=letter)
                styles = getSampleStyleSheet()
                custom_style = ParagraphStyle(
                    name='CustomStyle',
                    parent=styles['Normal'],
                    fontSize=11,
                    leading=14,
                    alignment=TA_JUSTIFY,
                )

                story = []
                for paragraph_text in summary.split('\n'):
                    if paragraph_text.strip(): # Avoid adding empty paragraphs
                        story.append(Paragraph(paragraph_text, custom_style))
                        story.append(Spacer(1, 0.2 * 11)) # Add a small space between paragraphs

                doc.build(story)
                pdf_output_buffer.seek(0) # Rewind the buffer to the beginning

                st.download_button(
                    label="📝 Download Summary as PDF",
                    data=pdf_output_buffer.getvalue(),
                    file_name="summary.pdf",
                    mime="application/pdf"
                )

    # ---------------------- #
    # Step 5 – Chat with Paper 🧠💬
    # ---------------------- #
    st.header("💬 5. Chat with Paper")

    # Only show Q&A if text has been extracted
    if st.session_state.extracted_text:
        user_question = st.text_input("Ask a question about the paper:")

        # When the user submits a question
        if user_question:
            with st.spinner("🤖 Thinking..."):
                response = ask_question_about_text(st.session_state.extracted_text, user_question)

            st.success("📢 Answer:")
            st.write(response)
    else:
        st.info("Upload a PDF and click 'Summarize' first to enable chatting with the paper.")