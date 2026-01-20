HTTPS with NGINX Ingress + cert-manager (Complete Hands-On Guide)

This document explains end-to-end HTTPS implementation on Kubernetes using NGINX Ingress and cert-manager, including real debugging steps, DNS configuration, and common mistakes.

It is written from first-principles, assuming no prior experience with HTTPS, ACM, Route53, or cert-manager.

📌 Architecture Overview
Browser (HTTPS)
   ↓
Public DNS (GoDaddy → Route53)
   ↓
AWS ELB (created by NGINX Ingress Controller)
   ↓
NGINX Ingress Controller (Kubernetes)
   ↓
Service (ClusterIP)
   ↓
Pod (FastAPI Application)


TLS termination happens inside Kubernetes using cert-manager + Let’s Encrypt.

🧠 Why NGINX + cert-manager (Instead of AWS ACM)
Aspect	NGINX + cert-manager
TLS Provider	Let’s Encrypt
Cloud Dependency	Cloud-agnostic
TLS Location	Inside cluster
Works with GoDaddy	✅ Yes
Production Ready	✅ Yes

⚠️ AWS ACM certificates cannot be used with NGINX, because ACM certificates are not exportable.

🧩 Prerequisites

Before starting, ensure:

Kubernetes cluster is running (EKS / Minikube)

Application Deployment and Service are working

Domain is purchased (GoDaddy used here)

DNS is delegated to Route53

kubectl configured correctly

🚀 Step 1 — Install NGINX Ingress Controller
kubectl apply -f https://raw.githubusercontent.com/kubernetes/ingress-nginx/main/deploy/static/provider/cloud/deploy.yaml

Verify
kubectl get pods -n ingress-nginx
kubectl get svc -n ingress-nginx


Expected:

ingress-nginx-controller → Running

Service type → LoadBalancer

AWS ELB DNS name generated

🚀 Step 2 — Install cert-manager

cert-manager automates certificate issuance and renewal.

kubectl apply -f https://github.com/cert-manager/cert-manager/releases/latest/download/cert-manager.yaml

Verify
kubectl get pods -n cert-manager


Expected pods:

cert-manager

cert-manager-cainjector

cert-manager-webhook

🚀 Step 3 — Create ClusterIssuer (Let’s Encrypt)
File: k8s/cluster-issuer.yaml
apiVersion: cert-manager.io/v1
kind: ClusterIssuer
metadata:
  name: letsencrypt-prod
spec:
  acme:
    server: https://acme-v02.api.letsencrypt.org/directory
    email: your-email@example.com
    privateKeySecretRef:
      name: letsencrypt-prod
    solvers:
      - http01:
          ingress:
            class: nginx

Apply
kubectl apply -f k8s/cluster-issuer.yaml

Verify
kubectl get clusterissuer


Expected:

letsencrypt-prod   READY=True

🌍 Step 4 — DNS Configuration (GoDaddy + Route53)
🔹 Important DNS Concept

GoDaddy → Domain registrar

Route53 → DNS authority

Application traffic must point to NGINX ELB, not ACM

🔹 Get NGINX ELB DNS
kubectl get svc -n ingress-nginx


Example:

aa0f0f14401864186b8a43ba93b6601c-966052478.us-west-2.elb.amazonaws.com

🔹 Create Record in Route53

Route53 → Hosted Zone → yourdomain.in

Create record:

Field	Value
Record name	ums
Type	CNAME
Value	<NGINX-ELB-DNS>
TTL	Default

📌 ACM validation records are NOT for routing traffic

🔹 Verify DNS
dig ums.yourdomain.in


Expected:

NOERROR

CNAME → ELB DNS

A → Public IP

🚀 Step 5 — HTTPS Ingress (Final & Correct)
File: k8s/ingress-nginx-https.yaml
apiVersion: networking.k8s.io/v1
kind: Ingress
metadata:
  name: ums-ingress
  annotations:
    cert-manager.io/cluster-issuer: letsencrypt-prod
