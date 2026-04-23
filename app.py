import streamlit as st
from config import client
from prompts import get_system_prompt
from utils.chat_utils import trim_chat_history
from utils.pdf_utils import extract_text_from_pdf, create_pdf
import re

# -------------------------
# 🔹 Math Renderer
# -------------------------
def render_answer(answer):
    parts = re.split(r'(\$.*?\$)', answer)

    for part in parts:
        if part.startswith("$") and part.endswith("$"):
            st.latex(part.strip("$"))
        else:
            st.write(part)

# -------------------------
# 🔹 Session State
# -------------------------
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

if "questions" not in st.session_state:
    st.session_state.questions = []

if "last_answer" not in st.session_state:
    st.session_state.last_answer = ""

if "summary" not in st.session_state:
    st.session_state.summary = ""

# -------------------------
# 🔹 Page Config
# -------------------------
st.set_page_config(page_title="Assignment Helper AI", page_icon="📚")

# -------------------------
# 🔹 Sidebar
# -------------------------
st.sidebar.title("⚙️ Settings")

mode_type = st.sidebar.selectbox(
    "Answer Mode",
    ["Normal", "Step-by-step", "Hints", "Exam"]
)

temperature = st.sidebar.slider("Creativity", 0.0, 1.0, 0.6)
word_limit = st.sidebar.text_input("Word Limit (optional)")

st.sidebar.write(f"Messages stored: {len(st.session_state.chat_history)}")
st.sidebar.write(f"Current Mode: {mode_type}")

if st.sidebar.button("🧹 Clear Chat"):
    st.session_state.chat_history = []
    st.session_state.summary = ""

# -------------------------
# 🔹 Main UI
# -------------------------
st.title("📚 Assignment Helper AI")
st.caption("Ask questions or upload assignments")

st.divider()

mode = st.radio("Choose Mode", ["💬 Chat", "📄 PDF"])

# =========================
# 🔹 CHAT MODE
# =========================
if mode == "💬 Chat":

    for msg in st.session_state.chat_history:
        with st.chat_message(msg["role"]):
            render_answer(msg["content"])

    question = st.chat_input("Ask something...")

    if question:

        st.session_state.chat_history.append(
            {"role": "user", "content": question}
        )

        # 🔹 Summarization
        if len(st.session_state.chat_history) > 10:
            try:
                summary_response = client.chat.completions.create(
                    model="llama-3.1-8b-instant",
                    messages=[
                        {"role": "system", "content": "Summarize briefly"},
                        {"role": "user", "content": str(st.session_state.chat_history)}
                    ],
                    temperature=0.3
                )

                st.session_state.summary = summary_response.choices[0].message.content
                st.session_state.chat_history = st.session_state.chat_history[-4:]

            except Exception as e:
                st.error(f"Summary error: {e}")

        # 🔹 Prompt
        system_prompt = get_system_prompt(word_limit, mode_type)

        messages = [
            {"role": "system", "content": system_prompt},
            {"role": "system", "content": f"Summary: {st.session_state.summary}"}
        ] + trim_chat_history(st.session_state.chat_history)

        # 🔹 API Call
        with st.spinner("🤖 Thinking..."):
            try:
                response = client.chat.completions.create(
                    model="llama-3.1-8b-instant",
                    messages=messages,
                    temperature=temperature
                )

                answer = response.choices[0].message.content

                st.session_state.chat_history.append(
                    {"role": "assistant", "content": answer}
                )

                st.session_state.last_answer = answer

                with st.chat_message("assistant"):
                    render_answer(answer)

            except Exception as e:
                st.error(f"Error: {e}")

# =========================
# 🔹 PDF MODE
# =========================
elif mode == "📄 PDF":

    uploaded_file = st.file_uploader("Upload PDF", type="pdf")

    if uploaded_file:
        text = extract_text_from_pdf(uploaded_file)

        st.subheader("📄 Preview")
        st.write(text[:1000])

        if st.button("📌 Extract Questions"):
            try:
                response = client.chat.completions.create(
                    model="llama-3.1-8b-instant",
                    messages=[
                        {"role": "system", "content": "Extract questions"},
                        {"role": "user", "content": text[:4000]}
                    ],
                    temperature=0.3
                )

                questions = response.choices[0].message.content.split("\n")
                questions = [q for q in questions if q.strip()]

                st.session_state.questions = [
                    re.sub(r'^\d+[\.\)]\s*', '', q) for q in questions
                ]

            except Exception as e:
                st.error(f"Error extracting questions: {e}")

    if st.session_state.questions:

        selected_q = st.selectbox("Select Question", st.session_state.questions)

        if st.button("🧠 Answer Question"):
            try:
                response = client.chat.completions.create(
                    model="llama-3.1-8b-instant",
                    messages=[
                        {"role": "system", "content": get_system_prompt(word_limit, mode_type)},
                        {"role": "user", "content": selected_q}
                    ],
                    temperature=temperature
                )

                answer = response.choices[0].message.content

                st.session_state.last_answer = answer

                st.subheader("📖 Answer")
                render_answer(answer)

            except Exception as e:
                st.error(f"Error: {e}")

# =========================
# 🔹 DOWNLOAD SECTION
# =========================
if st.session_state.last_answer:

    st.divider()
    st.subheader("📥 Download")

    # TXT
    st.download_button(
        "Download TXT",
        st.session_state.last_answer,
        file_name="answer.txt"
    )

    # PDF
    create_pdf(st.session_state.last_answer)

    with open("output.pdf", "rb") as f:
        st.download_button(
            label="Download PDF",
            data=f,
            file_name="answer.pdf",
            mime="application/pdf"
        )

# -------------------------
# 🔹 Chat History Download
# -------------------------
if st.session_state.chat_history:

    chat_text = ""

    for msg in st.session_state.chat_history:
        role = msg["role"].capitalize()
        chat_text += f"{role}: {msg['content']}\n\n"

    st.download_button(
      "📥 Download Chat History",
      chat_text,
      file_name="chat_history.txt",
      mime="text/plain"
    )

