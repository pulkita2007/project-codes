import os
import google.generativeai as genai
from dotenv import load_dotenv # Import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Configure the Gemini API key
# Ensure GEMINI_API_KEY is set in your environment variables
genai.configure(api_key=os.environ.get("GEMINI_API_KEY"))

# Function to summarize a given research paper text based on style and length preferences
def summarize_text(text, style, length):
    instructions = []

    # Add summary formatting instructions based on the selected style
    if style == "Bullet Points":
        instructions.append("Write the summary in bullet points.")
    elif style == "Section-wise Summary":
        instructions.append("Summarize under headings: Abstract, Methodology, Results, and Conclusion.")
    else:
        instructions.append("Write a simple and concise summary suitable for beginners.")

    # Add length constraint instructions
    if "Short" in length:
        instructions.append("Limit the summary to around 100 words.")
    elif "Medium" in length:
        instructions.append("Limit the summary to around 300 words.")
    elif "Long" in length:
        instructions.append("You can go up to 500 words for this summary.")

    # Avoid overly technical language
    instructions.append("Avoid technical jargon where possible.")

    # Build the final prompt string
    prompt = "📌 Summarize the following research paper with the instructions below:\n\n"
    prompt += "\n".join(f"- {instr}" for instr in instructions)
    prompt += f"\n\n📄 Paper:\n{text}"

    # Initialize the Gemini GenerativeModel
    model = genai.GenerativeModel(model_name="gemini-1.5-flash")


    try:
        # Call Gemini's generate_content API to generate the summary
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        return f"An error occurred while generating the summary: {e}"


# Function to allow users to ask questions about the paper content
def ask_question_about_text(text, question):
    """
    Takes paper text and a user's question,
    sends them to the Gemini API,
    and returns a relevant answer.
    """

    # Build the prompt by combining paper content and the user's question
    # Using a truncated text for efficiency as per your original code
    prompt = f"""
You are an AI assistant specialized in reading academic research papers.
Based on the following content of a research paper, answer the user's question clearly and accurately.

📄 Paper Content:
{text[:3000]}  # Only use the first 3000 characters for efficiency

❓ Question: {question}
"""
    # Initialize the Gemini GenerativeModel
    model = genai.GenerativeModel('gemini-1.5-flash')

    try:
        # Send the prompt to the generate_content API
        response = model.generate_content(prompt)
        # Return the model's answer
        return response.text
    except Exception as e:
        return f"An error occurred while answering the question: {e}"