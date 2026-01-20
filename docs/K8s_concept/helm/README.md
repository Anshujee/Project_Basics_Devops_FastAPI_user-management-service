HTTPS + Helm Implementation on EKS (NGINX Ingress)
📌 Purpose of This Document

This document explains how HTTPS was re-implemented from scratch and then cleanly migrated to Helm-managed resources for an application running on AWS EKS using NGINX Ingress Controller.

It is written assuming:

No prior HTTPS setup exists

DNS, TLS, and certificates must be recreated

Helm must become the single owner of Kubernetes resources

This follows real-world DevOps best practices.

🧠 Key Principle (Very Important)

Helm does NOT create DNS, TLS certificates, or domains.
Helm only consumes existing infrastructure.

Therefore:

HTTPS must work before Helm

Helm only manages Deployment, Service, and Ingress

🏗️ Final Architecture
Browser (https://ums.yourdomain.com)
   ↓
DNS (GoDaddy)
   ↓
AWS LoadBalancer (created by NGINX Service)
   ↓
NGINX Ingress Controller (TLS termination)
   ↓
Service (ClusterIP)
   ↓
Pod (FastAPI Application)


📌 TLS is terminated inside Kubernetes, not at AWS ALB.

✅ Assumptions Before Starting
Status	Requirement
✅	EKS cluster exists (created via Terraform)
✅	NGINX Ingress Controller installed
✅	Deployment + Service (raw YAML) working
❌	No TLS secret exists
❌	DNS records removed
❌	HTTPS completely reset
🔐 PART 1 — RE-IMPLEMENT HTTPS (FROM SCRATCH)
🟦 STEP 1 — Confirm NGINX Ingress Controller
kubectl get pods -n ingress-nginx
kubectl get svc -n ingress-nginx


You must see:

ingress-nginx-controller → Running

Service type → LoadBalancer

External DNS like:

xxxxx.us-west-2.elb.amazonaws.com


📌 Save this LoadBalancer DNS name.

🟦 STEP 2 — DNS Setup in GoDaddy
2.1 Decide Application Domain

Example:

ums.umsdevopsdemo.in


ums → application

umsdevopsdemo.in → root domain

2.2 Create DNS Record in GoDaddy

GoDaddy Console → DNS → Add Record:

Field	Value
Type	CNAME
Name	ums
Value	<NGINX-INGRESS-LB-DNS>
TTL	600

Example:

ums → a5e29b7b1024c437693cf5542b938c61.us-west-2.elb.amazonaws.com


💡 Why CNAME?

NGINX LoadBalancer DNS can change

CNAME handles this safely

2.3 Verify DNS Resolution
nslookup ums.umsdevopsdemo.in


or

dig ums.umsdevopsdemo.in


🚫 Do not proceed until DNS resolves to AWS ELB.

🟦 STEP 3 — Install cert-manager

NGINX does not generate certificates.
cert-manager automates TLS issuance and renewal.

kubectl apply -f https://github.com/cert-manager/cert-manager/releases/latest/download/cert-manager.yaml


Verify:

kubectl get pods -n cert-manager


All pods must be Running.

🟦 STEP 4 — Create Let’s Encrypt ClusterIssuer
cluster-issuer.yaml
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


Apply:

kubectl apply -f cluster-issuer.yaml


Verify:

kubectl get clusterissuer


Expected:

READY = True

🟦 STEP 5 — Create HTTPS Ingress (RAW YAML)
ingress.yaml
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
        - ums.umsdevopsdemo.in
      secretName: ums-tls
  rules:
    - host: ums.umsdevopsdemo.in
      http:
        paths:
          - path: /health
            pathType: Prefix
            backend:
              service:
                name: ums-service
                port:
                  number: 80


Apply:

kubectl apply -f ingress.yaml

5.2 Verify Certificate Creation
kubectl get certificate
kubectl describe certificate ums-tls
kubectl get secret ums-tls


You must see:

ums-tls


📌 cert-manager:

Proves domain ownership

Issues Let’s Encrypt certificate

Stores it as Kubernetes secret

🟦 STEP 6 — Test HTTPS

Browser:

https://ums.umsdevopsdemo.in/health


CLI:

curl https://ums.umsdevopsdemo.in/health


You should see:

🔒 Lock icon

Valid Let’s Encrypt certificate

JSON response

✅ HTTPS Re-Implementation Checklist

✅ DNS updated in GoDaddy

✅ Domain resolves to ingress LB

✅ cert-manager installed

✅ ClusterIssuer READY

✅ ums-tls secret created

✅ HTTPS working

🚀 PART 2 — MIGRATE TO HELM-MANAGED INGRESS
🧠 Golden Rule

Helm must be the single owner of resources it manages

Therefore:

Raw Ingress ❌ must be deleted

Helm will recreate it ✅

🟦 STEP 7 — Delete Raw Ingress
kubectl delete ingress ums-ingress


Verify:

kubectl get ingress


Expected:

No resources found


🚫 Do NOT delete:

ums-tls secret

cert-manager

NGINX Ingress Controller

🟦 STEP 8 — Verify TLS Secret Still Exists
kubectl get secret ums-tls


Must exist before Helm install.

🟦 STEP 9 — Validate Helm Chart
helm lint helm/user-management
helm template ums helm/user-management


Expected:

0 chart(s) failed

🟦 STEP 10 — Install Helm Chart (Clean)
helm install ums helm/user-management


Helm now creates:

Deployment

Service

HTTPS Ingress (NGINX-based)

🟦 STEP 11 — Verify Helm Resources
helm list
kubectl get pods
kubectl get svc
kubectl get ingress


Ingress should show:

Host: ums.umsdevopsdemo.in

Address: NGINX LoadBalancer DNS

🟦 STEP 12 — Final HTTPS Validation

Browser:

https://ums.umsdevopsdemo.in/health


CLI:

curl https://ums.umsdevopsdemo.in/health

🧠 Ownership Model (Production Standard)
Resource	Owner
Deployment	Helm
Service	Helm
Ingress	Helm
TLS Secret	cert-manager
DNS	GoDaddy
Ingress Controller	Helm (platform)

📌 Helm consumes, not creates, infrastructure.

🧪 Common Issues & Fixes
HTTPS returns 404
kubectl describe ingress ums


Check:

Host matches domain

Path is /health

Service name is correct

Certificate not used
kubectl describe certificate
kubectl describe ingress ums


Ensure:

secretName: ums-tls

Secret exists

Helm install fails (resource exists)

Delete leftover resources:

kubectl get ingress
kubectl get deploy
kubectl get svc

✅ Final Confirmation Checklist

✅ Raw Ingress deleted

✅ Helm install successful

✅ Helm-created Ingress visible

✅ HTTPS works

✅ /health responds

🎯 Outcome

You now have:

HTTPS secured Kubernetes app

Cloud-agnostic NGINX Ingress

cert-manager automated TLS

Helm-managed production deployment

This is real-world DevOps implementation.