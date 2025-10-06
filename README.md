# Spy Cats API

Postman collection: https://web.postman.co/1763055f-a2ef-45a6-a17e-9d3a2b3218de

## 🚀 Quick Start Guide for Local Development

### 1. Clone the repository

```bash
git clone git@github.com:Mykyta-Harashchenko/Test_Task_Developers_Today.git
cd Test_Task_Developers_Today
```

---

### 2. Create and configure your `.env` file

- Copy the example file:
  ```bash
  cp .env_example .env
  ```
- Fill in the variables in `.env` (or leave defaults for local development).

---

### 3. Start the PostgreSQL database with Docker Compose

```bash
docker-compose up -d
```

The database will be available at `localhost:5432` with credentials from your `.env`.

---

### 4. Create and activate a virtual environment

```bash
python3 -m venv .venv
source .venv/bin/activate
```

---

### 5. Install Python dependencies

```bash
pip install -r requirements.txt
```

---

### 6. Run Alembic migrations

```bash
alembic upgrade head
```

---

### 7. Start the FastAPI server

```bash
uvicorn main:app --reload
```

---

### 8. Open Swagger UI

Go to:  
[http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)
