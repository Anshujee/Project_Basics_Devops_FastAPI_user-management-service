Health Checks in Docker & FastAPI – Complete DevOps Guide
📘 What this README includes (important)

This is not just notes. It documents:

✔ What a health check is (from basics)

✔ Why DevOps engineers care about health checks

✔ Difference between running vs healthy

✔ App-level health (/health)

✔ DB health logic and why it belongs in /health

✔ Why /db-check returned 404 and why that is correct

✔ When /db-check is optional vs useful

✔ Docker healthchecks (container-level)

✔ Why depends_on alone is not enough

✔ Why DB healthcheck was added in Docker Compose

✔ Why app healthcheck must also be added

✔ Why stopping app “felt like” DB stopped

✔ Correct professional health-check design

✔ Interview-ready explanations

✔ Real DevOps mental models

This README literally reflects your entire thought process and learning path.
# 🩺 Health Checks in Docker & FastAPI – Complete DevOps Guide

This document is a **complete summary of everything learned about health checks** during the FastAPI + Docker + PostgreSQL journey.

It captures:

* All doubts raised
* Why those doubts are valid
* How health checks actually work
* How DevOps engineers design health checks in real systems

This README is written for **future revision**, **interview preparation**, and **real-world DevOps understanding**.

---

## 1️⃣ What Is a Health Check?

A **health check** is a mechanism to answer one simple but critical question:

> **Is my service actually working, or is it just running?**

In DevOps:

* "Running" ≠ "Healthy"
* A process may be alive but unable to serve traffic

Health checks help systems **detect failures automatically**.

---

## 2️⃣ Why Health Checks Are Important (DevOps Perspective)

Health checks are used by:

* Docker
* Docker Compose
* Load balancers
* Kubernetes
* Monitoring systems

They help to:

* Stop traffic to unhealthy services
* Restart failed containers
* Detect dependency failures (DB, cache, etc.)
* Improve reliability and uptime

Without health checks:

* Broken services may still receive traffic
* Failures remain hidden

---

## 3️⃣ Types of Health Checks in Our Project

We implemented **two layers of health checks**:

1. **Application-level health check** (FastAPI)
2. **Container-level health check** (Docker)

These two layers work together.

---

## 4️⃣ Application-Level Health Check (`/health`)

### What `/health` Does

The `/health` endpoint checks:

* CPU usage
* Memory usage
* Database connectivity

It represents the **overall system health**, not just the app process.

### Why DB Is Included in `/health`

Because:

* The app cannot function without the database
* If DB is down → system is effectively down

This is a **real production practice**.

---

## 5️⃣ Database Health Check Logic (Inside App)

We added a function:

```python
def check_database_connection():
    try:
        connection = psycopg2.connect(...)
        connection.close()
        return True
    except Exception:
        return False
```

This function:

* Tries to connect to PostgreSQL
* Returns `True` if successful
* Returns `False` if DB is unreachable

This result is used inside `/health`.

---

## 6️⃣ Why `/db-check` Initially Returned 404

### The Doubt

> "DB is running and healthy, but `/db-check` returns Not Found"

### The Reason

* `/db-check` endpoint was **not defined** in `main.py`
* FastAPI correctly returned `404 Not Found`

This behavior is **expected and correct**.

---

## 7️⃣ Why `/db-check` Is Optional (DevOps Best Practice)

In real systems:

* `/health` is the **single source of truth**
* Dependency-specific endpoints are usually internal or removed

However, `/db-check` was added:

* For learning
* For debugging
* For verification

Both approaches are valid depending on use case.

---

## 8️⃣ Docker Health Check (Container-Level)

Docker health checks allow Docker to determine:

> "Is this container healthy or unhealthy?"

Docker tracks health separately from container status.

Example:

```bash
docker ps
```

Output:

```text
Up 2 minutes (healthy)
Up 5 minutes (unhealthy)
```

---

## 9️⃣ Why DB Health Check Was Added in Docker Compose

### Problem Identified

`depends_on` only controls **startup order**, not readiness.

### Solution

Add a DB health check using PostgreSQL’s built-in command:

```yaml
healthcheck:
  test: ["CMD-SHELL", "pg_isready -U useradmin -d userdb"]
```

This ensures:

* Docker knows when DB is ready
* App starts only after DB is healthy

---

## 🔟 Why App Health Check Was Also Added in Docker Compose

### The Doubt

> "We added DB health, but what about app health?"

### The Answer

Each service can fail independently.

Therefore:

* DB needs its own health check
* App needs its own health check

Docker Compose now tracks:

* App health via `/health`
* DB health via `pg_isready`

This is **professional DevOps practice**.

---

## 1️⃣1️⃣ Complete Docker Compose Health Check Setup

```yaml
healthcheck:
  test: ["CMD", "curl", "-f", "http://localhost:8000/health"]
  interval: 30s
  timeout: 5s
  retries: 3
  start_period: 15s
```

This ensures:

* App is reachable
* App dependencies are healthy
* False failures are avoided during startup

---

## 1️⃣2️⃣ Why App Stop Felt Like DB Stop

### The Doubt

> "When app stops, DB also feels like it stopped"

### Explanation

* DB container was still running
* App was the only interface to DB
* When app stopped, visibility was lost

This was a **perception issue**, not a runtime issue.

---

## 1️⃣3️⃣ Correct Health Check Design Summary

| Layer              | Purpose               |
| ------------------ | --------------------- |
| `/health`          | Overall system health |
| DB check           | Dependency readiness  |
| Docker healthcheck | Container health      |

All three together form a **reliable system**.

---

## 1️⃣4️⃣ DevOps & Interview Takeaways

* Running ≠ Healthy
* Health checks are mandatory for production
* Dependencies must be included in health
* Docker Compose health checks mirror Kubernetes probes
* Good health design improves resilience

---

## 🏁 Final Notes

This health check implementation reflects:

* Real-world DevOps thinking
* Production-grade reliability
* Correct system-level design

This document serves as a **long-term reference** and can be extended further for:

* Kubernetes liveness/readiness probes
* Monitoring & alerting
* CI/CD health validation

---

✅ *Learning by questioning, understanding by implementing.*
