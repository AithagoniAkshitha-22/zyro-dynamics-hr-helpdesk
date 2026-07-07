
# TODO: Build your Streamlit chatbot application

import streamlit as st
import os

from langchain_community.document_loaders import PyPDFDirectoryLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS

from langchain_groq import ChatGroq

from langchain_core.prompts import ChatPromptTemplate

st.set_page_config(
    page_title="Zyro Dynamics HR Assistant",
    page_icon="💼",
    layout="wide"
)

st.title("💼 Zyro Dynamics HR Help Desk")
st.caption("Ask questions about HR policies")

GROQ_MODEL = "llama-3.3-70b-versatile"

CORPUS_PATH = "."

@st.cache_resource
def load_vectorstore():

    loader = PyPDFDirectoryLoader(CORPUS_PATH)
    documents = loader.load()

    splitter = RecursiveCharacterTextSplitter(
        chunk_size=500,
        chunk_overlap=100
    )

    chunks = splitter.split_documents(documents)

    embeddings = HuggingFaceEmbeddings(
        model_name="sentence-transformers/all-MiniLM-L6-v2"
    )

    vectorstore = FAISS.from_documents(
        chunks,
        embeddings
    )

    return vectorstore

vectorstore = load_vectorstore()

retriever = vectorstore.as_retriever(
    search_kwargs={"k":3}
)

llm = ChatGroq(
    model=GROQ_MODEL,
    temperature=0.1
)
RAG_PROMPT = ChatPromptTemplate.from_template('''
You are the official HR assistant for Zyro Dynamics.

Answer ONLY using the provided HR policy documents.

If the answer is not found in the documents, reply exactly:

I can only answer HR-related questions based on the Zyro Dynamics policy documents.

Context:
{context}

Question:
{question}

Answer:
''')

REFUSAL_MESSAGE = (
    "I can only answer HR-related questions based on the Zyro Dynamics policy documents."
)

def format_docs(docs):
    return "\n\n".join(doc.page_content for doc in docs)


def ask_bot(question):

    docs = retriever.invoke(question)

    if len(docs) == 0:
        return REFUSAL_MESSAGE, []

    context = format_docs(docs)

    prompt = RAG_PROMPT.invoke(
        {
            "context": context,
            "question": question
        }
    )

    response = llm.invoke(prompt)

    answer = response.content

   if "I don't know" in answer:
    return REFUSAL_MESSAGE, []

if REFUSAL_MESSAGE in answer:
    return REFUSAL_MESSAGE, []

return answer, docs
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display previous chat messages
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Chat input
question = st.chat_input("Ask an HR-related question...")

if question:

    # Display user message
    st.session_state.messages.append(
        {
            "role": "user",
            "content": question
        }
    )

    with st.chat_message("user"):
        st.markdown(question)

    # Generate assistant response
    with st.chat_message("assistant"):

        with st.spinner("Searching HR policies..."):

            answer, docs = ask_bot(question)

            st.markdown(answer)

            # Show source documents
            if docs:
                with st.expander("📄 Source Documents"):
                    for i, doc in enumerate(docs, 1):

                        source = doc.metadata.get("source", "Unknown")

                        st.markdown(f"**Source {i}:** {os.path.basename(source)}")

                        st.caption(doc.page_content[:350] + "...")

    st.session_state.messages.append(
        {
            "role": "assistant",
            "content": answer
        }
    )
# Sidebar
with st.sidebar:

    st.header("ℹ️ About")

    st.write(
        '''
This chatbot answers questions using
**Zyro Dynamics HR Policy Documents**.

Supported topics:

- Leave Policy
- Work From Home
- Employee Handbook
- Performance Reviews
- Compensation & Benefits
- IT & Data Security
- POSH Policy
- Travel & Expense
- Onboarding & Separation
        '''
    )

    st.divider()

    st.success("Powered by Groq + LangChain + FAISS")

# Welcome message
if len(st.session_state.messages) == 0:

    st.info(
        "👋 Welcome! Ask me anything about Zyro Dynamics HR policies."
    )
# your code here
