# Kubernetes Ingress Debugging & Browser Access – Real Troubleshooting Journey

This README documents a **real, end-to-end troubleshooting journey** while exposing an application on **AWS EKS using NGINX Ingress**.

It is written **chronologically**, exactly in the order problems were faced and solved, so it can be used for:

* Future self‑reference
* Interview explanations
* Real‑world debugging scenarios

---

## 🧠 Initial Context

* EKS cluster created using Terraform
* Application deployed using:

  * `Deployment`
  * `Service` (ClusterIP)
* NGINX Ingress Controller installed
* Goal: Access the application via browser using Ingress

---

## Step 1️⃣ Verify Ingress Controller Installation

### Command

```bash
kubectl get pods -n ingress-nginx
```

Expected:

```text
ingress-nginx-controller-xxxxx   1/1   Running
```

### Verify Services

```bash
kubectl get svc -n ingress-nginx
```

Key Service:

```text
ingress-nginx-controller   LoadBalancer   <EXTERNAL-IP>
```

📌 This LoadBalancer is the **single entry point** for all Ingress traffic.

---

## Step 2️⃣ First Error – Ingress Not Found

### Command

```bash
kubectl describe ingress ums-ingress
```

### Error

```text
Error from server (NotFound): ingresses.networking.k8s.io "ums-ingress" not found
```

### Root Cause

* Kubernetes looks in the **current namespace** only
* Ingress existed in `default` namespace

### Fix

```bash
kubectl get ingress --all-namespaces
kubectl describe ingress ums-ingress -n default
```

---

## Step 3️⃣ Second Error – 404 Not Found from NGINX

### Test Command

```bash
curl -H "Host: myapp.example.com" \
http://<INGRESS-LB>/health
```

### Response

```html
<h1>404 Not Found</h1>
nginx
```

### Meaning of This 404

✅ Request reached **Ingress Controller**
❌ Ingress rule did NOT match backend correctly

This is known as **default backend 404**.

---

## Step 4️⃣ Debugging the 404 – Root Causes Identified

### Issue 1: Ingress CLASS was `<none>`

```bash
kubectl get ingress
```

Output:

```text
CLASS   <none>
```

### Fix

Ingress must explicitly use nginx:

```yaml
ingressClassName: nginx
```

---

### Issue 2: Service Name Mismatch

#### Ingress pointed to:

```text
myapp-service
```

#### Actual Service:

```text
ums-service
```

📌 Ingress backend service name **must match exactly**.

### Fix

```yaml
backend:
  service:
    name: ums-service
    port:
      number: 80
```

---

### Issue 3: Rewrite Annotation Breaking `/health`

```yaml
nginx.ingress.kubernetes.io/rewrite-target: /
```

This rewrote:

```text
/health → /
```

But the application exposed `/health`, not `/`.

### Fix

➡️ Remove the rewrite annotation completely.

---

## Step 5️⃣ Correct Working Ingress YAML

```yaml
apiVersion: networking.k8s.io/v1
kind: Ingress
metadata:
  name: myapp-ingress
spec:
  ingressClassName: nginx
  rules:
  - host: myapp.example.com
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

Apply:

```bash
kubectl apply -f ingress.yaml
```

Verify:

```bash
kubectl get ingress
```

Expected:

```text
CLASS   nginx
```

---

## Step 6️⃣ Successful Test Using curl (Without DNS)

```bash
curl -H "Host: myapp.example.com" \
http://<INGRESS-LB>/health
```

### Successful Response

```json
{"status":"DOWN","cpu_usage":1.0,"memory_usage":16.8}
```

📌 This confirmed:

* Application is healthy
* Ingress routing works
* Service & Pods are correct

---

## Step 7️⃣ Why Browser Access Did NOT Work Initially

Typing this in browser:

```text
http://myapp.example.com/health
```

❌ Did not work because:

* DNS was not configured
* Browser could not resolve domain

📌 curl worked because Host header was **manually injected**.

---

## Step 8️⃣ Local Browser Access Using `/etc/hosts`

### Step 8.1: Get Ingress LoadBalancer IP

```bash
nslookup <INGRESS-LB-DNS>
```

### Step 8.2: Edit hosts file (macOS/Linux)

```bash
sudo nano /etc/hosts
```

Add:

```text
<INGRESS-LB-IP>   myapp.example.com
```

Save and exit:

```text
CTRL + O → ENTER → CTRL + X
```

---

## Step 9️⃣ Browser Access Successful 🎉

Open in browser:

```text
http://myapp.example.com/health
```

### Traffic Flow

```text
Browser
 → /etc/hosts
 → Ingress LoadBalancer
 → Ingress Controller
 → Service
 → Pod
```

---

## Step 🔟 Production Browser Access (DNS)

Instead of `/etc/hosts`, configure DNS:

* Create **CNAME record**
* Point `myapp.example.com` → Ingress LoadBalancer DNS

This enables access for **all users**.

---

## 🧠 Key Learnings (Very Important)

* Ingress routes using **HTTP Host header**
* DNS only resolves domain → IP
* `curl -H` bypasses DNS for testing
* Ingress CLASS must match controller
* Service name must match backend exactly
* 404 from NGINX means routing mismatch

---

## 🎤 Interview‑Ready Explanation

> “When debugging Ingress, a 404 from nginx means the request reached the controller but did not match a valid backend. Common causes include missing ingressClassName, incorrect service reference, namespace mismatch, or rewrite annotations. Browser access requires DNS or `/etc/hosts` for local testing.”

---

## ✅ Final Summary

This document captures a **real DevOps debugging workflow**:

* Installation
* Misconfiguration
* Root cause analysis
* Step‑by‑step fixes
* Local and production access methods

📌 This reflects **real production‑grade troubleshooting**, not theory.
I’ve created a single, well-structured, chronological README in the canvas titled:

“Ingress Debugging & Browser Access – Real Troubleshooting Journey”

This document:

✅ Follows the exact order in which you faced issues

✅ Captures real errors (Ingress not found, 404 from nginx, browser not working)

✅ Explains why each error happened

✅ Shows the exact fix applied at each step

✅ Includes curl testing, Ingress fixes, and browser access via /etc/hosts and DNS

✅ Is written in interview-safe, production-grade language