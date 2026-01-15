# Kubernetes Ingress vs LoadBalancer – Complete Beginner to Production Guide

## 📌 Why this README?

This document explains **why Ingress is needed**, **why LoadBalancer does not scale**, and **how to migrate from LoadBalancer Service to Ingress step by step**.

It is written for:

* Beginners in DevOps & Kubernetes
* Interview preparation
* Real-world production understanding

---

## 1️⃣ How Applications Are Exposed in Kubernetes (Beginner View)

In Kubernetes, applications run inside **Pods**.
Pods are **not accessible directly** from outside the cluster.

To expose Pods, Kubernetes provides a resource called **Service**.

---

## 2️⃣ What Is a Service of Type LoadBalancer?

Example:

```yaml
kind: Service
type: LoadBalancer
```

### What Kubernetes Does Internally

* Kubernetes asks the cloud provider (AWS/Azure/GCP)
* Cloud creates **one external Load Balancer**
* Traffic flow:

```
User → Cloud LoadBalancer → Service → Pod
```

### Why Beginners Like LoadBalancer

* Very easy to use
* Works immediately
* No extra configuration

---

## 3️⃣ Why LoadBalancer Does NOT Scale in Real Companies

### Problems with LoadBalancer Service

| Problem                      | Explanation                    |
| ---------------------------- | ------------------------------ |
| One LoadBalancer per Service | Every app creates a new ELB    |
| High Cost                    | LoadBalancers are billed 24/7  |
| No Path Routing              | Cannot route `/api` and `/web` |
| No Host Routing              | Cannot route `api.example.com` |
| No Central TLS               | Each service manages HTTPS     |
| Poor Traffic Control         | No rate-limit, rewrite, auth   |

📌 **This is why companies avoid exposing every app with LoadBalancer**.

---

## 4️⃣ Core Limitation: Service Works at Network Layer (L4)

A Service:

* Understands **IP and Port**
* Does NOT understand:

  * URLs
  * Paths
  * Hosts
  * HTTPS certificates

So a Service **cannot do HTTP routing**.

---

## 5️⃣ What Is Ingress? (Core Concept)

> **Ingress is NOT a LoadBalancer replacement**

Ingress is a Kubernetes object that defines **HTTP/HTTPS routing rules**.

Example rules:

* `/api` → api-service
* `/web` → web-service
* `admin.example.com` → admin-service

📌 Think of Ingress as:

> **Traffic rules for entering the cluster**

---

## 6️⃣ Very Important: Ingress Has TWO Parts

### 1️⃣ Ingress Controller (Mandatory)

* A real application (usually Nginx)
* Runs as Pods inside the cluster
* Handles incoming HTTP/HTTPS traffic

### 2️⃣ Ingress Resource (Rules)

* YAML configuration
* Tells the controller **how to route traffic**

### Mental Model

```
Ingress Controller = Engine
Ingress YAML       = Traffic Rules
```

---

## 7️⃣ Real Production Architecture (Ingress)

```
User
 ↓
Cloud LoadBalancer (ONLY ONE)
 ↓
Ingress Controller
 ↓
Service (ClusterIP)
 ↓
Pod
```

🔥 **Key Insight**:

> Ingress still uses a LoadBalancer — but only ONE for the whole cluster.

---

## 8️⃣ LoadBalancer vs Ingress (Clear Comparison)

| Feature             | LoadBalancer | Ingress   |
| ------------------- | ------------ | --------- |
| Cloud LoadBalancers | One per app  | One total |
| Cost                | High         | Low       |
| Path-based routing  | ❌            | ✅         |
| Host-based routing  | ❌            | ✅         |
| TLS management      | Per service  | Central   |
| Production usage    | ❌            | ✅         |

---

## 9️⃣ What Changes When Moving to Ingress?

### ❌ Deployment.yaml

* **NO change**
* Pods do not care how traffic enters

### ✅ Service.yaml

* Change type from `LoadBalancer` → `ClusterIP`

### ✅ New File

* Create `ingress.yaml`

---

## 🔟 Step-by-Step Migration: LoadBalancer → Ingress

### Step 1️⃣ Change Service Type

❌ Old Service:

```yaml
type: LoadBalancer
```

✅ New Service:

```yaml
apiVersion: v1
kind: Service
metadata:
  name: myapp-service
spec:
  type: ClusterIP
  selector:
    app: myapp
  ports:
    - port: 80
      targetPort: 8080
```

---

### Step 2️⃣ Install Ingress Controller

Ingress Controller:

* Runs as Pods
* Exposed using ONE LoadBalancer

(This step will be explained line-by-line separately.)

---

### Step 3️⃣ Create Ingress Resource

```yaml
apiVersion: networking.k8s.io/v1
kind: Ingress
metadata:
  name: myapp-ingress
spec:
  rules:
  - host: myapp.example.com
    http:
      paths:
      - path: /
        pathType: Prefix
        backend:
          service:
            name: myapp-service
            port:
              number: 80
```

---

### Step 4️⃣ DNS Configuration (Conceptual)

Point DNS:

```
myapp.example.com → Ingress LoadBalancer IP
```

---

## 1️⃣1️⃣ What Does NOT Change (Important)

| Component        | Changed? |
| ---------------- | -------- |
| Deployment       | ❌ No     |
| Container Image  | ❌ No     |
| Application Code | ❌ No     |
| Pod Ports        | ❌ No     |

---

## 1️⃣2️⃣ Interview-Ready Explanation

> “Using a LoadBalancer service exposes one application per cloud load balancer, which becomes expensive and does not support HTTP routing. Ingress introduces a centralized entry point where a single LoadBalancer fronts an Ingress Controller. Ingress resources define routing rules to internal ClusterIP services, enabling path-based routing, host-based routing, centralized TLS, and better scalability.”

---

## 1️⃣3️⃣ Golden Rule (Memorize)

> **Service exposes Pods, Ingress exposes Services**

---

## ✅ Summary

* LoadBalancer is simple but not scalable
* Ingress provides centralized traffic control
* Only Service type changes (not Deployment)
* Ingress is mandatory for production Kubernetes

---

📌 Next Step:
👉 **Ingress Controller installation explained line-by-line**
