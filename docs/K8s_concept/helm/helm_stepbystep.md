End-to-End Kubernetes Deployment on AWS EKS using Helm, NGINX Ingress & HTTPS
📌 Overview

This document provides a complete hands-on guide to deploy a production-ready application on AWS EKS using Helm, NGINX Ingress Controller, cert-manager (Let’s Encrypt), and custom DNS (GoDaddy).

The flow follows real IT DevOps best practices, starting from infrastructure provisioning (Terraform) to accessing the application securely via HTTPS in a browser.

Helm
 └── Deployment + Service + Ingress
        ↓
Ingress Resource
        ↓
NGINX Ingress Controller
        ↓
TLS Termination (cert-manager + Let’s Encrypt)
        ↓
DNS (GoDaddy → AWS LoadBalancer)
        ↓
Browser → https://your-domain/health

Prerequisites

Before starting, ensure the following:

Terraform has already created the EKS cluster

AWS CLI configured

kubectl, Helm installed locally

Domain purchased (e.g. GoDaddy)

EKS cluster details:

Region: us-west-2

Cluster Name: my-eks-cluster

#############################################################

🔹 STEP 1 — Connect to EKS Cluster
Command
aws eks update-kubeconfig \
  --region us-west-2 \
  --name my-eks-cluster

What this does

Fetches EKS cluster details from AWS

Updates ~/.kube/config

Enables kubectl and helm to communicate with EKS

Verify
kubectl config current-context
kubectl get nodes


✅ Worker nodes must be in Ready state.

################################################################

🔹 STEP 2 — Create Application Namespace

In real projects, applications are never deployed in default namespace.

Command
kubectl create namespace prod

Verify
kubectl get ns

#############################################################

🔹 STEP 3 — Install NGINX Ingress Controller (via Helm)

NGINX Ingress is cluster-level infrastructure, not app-level.

Add Helm repository
helm repo add ingress-nginx https://kubernetes.github.io/ingress-nginx
helm repo update

Install NGINX Ingress Controller
helm install ingress-nginx ingress-nginx/ingress-nginx \
  --namespace ingress-nginx \
  --create-namespace

What this does

Deploys NGINX Ingress Controller

Automatically provisions an AWS LoadBalancer

This LoadBalancer receives internet traffic

Verify
kubectl get pods -n ingress-nginx
kubectl get svc -n ingress-nginx


You MUST see:

Controller pod → Running

Service type → LoadBalancer

External DNS like:

xxxx.us-west-2.elb.amazonaws.com


📌 Copy this LoadBalancer DNS name

#########################################################

🔹 STEP 4 — Configure DNS (GoDaddy)
Goal

Map your domain to the NGINX LoadBalancer.

Example Domain
ums.umsdevopsdemo.in

GoDaddy → DNS Records

Add a CNAME record:

Field	Value
Type	CNAME
Name	ums
Value	<NGINX-LB-DNS>
TTL	600
Verify DNS (CRITICAL)
nslookup ums.umsdevopsdemo.in


✅ Must resolve to the AWS ELB DNS
🚫 Do NOT proceed until DNS works

##########################################################

🔹 STEP 5 — Install cert-manager (HTTPS Engine)

cert-manager automates TLS certificates using Let’s Encrypt.

Install cert-manager
kubectl apply -f https://github.com/cert-manager/cert-manager/releases/latest/download/cert-manager.yaml

Verify
kubectl get pods -n cert-manager


All pods must be Running.

############################################################

🔹 STEP 6 — Create ClusterIssuer (Let’s Encrypt)

This tells cert-manager how to issue certificates.

Create cluster-issuer.yaml
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
kubectl apply -f cluster-issuer.yaml

Verify
kubectl get clusterissuer


Status must be:

READY   True

🔹 STEP 7 — Helm Chart Structure (Application)
helm/user-management/
├── Chart.yaml
├── values.yaml
├── values-prod.yaml
└── templates/
    ├── deployment.yaml
    ├── service.yaml
    └── ingress.yaml

🚨 Important Rule

❌ Do NOT apply Kubernetes YAML manually
✅ Helm manages everything

#######################################################################

🔹 STEP 8 — Helm Ingress Template (TLS Enabled)
templates/ingress.yaml
apiVersion: networking.k8s.io/v1
kind: Ingress
metadata:
  name: {{ .Release.Name }}
  annotations:
    cert-manager.io/cluster-issuer: letsencrypt-prod
spec:
  ingressClassName: nginx
  tls:
    - hosts:
        - {{ .Values.ingress.host }}
      secretName: ums-tls
  rules:
    - host: {{ .Values.ingress.host }}
      http:
        paths:
          - path: {{ .Values.ingress.path }}
            pathType: Prefix
            backend:
              service:
                name: {{ .Release.Name }}
                port:
                  number: {{ .Values.service.port }}

What this does

Uses NGINX Ingress

Requests TLS certificate

Stores cert in ums-tls

#############################################################

🔹 STEP 9 — Install Application Using Helm

Run this from project root or use . if already inside chart directory.

Command
helm install ums ./helm/user-management \
  --namespace prod \
  --create-namespace \
  -f ./helm/user-management/values-prod.yaml

What Helm does

Creates Deployment

Creates Service

Creates Ingress

cert-manager automatically issues TLS certificate

#############################################################

🔹 STEP 10 — Verify Deployment
Pods & Service
kubectl get pods -n prod
kubectl get svc -n prod

Ingress
kubectl get ingress -n prod
kubectl describe ingress ums -n prod

Certificate & Secret
kubectl get certificate -n prod
kubectl get secret ums-tls -n prod


Certificate must show:

READY = True


###########################################################

🔹 STEP 11 — Access Application in Browser 🌍

Open:

https://ums.umsdevopsdemo.in/health

Expected Result

🔒 HTTPS lock icon

Valid Let’s Encrypt certificate

JSON response from application

#######################################################

🧠 Golden Rules (Memorize These)

1️⃣ Terraform → Infrastructure only
2️⃣ Helm → Application only
3️⃣ Never mix kubectl apply with Helm for same app
4️⃣ DNS must resolve before cert-manager works
5️⃣ Ingress + TLS are prerequisites for Helm HTTPS apps

🎯 Final Outcome

You now have:

AWS EKS cluster

NGINX Ingress Controller

HTTPS via cert-manager & Let’s Encrypt

DNS routing via GoDaddy

Application deployed using Helm

Production-ready architecture

