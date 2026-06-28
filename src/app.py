import hashlib

import streamlit as st
import os
from dotenv import load_dotenv
from langchain_groq import ChatGroq

load_dotenv()

llm = ChatGroq(
    model="llama-3.3-70b-versatile",
    model=os.getenv("GROQ_MODEL"),
    api_key=os.getenv("GROQ_API_KEY"),
    temperature=0,
)

# ---------------------------------
# Page Configuration
# ---------------------------------

st.set_page_config(
    page_title="AI PDF Assistant",
    page_icon="📚",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ---------------------------------
# Custom Styling
# ---------------------------------

st.markdown(
    """
<style>

#MainMenu {visibility: hidden;}
footer {visibility: hidden;}

.block-container {
    padding-top: 1rem;
}

h1 {
    text-align: center;
}

.stChatMessage {
    border-radius: 15px;
    padding: 12px;
    margin-bottom: 10px;
}

</style>
""",
    unsafe_allow_html=True,
)

# ---------------------------------
# Session State
# ---------------------------------

if "messages" not in st.session_state:
    st.session_state.messages = []

if "processed_file_id" not in st.session_state:
    st.session_state.processed_file_id = None

if "document_ready" not in st.session_state:
    st.session_state.document_ready = False

if "current_doc_name" not in st.session_state:
    st.session_state.current_doc_name = None


def _file_id(name, data: bytes) -> str:
    digest = hashlib.sha256(data).hexdigest()[:16]
    return f"{name}:{digest}"


# ---------------------------------
# Sidebar
# ---------------------------------

with st.sidebar:

    st.title("🤖 AI PDF Assistant")

    st.markdown("---")

    st.markdown(
        """
### Features

✅ Upload any PDF

✅ Chat with PDF

✅ AI Summary

✅ Source References

⚡ Powered by Groq

"""
    )

    st.markdown("---")

    if st.session_state.document_ready and st.session_state.current_doc_name:
        st.info(f"📄 Active: **{st.session_state.current_doc_name}**")
    else:
        st.caption("No document loaded yet.")

    st.markdown("---")

    if st.button("🗑 Clear Chat"):
        st.session_state.messages = []
        st.rerun()

    st.markdown("---")

    st.caption("Powered by Groq + FAISS + MiniLM")

# ---------------------------------
# Main Header
# ---------------------------------

st.title("📚 AI PDF Assistant")

st.caption("Upload a PDF below — no backend access needed.")

# ---------------------------------
# PDF Upload (frontend only)
# ---------------------------------

uploaded_file = st.file_uploader(
    "Upload a PDF",
    type=["pdf"],
    help="Select a PDF from your computer. It is processed in this session only.",
)

if uploaded_file is not None:
    pdf_bytes = uploaded_file.getvalue()
    file_id = _file_id(uploaded_file.name, pdf_bytes)

    if file_id != st.session_state.processed_file_id:

        with st.spinner("🔄 Reading and indexing your PDF..."):
            try:
                from ingest import ingest_pdf
                from retriever import reload

                chunk_count = ingest_pdf(pdf_bytes)
                reload()

                st.session_state.processed_file_id = file_id
                st.session_state.document_ready = True
                st.session_state.current_doc_name = uploaded_file.name
                st.session_state.messages = []

            except Exception as exc:
                st.session_state.document_ready = False
                st.error(f"❌ Failed to process PDF: {exc}")
                st.stop()

        st.success(
            f"✅ **{uploaded_file.name}** ready — "
            f"{chunk_count} sections indexed. You can ask questions now."
        )

    elif st.session_state.document_ready:
        st.success(f"📄 **{uploaded_file.name}** is loaded and ready.")

# ---------------------------------
# PDF Summary
# ---------------------------------

if st.button(
    "📄 Generate Document Summary",
    use_container_width=True,
):

    if not st.session_state.document_ready:
        st.warning("Please upload a PDF first.")
    else:
        from retriever import get_all_chunks

        all_chunks = get_all_chunks()
        context = "\n\n".join(all_chunks)[:12000]

        prompt = f"""
Analyze this document and create a structured summary.

If it is lecture notes:
- Main topic
- Key concepts
- Important formulas

If it is a notice:
- Purpose
- Important dates
- Key instructions

If it is a report:
- Objective
- Findings
- Conclusions

Document:
{context}
"""

        with st.spinner("Generating summary..."):
            response = llm.invoke(prompt)
            st.subheader("📄 Document Summary")
            st.markdown(response.content)


# ---------------------------------
# Display Chat History
# ---------------------------------

for message in st.session_state.messages:
    with st.chat_message(
        message["role"],
        avatar="👤" if message["role"] == "user" else "🤖",
    ):
        st.markdown(message["content"])

# ---------------------------------
# Chat Input
# ---------------------------------

question = st.chat_input("Ask a question about your PDF...")

if question:

    if not st.session_state.document_ready:
        st.warning("Please upload a PDF before asking questions.")
    else:
        from retriever import retrieve

        st.session_state.messages.append(
            {"role": "user", "content": question}
        )

        with st.chat_message("user", avatar="👤"):
            st.markdown(question)

        with st.spinner("Searching document..."):
            chunks = retrieve(question)

        context = "\n\n".join(chunks)
        
        chat_history = "\n".join(
            [
                f"{msg['role']}: {msg['content']}"
                for msg in st.session_state.messages[-6:]
            ]
        )

        prompt = f"""
You are a helpful study assistant.

Use the conversation history and document context
to answer the user's question.

Conversation History:
{chat_history}

Document Context:
{context}

Current Question:
{question}

If the answer is not present in the document context,
say:

I could not find that information in the document.
"""

        with st.spinner("Generating answer..."):
            response = llm.invoke(prompt)

            answer = response.content

        st.session_state.messages.append(
            {"role": "assistant", "content": answer}
        )

        with st.chat_message("assistant", avatar="🤖"):
            st.markdown(answer)

            with st.expander("📄 View Sources"):
                for i, chunk in enumerate(chunks, start=1):
                    st.markdown(f"### Source {i}")
                    st.code(chunk)
