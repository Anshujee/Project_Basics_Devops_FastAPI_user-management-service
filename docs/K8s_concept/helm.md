# Helm Charts – Packaging Kubernetes Applications (Complete Guide)

## 📌 Overview

This document explains **Helm Charts in depth** using a real DevOps project.
It covers:

- Why Helm is required in production
- Helm architecture and core concepts
- Helm chart structure
- Line-by-line explanation of all Helm files
- How Helm manages deployments, upgrades, and rollbacks
- How Helm fits into CI/CD and real IT environments

This documentation is written for **learning, revision, and interview preparation**.

---

## 🧠 Why Helm is Required (Problem Statement)

### ❌ Without Helm (Plain Kubernetes YAML)

Managing Kubernetes using raw YAML files causes:
- Hard-coded values
- Duplicate YAML across environments
- Manual edits for image versions
- No rollback mechanism
- No versioning
- High risk during production changes

This approach does **not scale** in real organizations.

---

### ✅ With Helm (Solution)

Helm is the **package manager for Kubernetes**.

It provides:
- Reusable templates
- Centralized configuration
- Versioned releases
- Safe upgrades
- Easy rollback
- Environment-specific deployments

📌 **Helm = Kubernetes deployment standard in production**

---

## 🧩 Core Helm Concepts

| Concept | Meaning |
|------|--------|
Chart | A Helm package |
Release | A deployed instance of a chart |
values.yaml | Configuration file |
templates/ | Kubernetes YAML templates |
helm install | Deploy application |
helm upgrade | Update application |
helm rollback | Revert to previous version |

---

## 📂 Helm Chart Structure

helm/
└── user-management/
├── Chart.yaml
├── values.yaml
└── templates/
├── deployment.yaml
├── service.yaml
└── ingress.yaml


Each file has a **specific responsibility**, explained below.

---

## 📄 Chart.yaml (Chart Metadata)

### File: `Chart.yaml`

```yaml
apiVersion: v2
name: user-management
description: Helm chart for User Management Service
type: application
version: 0.1.0
appVersion: "1.0.0"
Line-by-Line Explanation
Line	Explanation
apiVersion: v2	Helm chart API version
name	Name of the chart
description	Human-readable chart description
type: application	Deployable application
version	Helm chart version
appVersion	Application version (image version reference)

📌 Important concept

version → Helm chart lifecycle

appVersion → Application lifecycle

📄 values.yaml (Configuration File)
File: values.yaml
replicaCount: 2


Defines how many pod replicas should run.

image:
  repository: dockerhub-username/user-management-service
  tag: latest
  pullPolicy: Always

Field	Explanation
repository	Docker image repository
tag	Image version
pullPolicy	Always pull latest image
service:
  type: ClusterIP
  port: 80
  targetPort: 8000

Field	Explanation
type	Service type (ClusterIP for Ingress)
port	Service port
targetPort	Container port
ingress:
  enabled: true
  host: ums.example.com
  path: /health


Controls whether Ingress is created and how traffic is routed.

  annotations:
    kubernetes.io/ingress.class: alb
    alb.ingress.kubernetes.io/scheme: internet-facing
    alb.ingress.kubernetes.io/target-type: ip
    alb.ingress.kubernetes.io/listen-ports: '[{"HTTP":80},{"HTTPS":443}]'
    alb.ingress.kubernetes.io/ssl-redirect: "443"
    alb.ingress.kubernetes.io/certificate-arn: ACM_CERT_ARN


These annotations instruct AWS Load Balancer Controller to:

Create ALB

Enable HTTPS

Attach ACM certificate

Redirect HTTP → HTTPS

📄 Deployment Template
File: templates/deployment.yaml
apiVersion: apps/v1
kind: Deployment


Defines a Kubernetes Deployment resource.

metadata:
  name: {{ .Release.Name }}


.Release.Name → Helm-generated release name

Ensures unique resource naming

spec:
  replicas: {{ .Values.replicaCount }}


Replica count is dynamically read from values.yaml.

selector:
  matchLabels:
    app: {{ .Release.Name }}


Ensures pods match the deployment selector.

template:
  metadata:
    labels:
      app: {{ .Release.Name }}


Labels applied to pods for service discovery.

containers:
  - name: {{ .Release.Name }}


Container name matches Helm release.

image: "{{ .Values.image.repository }}:{{ .Values.image.tag }}"


Dynamic image reference from values.yaml.

ports:
  - containerPort: {{ .Values.service.targetPort }}


Exposes application port.

📄 Service Template
File: templates/service.yaml
apiVersion: v1
kind: Service


Defines Kubernetes Service.

name: {{ .Release.Name }}


Service name is dynamically generated.

type: {{ .Values.service.type }}


Service type comes from values.yaml.

selector:
  app: {{ .Release.Name }}


Routes traffic to matching pods.

ports:
  - port: {{ .Values.service.port }}
    targetPort: {{ .Values.service.targetPort }}


Maps external traffic to container.

📄 Ingress Template
File: templates/ingress.yaml
{{- if .Values.ingress.enabled }}


Conditional logic:

Ingress is created only if enabled.

kind: Ingress
metadata:
  name: {{ .Release.Name }}


Ingress resource definition.

annotations:
{{ toYaml .Values.ingress.annotations | indent 4 }}


Injects all annotations dynamically.

rules:
  - host: {{ .Values.ingress.host }}


Defines domain-based routing.

path: {{ .Values.ingress.path }}
pathType: Prefix


Path-based routing configuration.

backend:
  service:
    name: {{ .Release.Name }}
    port:
      number: {{ .Values.service.port }}


Ingress routes traffic to Kubernetes Service.

{{- end }}


Ends conditional block.

🚀 Helm Commands Used
Install Application
helm install ums helm/user-management

Upgrade Application
helm upgrade ums helm/user-management \
  --set image.tag=v2

Rollback Application
helm rollback ums 1

Uninstall Application
helm uninstall ums

How Helm Fits Into CI/CD
Git Push
 → CI builds image
 → Image pushed to registry
 → CD runs helm upgrade


Helm is commonly used with:

GitHub Actions

Jenkins

ArgoCD (GitOps)

🗣️ Interview-Ready Summary

“Helm charts package Kubernetes resources using templates and values, enabling reusable, versioned, and environment-specific deployments with safe upgrades and rollbacks.”

✅ What This Project Demonstrates

Real production Kubernetes deployment

Helm templating mastery

AWS ALB + HTTPS integration

DevOps best practices

Strong troubleshooting and documentation skills


---

## ✅ What You Should Do Now

1. Save this as `README.md`
2. Commit & push to GitHub
3. Use this for:
   - Interview explanation
   - Revision
   - Portfolio showcase

---------------------