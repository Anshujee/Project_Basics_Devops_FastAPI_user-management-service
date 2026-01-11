## This DOCUMENT serves as a complete beginner-to-intermediate Kubernetes reference with real-world DevOps clarity.

# 🚀 Why Kubernetes Exists (The REAL Problem It Solves)

This document explains **why Kubernetes was created**, **what real problems it solves**, and **how core Kubernetes objects work**, using a **hands-on, real-world DevOps perspective**.

---

## ❌ Life Without Kubernetes (Only Docker)

Imagine a production system running only Docker containers:

- App crashes ❌ → Manual restart needed
- Traffic increases ❌ → Manual scaling
- Server dies ❌ → Application goes down
- New version deployment ❌ → Downtime during redeploy
- No built-in load balancing ❌
- No self-healing ❌

👉 **Docker is excellent for packaging apps, but Docker alone is not enough for production workloads.**

---

## ✅ What Kubernetes Does

**Kubernetes is a container orchestration platform.**

In simple words:

> **Kubernetes runs, manages, heals, and scales your containers automatically.**

---

## 🧩 Kubernetes Superpowers

| Problem | Kubernetes Solution |
|------|------------------|
| App crash | Auto-restart |
| High traffic | Auto-scale |
| Server failure | Self-healing |
| New version deployment | Rolling updates |
| Multiple containers | Load balancing |
| Configuration management | ConfigMaps & Secrets |

---

## 📌 Interview One-Liner

> **“Kubernetes automates deployment, scaling, and management of containerized applications.”**

---

# 🧠 Core Kubernetes Concepts (Beginner → Pro)

Let’s map Kubernetes concepts to **real-world usage**.

---

## 1️⃣ Pod (Smallest Deployable Unit)

- Smallest unit in Kubernetes
- Contains **one or more containers**
- Containers inside a Pod share:
  - Network
  - Storage

📌 **Important Notes**
- Usually **one container per Pod**
- You **never deploy containers directly** in Kubernetes

---

## 2️⃣ Deployment (Most Important Object)

A **Deployment** tells Kubernetes **how your application should run**.

It defines:
- Which Docker image to run
- How many replicas
- How to update the app
- How to recover from failures

📌 **This is why we use `deployment.yaml`**

---

## 3️⃣ Service (Networking & Access)

Pods are:
- Ephemeral (can die and restart)
- Assigned dynamic IPs ❌

A **Service**:
- Provides stable networking
- Load balances traffic
- Exposes Pods internally or externally

📌 **This is why we use `service.yaml`**

---

# 🧠 Why Two Files? (`deployment.yaml` + `service.yaml`)

| File | Responsibility |
|---|---|
| `deployment.yaml` | How the app runs |
| `service.yaml` | How the app is accessed |

👉 **This separation is intentional and fundamental to Kubernetes design.**

---

# 📦 deployment.yaml — Line-by-Line Explanation

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: ums-deployment
spec:
  replicas: 2
  selector:
    matchLabels:
      app: ums
  template:
    metadata:
      labels:
        app: ums
    spec:
      containers:
        - name: ums-app
          image: <DOCKER_USERNAME>/user-management-service:latest
          imagePullPolicy: Always
          ports:
            - containerPort: 8000
          env:
            - name: CPU_THRESHOLD
              value: "75"
            - name: MEMORY_THRESHOLD
              value: "75"
🔹 apiVersion: apps/v1

Specifies Kubernetes API version

apps/v1 is stable for Deployments

📌 Different Kubernetes objects use different API versions.

🔹 kind: Deployment

Declares the object type

Here, we are creating a Deployment

🔹 metadata
metadata:
  name: ums-deployment


Name of the Deployment

Used in:

Scaling

Logs

Rollouts

📌 Think of this as the identity of the object.

🔹 spec (Desired State)
spec:


Describes what you want Kubernetes to maintain

Kubernetes continuously works to match real state with this desired state

🔹 replicas: 2
replicas: 2


Runs 2 Pods of the application

If one Pod crashes → Kubernetes creates another automatically

📌 High availability achieved here

🔹 selector
selector:
  matchLabels:
    app: ums


Tells the Deployment:

“These Pods belong to me”

📌 Labels are the glue of Kubernetes

🔹 template (Pod Blueprint)

Defines how each Pod should look.

🔹 Pod labels
metadata:
  labels:
    app: ums


Labels applied to Pods

Used by:

Deployment

Service

📌 Labels = routing + ownership + identity

🔹 Containers Section

Defines what runs inside the Pod.

🔹 Container name
name: ums-app


Logical name for the container

Useful for logs and debugging

🔹 Docker image
image: <DOCKER_USERNAME>/user-management-service:latest


Image pulled from Docker Hub

Built by CI/CD pipeline

📌 This is where CI/CD meets Kubernetes

🔹 imagePullPolicy: Always

Always pulls latest image

Useful during development

🔹 Container Port
containerPort: 8000


Port exposed inside the container

Must match application port (e.g., FastAPI)

📌 Kubernetes does not expose this automatically

🔹 Environment Variables
env:
  - name: CPU_THRESHOLD
    value: "75"


Runtime configuration

No code change required

Same image → different behavior

📌 12-Factor App principle

🌐 service.yaml — Line-by-Line Explanation
apiVersion: v1
kind: Service
metadata:
  name: ums-service
spec:
  type: NodePort
  selector:
    app: ums
  ports:
    - port: 80
      targetPort: 8000
      nodePort: 30007

🔹 kind: Service

Creates a networking abstraction

Provides:

Stable IP

Load balancing

🔹 Service Name
metadata:
  name: ums-service


DNS name inside cluster

Accessible as:

http://ums-service

🔹 type: NodePort
type: NodePort


Exposes app on:

<NodeIP>:<NodePort>


📌 Used mainly in Minikube / local clusters

🔹 selector
selector:
  app: ums


Matches Pods using labels

Routes traffic to them

📌 Services do not track Pods directly — only labels

🔹 Ports Mapping
ports:
  - port: 80
    targetPort: 8000
    nodePort: 30007

Field	Meaning
port	Service port
targetPort	Container port
nodePort	External access port
🔁 Traffic Flow
Browser → NodePort → Service → Pod → Container

✅ Final Takeaway

Docker packages applications

Kubernetes runs applications in production

Deployment manages how apps run

Service manages how apps are accessed

Labels connect everything