spec:
  ingressClassName: nginx
  tls:
    - hosts:
        - ums.yourdomain.in
      secretName: ums-tls
  rules:
    - host: ums.yourdomain.in
      http:
        paths:
          - path: /
            pathType: Prefix
            backend:
              service:
                name: ums-service
                port:
                  number: 80

Apply
kubectl apply -f k8s/ingress-nginx-https.yaml

🔍 Step 6 — Certificate Lifecycle Debugging
Check certificate
kubectl get certificate


Expected flow:

READY=False (initial)

READY=True (after 1–5 minutes)

Describe certificate (most important debug)
kubectl describe certificate ums-tls


Look for:

Order created

Challenge completed

Certificate issued

Common Failure (Learned the Hard Way)

❌ Using example.com

acme:error:rejectedIdentifier
Cannot issue for "example.com"


✅ Fix: Always use a real domain

🔐 Step 7 — Verify HTTPS
Browser
https://ums.yourdomain.in/health

Curl
curl -v https://ums.yourdomain.in/health


Expected:

Valid TLS certificate

Let’s Encrypt issuer

Application JSON response

🧠 Key Debugging Lessons Learned
1️⃣ cert-manager only reacts to Ingress

No Ingress → No Certificate

2️⃣ DNS must be correct before applying Ingress
3️⃣ ACM validation ≠ application routing
4️⃣ example.com is forbidden by Let’s Encrypt
5️⃣ TLS Secret is auto-created by cert-manager
🏆 Outcome

✔ HTTPS implemented successfully
✔ DNS debugging mastered
✔ cert-manager lifecycle understood
✔ Real-world production troubleshooting done

This setup is cloud-agnostic, production-grade, and interview-ready.

Expalnation 2 

# 🔐 HTTPS Implementation with NGINX Ingress Controller

*(cert-manager + Let’s Encrypt + GoDaddy DNS)*

---

## 📌 Overview

This document explains **step-by-step how HTTPS is implemented in Kubernetes using the NGINX Ingress Controller**, along with **cert-manager**, **Let’s Encrypt**, and a **domain purchased from GoDaddy**.

This approach is:

* Cloud-agnostic
* Production-proven
* Widely used in real Kubernetes environments

This README is written for:

* Hands-on learning
* Future revision
* Interview preparation
* Real DevOps project documentation

---

## 🧠 Why This Approach?

### ❓ Why not AWS ACM here?

* AWS ACM certificates **cannot be exported**
* NGINX requires `.crt` and `.key` files
* Therefore, **ACM cannot be used directly with NGINX**

### ✅ Correct Solution

Use:

* **NGINX Ingress Controller** for routing
* **cert-manager** for certificate automation
* **Let’s Encrypt** as the Certificate Authority

---

## 🏗️ Final Architecture

```
Browser (HTTPS)
   ↓
DNS (GoDaddy / Route53)
   ↓
AWS ELB (created by NGINX Service)
   ↓
NGINX Ingress Controller
   ↓
TLS termination (cert-manager + Let's Encrypt)
   ↓
Service (ClusterIP)
   ↓
Application Pod (FastAPI on HTTP)
```

---

## 📋 Prerequisites

* Kubernetes cluster (EKS / Minikube / any managed K8s)
* Application deployed and reachable via Service
* Domain purchased from **GoDaddy**
* Public internet access enabled

---

## 🧩 Step 1 — Install NGINX Ingress Controller

### Why?

* NGINX handles host/path routing
* Runs inside Kubernetes
* Exposed using a Service of type `LoadBalancer`

### Command

```bash
kubectl apply -f https://raw.githubusercontent.com/kubernetes/ingress-nginx/main/deploy/static/provider/cloud/deploy.yaml
```

### Verify

```bash
kubectl get pods -n ingress-nginx
kubectl get svc -n ingress-nginx
```

Expected:

* `ingress-nginx-controller` pod → Running
* Service type → `LoadBalancer`
* AWS ELB DNS created automatically

---

## 🧩 Step 2 — Install cert-manager

### Why?

cert-manager:

* Requests certificates from Let’s Encrypt
* Handles renewals automatically
* Stores certificates as Kubernetes Secrets

### Install

