# 🐳 Docker Compose – Correct & Professional Setup (DevOps Best Practices)

This document explains the **correct Docker Compose configuration** to resolve the issue I faced where code changes were not reflected at runtime.

It also documents **best practices followed by professional DevOps engineers**, so this file can be used for **future reference, revision, and interviews**.

---

## 📌 Problem Summary (Why This Was Needed)

I observed that:

* Environment variables were updated in `docker-compose.yml`
* Containers were restarted using `docker compose down && up -d`
* But application behavior did NOT change

### Root Cause

The Docker Compose file was using:

```yaml
image: user-management-service:1.0
```

This means Docker Compose was running a **pre-built, frozen image** that did **not contain the latest `main.py` code**.

👉 **Code changes require image rebuild**.

---

## ✅ Correct Docker Compose File (Professional & Recommended)

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
    environment:
      CPU_THRESHOLD: 10
      MEMORY_THRESHOLD: 10
    restart: unless-stopped
```

---

## 🔍 Line-by-Line Explanation (From Basics to Advanced)

---

### 1️⃣ `version: "3.9"`

* Defines Docker Compose file format version
* `3.9` is stable and widely used
* Ensures Docker interprets YAML correctly

---

### 2️⃣ `services:`

* Declares all containers managed by Docker Compose
* Each service = one container

---

### 3️⃣ `app:`

* Logical service name
* Used internally for networking, logs, scaling

---

### 4️⃣ `build:` (MOST IMPORTANT FIX)

```yaml
build:
  context: .
  dockerfile: docker/Dockerfile
```

#### What this means

* Docker Compose will **build a new image** from source
* Uses current project directory as build context
* Uses the specified Dockerfile

#### Why this is critical

* Ensures latest `main.py` is baked into image
* Prevents stale code issues
* Standard for local development

---

### 5️⃣ `image: user-management-service:1.0`

* Names and tags the built image
* Allows reuse of the same image
* Enables push to Docker Hub later

👉 **Best Practice:** Use both `build` and `image` together

---

### 6️⃣ `container_name: user-management-app`

* Explicit container name
* Easier debugging and logs

```bash
docker logs user-management-app
```

---

### 7️⃣ `ports:`

```yaml
ports:
  - "8000:8000"
```

* Maps container port → host port
* Makes FastAPI accessible from browser

---

### 8️⃣ `environment:`

```yaml
environment:
  CPU_THRESHOLD: 10
  MEMORY_THRESHOLD: 10
```

* Injects runtime configuration
* Keeps code environment-agnostic
* Follows **12-Factor App principles**

---

### 9️⃣ `restart: unless-stopped`

* Automatically restarts container if it crashes
* Stops only when explicitly stopped by user

#### Why DevOps engineers use this

* Improves resilience
* Mimics production behavior

---

## 🧠 How Docker Compose Works Internally

When you run:

```bash
docker compose up -d
```

Docker Compose:

1. Reads `docker-compose.yml`
2. Builds image using Dockerfile
3. Injects environment variables
4. Creates container
5. Starts application

---

## 🔄 Correct Workflow After Code Changes

```bash
docker compose down
docker compose build --no-cache
docker compose up -d
```

This guarantees:

* Fresh image
* Latest code
* Correct configuration

---

## 🔐 DevOps & DevSecOps Best Practices Applied

* No secrets hardcoded
* Configuration via environment variables
* Reproducible builds
* Explicit container naming
* Automatic restart policy
* Versioned image tags

---

## 🎯 Interview-Ready Explanation

> "In Docker Compose, using the `build` directive ensures that application code changes are reflected by rebuilding the image. Relying only on the `image` directive can lead to stale code issues. Best practice is to combine both for development workflows."

---

## 🏁 Final Takeaways

* Containers are immutable
* Images must be rebuilt after code changes
* Docker Compose does NOT auto-rebuild
* `build:` is mandatory for active development

---

✅ *This document represents a real-world Docker Compose debugging scenario and its professional resolution.*
