# 🧠 FastAPI + Tortoise ORM + GraphQL Authentication API

This project demonstrates how to build a fully functional backend with:

- ✅ FastAPI (REST & GraphQL APIs)
- ✅ Tortoise ORM with SQLite/PostgreSQL
- ✅ JWT-based Authentication (Login / Signup)
- ✅ Protected routes with group-based access control
- ✅ GraphQL integration via Strawberry
- ✅ Ready for deployment via Render (Backend) + GitHub Pages (Frontend)

---

## 🛠️ Tech Stack

- **Python 3.10+**
- [FastAPI](https://fastapi.tiangolo.com/)
- [Tortoise ORM](https://tortoise-orm.readthedocs.io/)
- [Strawberry GraphQL](https://strawberry.rocks/)
- JWT (`python-jose`)
- Auth (`passlib`, `python-multipart`)
- SQLite

---

## 📦 Setup Instructions

```bash
git clone https://github.com/badfr0g/challenge1.git
cd challenge1

### 🔃 2. Sync project's dependencies
uv sync

🚀 3. Run the Server
uv run main.py

REST API: http://localhost:8000/docs
GraphQL Playground: http://localhost:8000/graphql


📁 Project Structure
.
├── main.py              # FastAPI entry point
├── auth.py              # Auth utilities (JWT, password)
├── models.py            # Tortoise ORM models
├── schema.py            # GraphQL Schema
├── routes/              # REST API routers
├── .env                 # Environment variables
├── requirements.txt
├── init_db.py           # Optional DB initializer
└── README.md

✍️ License
MIT License. Feel free to modify and use.