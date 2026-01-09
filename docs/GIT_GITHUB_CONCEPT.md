# 📘 Git & GitHub Workflow – DevOps Learning Notes

This document captures my **complete understanding of Git and GitHub workflows** as I learned them step by step while working on my Docker + FastAPI project.

The goal of this README is:

* 🧠 To preserve concepts clearly for future revision
* 🔁 To track my learning journey step by step
* 💼 To follow **real-world DevOps and DevSecOps best practices**
* 📚 To help beginners (including future-me) avoid common confusion

---

## 🔹 Why Git & GitHub Are Important in DevOps

In DevOps:

* **Git** is the *single source of truth*
* All automation (CI/CD, Docker builds, Kubernetes deployments) starts from Git
* GitHub provides collaboration, review, security, and history

Key idea:

> *If it is not in Git, it does not exist.*

---

## 🔹 Git vs GitHub (Very Simple)

| Tool   | Purpose                                                      |
| ------ | ------------------------------------------------------------ |
| Git    | Version control system (runs locally)                        |
| GitHub | Remote platform to store and collaborate on Git repositories |

Git works on your laptop.
GitHub works on the cloud.

---

## 🔹 Repository Initialization (From Scratch)

Steps followed:

```bash
git init
git branch -M main
```

This creates a local Git repository and sets `main` as the default branch.

---

## 🔹 DevSecOps: Using `.gitignore` (VERY IMPORTANT)

`.gitignore` is a normal text file that tells Git **what NOT to track**.

### Why `.gitignore` is important

* Prevents pushing sensitive data (secrets, env files)
* Avoids large unnecessary folders (venv, cache)
* Keeps repository clean and secure

### Example `.gitignore`

```gitignore
# Python
__pycache__/
*.pyc
venv/
.env

# Docker
*.log

# OS
.DS_Store

# IDE
.vscode/
```

### Important clarification

* `.gitignore` **SHOULD be committed to GitHub**
* The file itself is safe
* It protects sensitive/unnecessary files from being committed

---

## 🔹 First Commit (Baseline Snapshot)

After setting up `.gitignore`:

```bash
git add .
git commit -m "Initial commit: baseline FastAPI + Docker setup"
```

This commit acts as a **safe checkpoint**.
I can always return to this state.

---

## 🔹 Branching Strategy (Beginner-Friendly & Professional)

### Branches Used

| Branch    | Purpose                  |
| --------- | ------------------------ |
| main      | Stable, working code     |
| feature/* | New changes, experiments |

### Golden Rule

> **Never experiment directly on `main`.**

---

## 🔹 Feature Branch Workflow

### 1️⃣ Create feature branch

```bash
git checkout -b feature/env-based-healthcheck
```

### 2️⃣ Make changes

* Modify code
* Test locally

### 3️⃣ Commit changes

```bash
git add .
git commit -m "Add env-based health check"
```

### 4️⃣ Push feature branch

```bash
git push -u origin feature/env-based-healthcheck
```

At this stage:

* Local feature branch ✅
* GitHub feature branch ✅
* GitHub main ❌
* Local main ❌

---

## 🔹 Merge vs Pull Request (Most Important Concept)

### 🔸 Merge

* Directly combines branches
* Usually done locally
* Suitable only for personal or learning projects

### 🔸 Pull Request (PR)

A Pull Request means:

> "I have changes ready. Please review and merge them."

PRs provide:

* Code review
* Audit history
* CI/CD checks
* Security visibility

### Real-world rule

> **In companies, PRs are mandatory.**

---

## 🔹 Pull Request Workflow (Step by Step)

### 1️⃣ Push feature branch to GitHub

```bash
git push origin feature/env-based-healthcheck
```

### 2️⃣ Create Pull Request (GitHub UI)

* Click **Compare & Pull Request**
* Add title and description

⚠️ No code is merged yet at this stage.

### 3️⃣ Merge Pull Request (GitHub UI)

* GitHub merges:

  * remote feature → remote main

Important:

* Local machine is **NOT updated automatically**

---

## 🔹 What Happens After PR Merge (Critical Understanding)

After merging PR:

| Location       | Status            |
| -------------- | ----------------- |
| GitHub main    | ✅ Updated         |
| GitHub feature | Exists (optional) |
| Local main     | ❌ Outdated        |
| Local feature  | ❌ Outdated        |

GitHub cannot update local machines automatically.

---

## 🔹 Syncing Local Code After PR Merge (MANDATORY)

### Step 1: Switch to main

```bash
git checkout main
```

### Step 2: Pull latest changes

```bash
git pull origin main
```

Now:

* Local main matches GitHub main

---

## 🔹 Cleaning Up Feature Branches

After successful merge:

```bash
git branch -d feature/env-based-healthcheck
git push origin --delete feature/env-based-healthcheck
```

Keeps repository clean and professional.

---

## 🔹 Mental Model (Very Important)

```
Local feature  → push → GitHub feature
GitHub feature → PR → GitHub main
GitHub main    → pull → Local main
```

---

## 🔹 DevOps & DevSecOps Best Practices Learned

* Always use feature branches
* Never push secrets
* Commit `.gitignore`
* Use pull requests
* Pull after merging PR
* Keep main branch stable

---

## 🔹 Interview-Ready Explanation

> "I follow a feature-branch workflow with pull requests to ensure safe experimentation, code review, and auditability. After merging PRs on GitHub, I sync my local main branch using git pull to stay aligned with the remote repository."

---

## 🏁 Final Note

This document represents my **hands-on understanding** of Git and GitHub as a DevOps learner.

The focus was not just on commands, but on:

* Why things work
* What happens behind the scenes
* How real DevOps teams operate

This README will evolve as my DevOps journey continues.

✅ *Learning by doing, documenting by understanding.*
