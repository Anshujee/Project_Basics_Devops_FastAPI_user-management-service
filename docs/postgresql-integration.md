## In this Document I captures everything you learned about adding PostgreSQL to your FastAPI app using Docker Compose.
## What this document gives you

📘 Beginner-friendly explanation (no assumptions)

🧠 Clear mental models (why DevOps cares about DBs)

🐳 How multi-service Docker Compose works

🌐 Container networking explained simply

🔐 Safe environment-variable–based configuration

🧪 Hands-on verification & failure testing

💼 Real-world DevOps perspective, not just tutorial steps

# 🐘 Adding PostgreSQL to FastAPI using Docker Compose

This document captures my **step-by-step learning of connecting a FastAPI application to a PostgreSQL database using Docker Compose**.

## The goal of this README is:

* 📘 To preserve concepts clearly for future revision
* 🧠 To understand *why* each step is needed (not just how)
* 💼 To learn how DevOps engineers run **multiple services together**
* 🛠️ To move from a single-container app to a **realistic system setup**

This guide is written assuming **no prior database experience**.

---

## 1️⃣ Why DevOps Engineers Care About Databases

In real-world systems:

* Applications almost always need a database
* Databases are **separate services**, not part of the app
* DevOps engineers must ensure:

  * App and DB run together
  * Networking between services works
  * Configuration is handled safely

👉 This is why tools like **Docker Compose** exist.

---

## 2️⃣ What We Are Building

We are running **two services together**:

1. **FastAPI application** (user-management-service)
2. **PostgreSQL database**

Both services:

* Run as separate containers
* Share the same Docker network
* Communicate using service names

---

## 3️⃣ Understanding Container Networking (Very Important)

In Docker Compose:

* All services are placed on a **default internal network**
* Each service name becomes a **hostname**

Example:

```yaml
services:
  app:
  db:
```

Inside the `app` container:

* Database host = `db`
* NOT `localhost`

This concept is critical for DevOps and Kubernetes.

---

## 4️⃣ Extending `docker-compose.yml` to Add PostgreSQL

### Complete `docker-compose.yml`

```yaml
version: "3.9"

services:
  app:
    build:
      context: .
      dockerfile: docker/Dockerfile
    image: user-management-service:1.0
    container_name: user-management-app
    ports:
      - "8000:8000"
    env_file:
      - .env
    depends_on:
      - db
    restart: unless-stopped

  db:
    image: postgres:15
    container_name: postgres-db
    environment:
      POSTGRES_DB: userdb
      POSTGRES_USER: useradmin
      POSTGRES_PASSWORD: userpassword
    ports:
      - "5432:5432"
```

---

## 5️⃣ Explanation of Each New Part in Docker Compose

### 🔹 `db` service

* Runs PostgreSQL as a container
* Uses official PostgreSQL image
* Version pinned (`15`) for stability

### 🔹 Database environment variables

```yaml
POSTGRES_DB
POSTGRES_USER
POSTGRES_PASSWORD
```

These tell PostgreSQL:

* Which database to create
* Which user owns it
* What password to use

---

### 🔹 `depends_on`

```yaml
depends_on:
  - db
```

Ensures:

* DB container is started before app container

⚠️ Note: This does **not** guarantee DB readiness, only start order.

---

## 6️⃣ Using `.env` for Database Configuration

### `.env` file

```env
CPU_THRESHOLD=80
MEMORY_THRESHOLD=80

DB_HOST=db
DB_PORT=5432
DB_NAME=userdb
DB_USER=useradmin
DB_PASSWORD=userpassword
```

### Why this is important

* Keeps config separate from code
* Makes app environment-agnostic
* Follows **12-factor app principles**

---

## 7️⃣ Adding PostgreSQL Driver Dependency

FastAPI cannot connect to PostgreSQL directly.
We need a **database driver**.

### `requirements.txt`

```txt
fastapi
uvicorn
psutil
psycopg2-binary
```

---

## 8️⃣ Updating Application Code (Database Awareness)

### Key goals in code:

* Read DB config from environment variables
* Attempt DB connection
* Handle success and failure cleanly

---

### Full Updated `main.py`

```python
import os
from fastapi import FastAPI
import psutil
import psycopg2

app = FastAPI()

# ---------- CPU / Memory Config ----------
CPU_THRESHOLD = int(os.getenv("CPU_THRESHOLD", 80))
MEMORY_THRESHOLD = int(os.getenv("MEMORY_THRESHOLD", 80))

# ---------- Database Config ----------
DB_HOST = os.getenv("DB_HOST")
DB_PORT = os.getenv("DB_PORT")
DB_NAME = os.getenv("DB_NAME")
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")


@app.get("/health")
def health_check():
    cpu_usage = psutil.cpu_percent(interval=1)
    memory_usage = psutil.virtual_memory().percent

    status = "UP"
    if cpu_usage > CPU_THRESHOLD or memory_usage > MEMORY_THRESHOLD:
        status = "DOWN"

    return {
        "status": status,
        "cpu_usage": cpu_usage,
        "memory_usage": memory_usage,
        "cpu_threshold": CPU_THRESHOLD,
        "memory_threshold": MEMORY_THRESHOLD
    }


@app.get("/db-check")
def db_check():
    try:
        connection = psycopg2.connect(
            host=DB_HOST,
            port=DB_PORT,
            dbname=DB_NAME,
            user=DB_USER,
            password=DB_PASSWORD,
            connect_timeout=3
        )
        connection.close()
        return {"db_status": "CONNECTED"}
    except Exception as e:
        return {
            "db_status": "NOT CONNECTED",
            "error": str(e)
        }
```

---

## 9️⃣ Running the Multi-Service Stack

After all changes:

```bash
docker compose down
docker compose build --no-cache
docker compose up -d
```

This:

* Builds a fresh image with DB support
* Starts both app and database
* Connects them via Docker network

---

## 🔍 Verification Steps

### Check running containers

```bash
docker ps
```

Expected:

* `user-management-app`
* `postgres-db`

---

### Test DB connectivity

Open in browser:

```
http://localhost:8000/db-check
```

Expected response:

```json
{
  "db_status": "CONNECTED"
}
```

---

### Failure testing (important learning)

```bash
docker stop postgres-db
```

Then call `/db-check` again.

Expected:

```json
{
  "db_status": "NOT CONNECTED"
}
```

This proves real service dependency handling.

---

## 🔑 Key Concepts Learned

* Running multiple services together
* Docker Compose networking
* Service-to-service communication
* Environment-based configuration
* Database drivers
* Realistic DevOps debugging

---

## 🏁 Final Notes

This setup mirrors **real-world DevOps workflows** where:

* Applications depend on databases
* Services are isolated but connected
* Configuration is externalized

This document serves as a **personal DevOps knowledge reference** and will be extended later with:

* DB health checks
* Data persistence using volumes
* Migrations
* Kubernetes equivalents

✅ *Learning by doing, understanding by documenting.*
