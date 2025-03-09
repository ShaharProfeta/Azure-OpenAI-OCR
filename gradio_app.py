import gradio as gr
import pdfplumber
from openai_client import extract_structured_data

# Function to extract text from PDFs while keeping newlines
def extract_text_from_pdf(pdf_file):
    with pdfplumber.open(pdf_file) as pdf:
        text = "\n".join([page.extract_text() for page in pdf.pages if page.extract_text()])
    return text.strip() if text else None


# Gradio function to handle uploads & process text
def process_uploaded_file(pdf_file):
    if not pdf_file:
        return "", {"error": "No file uploaded"}
    
    extracted_text = extract_text_from_pdf(pdf_file)
    
    if not extracted_text:
        return "", {"error": "No text extracted from PDF. Try another file."}

    print("Extracted OCR Text (One Line):", extracted_text)  # Debugging step

    structured_data = extract_structured_data(extracted_text)

    # Ensure two outputs are always returned
    return extracted_text, structured_data


# Define the Gradio interface
with gr.Blocks() as demo:
    gr.Markdown("# 📝 PDF Form Extractor with Azure OpenAI")
    
    with gr.Row():
        pdf_input = gr.File(label="Upload a PDF Form", file_types=[".pdf"])
    
    extracted_text_output = gr.Textbox(label="Extracted OCR Text (One Line)", lines=2)
    output_json = gr.JSON(label="Extracted Data (JSON Format)")
    
    process_button = gr.Button("Extract Data")
    process_button.click(process_uploaded_file, inputs=[pdf_input], outputs=[extracted_text_output, output_json])

# Run the Gradio app
if __name__ == "__main__":
    demo.launch(share=True)
