# 🐳 Docker Compose Explained – User Management Service

This document explains **Docker Compose from absolute basics to an intermediate–advanced DevOps level**, using the following `docker-compose.yml` file as a real example.

The goal of this document is:

* 📘 To preserve my learning for future revision
* 🧠 To deeply understand *why* Docker Compose is used
* 💼 To align with real-world DevOps and industry practices
* 🛠️ To explain **each line clearly**, assuming I am a beginner

---

## 📌 What Is Docker Compose?

**Docker Compose** is a tool that allows you to:

> **Define, configure, and run multiple Docker containers using a single YAML file.**

Instead of running long `docker run` commands again and again, Docker Compose lets you describe everything **once**, in a file, and then run it with **one command**.

```bash
docker compose up
```

---

## 🧩 Real-Life Analogy

Imagine you are running a small office:

* You have:

  * One application server
  * Some configuration rules
  * Fixed ports

Without Docker Compose:

* You give instructions **verbally every day**

With Docker Compose:

* You write a **standard operating procedure (SOP)**
* Anyone can follow it and start the office the same way

👉 Docker Compose = **Written SOP for containers**

---

## 🔹 Why Docker Compose Is Used in DevOps

Docker Compose is commonly used for:

* Local development
* Testing environments
* Running multiple services together
* Simulating production-like setups

### Problems Docker Compose Solves

| Without Compose       | With Compose             |
| --------------------- | ------------------------ |
| Long CLI commands     | Clean YAML file          |
| Easy to forget flags  | Everything documented    |
| Hard to share setup   | Easy team collaboration  |
| Manual config changes | Environment-based config |

---

## 📄 Docker Compose File Used in This Project

```yaml
version: "3.9"

services:
  app:
    image: user-management-service:1.0
    ports:
      - "8000:8000"
    environment:
      CPU_THRESHOLD: 75
      MEMORY_THRESHOLD: 75
```

---

## 🔹 Line-by-Line Explanation

---

## 1️⃣ `version: "3.9"`

### What it means

* Specifies the **Docker Compose file format version**
* `3.9` is a stable and widely used version

### Why it matters

* Docker Compose evolves over time
* Version tells Docker **how to interpret the file**

📌 *Think of this like a document format version (PDF v1, v2, etc.)*

---

## 2️⃣ `services:`

### What it means

* Defines **applications (containers)** to be run
* Each service represents **one container**

### Why it is important

* Docker Compose is service-oriented
* Each service can have:

  * Its own image
  * Ports
  * Environment variables
  * Volumes

📌 In real projects, you may have:

* app
* database
* cache
* message queue

---

## 3️⃣ `app:`

### What it means

* Logical **service name**
* Used internally by Docker Compose

### Important notes

* This is NOT the image name
* This is NOT the container name (unless explicitly set)

### Why it matters

* Used in logs, networking, scaling

Example:

```bash
docker compose logs app
```

---

## 4️⃣ `image: user-management-service:1.0`

### What it means

* Specifies the Docker image to use
* Uses a **local image** named `user-management-service:1.0`

### What Docker does internally

1. Checks if image exists locally
2. If not found → pulls from registry

### DevOps best practice

* Use versioned tags (avoid `latest` in production)

---

## 5️⃣ `ports:`

```yaml
ports:
  - "8000:8000"
```

### What it means

* Maps container port to host port

### Format

```text
<host_port>:<container_port>
```

### Why it is required

* Containers are isolated by default
* Port mapping exposes application to host

### Real-life analogy

* Office extension number → main reception number

---

## 6️⃣ `environment:`

```yaml
environment:
  CPU_THRESHOLD: 75
  MEMORY_THRESHOLD: 75
```

### What it means

* Injects environment variables into the container

Inside the container:

```text
CPU_THRESHOLD=75
MEMORY_THRESHOLD=75
```

### Why environment variables are used

* Avoid hard-coding values in code
* Enable configuration per environment
* Follow **12-Factor App principles**

### How this connects to Python code

```python
os.getenv("CPU_THRESHOLD", 80)
```

Docker Compose provides the value.
Python reads it at runtime.

---

## 🧠 Working Principle of Docker Compose (Internals)

When you run:

```bash
docker compose up
```

Docker Compose:

1. Reads `docker-compose.yml`
2. Creates a network
3. Starts defined services
4. Applies ports & environment variables
5. Runs containers

---

## 🧠 Docker Compose vs Docker Run

| Docker Run    | Docker Compose      |
| ------------- | ------------------- |
| One container | Multiple containers |
| Long commands | Clean YAML          |
| Manual setup  | Declarative         |
| Hard to scale | Easy to extend      |

---

## 🔐 DevOps & DevSecOps Best Practices

* Do NOT store secrets directly in YAML
* Use `.env` file or secret managers
* Commit `docker-compose.yml` to Git
* Keep configuration separate from code

---

## 🎯 Interview-Ready Explanation

> "Docker Compose allows defining and running multi-container applications using a declarative YAML file, making local development and testing consistent, repeatable, and closer to production environments."

---

## 🏁 Final Takeaways

* Docker Compose simplifies container orchestration
* YAML file acts as documentation + configuration
* Environment variables make apps configurable
* This approach reflects real DevOps workflows

---

✅ *This document represents my hands-on learning of Docker Compose and container orchestration fundamentals.*
