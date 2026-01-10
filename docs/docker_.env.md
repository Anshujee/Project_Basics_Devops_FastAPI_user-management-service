# 🔐 Using `.env` Files with Docker Compose – DevOps Best Practices

This document explains **why and how to use `.env` files with Docker Compose**, starting from absolute basics and moving toward **real-world DevOps and DevSecOps practices**.

This builds directly on the previous Docker Compose setup and solves the problem of **hard‑coding configuration values** inside `docker-compose.yml`.

---

## 📌 Why `.env` Files Are Needed

### Problem with hard-coded values

Earlier, we had:

```yaml
environment:
  CPU_THRESHOLD: 10
  MEMORY_THRESHOLD: 10
```

This works, but it has limitations:

* ❌ Values are fixed in the file
* ❌ Same config for dev, test, prod
* ❌ Risk of committing sensitive data
* ❌ Hard to change without editing YAML

---

## ✅ What Is a `.env` File?

A `.env` file is a **simple text file** that stores **environment variables** as key–value pairs.

Example:

```env
CPU_THRESHOLD=10
MEMORY_THRESHOLD=10
```

Docker Compose automatically reads this file and injects values into containers.

---

## 🧩 Real-Life Analogy

Think of:

* `docker-compose.yml` → Office rule book
* `.env` → Whiteboard with daily limits

You don’t rewrite the rule book every day — you just change the whiteboard.

---

## 📂 Recommended Project Structure (Professional)

```text
user-management-service/
├── app/
│   └── main.py
├── docker/
│   └── Dockerfile
├── docker-compose.yml
├── .env
├── .gitignore
└── README.md
```

---

## 🛠️ Step 1: Create `.env` File

```bash
nano .env
```

Add:

```env
CPU_THRESHOLD=10
MEMORY_THRESHOLD=10
```

Save and exit.

---

## 🔐 Step 2: Protect `.env` (DevSecOps Rule)

Ensure `.env` is ignored by Git:

```gitignore
.env
```

✔ `.env` must NEVER be committed
✔ Keeps secrets and config safe

---

## 🐳 Step 3: Update `docker-compose.yml`

### ✅ Correct & Clean Compose File

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
    restart: unless-stopped
```

---

## 🔍 Key Change Explained: `env_file`

```yaml
env_file:
  - .env
```

### What this does

* Docker Compose reads `.env`
* Injects variables into container
* Keeps YAML clean

### Inside container, values become:

```text
CPU_THRESHOLD=10
MEMORY_THRESHOLD=10
```

---

## 🧠 How This Connects to Python Code

Your `main.py` already does this correctly:

```python
CPU_THRESHOLD = int(os.getenv("CPU_THRESHOLD", 80))
MEMORY_THRESHOLD = int(os.getenv("MEMORY_THRESHOLD", 80))
```

Docker provides values → Python reads them at runtime.

---

## 🔄 Correct Workflow After Changes

When `.env` or code changes:

```bash
docker compose down
docker compose build --no-cache
docker compose up -d
```

---

## 🧠 Docker Compose `.env` vs App `.env`

| Use Case              | `.env`                    |
| --------------------- | ------------------------- |
| Docker Compose config | ✅ Yes                     |
| App secrets           | ⚠️ Prefer secret managers |
| Production secrets    | ❌ Avoid                   |

---

## 🔐 DevOps & DevSecOps Best Practices

* Never commit `.env`
* Use `.env.example` for documentation
* Separate env files per environment
* Use secret managers in production

---

## 🎯 Interview-Ready Explanation

> "Using `.env` files with Docker Compose allows separating configuration from code, enabling environment-specific settings while keeping sensitive data out of version control."

---

## 🏁 Final Takeaways

* `.env` improves security and flexibility
* Docker Compose automatically reads it
* Keeps YAML clean and reusable
* Matches real-world DevOps workflows

---

✅ *This document represents best practices for configuration management using Docker Compose.*
I’ve created a new, clean, professional documentation file in the canvas that explains .env files with Docker Compose from absolute basics → real-world DevOps & DevSecOps practices.

📘 What this new document covers

✅ Why hard-coding values in docker-compose.yml is a bad idea

✅ What a .env file really is (no assumptions)

✅ How Docker Compose automatically reads .env

✅ How .env connects to your main.py using os.getenv()

✅ Proper project structure used by DevOps engineers

✅ DevSecOps rules (what to commit vs what NOT to commit)

✅ Interview-ready explanations

✅ Real production mindset (dev vs prod configs) 