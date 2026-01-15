
# EKS Application Deployment Using LoadBalancer (Step-by-Step Guide)

This README documents the **exact workflow** to deploy an application on **AWS EKS** using Kubernetes **Deployment** and **Service (LoadBalancer type)**, verify it, access it externally, and clean up the resources.

This guide is written for **beginners in Kubernetes and DevOps** and is suitable for **GitHub reference and interview revision**.

---

## 1️⃣ Verify EKS Cluster Is Up and Running

Before doing anything with Kubernetes, make sure your **EKS cluster is already created** (for example, using Terraform).

---

## 2️⃣ Check Kubernetes Contexts

List all Kubernetes contexts available on your system:

```bash
kubectl config get-contexts
```

This command shows all clusters that `kubectl` knows about.

---

## 3️⃣ Check the Current Active Context

```bash
kubectl config current-context
```

This tells you which Kubernetes cluster `kubectl` is currently pointing to.

---

## 4️⃣ Connect kubectl to the EKS Cluster

Update kubeconfig to connect to your EKS cluster:

```bash
aws eks update-kubeconfig \
  --region us-west-2 \
  --name my-eks-cluster # your cluster name
```

After this command:

* `kubectl` is connected to your EKS cluster
* A new context is added automatically

Verify again:

```bash
kubectl config current-context
```

---

## 5️⃣ Deploy Application Manifests

Navigate to the Kubernetes manifests directory of your project:

```bash
cd k8s
```

Apply the Deployment and Service YAML files:

```bash
kubectl apply -f deployment.yaml
kubectl apply -f service.yaml
```

This creates:

* Pods (via Deployment)
* A Service of type **LoadBalancer**

---

## 6️⃣ Verify Pods Are Running

```bash
kubectl get pods
```

Expected output:

```text
NAME                              READY   STATUS    RESTARTS   AGE
ums-deployment-7cdc688b47-4lk2m   1/1     Running   0          9m26s
ums-deployment-7cdc688b47-dpk6b   1/1     Running   0          9m26s
```

---

## 7️⃣ Verify Deployment Status

```bash
kubectl get deployments
```

Expected output:

```text
NAME             READY   UP-TO-DATE   AVAILABLE   AGE
ums-deployment   2/2     2            2           11m
```

This confirms:

* Desired replicas are running
* Pods are healthy

---

## 8️⃣ Verify Services and External LoadBalancer

```bash
kubectl get services
```

Expected output:

```text
NAME          TYPE           CLUSTER-IP       EXTERNAL-IP                                                             PORT(S)        AGE
kubernetes    ClusterIP      172.20.0.1       <none>                                                                  443/TCP        42m
ums-service   LoadBalancer   172.20.253.132   a718a0d6e3d0d4ef4977e5e25f05bc94-89937777.us-west-2.elb.amazonaws.com   80:31975/TCP   12m
```

Key points:

* AWS automatically creates an **Elastic Load Balancer (ELB)**
* The ELB URL appears in the `EXTERNAL-IP` column

---

## 9️⃣ Access the Application

Use the AWS-provided LoadBalancer URL to access the application:

```text
http://a718a0d6e3d0d4ef4977e5e25f05bc94-89937777.us-west-2.elb.amazonaws.com/health
```

If the application responds correctly, the deployment is successful.

---

## 🔟 View All Kubernetes Resources

To list all resources in the current namespace:

```bash
kubectl get all
```

This shows:

* Pods
* Services
* Deployments
* ReplicaSets

---

## 1️⃣1️⃣ Delete Application Resources (Cleanup)

Delete the Kubernetes resources created for the application:

```bash
kubectl delete -f deployment.yaml
kubectl delete -f service.yaml
```

This removes:

* Pods
* Deployment
* Service
* AWS LoadBalancer

⚠️ The EKS cluster still exists at this point.

---

## ✅ Summary

* EKS cluster is created using Terraform
* kubectl is configured using `aws eks update-kubeconfig`
* Application is deployed using Kubernetes manifests
* Service of type LoadBalancer exposes the app externally
* AWS ELB URL is used to access the application
* All Kubernetes resources are cleaned up using `kubectl delete`

---

📌 **Next Evolution Step**

Instead of using one LoadBalancer per service, production systems use:

* **Ingress Controller**
* **Ingress resources**

This reduces cost and enables advanced routing.
# EKS Application Deployment Using Ingress (Complete Step-by-Step Guide)

This README explains **how to deploy an application on AWS EKS using Ingress** instead of exposing every service with a LoadBalancer.

It assumes:

* EKS cluster is already created using Terraform
* `terraform apply` has been executed successfully
* Kubernetes manifests (`deployment.yaml`, `service.yaml`, `ingress.yaml`) exist inside a `k8s/` folder

This guide is written for **beginners in Kubernetes and DevOps** and is suitable for **GitHub reference and interview preparation**.

---

## 1️⃣ Verify EKS Cluster Is Running

Ensure the EKS cluster is up (created by Terraform).

---

## 2️⃣ Check Kubernetes Contexts

List all Kubernetes contexts:

```bash
kubectl config get-contexts
```

Check the current active context:

```bash
kubectl config current-context
```

---

## 3️⃣ Connect kubectl to the EKS Cluster

Update kubeconfig for the EKS cluster:

```bash
aws eks update-kubeconfig \
  --region us-west-2 \
  --name my-eks-cluster
```

Verify again:

```bash
kubectl config current-context
```

---

## 4️⃣ Folder Structure (Recommended)

```text
project-root/
├── terraform/
│   └── main.tf
└── k8s/
    ├── deployment.yaml
    ├── service.yaml
    └── ingress.yaml
```

---

## 5️⃣ Update Service to Use ClusterIP (IMPORTANT)

When using Ingress, services must be **internal only**.

### service.yaml

```yaml
apiVersion: v1
kind: Service
metadata:
  name: ums-service
spec:
  type: ClusterIP
  selector:
    app: ums
  ports:
    - port: 80
      targetPort: 8080
```

📌 Do NOT use `LoadBalancer` for application services when using Ingress.

---

## 6️⃣ Deploy Application (Deployment + Service)

Navigate to the Kubernetes folder:

```bash
cd k8s
```

Apply Deployment:

```bash
kubectl apply -f deployment.yaml
```

Apply Service:

```bash
kubectl apply -f service.yaml
```

Verify:

```bash
kubectl get pods
kubectl get deployments
kubectl get services
```

Expected:

* Pods in `Running` state
* Service type = `ClusterIP`

---

## 7️⃣ Install Ingress Controller (Beginner-Friendly Method)

We use the **official ingress-nginx manifest** (no Helm).

### Command

```bash
kubectl apply -f https://raw.githubusercontent.com/kubernetes/ingress-nginx/main/deploy/static/provider/cloud/deploy.yaml
```

---

## 8️⃣ What This Command Installs (Conceptual)

The above command creates all components required for the Ingress Controller:

* Namespace: `ingress-nginx`
* ServiceAccount
* RBAC (ClusterRole & ClusterRoleBinding)
* ConfigMap
* Deployment (Ingress Controller Pods)
* Service (type LoadBalancer)
* Admission Webhooks

📌 These components are **only for traffic routing**, not for deploying apps.

---

## 9️⃣ Verify Ingress Controller Installation

### Check Pods

```bash
kubectl get pods -n ingress-nginx
```

Expected:

```text
ingress-nginx-controller-xxxxx   Running
```

---

### Check Ingress Controller Service

```bash
kubectl get svc -n ingress-nginx
```

Expected:

```text
ingress-nginx-controller   LoadBalancer   <EXTERNAL-IP>
```

📌 This is the **single AWS LoadBalancer** for all applications.

---

## 🔟 Create Ingress Resource

### ingress.yaml

```yaml
apiVersion: networking.k8s.io/v1
kind: Ingress
metadata:
  name: ums-ingress
  annotations:
    nginx.ingress.kubernetes.io/rewrite-target: /
spec:
  ingressClassName: nginx
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

Apply Ingress:

```bash
kubectl apply -f ingress.yaml
```

---

## 1️⃣1️⃣ Verify Ingress

```bash
kubectl get ingress
```

Describe Ingress (recommended):

```bash
kubectl describe ingress ums-ingress
```

---

## 1️⃣2️⃣ Access Application via Ingress

### Option 1: Using Host Header (Without DNS)

```bash
curl -H "Host: ums.example.com" http://<INGRESS-LOADBALANCER-IP>/health
```

### Option 2: Using DNS (Production)

```text
ums.example.com → Ingress LoadBalancer IP
```

---

## 1️⃣3️⃣ Verify All Resources

```bash
kubectl get all
```

---

## 1️⃣4️⃣ Cleanup Kubernetes Resources (Optional)

```bash
kubectl delete -f ingress.yaml
kubectl delete -f service.yaml
kubectl delete -f deployment.yaml
```

Ingress Controller can also be removed if required:

```bash
kubectl delete -f https://raw.githubusercontent.com/kubernetes/ingress-nginx/main/deploy/static/provider/cloud/deploy.yaml
```

---

## 1️⃣5️⃣ Key Concepts to Remember

* Terraform manages **infrastructure (EKS)**
* Kubernetes manifests manage **applications**
* Ingress Controller provides **single entry point**
* Services must be **ClusterIP** when using Ingress
* Only Ingress Controller uses `LoadBalancer`

---

## ✅ Summary

* EKS created using Terraform
* kubectl configured using `aws eks update-kubeconfig`
* App deployed using Deployment + ClusterIP Service
* Ingress Controller installed using official manifest
* Ingress resource created for routing
* App accessed using a single shared LoadBalancer

-------------------------------------------------------------------

📌 This setup reflects **real production Kubernetes architecture**.

# Accessing Application via Kubernetes Ingress

This README explains **how to access an application exposed through Kubernetes Ingress** in **two correct and commonly used ways**:

1. **Local Access (Without DNS)** – for learning, testing, and debugging
2. **DNS-Based Access (Production Way)** – for real-world usage

This guide is written for **beginners in Kubernetes and DevOps** and is suitable for **GitHub reference and interview preparation**.

---

## 🧠 Core Concept (Must Understand First)

Ingress does **NOT** route traffic based on DNS.

Ingress routes traffic based on the **HTTP Host header**.

| Layer   | Responsibility                         |
| ------- | -------------------------------------- |
| DNS     | Converts domain name → IP address      |
| Ingress | Uses `Host` header → routes to Service |

DNS and Ingress are **two separate layers**.

---

## ✅ Prerequisites

Before following this guide, ensure:

* EKS cluster is running
* Ingress Controller is installed
* Application is deployed using:

  * Deployment
  * Service (`ClusterIP` type)
  * Ingress resource

---

# OPTION 1️⃣: Local Access (Without DNS)

Local access is mainly used for:

* Learning Ingress
* Testing routing rules
* Debugging issues
* Validating Ingress before DNS setup

In this option, **DNS is completely skipped**.

---

## Option 1A: Local Access Using `curl` (Most Important for Beginners)

### Why this works

Ingress matches traffic using the **HTTP Host header**. With `curl`, we can **manually set this header**.

---

### Step 1: Get Ingress LoadBalancer Address

```bash
kubectl get svc -n ingress-nginx
```

Example output:

```text
ingress-nginx-controller   LoadBalancer   a1b2c3d4.elb.us-west-2.amazonaws.com
```

This LoadBalancer is the **entry point into the cluster**.

---

### Step 2: Send Request with Host Header

```bash
curl -H "Host: ums.example.com" http://<INGRESS-LB-ADDRESS>/health
```

Example HTTP request sent by curl:

```http
GET /health HTTP/1.1
Host: ums.example.com
```

---

### Step 3: How Traffic Flows

```text
curl
 → Ingress LoadBalancer
 → Ingress Controller
 → Service (ClusterIP)
 → Pod
