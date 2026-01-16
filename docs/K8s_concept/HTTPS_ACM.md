# HTTPS on Kubernetes (EKS) using Ingress + AWS ALB + ACM  
## Complete Conceptual & Hands-on Guide (Beginner → Industry Level)

---

## 📌 Purpose of This Document

This README documents **all core concepts and practical steps** related to:

- HTTPS
- TLS / SSL
- Domains & DNS
- AWS Certificate Manager (ACM)
- Kubernetes Ingress
- AWS Application Load Balancer (ALB)
- AWS Load Balancer Controller (ALB Controller)

It is written as **one continuous learning document**, following **real IT industry DevOps practices**, and is intended for:

- Future revision
- Interview preparation
- Portfolio demonstration
- Deep conceptual understanding

---

## 1️⃣ Why HTTPS Is Mandatory in Real IT Industry

### What happens with HTTP?

When an application is accessed using HTTP:

http://myapp.com


- Data is transmitted in **plain text**
- Anyone on the network can read the data
- Usernames, passwords, tokens, cookies are exposed
- Vulnerable to Man-in-the-Middle (MITM) attacks

Example risk:
- User logs in from public Wi-Fi
- Attacker captures credentials

---

### Why companies never allow HTTP in production

In real IT organizations:
- Security compliance is mandatory (ISO, SOC2, PCI-DSS)
- Customer trust is critical
- Legal and financial risks exist

**Industry rule**:
> Any public-facing application must use HTTPS.

If HTTPS is missing:
- Application fails security review
- It never goes to production

---

## 2️⃣ What Is HTTPS, SSL, and TLS?

- **SSL** → Old, deprecated term
- **TLS** → Modern encryption protocol
- People still say “SSL certificate”, but technically it is **TLS**

### What TLS provides

TLS guarantees three things:

1. **Encryption**  
   Data cannot be read during transmission

2. **Authentication**  
   Confirms the identity of the server

3. **Integrity**  
   Ensures data is not modified in transit

When TLS is valid:
- Browser shows 🔒 lock icon
- Users trust the application

---

## 3️⃣ Why TLS Is NOT Configured Inside Kubernetes Pods

### Common beginner mistake

Many beginners think:
> “I should install TLS certificates inside the application container.”

This leads to:
- Certificate expiry causing downtime
- Manual certificate renewal
- Pod restarts
- Complex operations
- Poor scalability

---

### Industry best practice

**TLS termination is done at the Load Balancer, not inside pods**

Meaning:
- Browser → HTTPS
- Load Balancer → HTTPS
- Inside Kubernetes → HTTP

Benefits:
- Centralized security
- Automatic certificate renewal
- Zero-downtime rotation
- Simpler application containers

---

## 4️⃣ What Is a Domain and Why It Is Required

### What is a domain?

A domain is a **human-readable name** for a server.

Example:


ums.example.com


Instead of:


a1b2c3.elb.amazonaws.com


---

### Why HTTPS requires a domain

TLS certificates:
- Are issued **only for domain names**
- Cannot be issued for random IP addresses

Without a domain:
- HTTPS cannot be implemented correctly

---

## 5️⃣ What Is DNS and Route53?

### DNS (Simple Explanation)

DNS is the internet’s phonebook.

It maps:


Domain Name → Server (ALB)


When a user types:


ums.example.com


DNS resolves it to:


ALB DNS name


---

### Route53

Route53 is AWS’s DNS service:
- Manages domain records
- Integrates with ACM
- Maps domain → Load Balancer

This enables traffic to reach your Kubernetes cluster.

---

## 6️⃣ What Is AWS Certificate Manager (ACM)?

**AWS ACM** is a managed service that:

- Issues **free TLS certificates**
- Automatically renews certificates
- Integrates with AWS services like:
  - Application Load Balancer (ALB)
  - CloudFront
  - API Gateway

Why companies use ACM:
- No manual certificate renewal
- No certificate storage in pods
- Secure and AWS-managed

**Interview line**:
> We use ACM to manage TLS certificates securely and automatically.

---

## 7️⃣ What Is Kubernetes Ingress?

### Problem with Service type LoadBalancer

