# Zyro Dynamics HR Help Desk

An AI-powered HR chatbot built using Retrieval-Aug-Augmented Generation (RAG) that answers employee HR policy questions using company policy documents.

## Live Demo

https://zyro-dynamics-hr-appdesk-eajzdehbnu3ae2847zfbbc.streamlit.app/

## Features

- Answers HR policy questions using company documents
- Retrieval-Augmented Generation (RAG)
- Semantic search with FAISS
- PDF document ingestion
- Source document references for responses
- Restricts responses to HR policy documents
- Powered by Groq Llama 3.3 70B

## Tech Stack

- Python
- Streamlit
- LangChain
- FAISS
- HuggingFace Embeddings
- Groq
- LangSmith
- PyPDF

## Documents

- Company Profile
- Employee Handbook
- Leave Policy
- Work From Home Policy
- Code of Conduct
- Performance Review Policy
- Compensation & Benefits Policy
- IT & Data Security Policy
- Prevention of Sexual Harassment (POSH) Policy
- Onboarding & Separation Policy
- Travel & Expense Policy

## Project Structure

```
.
├── app.py
├── requirements.txt
├── README.md
├── 00_Company_Profile.pdf
├── 01_Employee_Handbook.pdf
├── ...
└── 10_Travel_and_Expense_Policy.pdf
```

## How to Run

Clone the repository:

```bash
git clone https://github.com/AithagoniAkshitha-22/zyro-dynamics-hr-helpdesk.git
cd zyro-dynamics-hr-helpdesk
```

Install dependencies:

```bash
pip install -r requirements.txt
```

Create a `.streamlit/secrets.toml` file:

```toml
GROQ_API_KEY = "your_groq_api_key"
```

Run the application:

```bash
streamlit run app.py
```

## Author

Akshitha Aithagoni
