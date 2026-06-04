import streamlit as st
import ollama
import subprocess
import sys

from retriever import retrieve

# ---------------------------------
# Page Configuration
# ---------------------------------

st.set_page_config(
    page_title="AI PDF Assistant",
    page_icon="📚",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ---------------------------------
# Custom Styling
# ---------------------------------

st.markdown("""
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
""", unsafe_allow_html=True)

# ---------------------------------
# Session State
# ---------------------------------

if "messages" not in st.session_state:
    st.session_state.messages = []

# ---------------------------------
# Sidebar
# ---------------------------------

with st.sidebar:

    st.title("🤖 AI PDF Assistant")

    st.markdown("---")

    st.markdown("""
### Features

✅ Upload any PDF

✅ Chat with PDF

✅ AI Summary

✅ Source References

✅ Local AI (Ollama)
""")

    st.markdown("---")

    if st.button("🗑 Clear Chat"):

        st.session_state.messages = []

        st.rerun()

    st.markdown("---")

    st.caption(
        "Powered by Ollama + FAISS + MiniLM"
    )

# ---------------------------------
# Main Header
# ---------------------------------

st.title("📚 AI PDF Assistant")

st.caption(
    "Upload any PDF and chat with it using AI"
)

# ---------------------------------
# PDF Upload
# ---------------------------------

uploaded_file = st.file_uploader(
    "Upload a PDF",
    type=["pdf"]
)

if uploaded_file is not None:

    with open(
        "documents/uploaded.pdf",
        "wb"
    ) as f:

        f.write(
            uploaded_file.getbuffer()
        )

    st.success(
        f"📄 Uploaded: {uploaded_file.name}"
    )

    with st.spinner(
        "🔄 Building Knowledge Base..."
    ):

        result = subprocess.run(
            [sys.executable, "src/ingest.py"],
            capture_output=True,
            text=True
        )

    if result.returncode == 0:

        st.success(
            "✅ Knowledge Base Built Successfully!"
        )

    else:

        st.error(
            "❌ Error Building Knowledge Base"
        )

        st.code(
            result.stderr
        )

# ---------------------------------
# PDF Summary
# ---------------------------------

if st.button(
    "📄 Generate Document Summary",
    use_container_width=True
):

    import pickle

    with open(
        "vectorstore/chunks.pkl",
        "rb"
    ) as f:
        all_chunks = pickle.load(f)

    context = "\n\n".join(all_chunks)

    # limit context size
    context = context[:12000]

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

    with st.spinner(
        "Generating summary..."
    ):

        response = ollama.chat(
            model="llama3.2:1b",
            messages=[
                {
                    "role": "user",
                    "content": prompt
                }
            ]
        )

    st.subheader(
        "📄 Document Summary"
    )

    st.markdown(
        response["message"]["content"]
    )
# ---------------------------------
# Display Chat History
# ---------------------------------

for message in st.session_state.messages:

    with st.chat_message(
        message["role"],
        avatar="👤" if message["role"] == "user" else "🤖"
    ):

        st.markdown(
            message["content"]
        )

# ---------------------------------
# Chat Input
# ---------------------------------

question = st.chat_input(
    "Ask a question about your PDF..."
)

if question:

    # Save user message
    st.session_state.messages.append(
        {
            "role": "user",
            "content": question
        }
    )

    # Display user message
    with st.chat_message(
        "user",
        avatar="👤"
    ):

        st.markdown(
            question
        )

    # Retrieve relevant chunks
    with st.spinner(
        "Searching document..."
    ):

        chunks = retrieve(
            question
        )

    context = "\n\n".join(
        chunks
    )

    prompt = f"""
You are a helpful study assistant.

Answer ONLY from the provided context.

Format your answer as:

Definition:
...

Explanation:
...

Key Points:
• ...
• ...
• ...

Context:
{context}

Question:
{question}

If the answer is not present in the context, reply:

I could not find that information in the document.
"""

    # Query Ollama
    with st.spinner(
        "Generating answer..."
    ):

        response = ollama.chat(
            model="llama3.2",
            messages=[
                {
                    "role": "user",
                    "content": prompt
                }
            ]
        )

    answer = response[
        "message"
    ][
        "content"
    ]

    # Save assistant response
    st.session_state.messages.append(
        {
            "role": "assistant",
            "content": answer
        }
    )

    # Display assistant response
    with st.chat_message(
        "assistant",
        avatar="🤖"
    ):

        st.markdown(
            answer
        )

        with st.expander(
            "📄 View Sources"
        ):

            for i, chunk in enumerate(
                chunks,
                start=1
            ):

                st.markdown(
                    f"### Source {i}"
                )

                st.code(
                    chunk
                )