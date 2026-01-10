# CI Pipeline using GitHub Actions

## 📌 Overview

This repository contains a **Continuous Integration (CI) pipeline** implemented using **GitHub Actions** for a **Python FastAPI application**.

The CI pipeline automatically validates code changes by:
- Installing dependencies
- Verifying application startup
- Building a Docker image

This setup follows **industry-standard DevOps best practices** and ensures code quality before moving to deployment (CD).

---

## 🧠 What is Continuous Integration (CI)?

**Continuous Integration (CI)** is a DevOps practice where every code change is automatically:
- Built
- Validated
- Tested (basic checks)

The purpose of CI is to **detect issues early** and prevent broken code from progressing further in the delivery pipeline.

> CI answers the question:  
> **“Is this code safe and buildable?”**

---

## 🔁 CI vs CD (Important Concept)

| CI (Continuous Integration) | CD (Continuous Delivery) |
|-----------------------------|--------------------------|
| Validates code changes | Deploys the application |
| Runs in isolated environment | Runs in target environment |
| Builds Docker image | Runs Docker container |
| App is NOT accessible | App becomes accessible |

📌 **CI does not deploy or expose the application.**

---

## 📂 Repository Structure

├── app/
│ ├── main.py
│ └── requirements.txt
│
├── docker/
│ └── Dockerfile
│
├── ci/
│ └── (CI helper scripts - optional)
│
├── .github/
│ └── workflows/
│ └── ci.yml
│
├── docker-compose.yml
└── README.md


---

## 📍 Why `.github/workflows` Is at Repository Root

GitHub Actions **only detects workflows** placed in:



.github/workflows/*.yml


- This path is **mandatory**
- Placing workflows inside `ci/` will **not work**

The `ci/` directory is used for **scripts**, not workflow definitions.

---

## ⚙️ CI Workflow Configuration (`ci.yml`)

**Location:**


.github/workflows/ci.yml


### Full CI Pipeline File

```yaml
name: CI Pipeline

on:
  push:
    branches:
      - main
  pull_request:

jobs:
  build:
    runs-on: ubuntu-latest

    steps:
      - name: Checkout code
        uses: actions/checkout@v4

      - name: Set up Python
        uses: actions/setup-python@v5
        with:
          python-version: "3.11"

      - name: Install dependencies
        run: |
          pip install -r app/requirements.txt

      - name: Validate app startup
        run: |
          python -c "import app.main"

      - name: Build Docker image
        run: |
          docker build -t user-management-service:ci -f docker/Dockerfile .

🔍 Workflow Explanation (Step-by-Step)
1. Workflow Name
name: CI Pipeline


Defines the display name shown in the GitHub Actions UI.

2. Triggers
on:
  push:
    branches:
      - main
  pull_request:


The pipeline runs when:

Code is pushed to the main branch

A pull request is created or updated

This ensures all changes are automatically validated.

3. Jobs
jobs:
  build:


A job represents a set of steps executed on a fresh virtual machine.

4. Runner
runs-on: ubuntu-latest


Uses a temporary Linux VM provided by GitHub

VM is destroyed after the job completes

Ensures clean, reproducible builds

📌 This runner is not your local machine.

5. Checkout Code
uses: actions/checkout@v4


Downloads the repository code into the runner so the pipeline can access it.

6. Setup Python
uses: actions/setup-python@v5


Installs Python 3.11 in the runner environment.

📌 Pinning versions avoids environment inconsistencies.

7. Install Dependencies
pip install -r app/requirements.txt


Validates that:

Dependency definitions are correct

Required packages can be installed

8. Validate Application Startup
python -c "import app.main"


Checks:

No syntax errors

No missing imports

Application can start

This is a fail-fast validation step.

9. Build Docker Image
docker build -t user-management-service:ci -f docker/Dockerfile .


Validates:

Dockerfile correctness

Application packaging

❌ Does NOT run or deploy the container.

🚫 Why the App Is Not Accessible After CI

After CI completes:

No container is running locally

No ports are exposed

CI runs on GitHub’s cloud runner, not on localhost

To access the app locally, it must be started explicitly:

docker compose up -d

🔄 Running CI Again Without Code Changes

CI pipelines can be re-run without modifying code using:

1. GitHub UI

Go to Actions

Select workflow

Click Re-run jobs

2. Manual Trigger (Recommended)

Add:

workflow_dispatch:


Then run the workflow manually from the Actions UI.

✅ DevOps Best Practices Covered

Event-driven automation

Clean CI/CD separation

Immutable build environments

Fail-fast validation

Docker-based builds

GitHub Actions industry standards

🗣️ Interview-Ready Summary

“I implemented a CI pipeline using GitHub Actions that validates dependencies, checks application startup, and builds Docker images automatically on every push and pull request.”