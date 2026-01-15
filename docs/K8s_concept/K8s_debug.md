# 🐳➡️☸️ Kubernetes Debug Journey (Minikube + Docker + FastAPI)

This document captures my **end-to-end Kubernetes debugging journey**, starting from deployment failures to successfully accessing the application in the browser.

The goal is to **preserve real-world learnings**, common mistakes, and the exact reasoning process used by a DevOps Engineer.

---

## 🧠 Project Context

- Application: FastAPI-based User Management Service
- Containerized using: Docker
- Orchestrated using: Kubernetes (Minikube on macOS)
- Exposure method: NodePort Service

---

## 🚦 Initial Deployment Steps

```bash
kubectl apply -f deployment.yaml
kubectl apply -f service.yaml

❌ Problem 1: Pods Not Running (InvalidImageName)
🔍 Observed Output
kubectl get deployments

READY: 0/2

kubectl get pods

STATUS: InvalidImageName

🧠 Root Cause

The Deployment YAML used a placeholder image name:

image: <DOCKER_USERNAME>/user-management-service:latest


Kubernetes tried to pull this literally, which is invalid.

✅ Fix

Replaced placeholder with actual Docker Hub username:

image: anshujee/user-management-service:latest


Built and pushed the image:

docker build -t anshujee/user-management-service:latest .
docker push anshujee/user-management-service:latest


Restarted deployment:

kubectl rollout restart deployment ums-deployment

✅ Result After Fix
kubectl get pods

READY: 1/1
STATUS: Running


✔ Image issue resolved
✔ Pods are now running

❌ Problem 2: App Still Not Accessible in Browser

Even though:

Pods were Running

Service existed

NodePort was assigned

The app was not opening in the browser.

🔍 Step 1: Verify Application Inside Pod

Checked pod logs:

kubectl logs ums-deployment-6754995d5-nbwgr

✅ Log Output
Uvicorn running on http://0.0.0.0:8000

🧠 What This Confirmed
Check	Status
App started	✅
App listening on correct port	✅
App bound to 0.0.0.0	✅
Container is healthy	✅

👉 The application itself was NOT the problem

🧠 Critical Realization

Pod Running ≠ Application Reachable

At this point:

Docker ✅

App ✅

Deployment ✅

Service ✅

The only remaining layer was Minikube networking.

❌ Problem 3: NodePort Not Reachable via <minikube-ip>:nodePort

Attempted:

http://192.168.49.2:30007


❌ Did not work on macOS.

🧠 Root Cause (Minikube Networking Limitation)

On macOS (Docker driver):

Minikube runs inside a VM

NodePort is bound inside the VM

Direct routing via <minikube-ip>:nodePort may fail

📌 This is expected behavior, not a Kubernetes misconfiguration.

✅ Correct Ways to Access Service in Minikube
✅ Solution 1: minikube service (Recommended)
minikube service ums-service


What this does:

Creates a tunnel

Handles networking automatically

Opens the app in browser

✔ This worked successfully

✅ Solution 2: Port Forwarding (Always Works)
kubectl port-forward service/ums-service 8080:80


Then open:

http://localhost:8080


✔ Useful for debugging and local testing

🧠 Important Kubernetes Concepts Learned
1️⃣ Kubernetes Does NOT Deploy GitHub Code

Kubernetes deploys container images

It does NOT:

Read GitHub repos

Build code

Compile applications

Correct flow:

GitHub → CI/CD → Docker Image → Registry → Kubernetes

2️⃣ imagePullPolicy Does NOT Build Images
imagePullPolicy: Always


Means:

Always pull image if it exists

Does NOT build image

Does NOT read GitHub

3️⃣ Local Docker Images ≠ Minikube Docker Images

Mac Docker daemon and Minikube Docker daemon are different

Local images are NOT automatically visible to Minikube

🧪 Key Debugging Commands Used
kubectl get deployments
kubectl get pods
kubectl get services
kubectl logs <pod-name>
kubectl describe pod <pod-name>
kubectl rollout restart deployment <name>
kubectl port-forward service/<name> <port>
minikube service <service-name>

🎯 Final Mental Model
Pod ✅
Service ✅
NodePort ❌ (Minikube macOS)
minikube service ✅
port-forward ✅

🏁 Final Outcome

✔ Application running inside Pods
✔ Service routing correctly
✔ Application accessible via browser
✔ Root causes fully understood

💡 Interview-Ready Summary

“In Minikube on macOS, NodePort may not be directly accessible via node IP. Using minikube service or port-forwarding is the recommended approach. Kubernetes deploys container images, not source code, and requires CI/CD to integrate with GitHub.”
