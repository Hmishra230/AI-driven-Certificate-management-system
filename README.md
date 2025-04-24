# 🧠 AI-driven Certificate Management System

A Flask-based web application to manage digital certificate generation, storage, preview, and download. It includes user authentication, admin analytics, and an AI assistant powered by GPT-Neo for answering insights about certificate data.

---

## 🚀 Features

- 👤 User & Admin Authentication (Flask-Login)
- 🧾 Digital Certificate Generation with Unique ID
- 📄 Downloadable PDF Certificates (ReportLab)
- 📊 Admin Dashboard with Stats:
  - Most Active User
  - Most Common Certificate Type
  - Certificates Generated Today
- 🤖 AI Assistant using GPT-Neo (Hugging Face Transformers)
- 🔒 Role-Based Access (Admin/User)
- 🗑️ Admin can delete certificates
- 🧠 AI Q&A interface for certificate insights

---

## 📸 Screenshots

Coming soon…

---

## 🛠️ Tech Stack

- **Backend:** Flask, SQLAlchemy
- **Frontend:** HTML, Jinja2, Bootstrap
- **AI Model:** GPT-Neo (`EleutherAI/gpt-neo-1.3B`)
- **Database:** SQLite
- **PDF Generator:** ReportLab

---

## 📦 Installation

```bash
# Clone the repository
git clone https://github.com/Hmishra230/AI-driven-Certificate-management-system.git
cd AI-driven-Certificate-management-system

# Create a virtual environment
python -m venv venv
source venv/bin/activate  # on Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