```bash
kubectl apply -f https://github.com/cert-manager/cert-manager/releases/latest/download/cert-manager.yaml
```

### Verify

```bash
kubectl get pods -n cert-manager
```

Expected pods:

* cert-manager
* cert-manager-cainjector
* cert-manager-webhook

---

## 🧩 Step 3 — Create ClusterIssuer (Let’s Encrypt)

### What is ClusterIssuer?

A **cluster-wide configuration** that defines:

* Which CA to use
* How certificates should be issued

### `cluster-issuer.yaml`

```yaml
apiVersion: cert-manager.io/v1
kind: ClusterIssuer
metadata:
  name: letsencrypt-prod
spec:
  acme:
    server: https://acme-v02.api.letsencrypt.org/directory
    email: your-email@example.com
    privateKeySecretRef:
      name: letsencrypt-prod
    solvers:
      - http01:
          ingress:
            class: nginx
```

### Apply

```bash
kubectl apply -f cluster-issuer.yaml
```

---

## 🧩 Step 4 — DNS Configuration (GoDaddy)

### Why DNS Is Mandatory

Let’s Encrypt must reach your domain over the internet to verify ownership.

---

### Configure DNS in GoDaddy

1. Login to GoDaddy
2. Go to **My Products → DNS**
3. Add a new record:

| Field | Value                  |
| ----- | ---------------------- |
| Type  | A                      |
| Host  | ums                    |
| Value | `<NGINX-ELB-DNS-NAME>` |
| TTL   | Default                |

Example:

```
ums.example.com → a5e29b7b1024c4376.us-west-2.elb.amazonaws.com
```

---

## 🧩 Step 5 — HTTPS Ingress Resource (Final)

### Correct Ingress YAML (HTTPS-enabled)

```yaml
apiVersion: networking.k8s.io/v1
kind: Ingress
metadata:
  name: ums-ingress
  annotations:
    kubernetes.io/ingress.class: nginx
    cert-manager.io/cluster-issuer: letsencrypt-prod
spec:
  tls:
    - hosts:
        - ums.example.com
      secretName: ums-tls
  rules:
    - host: ums.example.com
      http:
        paths:
          - path: /
            pathType: Prefix
            backend:
              service:
                name: ums-service
                port:
                  number: 80
```

### Apply

```bash
kubectl apply -f ingress-nginx-https.yaml
```

---

## 🧩 Step 6 — Observe Certificate Lifecycle

### Check certificate

```bash
kubectl get certificate
kubectl describe certificate ums-tls
```

Expected:

```
Ready: True
```

### Check challenge

```bash
kubectl get challenges
```

This shows how cert-manager completes the HTTP-01 challenge.

---

## 🧩 Step 7 — Test HTTPS

### Browser

```
https://ums.example.com/health
```

### Curl

```bash
curl https://ums.example.com/health
```

Expected:

* HTTPS lock icon 🔒
* Valid Let’s Encrypt certificate
* Application JSON response

---

## 🧪 Debugging Commands (Very Important)

```bash
kubectl describe ingress ums-ingress
kubectl logs -n cert-manager deploy/cert-manager
kubectl get events
```

---

## ❌ Common Issues & Fixes

### Certificate stuck in `Pending`

* DNS not pointing to NGINX ELB
* Host mismatch

### HTTPS not working

* cert-manager not running
* TLS secret not created

### 404 error

* Wrong service name
* Path mismatch

---

## 🗣️ Interview-Ready Explanation

> “I implemented HTTPS using NGINX Ingress Controller with cert-manager and Let’s Encrypt. TLS is terminated inside the Kubernetes cluster, making the solution cloud-agnostic and production-ready.”

---

## ✅ What This Setup Demonstrates

* Deep Kubernetes Ingress knowledge
* TLS lifecycle understanding
* cert-manager automation
* DNS integration
* Production-grade HTTPS implementation

---

## 🔜 Next Steps

* Package everything using **Helm**
* Compare with **AWS ALB + ACM**
* Implement **HPA and monitoring**

---

## 📌 Final Note

This documentation is based on **real debugging, failures, and fixes**, not just theory.
It represents **practical DevOps experience**.

---
