# AI-Powered Document Processing System

## 📌 Overview

This project is an **AI-powered document processing system** that leverages **Azure AI Services** for Optical Character Recognition (OCR) and **Azure OpenAI** for extracting structured information. It features a **Gradio-based frontend UI** and **automated testing**.

## 🚀 Features

- ✅ **Extracts structured data from PDF forms** using Azure Document Intelligence.
- ✅ **Utilizes GPT-4o for advanced field extraction and formatting.**
- ✅ **Provides a user-friendly Gradio UI for document upload and analysis.**
- ✅ **Supports multi-language processing (Hebrew & English).**

## 🏗 Project Structure

```
📂 project_root
│── 📜 .env                     # Environment variables (Azure AI & OpenAI credentials)
│── 📜 analyze.py               # Performs OCR and extracts structured data
│── 📜 gradio_app.py            # Gradio-based frontend for document upload
│── 📜 openai_client.py         # Handles communication with Azure OpenAI
│── 📜 test_analyze.py          # Unit tests for document processing
│── 📜 test_api.py              # API tests for Azure OCR
│── 📜 test_openai.py           # Unit tests for OpenAI field extraction
│── 📜 requirements.txt         # Required dependencies
│── 📜 README.md                # Project documentation
```

## 🛠 Setup & Installation

### 1️⃣ Prerequisites

- Python 3.8+
- Azure AI Services & OpenAI credentials
- Required Python packages (listed in `requirements.txt`)

### 2️⃣ Clone the Repository

```bash
git clone https://github.com/your-repo/your-project.git
cd your-project
```

### 3️⃣ Install Dependencies

```bash
pip install -r requirements.txt
```

### 4️⃣ Configure Environment Variables

Create a `.env` file and add your **Azure AI & OpenAI** credentials:

```ini
# Azure AI Services
AZURE_AI_SERVICES_URL=https://your-ai-service-url/
AZURE_AI_SERVICES_KEY=your_api_key

# Azure OpenAI API
AZURE_OPENAI_ENDPOINT=https://your-openai-endpoint/
AZURE_OPENAI_KEY=your_api_key
AZURE_OPENAI_VERSION=2024-02-01
AZURE_OPENAI_DEPLOYMENT=gpt-4o
```

### 5️⃣ Start the Gradio UI

```bash
python gradio_app.py
```

This will launch an interactive UI for uploading PDFs and viewing extracted data.

### 6️⃣ Run Tests

To validate functionality, run:

```bash
python test_analyze.py
python test_api.py
python test_openai.py
```

## 🎨 Frontend UI

The **Gradio-based UI** allows users to:

- Upload a **PDF document**.
- Receive **extracted text & structured JSON data**.
- Visualize field extraction results.



