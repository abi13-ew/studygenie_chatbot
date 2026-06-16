# 📚 StudyGenie AI – Lecture to Knowledge Assistant

## 🚀 Overview

StudyGenie AI is an AI-powered learning assistant that helps students transform lectures and study materials into structured learning resources. Users can upload PDF documents or lecture recordings and instantly generate summaries, quizzes, flashcards, exam preparation materials, study plans, and interact with an AI chatbot.

The application combines Speech-to-Text, Retrieval-Augmented Generation (RAG), Vector Search, and Large Language Models (LLMs) to create a smarter learning experience.

---

## 🎯 Problem Statement

Students often face challenges such as:

* Difficulty taking notes during lectures.
* Spending excessive time reading lengthy study materials.
* Creating revision notes manually.
* Preparing quizzes and flashcards for self-assessment.
* Finding relevant information quickly within large documents.

StudyGenie AI automates these tasks and improves learning efficiency.

---

## ✨ Features

### 📄 PDF Processing

* Upload PDF notes and study materials.
* Automatic text extraction.

### 🎤 Audio Lecture Processing

* Upload lecture recordings (MP3, WAV, M4A).
* Speech-to-text conversion using Whisper AI.

### 📝 AI Summary Generation

* Student-friendly summaries.
* Key concepts and important points highlighted.

### ❓ Quiz Generation

* Automatically generates multiple-choice questions.
* Helps with exam preparation and self-assessment.

### 🧠 Flashcard Generation

* Creates question-answer flashcards from study material.

### 📚 Exam Preparation Assistant

Generates:

* Important Topics
* 2-Mark Questions
* 5-Mark Questions
* Revision Checklists

### 📅 Study Plan Generator

* Creates a personalized 7-day study schedule.

### 🤖 AI Chat Assistant

* Ask questions about uploaded documents or lectures.
* Answers are generated using retrieved content from the uploaded material.

---

## 🏗️ System Workflow

```text
PDF / Audio Upload
        │
        ▼
Text Extraction
(PDF Parser / Whisper)
        │
        ▼
Text Chunking
        │
        ▼
MiniLM Embeddings
        │
        ▼
FAISS Vector Search
        │
        ▼
Gemini 2.5 Flash
        │
        ▼
Summary
Quiz
Flashcards
Exam Prep
Study Plan
Chat Assistant
```

---

## 🛠️ Technologies Used

| Category             | Technology                |
| -------------------- | ------------------------- |
| Frontend             | Streamlit                 |
| Speech Recognition   | OpenAI Whisper            |
| Embedding Model      | all-MiniLM-L6-v2          |
| Vector Database      | FAISS                     |
| Large Language Model | Gemini 2.5 Flash          |
| PDF Processing       | PyPDF                     |
| Programming Language | Python                    |
| AI Framework         | Hugging Face Transformers |

---

## 📂 Project Structure

```text
StudyGenieAI/
│
├── app.py
├── requirements.txt
└── README.md
```

---

## ⚙️ Installation

### Clone Repository

```bash
git clone https://github.com/your-username/studygenie-ai.git
cd studygenie-ai
```

### Create Virtual Environment

```bash
conda create -n studygenie python=3.10
conda activate studygenie
```

### Install Dependencies

```bash
pip install -r requirements.txt
```

---

## 🔑 Configure Gemini API

Add your Gemini API Key inside the application or use Streamlit Secrets:

```toml
GEMINI_API_KEY="YOUR_API_KEY"
```

---

## ▶️ Run the Application

```bash
streamlit run app.py
```

Application will run at:

```text
http://localhost:8501
```

---

## 📊 Results

### Implemented Features

| Feature           | Status |
| ----------------- | ------ |
| PDF Upload        | ✅      |
| Audio Upload      | ✅      |
| Speech-to-Text    | ✅      |
| AI Summary        | ✅      |
| Quiz Generation   | ✅      |
| Flashcards        | ✅      |
| Exam Prep         | ✅      |
| Study Plan        | ✅      |
| AI Chat Assistant | ✅      |

### Benefits

* Faster note creation.
* Improved revision process.
* Personalized learning support.
* Enhanced student productivity.
* Better understanding of lecture content.

---

## 🚀 Future Scope

* Multilingual Support
* Student Progress Dashboard
* AI Mind Map Generation
* Mobile Application
* Voice-Based Learning Assistant
* Cloud Storage Integration
* Learning Analytics
* LMS Integration

---

## 👨‍💻 Author

**Abijith Kalingaraj**

IBM SkillsBuild Internship Project

Artificial Intelligence & Data Science

Jappiaar Engineering College

---

## 📜 License

This project is developed for educational and research purposes as part of the IBM SkillsBuild Internship Program.