Using:
```yaml
type: LoadBalancer


Creates:

One AWS Load Balancer per service

High AWS cost

No routing control

Poor scalability

What Ingress solves

Ingress is a Kubernetes object that:

Manages external access to services

Provides routing rules

Uses a single Load Balancer

Supports:

Path-based routing

Host-based routing

HTTPS

Ingress defines traffic rules, not the load balancer itself.

8️⃣ What Is AWS ALB Controller (AWS Load Balancer Controller)?

Kubernetes cannot directly create AWS resources.

AWS provides AWS Load Balancer Controller, which:

Watches Kubernetes Ingress resources

Automatically creates:

Application Load Balancer (ALB)

Listeners

Target groups

Keeps AWS and Kubernetes in sync

Key concept:

Ingress defines rules
ALB Controller implements those rules in AWS

9️⃣ End-to-End Architecture
User Browser (HTTPS)
        ↓
      DNS (Route53)
        ↓
 AWS ALB (TLS via ACM)
        ↓
 Kubernetes Ingress
        ↓
 Service (ClusterIP)
        ↓
 Pod (Application - HTTP)


Key points:

TLS terminates at ALB

Kubernetes manages routing

Pods remain simple and scalable

🔟 Prerequisites for HTTPS Implementation

AWS EKS cluster is running

Application is deployed on EKS

AWS Load Balancer Controller is installed

A domain is purchased

Domain is managed via Route53

1️⃣1️⃣ Step-by-Step Hands-On Implementation
Step 1: Buy a Domain

Buy a domain from:

GoDaddy

Namecheap

Google Domains

Example:

anshu-devops.site

Step 2: Create Hosted Zone in Route53

AWS Console → Route53 → Hosted Zones → Create

Domain name: anshu-devops.site

Type: Public Hosted Zone

Route53 provides Name Servers.

Step 3: Update Name Servers at Domain Registrar

Go to domain provider

Replace default name servers

Paste Route53 name servers

This connects your domain to AWS.

Step 4: Request TLS Certificate in ACM

AWS Console → ACM
⚠️ Region: us-east-1 (mandatory for ALB)

Request:

Public certificate

Domain: *.anshu-devops.site

Validation method: DNS

Approve DNS records in Route53.

Wait until status:

ISSUED

Step 5: Configure Kubernetes Ingress with HTTPS

Create k8s/ingress.yaml:

apiVersion: networking.k8s.io/v1
kind: Ingress
metadata:
  name: ums-ingress
  annotations:
    kubernetes.io/ingress.class: alb
    alb.ingress.kubernetes.io/scheme: internet-facing
    alb.ingress.kubernetes.io/target-type: ip
    alb.ingress.kubernetes.io/listen-ports: '[{"HTTP":80},{"HTTPS":443}]'
    alb.ingress.kubernetes.io/certificate-arn: <ACM_CERT_ARN>
    alb.ingress.kubernetes.io/ssl-redirect: "443"
spec:
  rules:
    - host: ums.anshu-devops.site
      http:
        paths:
          - path: /health
            pathType: Prefix
            backend:
              service:
                name: ums-service
                port:
                  number: 80

Step 6: Apply Ingress
kubectl apply -f k8s/ingress.yaml


Verify:

kubectl get ingress

Step 7: Create DNS Record in Route53

Route53 → Hosted Zone → Create Record

Record type: A (Alias)

Record name: ums

Alias target: ALB DNS name

Step 8: Access Application Securely

Open browser:

https://ums.anshu-devops.site/health


Expected:

🔒 Lock icon

Valid certificate

Application response

🧪 Common Issues and Solutions
HTTPS not working

Certificate not ISSUED

Certificate in wrong region

Domain mismatch in Ingress

ALB not created

ALB Controller not running

IAM permissions missing

Subnet tags missing

🧠 Interview-Ready Summary

We use Kubernetes Ingress with AWS ALB and ACM to terminate TLS at the load balancer, ensuring secure HTTPS access while keeping application containers simple and scalable.

🚀 What This README Demonstrates

Real-world DevOps security practices

Kubernetes traffic management

AWS-native integrations

Production-grade HTTPS architecture

Strong conceptual foundation

🔐 What is a TLS Certificate?

A TLS certificate is a digital identity card for a website or service.

It proves who the server really is and enables secure (encrypted) communication between:

a client (browser, app, API)

and a server (website, backend, load balancer, Kubernetes ingress, etc.)

👉 If a website uses HTTPS, it is using a TLS certificate.

🧠 Why Do We Even Need TLS?

Imagine this situation without TLS:

You open http://mybank.com

You type your username & password

Data travels as plain text

Anyone on the network (Wi-Fi owner, hacker, ISP) can read or modify it

❌ Very dangerous.

TLS solves this.

✅ What TLS Gives Us (3 Core Guarantees)
1️⃣ Encryption (Privacy)

Data is scrambled

Even if someone intercepts it → they see gibberish

2️⃣ Authentication (Trust)

Proves the server is really who it claims to be

Prevents fake or phishing servers

3️⃣ Integrity (No Tampering)

Ensures data is not altered in transit

🪪 What Exactly Is Inside a TLS Certificate?

A TLS certificate contains:

Domain name (e.g. example.com)

Public key (used for encryption)

Owner / Organization info

Certificate Authority (CA) signature

Validity period (start & expiry date)

Think of it like:

A passport signed by a trusted authority.

🏛️ Who Issues TLS Certificates?

TLS certificates are issued by Certificate Authorities (CA), such as:

Let’s Encrypt

DigiCert

GlobalSign

AWS Certificate Manager (ACM)

Browsers trust these authorities by default.

Step-by-step (Beginner friendly):

1️⃣ Browser → Server

“Hello, I want to connect securely”

2️⃣ Server → Browser

“Here is my TLS certificate”

3️⃣ Browser checks

Is certificate valid?

Is it issued by a trusted CA?

Does domain name match?

Is it expired?

4️⃣ If trusted

Browser generates a secret key

Encrypts it using server’s public key

Sends it to server

5️⃣ Secure channel established

Both sides now use the same secret key

All data is encrypted 🔒

🔐 Public Key vs Private Key (Very Important)

Public Key

Shared openly

Used to encrypt data

Private Key

Secret

Stays on server

Used to decrypt data

👉 Anyone can lock the box (public key)
👉 Only server can open it (private key)

🌐 TLS vs SSL (Common Confusion)
Term	Status
SSL	❌ Old, deprecated
TLS	✅ Modern, secure

People still say SSL certificate, but technically:

All modern “SSL certificates” are TLS certificates

🧩 Real-Life DevOps Example
Example: Kubernetes + Ingress

User opens: https://myapp.company.com

Traffic hits:

Load Balancer

Ingress Controller

TLS certificate:

Terminates HTTPS

Encrypts traffic

Backend pods receive secure requests

Without TLS:

Browser shows “Not Secure”

Passwords & tokens are at risk

🚨 What Happens If TLS Is Missing or Invalid?

Browser warning: ⚠️ Your connection is not private

API calls fail

OAuth / login breaks

Compliance violations (PCI, SOC2, ISO)

🧠 One-Line Summary (Interview Ready)

A TLS certificate is a digital certificate that authenticates a server’s identity and enables encrypted, secure communication over HTTPS using public-key cryptography.