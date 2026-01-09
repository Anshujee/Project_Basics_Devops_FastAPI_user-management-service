# 📘 FastAPI Health Check Project – Troubleshooting & Solutions

This document captures **all the issues I faced while building and running my first FastAPI-based Python application**, along with **clear explanations and permanent solutions**.

The goal of this README is:

* To help **future-me** quickly debug similar issues
* To help **reviewers/interviewers** understand my problem-solving skills
* To help **other beginners** avoid common mistakes

---

## 🧩 Project Context

* **Language**: Python 3
* **Framework**: FastAPI
* **Server**: Uvicorn
* **Environment**: Virtual Environment (venv)
* **IDE**: VS Code
* **OS**: macOS

---

## ❗ Problem 1: `python3` / `uvicorn` Command Not Working

### 🔴 Symptoms

* `python3` command not found
* `uvicorn` command not found
* Application not starting

### 🧠 Root Cause

The virtual environment was **not activated**, so the system was using global Python instead of project-specific Python.

### ✅ Solution

Activate the virtual environment before running anything:

```bash
cd app
source venv/bin/activate
```

Verify:

```bash
which python
```

Expected output:

```
.../app/venv/bin/python
```

---

## ❗ Problem 2: VS Code Error – `import fastapi could not be resolved`

### 🔴 Symptoms

* Red underline under `fastapi` or `psutil`
* VS Code warning: *Import could not be resolved*
* Code runs in terminal but editor shows errors

### �� Root Cause

VS Code editor was using **system Python**, while dependencies were installed in **virtual environment Python**.

### ✅ Solution

Explicitly tell VS Code to use the venv interpreter:

1. Open Command Palette:

   * macOS: `Cmd + Shift + P`
2. Select:

   ```
   Python: Select Interpreter
   ```
3. Choose:

   ```
   app/venv/bin/python
   ```
4. Restart VS Code

---

## ❗ Problem 3: Application Works Once but Fails After Restarting VS Code

### 🔴 Symptoms

* App works initially
* After restarting VS Code, imports fail again
* `uvicorn` fails or FastAPI not found

### 🧠 Root Cause

Virtual environment **activation is temporary** and resets when terminal/VS Code restarts.

> Virtual Environment folder = permanent
> Virtual Environment activation = session-based

### ✅ Solution (Correct Workflow)

Every time you open VS Code terminal:

```bash
cd app
source venv/bin/activate
uvicorn main:app --host 0.0.0.0 --port 8000
```

🚫 Do NOT recreate the venv again.

---

## ❗ Problem 4: Health Check Always Returns `UP`

### 🔴 Symptoms

* `/health` endpoint always returns `UP`
* `if–else` logic never changes result

### 🧠 Root Cause

The health check logic used **hard-coded values**, not real system checks.

Example (wrong):

```python
server_running = True
```

### ✅ Solution

Replace static values with **real runtime checks** using `psutil`:

```python
cpu_usage = psutil.cpu_percent(interval=1)
memory_usage = psutil.virtual_memory().percent
```

Add conditional logic:

```python
if cpu_usage < 80 and memory_usage < 80:
    status = "UP"
else:
    status = "DOWN"
```

---

## ❗ Problem 5: Packages Reinstalled Every Time (Wrong Practice)

### 🔴 Symptoms

* Running `pip install` repeatedly
* Recreating venv again and again

### 🧠 Root Cause

Misunderstanding between **creating a venv** and **activating a venv**.

### ✅ Correct Understanding

| Action                     | Frequency     |
| -------------------------- | ------------- |
| `python3 -m venv venv`     | One time only |
| `pip install ...`          | One time only |
| `source venv/bin/activate` | Every session |

---

## ❗ Problem 6: `psutil` / `fastapi` Works in Terminal but Not in VS Code

### 🔴 Symptoms

* Terminal runs fine
* VS Code editor shows unresolved imports

### 🧠 Root Cause

VS Code terminal and VS Code Python language server were pointing to **different Python interpreters**.

### ✅ Solution

Ensure all of the following point to the same Python:

* `which python`
* `which pip`
* VS Code Interpreter

Expected path:

```
.../app/venv/bin/python
```

---

## ✅ Best Practices Learned

* Always use a virtual environment
* Never install packages globally
* Never recreate venv unnecessarily
* Always verify `which python`
* Configure VS Code interpreter explicitly
* Health checks must be dynamic, not static

---

## 🏁 Final Takeaway

This project helped me understand **real-world Python & DevOps issues**, including:

* Environment mismatch
* IDE vs terminal differences
* Dependency isolation
* Health check best practices
* Debugging mindset

These issues are **common in production systems**, CI/CD pipelines, Docker containers, and Kubernetes clusters.

Solving them strengthened my fundamentals and made me confident working with Python-based microservices.

---

✅ *This troubleshooting guide is intentionally detailed to reflect real-world learning and debugging experience.*

