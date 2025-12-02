# 💬 NebulaChat AI

<img width="935" height="887" alt="Screenshot 2025-12-02 181126" src="https://github.com/user-attachments/assets/6ece66dd-8da4-4678-85c2-246adde2a4b6" />


NebulaChat is an **AI-powered chatbot** built using **LangGraph** and **LangChain**, with a **Streamlit front-end**. It supports **multi-threaded chat history** with persistent storage, allowing you to continue conversations even after closing the app.

---

## 🌟 Features

- Persistent chat threads with history
- Multi-thread conversation management
- Clean, intuitive Streamlit interface
- AI-powered responses using LangGraph & LangChain
- Easy to extend and customize

---

## ⚙️ Installation

1. Clone the repository:

```bash
git clone https://github.com/<your-username>/<repo-name>.git
cd <repo-name>
Create a virtual environment:

bash
Copy code
python -m venv venv
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate     # Windows
Install dependencies:

bash
Copy code
pip install -r requirements.txt
Create a .env file and add your API key:

ini
Copy code
GROQ_API_KEY=your_api_key_here
🚀 Usage
Run the app:

bash
Copy code
streamlit run streamlit_frontend.py
