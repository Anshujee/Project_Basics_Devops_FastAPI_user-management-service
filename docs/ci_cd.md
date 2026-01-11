# CI/CD Pipeline for User Management Service using GitHub Actions & Docker

## 📌 Overview

This repository demonstrates a **complete CI/CD (Continuous Integration & Continuous Deployment)** pipeline using **GitHub Actions** to:

- Validate a Python application  
- Build a Docker image  
- Securely push the image to Docker Hub  
- Follow industry-grade DevOps best practices  

This document explains:

- CI/CD concepts from basics  
- Line-by-line explanation of the pipeline  
- Why secrets are required  
- Common issues faced (threshold = 80, DB not connected, Docker errors)  
- Correct solutions and best practices  

---

## 🧠 What is CI/CD?

### 🔹 Continuous Integration (CI)

CI ensures that:

- Code is automatically tested  
- Dependencies are validated  
- Errors are caught early  

Every time code is pushed:

Developer → Git Push → Automated Checks


---

### 🔹 Continuous Deployment (CD)

CD ensures that:

- The application is packaged  
- Docker images are built  
- Images are pushed to a registry  
- Ready for deployment  



Validated Code → Docker Image → Docker Hub


---

## 📂 CI/CD Pipeline File

**File path:**


.github/workflows/ci-cd.yml


---

## 🧾 Full CI/CD Pipeline YAML

```yaml
name: CI-CD Pipeline

on:
  push:
    branches:
      - main
  pull_request:
    branches:
      - main
  workflow_dispatch:

jobs:
  build-and-push:
    name: Build and Push Docker Image
    runs-on: ubuntu-latest

    steps:
      - name: Checkout code
        uses: actions/checkout@v4

      - name: Set up Python
        uses: actions/setup-python@v5
        with:
          python-version: "3.11"

      - name: Install dependencies
        run: pip install -r app/requirements.txt

      - name: Validate app startup
        run: python -c "import app.main"

      - name: Login to Docker Hub
        run: |
          echo "${{ secrets.DOCKER_PASSWORD }}" | docker login \
          -u "${{ secrets.DOCKER_USERNAME }}" --password-stdin

      - name: Build Docker image
        run: docker build -t ${{ secrets.DOCKER_USERNAME }}/user-management-service:latest -f docker/Dockerfile .

      - name: Push Docker image
        run: docker push ${{ secrets.DOCKER_USERNAME }}/user-management-service:latest

🧱 Line-by-Line Explanation of CI/CD Pipeline
name: CI-CD Pipeline

Defines the workflow name

Visible in GitHub → Actions tab

Helps identify pipeline purpose

on: push

Pipeline triggers when code is pushed to the main branch

Ensures CI/CD runs only on production-ready code

pull_request

Runs pipeline when a PR is raised against main

Used for pre-merge validation

Prevents broken code from reaching production

workflow_dispatch

Allows manual execution of pipeline

Useful for:

Debugging

Re-running pipelines

Emergency rebuilds

jobs: build-and-push

A job is a collection of steps

Represents one execution unit

runs-on: ubuntu-latest

GitHub provides a Linux virtual machine

Industry standard for CI/CD & Docker workloads

Checkout Code
- name: Checkout code
  uses: actions/checkout@v4


Downloads repository source code into runner

Mandatory step for every CI job

Setup Python
- name: Set up Python
  uses: actions/setup-python@v5


Installs Python 3.11

Prevents runtime version mismatch issues

Install Dependencies
- name: Install dependencies
  run: pip install -r app/requirements.txt


Validates dependency correctness

CI fails early if packages are broken

Validate App Startup
- name: Validate app startup
  run: python -c "import app.main"


Confirms application can start

Catches:

Syntax errors

Import errors

Missing dependencies

Login to Docker Hub
- name: Login to Docker Hub


Secure authentication using GitHub Secrets

Prevents credential exposure

Required before pushing images

Build Docker Image
docker build -t <image> -f docker/Dockerfile .


-t → Image name & tag

-f → Dockerfile path

. → Build context (mandatory)

Push Docker Image
docker push <image>


Pushes image to Docker Hub

Completes CD phase

Image becomes deployable

🔐 Why GitHub Secrets Are Required
❌ Without Secrets

Credentials exposed in repository

Security breaches

Compliance failures

✅ With Secrets

Encrypted at rest

Injected only at runtime

Masked in logs

Secrets Used
Secret Name	Purpose
DOCKER_USERNAME	Docker Hub login
DOCKER_PASSWORD	Docker Hub access token
🧩 Common Issues & Fixes
🧩 Issue 1: CPU & Memory Threshold Showing 80 Instead of 40
🔍 Root Cause
CPU_THRESHOLD = os.getenv("CPU_THRESHOLD", 80)


ENV variable not provided

Default value (80) used

✅ Solutions

Option 1: Pass ENV at runtime

docker run -e CPU_THRESHOLD=40 -e MEMORY_THRESHOLD=40 ...


Option 2: Set defaults in Dockerfile

ENV CPU_THRESHOLD=40
ENV MEMORY_THRESHOLD=40

🧩 Issue 2: DB Connection Showing false
🔍 Root Cause

No database container running

Containers are isolated

localhost inside container ≠ host machine

✅ Industry Solution

Use Docker Compose:

Run App + DB together

Shared Docker network

Service-name-based communication

DB_HOST=db

🧩 Issue 3: Docker Build Failed (buildx error)
🔍 Root Cause

Broken multiline command:

docker build -t image \
-f Dockerfile .

✅ Fix

Use single-line command:

docker build -t image -f Dockerfile .

🧩 Issue 4: Old Docker Image Still Running
🔍 Root Cause

Docker does not auto-update local images

✅ Fix
docker stop $(docker ps -q)
docker rm $(docker ps -aq)
docker rmi -f image:latest
docker pull image:latest

🏆 Industry Best Practices Followed

✔ Secrets-based authentication
✔ CI validation before CD
✔ Docker image immutability
✔ ENV-based configuration
✔ Clean YAML structure
✔ Secure credential handling