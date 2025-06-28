
# 🎓 EduTutor AI: Personalized Learning with Generative AI and LMS Integration
---

  ## Project Overview  :
   EduTutor AI is a cloud-based, AI-powered educational platform that revolutionizes how students learn and educators assess. Built using IBM Watsonx, Granite   
   foundation models, Google Classroom APIs, Pinecone vector DB, and Streamlit, this project demonstrates a modular, intelligent, and adaptive learning ecosystem.


##  Project Architecture

```bash
EDUTUTOR-AI/
├── .streamlit/                   # Streamlit credentials & secrets
│   ├── client_secret.json
│   └── secrets.toml
│
├── backend/                      # FastAPI backend logic
│   ├── routes/                   # Route handlers for API endpoints
│   │   ├── auth.py
│   │   ├── educator.py
│   │   ├── quiz.py
│   │   ├── submission.py
│   │   ├── user.py
│   │   └── user_auth.py
│   │
│   ├── services/                 # Services for external integrations
│   │   ├── llm_service.py        # Watsonx / Granite model logic
│   │   └── vector_service.py     # Pinecone vector search logic
│   │
│   ├── utils/                    # Helper and auth logic
│   │   ├── api.py
│   │   ├── auth.py
│   │   ├── session.py
│   │   └── watsonx_auth.py
│   │
│   ├── .env                      # Environment variables
│   ├── main.py                   # FastAPI entry point
│   └── students.db               # SQLite database file (or used for local storage)
│
├── frontend/                     # Streamlit frontend
│   ├── pages/                    # Individual UI screens
│   │   ├── google_login.py
│   │   ├── students_dashboard.py
│   │   └── take_quiz.py
│   ├── app.py                    # Main app file
│   └── static/                   # Static assets like CSS/images
│       └── style.css
│
├── requirements.txt              # Python dependencies
├── README.md                     # Project documentation
└── venv/                         # Python virtual environment
```


## 🔧 Technologies Used

- 🧠 IBM Watsonx (Granite LLM via LangChain)
- 🚀 FastAPI + Uvicorn
- 📊 Pinecone Vector DB
- 🌐 Google Classroom API
- 🖥️ Streamlit (Role-based Dashboards)
- 🔐 OAuth (Google Auth)
- 📦 Python Environment Management with `venv`



## 💫 Project Work flow :

###  Requirement Setup

Technologies used:
- `fastapi`, `uvicorn`
- `langchain_ibm`
- `pinecone-client`
- `streamlit`
- `google-auth-oauthlib`
- `google-api-python-client`
- `python-dotenv`

Install them via:

```bash
pip install -r requirements.txt
```

### Environment Initialization

`.env` file stores all keys securely for:
- IBM Watsonx
- Pinecone DB
- OAuth credentials

### FastAPI Backend
 - Handles student/educator login, quiz generation, answer evaluation, classroom sync, and metadata updates.
   

### IBM Watsonx AI Integration

- Granite model loaded via `langchain_ibm.WatsonxLLM`
- LangChain `PromptTemplate` dynamically forms questions
- Output parsed into quiz-ready JSON


### Google Classroom Sync

- Login via Google OAuth
- Retrieve class names, topics, student data using Classroom APIs

### Pinecone Integration

- Embeddings stored for each user
- Metadata like quiz scores, topics, dates
- Vector similarity used for personalized quiz suggestions
  

### Streamlit Frontend

#### Student Panel
- Google/Manual Login
- Personalized Dashboard
- Take Quiz
- View Quiz History


#### Educator Panel
- Dashboard with performance insights
- View student activity
- Analyze progress via Pinecone data

---

##  How to Run the Project Locally

### 1️⃣ Clone the Repository

```bash
git clone https://github.com/SK-LIYA/EduTutor-AI.git
cd EduTutor-AI
```

### 2️⃣ Create and Activate Virtual Environment

```bash
# Windows
python -m venv venv
venv\Scripts\activate

# macOS/Linux
python3 -m venv venv
source venv/bin/activate
```

### 3️⃣ Install Dependencies

```bash
pip install -r requirements.txt
```

### 4️⃣ Configure Environment Variables

Create a `.env` file in the root directory with the following:

```env
WATSONX_MODEL_ID=granite-13b-instruct-v2
WATSONX_API_KEY=your_ibm_watsonx_api_key
WATSONX_ENDPOINT=https://us-south.ml.cloud.ibm.com
WATSONX_PROJECT_ID=your_project_id

PINECONE_API_KEY=your_pinecone_api_key
PINECONE_INDEX_NAME=edututor
```

### 5️⃣ Run Backend (FastAPI)

```bash
cd backend
uvicorn main:app --reload
```

- Visit API Docs: http://127.0.0.1:8000/docs

### 6️⃣ Run Frontend (Streamlit)

```bash
cd frontend
streamlit run app.py
```


## 🙌 Contributions

We welcome contributors! Please fork this repo, create a new branch, and raise a PR.  

---


## ⭐ Star This Project

If you found this project useful or inspiring, please consider starring the repo 🙏

---