```

Since the `Host` header matches the Ingress rule, traffic is routed correctly.

---

### Why This Method Is Important

* Confirms Ingress is working
* Removes DNS complexity
* Used heavily for real-world debugging

If this works, **Ingress is correctly configured**.

---

## Option 1B: Local Browser Access Using `/etc/hosts`

This method allows access **from a browser**, without real DNS.

It simulates DNS **only on your local machine**.

---

### Step 1: Get Ingress LoadBalancer IP

```bash
kubectl get svc -n ingress-nginx
```

(Optional) Resolve to IP:

```bash
nslookup <INGRESS-LB-ADDRESS>
```

---

### Step 2: Update `/etc/hosts` (Mac/Linux)

```bash
sudo nano /etc/hosts
```

Add the following line:

```text
<INGRESS-LB-IP>   ums.example.com
```

Save and exit.

---

### Step 3: Access in Browser

```text
http://ums.example.com/health
```

### How It Works

```text
Browser
 → /etc/hosts (local DNS)
 → Ingress LoadBalancer
 → Ingress Controller
 → Service
 → Pod
```

⚠️ This mapping works **only on your local machine**.

---

# OPTION 2️⃣: DNS-Based Access (Production Way)

This is how applications are accessed in **real production environments**.

---

## Step 1: Get Ingress LoadBalancer DNS Name

```bash
kubectl get svc -n ingress-nginx
```

Example:

```text
a1b2c3d4.elb.us-west-2.amazonaws.com
```

---

## Step 2: Create DNS Record

Create a DNS record using Route53 or any DNS provider.

### Recommended Record Type: `CNAME`

| Field       | Value                                |
| ----------- | ------------------------------------ |
| Record Type | CNAME                                |
| Name        | ums.example.com                      |
| Value       | a1b2c3d4.elb.us-west-2.amazonaws.com |
| TTL         | 300                                  |

This maps:

```text
ums.example.com → Ingress LoadBalancer
```

---

## Step 3: Wait for DNS Propagation

DNS usually propagates within a few minutes.

Verify:

```bash
nslookup ums.example.com
```

---

## Step 4: Access Application in Browser

```text
http://ums.example.com/health
```

### Production Traffic Flow

```text
Browser
 → DNS Resolution
 → Ingress LoadBalancer
 → Ingress Controller
 → Service
 → Pod
```

---

## 🔍 Common Beginner Confusions

| Confusion                      | Reality                          |
| ------------------------------ | -------------------------------- |
| Ingress is broken              | DNS is missing                   |
| curl works but browser doesn’t | Browser needs DNS                |
| Service must be LoadBalancer   | Only Ingress Controller needs LB |

---

## 🎤 Interview-Ready Explanation

> “Ingress routes traffic based on the HTTP Host header. For local testing, we can bypass DNS by manually setting the Host header using curl or by using `/etc/hosts`. In production, DNS is configured to point the domain to the Ingress Controller’s LoadBalancer so browsers automatically send the correct Host header.”

---

## 🧠 Golden Rule (Memorize)

> **DNS brings traffic to Ingress, Ingress decides where it goes**

---

## ✅ Summary

* Ingress routing depends on the Host header
* Local access is possible without DNS
* curl is best for testing and debugging
* `/etc/hosts` simulates DNS locally
* Production requires proper DNS configuration

---

📌 This document explains **both learning and production approaches** to accessing applications via Kubernetes Ingress.
