# Helm `values.yaml` – Deep Conceptual Guide (For Lifetime Revision)

## 📌 Overview

This document explains **Helm configuration (`values.yaml`) in complete depth** using a real DevOps project.

The goal of this document is:

* Long-term revision
* Strong conceptual clarity
* Interview preparation
* Production-level understanding

This file focuses on **WHY each field exists**, **HOW Helm uses it**, and **HOW it impacts Kubernetes and AWS**.

---

## 🧠 Core Principle (Must Remember Forever)

> **Helm separates CONFIGURATION from LOGIC**

* `values.yaml` → **WHAT you want**
* `templates/*.yaml` → **HOW Kubernetes objects are created**

Kubernetes **never sees `values.yaml`**.
Helm renders templates first, then sends **pure YAML** to Kubernetes.

---

## 📄 Example `values.yaml`

```yaml
replicaCount: 2

image:
  repository: dockerhub-username/user-management-service
  tag: latest
  pullPolicy: Always

service:
  type: ClusterIP
  port: 80
  targetPort: 8000

ingress:
  enabled: true
  host: ums.example.com
  path: /health
  annotations:
    kubernetes.io/ingress.class: alb
    alb.ingress.kubernetes.io/scheme: internet-facing
    alb.ingress.kubernetes.io/target-type: ip
    alb.ingress.kubernetes.io/listen-ports: '[{"HTTP":80},{"HTTPS":443}]'
    alb.ingress.kubernetes.io/ssl-redirect: "443"
    alb.ingress.kubernetes.io/certificate-arn: ACM_CERT_ARN
```

---

## 🔢 Replica Configuration

```yaml
replicaCount: 2
```

### What it means

Defines how many **Pod replicas** Kubernetes should run.

### Where it is used

```yaml
replicas: {{ .Values.replicaCount }}
```

### Why this exists

* Ensures **high availability**
* Enables easy scaling
* Avoids editing Kubernetes YAML

### Real-world usage

| Environment | Value |
| ----------- | ----- |
| Dev         | 1     |
| QA          | 2     |
| Prod        | 3–10  |

📌 **Key Insight**
Scaling becomes a **configuration change**, not a deployment rewrite.

---

## 🐳 Image Configuration Block

```yaml
image:
```

This block controls **which container image runs**.

---

### 📦 Image Repository

```yaml
repository: dockerhub-username/user-management-service
```

Defines **where the image is stored**.

Used in template:

```yaml
image: "{{ .Values.image.repository }}:{{ .Values.image.tag }}"
```

Why this matters:

* Chart stays reusable
* Image source can change per environment
* Supports Docker Hub, ECR, GCR, ACR

---

### 🏷️ Image Tag

```yaml
tag: latest
```

Defines **which version of the image** is deployed.

⚠️ Production Best Practice:

```yaml
tag: v1.2.3
```

Why Helm loves this:

```bash
helm upgrade ums chart --set image.tag=v2
```

📌 **Key Insight**
Helm upgrades = **config change**, not YAML editing.

---

### 🔄 Image Pull Policy

```yaml
pullPolicy: Always
```

Controls when Kubernetes pulls images.

| Value        | Meaning         |
| ------------ | --------------- |
| Always       | Always pull     |
| IfNotPresent | Pull if missing |
| Never        | Never pull      |

Used heavily in CI/CD to ensure **latest build is deployed**.

---

## 🌐 Service Configuration

```yaml
service:
```

Defines **how Pods are exposed inside Kubernetes**.

---

### 🔌 Service Type

```yaml
type: ClusterIP
```

Meaning:

* Service is internal-only
* Accessed via Ingress

Why ClusterIP?

* Secure
* Scalable
* Required for Ingress-based architecture

---

### 🌍 Service Port

```yaml
port: 80
```

Port exposed by Kubernetes Service.

---

### 🎯 Target Port

```yaml
targetPort: 8000
```

Port where application runs inside the container.

Example flow:

```
Ingress → Service:80 → Pod:8000
```

📌 **Key Insight**
Service abstracts container internals from the outside world.

---

## 🚪 Ingress Configuration

```yaml
ingress:
```

Ingress controls **external access** to the application.

---

### ✅ Enable / Disable Ingress

```yaml
enabled: true
```

Used in template:

```yaml
{{- if .Values.ingress.enabled }}
```

Why this is powerful:

* Same chart works with or without Ingress
* Feature toggling without code changes

---

### 🌍 Host (Domain Name)

```yaml
host: ums.example.com
```

Defines the **domain users access**.

Supports:

* Host-based routing
* Multiple environments
* Microservices architecture

---

### 🧭 Path

```yaml
path: /health
```

Defines **URL routing path**.

Examples:

* `/`
* `/api`
* `/health`

---

## 🏷️ Ingress Annotations (AWS ALB Integration)

Annotations instruct **AWS Load Balancer Controller**.

Think of them as:

> “How AWS should create and manage the ALB”

---

### 🔑 Ingress Class

```yaml
kubernetes.io/ingress.class: alb
```

Ensures:

* AWS ALB Controller handles this Ingress
* Other controllers ignore it

---

### 🌍 ALB Scheme

```yaml
alb.ingress.kubernetes.io/scheme: internet-facing
```

| Value           | Meaning |
| --------------- | ------- |
| internet-facing | Public  |
| internal        | Private |

---

### 🎯 Target Type

```yaml
alb.ingress.kubernetes.io/target-type: ip
```

ALB sends traffic **directly to pod IPs**.

Why this is best:

* Dynamic pods
* No NodePort issues
* AWS recommended

---

### 👂 Listener Ports

```yaml
alb.ingress.kubernetes.io/listen-ports: '[{"HTTP":80},{"HTTPS":443}]'
```

Configures ALB listeners.

Required for HTTPS support.

---

### 🔁 SSL Redirect

```yaml
alb.ingress.kubernetes.io/ssl-redirect: "443"
```

Forces:

```
HTTP → HTTPS
```

Security best practice.

---

### 🔐 ACM Certificate ARN

```yaml
alb.ingress.kubernetes.io/certificate-arn: ACM_CERT_ARN
```

Attaches AWS ACM certificate for TLS.

Benefits:

* Free
* Auto-renewal
* Managed by AWS

---

## 🧠 Big Picture Summary

| Area          | Controlled By   |
| ------------- | --------------- |
| Scaling       | replicaCount    |
| Image version | image.tag       |
| Networking    | service.*       |
| Public access | ingress.*       |
| Security      | TLS annotations |

📌 **Not a single Kubernetes YAML file needs to change.**

---

## 🗣️ Interview-Ready One-Liner

> “Helm `values.yaml` externalizes configuration from Kubernetes manifests, enabling reusable, environment-specific, and CI/CD-friendly deployments.”

---

## ✅ Final Thought (Remember This)

If you understand **this one file deeply**, you understand:

* Helm philosophy
* Kubernetes deployment strategy
* Production DevOps workflows

This knowledge **stays with you forever**.
