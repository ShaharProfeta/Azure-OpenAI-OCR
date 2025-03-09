import os
import json
from dotenv import load_dotenv
from azure.ai.formrecognizer import DocumentAnalysisClient
from azure.core.credentials import AzureKeyCredential

# Load environment variables
load_dotenv()

# Retrieve credentials
ENDPOINT = os.getenv("AZURE_AI_SERVICES_URL")
API_KEY = os.getenv("AZURE_AI_SERVICES_KEY")

# Initialize Document Analysis Client (Using prebuilt-layout for OCR)
client = DocumentAnalysisClient(endpoint=ENDPOINT, credential=AzureKeyCredential(API_KEY))

def format_table_as_key_value(table_rows):
    """
    Converts a table into a key-value format.
    """
    if len(table_rows) < 2:
        return ""  # If the table is incomplete, return nothing

    headers = table_rows[0]  # First row is headers
    values = table_rows[1]   # Second row contains actual values

    key_value_pairs = [f"{headers[i]} - {values[i]}" for i in range(len(headers))]
    
    return "\n".join(key_value_pairs)  # Join them as key-value lines

def analyze_document(file_path):
    """
    Uses 'prebuilt-layout' to perform OCR and extract structured text with key-value formatted tables.
    """
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"File not found: {file_path}")

    with open(file_path, "rb") as document:
        poller = client.begin_analyze_document("prebuilt-layout", document)  # ✅ Using Layout OCR
        result = poller.result()

    # ✅ Extract OCR text (full document text)
    extracted_text = result.content.strip()

    # ✅ Extract tables and convert them to key-value format
    tables_formatted = []
    if hasattr(result, "tables"):
        for table in result.tables:
            table_data = {}  # Store row-wise data
            max_cols = max(cell.column_index for cell in table.cells) + 1  # Number of columns

            # Organize table data into rows
            for cell in table.cells:
                row_index, col_index, text = cell.row_index, cell.column_index, cell.content.strip()

                if row_index not in table_data:
                    table_data[row_index] = [""] * max_cols  # Ensure all rows have the same column count
                table_data[row_index][col_index] = text

            # Convert dictionary to sorted list of lists (ensuring correct order)
            sorted_table = [table_data[row] for row in sorted(table_data.keys())]

            # Convert to key-value format
            formatted_table = format_table_as_key_value(sorted_table)
            tables_formatted.append(formatted_table)

    # ✅ Combine OCR text and structured tables into a single file
    output_path = f"output/{os.path.basename(file_path)}_layout_combined.txt"
    os.makedirs("output", exist_ok=True)

    with open(output_path, "w", encoding="utf-8") as combined_file:
        combined_file.write("✅ Extracted OCR Text:\n")
        combined_file.write(extracted_text + "\n\n")

        if tables_formatted:
            combined_file.write("✅ Extracted Key-Value Data:\n")
            for idx, table in enumerate(tables_formatted, 1):
                combined_file.write(f"\n🔹 Table {idx}:\n")
                combined_file.write(table + "\n")

    print("\n✅ Layout OCR Extraction Complete!")
    print(f"✅ Combined file saved to: {output_path}")

    return {
        "text": extracted_text,
        "tables": tables_formatted
    }