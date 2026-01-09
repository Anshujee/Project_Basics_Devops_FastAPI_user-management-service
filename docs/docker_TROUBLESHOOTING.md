# 🐳 Dockerfile Explained – User Management Service

This document explains **each line of the Dockerfile used in this project**, written in a **beginner-friendly but DevOps-ready way**.

The purpose of this README is:

* 📘 Future revision for myself
* 🧠 Clear understanding of Docker fundamentals
* 💼 Interview preparation for DevOps roles

---

## 📌 What Is a Dockerfile?

A **Dockerfile** is a text file that contains step-by-step instructions to build a **Docker image**.

Think of it as:

* 🍳 **Recipe** → Dockerfile
* 📦 **Cooked food** → Docker Image
* 🍽️ **Food being eaten** → Docker Container

Docker reads the Dockerfile **top to bottom** and creates image layers.

---

## 📄 Dockerfile Used in This Project

```dockerfile
FROM python:3.11-slim

WORKDIR /app

RUN apt-get update && apt-get install -y gcc \
    && rm -rf /var/lib/apt/lists/*

COPY app/requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY app/ .

EXPOSE 8000

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
```

---

## 🔹 1. `FROM python:3.11-slim`

### What it does

* Uses an **official Python base image**
* Python version: **3.11**
* `slim` = minimal Linux OS

### Why it is used

* Smaller image size
* Faster build and pull
* Reduced security attack surface

📌 *Best Practice*: Always use minimal base images unless extra tools are required.

---

## 🔹 2. `WORKDIR /app`

### What it does

* Sets `/app` as the working directory inside the container
* All future commands run from this directory

### Why it is used

* Avoids hard-coded paths
* Keeps application files organized

Equivalent to:

```bash
cd /app
```

---

## 🔹 3. Installing System Dependencies

```dockerfile
RUN apt-get update && apt-get install -y gcc \
    && rm -rf /var/lib/apt/lists/*
```

### What it does

* Updates package list
* Installs `gcc` compiler
* Cleans package cache

### Why `gcc` is required

* Some Python packages (like `psutil`) need C compilation

### Why cleanup is important

* Reduces image size
* Keeps image lightweight

---

## 🔹 4. `COPY app/requirements.txt .`

### What it does

* Copies only `requirements.txt` into the container

### Why this is important

* Enables **Docker layer caching**
* Dependencies are installed only when requirements change

📌 This significantly speeds up rebuilds during development and CI/CD.

---

## 🔹 5. `RUN pip install --no-cache-dir -r requirements.txt`

### What it does

* Installs Python dependencies listed in `requirements.txt`

### Why `--no-cache-dir`

* Prevents pip from storing cache
* Reduces image size

---

## 🔹 6. `COPY app/ .`

### What it does

* Copies the entire application code into the container

### Why this step comes AFTER dependency install

* Application code changes frequently
* Dependencies change less often
* This improves Docker build performance

---

## 🔹 7. `EXPOSE 8000`

### What it does

* Documents that the container listens on port `8000`

### Important Note

* `EXPOSE` does **not** open the port
* Port mapping is done using `-p` during `docker run`

---

## 🔹 8. `CMD [...]`

```dockerfile
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
```

### What CMD does

* Defines the **default command** when the container starts
* Can be overridden at runtime

### Why CMD is used (instead of ENTRYPOINT)

* Provides flexibility
* Allows debugging and command override

Example override:

```bash
docker run -it user-management-service:1.0 bash
```

---

## 🆚 CMD vs ENTRYPOINT (Beginner-Friendly Comparison)

| Feature     | CMD             | ENTRYPOINT       |
| ----------- | --------------- | ---------------- |
| Purpose     | Default command | Fixed executable |
| Overridable | ✅ Yes           | ❌ No (easily)    |
| Flexibility | High            | Low              |
| Best for    | Applications    | CLI tools        |

📌 *Rule of Thumb*:

* **CMD** → when flexibility is needed
* **ENTRYPOINT** → when container has one fixed job

---

## 🧠 How This Dockerfile Works (Flow)

```
Dockerfile
   ↓
Docker Image
   ↓
Docker Container
   ↓
FastAPI App running on port 8000
```

---

## 🎯 DevOps Learning Takeaways

* Image ≠ Container
* Containers are temporary
* Images are reusable
* Dockerfile layers matter
* CMD vs ENTRYPOINT is a design decision

---

## 🏁 Final Notes

This Dockerfile is:

* Beginner-friendly
* Production-capable
* Easy to debug
* Optimized for learning

As I gain more experience, this Dockerfile can be improved using:

* ENTRYPOINT + CMD combination
* Multi-stage builds
* Non-root users
* Docker Compose
* Kubernetes deployment

---

✅ *This document reflects my hands-on learning journey and understanding of Docker fundamentals.*
