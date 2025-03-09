import os
import json
import openai
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Initialize Azure OpenAI client
client = openai.AzureOpenAI(
    api_key=os.getenv("AZURE_OPENAI_KEY"),
    api_version=os.getenv("AZURE_OPENAI_VERSION"),
    azure_endpoint=os.getenv("AZURE_OPENAI_ENDPOINT")
)
deployment_name = os.getenv("AZURE_OPENAI_DEPLOYMENT")

# Instruction prompt
INSTRUCTION_PROMPT = """
You are an advanced AI agent responsible for extracting structured data from forms filled in either Hebrew or English, transforming it into a standardized English JSON format, and ensuring missing values are handled correctly.

📌 Instructions
Step 1: Detect the Language of the Form
- If the form is in Hebrew, extract data and translate field names into English.
- If the form is in English, extract data as is.
- Ensure consistent formatting across different languages.

Step 2: Extract Key-Value Data from the Given Text
Identify and extract fields related to:
- Personal details (name, ID number, birth date, gender, contact details, address)
- Accident details (injury date, injury time, location, description, affected body part)
- Medical details (health fund membership, diagnosis)
- Form submission details (form filling date, form receipt date)
- For any field that is missing or cannot be extracted, insert an empty string ("") instead of omitting it.

Step 3: Generate the Standardized English JSON Output
Return the extracted data in the following JSON format:

{
  "lastName": "{lastName}",
  "firstName": "{firstName}",
  "idNumber": "{idNumber}",
  "gender": "{gender}",
  "dateOfBirth": {
    "day": "{dob_day}",
    "month": "{dob_month}",
    "year": "{dob_year}"
  },
  "address": {
    "street": "{street}",
    "houseNumber": "{houseNumber}",
    "entrance": "{entrance}",
    "apartment": "{apartment}",
    "city": "{city}",
    "postalCode": "{postalCode}",
    "poBox": "{poBox}"
  },
  "landlinePhone": "{landlinePhone}",
  "mobilePhone": "{mobilePhone}",
  "jobType": "{jobType}",
  "dateOfInjury": {
    "day": "{injury_day}",
    "month": "{injury_month}",
    "year": "{injury_year}"
  },
  "timeOfInjury": "{timeOfInjury}",
  "accidentLocation": "{accidentLocation}",
  "accidentAddress": "{accidentAddress}",
  "accidentDescription": "{accidentDescription}",
  "injuredBodyPart": "{injuredBodyPart}",
  "signature": "{signature}",
  "formFillingDate": {
    "day": "{formFilling_day}",
    "month": "{formFilling_month}",
    "year": "{formFilling_year}"
  },
  "formReceiptDateAtClinic": {
    "day": "{formReceipt_day}",
    "month": "{formReceipt_month}",
    "year": "{formReceipt_year}"
  },
  "medicalInstitutionFields": {
    "healthFundMember": "{healthFundMember}",
    "natureOfAccident": "{natureOfAccident}",
    "medicalDiagnoses": "{medicalDiagnoses}"
  }
}

Step 4: Ensure Accuracy and Consistency
- Validate extracted values and ensure correct mapping from Hebrew to English if necessary.
- Maintain date formats correctly (e.g., DD-MM-YYYY or YYYY-MM-DD).
- Ensure numerical values such as ID numbers and phone numbers are correctly extracted.
- If any value is missing, insert "" instead of omitting the key.
"""

def extract_structured_data(text):
    try:
        formatted_prompt = f"Extract structured JSON data from the following text:\n\n{text}\n\nReturn only valid JSON output without extra text."

        response = client.chat.completions.create(
            model=deployment_name,
            messages=[
                {"role": "system", "content": INSTRUCTION_PROMPT},
                {"role": "user", "content": formatted_prompt}
            ],
            temperature=0,
            max_tokens=800
        )

        structured_data = response.choices[0].message.content.strip()

        print("Raw Response from OpenAI:", structured_data)  # Debugging output

        # Clean up the response by removing code block markers (```json ... ```)
        if structured_data.startswith("```json"):
            structured_data = structured_data[7:]  # Remove leading ```json
        if structured_data.endswith("```"):
            structured_data = structured_data[:-3]  # Remove trailing ```

        structured_data = structured_data.strip()  # Ensure no leading/trailing spaces

        if not structured_data:
            return {"error": "OpenAI returned an empty response."}

        try:
            return json.loads(structured_data)
        except json.JSONDecodeError as e:
            return {"error": f"Invalid JSON format returned by OpenAI: {str(e)}"}

    except Exception as e:
        return {"error": str(e)}
