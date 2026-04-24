# 📚 Assignment Helper AI

An AI-powered academic assistant designed to help students **understand and solve assignments efficiently**.

It supports interactive Q&A, PDF-based question extraction, and generates structured answers for coding, mathematics, and theory.

---

## 🎯 Problem It Solves

Students often:

* Spend too much time formatting answers
* Struggle to extract questions from PDFs
* Need different explanation styles (detailed vs exam-ready)

This tool provides:
→ Instant, structured, and customizable answers

---

## 🚀 Features

### 💬 Chat Mode

* Ask any academic question
* Maintains conversation history
* Smart summarization for long chats

### 📄 PDF Mode

* Upload assignment PDFs
* Automatically extracts questions
* Select and solve specific questions

### 🧠 Answer Modes

* **Normal** → Balanced explanation
* **Step-by-step** → Detailed breakdown
* **Hints** → Guidance without full solution
* **Exam Mode** → Concise, to-the-point answers

### 📊 Smart Output Formatting

* Code → Proper code blocks
* Math → LaTeX-style formatting
* Theory → Structured explanations

### 📥 Export Options

* Download answers as `.txt`
* Download answers as `.pdf`

---

## 🛠️ Tech Stack

* **Frontend:** Streamlit
* **LLM API:** Groq
* **PDF Processing:** PyPDF2
* **PDF Generation:** ReportLab
* **Language:** Python

---

## ⚙️ How to Run Locally

```bash
pip install -r requirements.txt
streamlit run app.py
```

---

## 🔐 Environment Setup

Create a `.env` file:

```
GROQ_API_KEY=your_api_key_here
```

---

## 🧪 Example Use Cases

* Solving assignment questions quickly
* Understanding step-by-step math solutions
* Extracting questions from PDFs
* Practicing exam-style answers

---

## 📌 Design Decisions

* Modular code structure for scalability
* Prompt engineering for different answer styles
* Lightweight UI for fast interaction
* Separation of logic (utils, prompts, config)

---

## 🔮 Future Improvements

* User authentication
* Save chat history in database
* Better PDF rendering (LaTeX in PDF)
* Mobile-friendly UI
* Multi-language support

---

## 🌐 Live Demo

https://assignment-h-ai.streamlit.app/

---

## 👨‍💻 Author

**Chinmay Dadhich**
Student @ IIT Ropar
Focused on AI + Product Development
