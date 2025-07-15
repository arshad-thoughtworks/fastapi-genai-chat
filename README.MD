cat << 'EOF' > README.md
# GenAI Chat App Backend (FastAPI)

This project is a lightweight backend implementation for managing chat sessions and messages in a GenAI-powered Chat App using **FastAPI**.

---

## 🚀 Features

- ✅ Create new chat sessions (in-memory storage)
- ✅ Add user/assistant messages to sessions
- ✅ Retrieve full chat history (with optional role-based filtering)
- ✅ Full test coverage using `pytest`
- ✅ Swagger UI for easy API interaction

---

## 📂 Project Structure

\`\`\`
fastapi/
├── main.py            # FastAPI application with routes
├── requirements.txt   # Python dependencies
├── tests/
│   └── test_main.py   # Unit tests for API endpoints
└── README.md          # This file
\`\`\`

---

## 🛠️ Requirements

- Python 3.9+
- pip

---

## 📦 Setup & Run

\`\`\`bash
# Navigate to project folder
cd fastapi

# (Optional) Create virtual environment
python3 -m venv fastapienv
source fastapienv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Run the FastAPI app
python3 main.py
\`\`\`

App will be available at: [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs) ✅

---

## 🧪 Running Tests

\`\`\`bash
# Run unit tests
pytest
\`\`\`

All endpoints are fully tested using `pytest` and `TestClient`.

---

## 🧠 Example Endpoints

### 🔹 Create Session

\`\`\`http
POST /sessions
{
  "session_user": "arshad"
}
\`\`\`

### 🔹 Add Message

\`\`\`http
POST /sessions/1/messages
{
  "role": "user",
  "content": "What is AI?"
}
\`\`\`

### 🔹 Get All Messages

\`\`\`http
GET /sessions/1/messages
\`\`\`

### 🔹 Get Messages (Filtered by Role)

\`\`\`http
GET /sessions/1/messages?role=user
\`\`\`

---

## 💡 Notes

- No external database is used — all data is stored in Python in-memory structures.
- Suitable as a learning/demo project for FastAPI + testing best practices.

---

## 🙌 Author

**Arshad Qureshi**  
Infrastructure Consultant at ThoughtWorks

---

## 📜 License

This project is for educational and demonstration purposes only. No license restrictions applied.
EOF
