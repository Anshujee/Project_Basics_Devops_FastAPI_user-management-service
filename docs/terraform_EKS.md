# End-to-End DevOps Project: AWS EKS with Terraform (Modular Approach)

## 📌 Project Overview

This project demonstrates a **complete, real-world DevOps implementation** where:

- Infrastructure is provisioned on AWS using **Terraform (IaC)**
- Terraform is written using a **modular architecture**
- Remote backend with **S3 + DynamoDB state locking** is used
- An **Amazon EKS cluster** is created
- A **containerized application** is deployed on Kubernetes
- The application is exposed publicly via **AWS LoadBalancer**
- All common **Terraform + EKS issues** are identified and resolved

This project was built step by step for **deep understanding, hands-on learning, and interview readiness**.

---

## 🧠 Why Kubernetes & EKS?

### Why Kubernetes?
Kubernetes is used to:
- Run containers reliably
- Self-heal failed pods
- Scale applications
- Perform rolling updates
- Abstract infrastructure complexity

### Why Amazon EKS?
- Managed Kubernetes control plane
- High availability
- Secure and scalable
- Industry standard for production workloads on AWS

---

## 🧠 Why Terraform?

Terraform is used because:
- Infrastructure is defined as code
- Changes are version-controlled
- Infrastructure is reproducible
- No manual AWS console dependency
- Supports modular, reusable design

📌 **Interview one-liner**:  
> “Terraform enables declarative, version-controlled infrastructure provisioning.”

---

## 📂 Repository Structure

├── terraform/
│ ├── backend/ # Backend infra (S3 + DynamoDB)
│ ├── modules/
│ │ ├── vpc/ # Custom VPC module
│ │ └── eks/ # Custom EKS module
│ ├── backend.tf # Remote backend config
│ ├── main.tf # Root module (orchestrator)
│ ├── variables.tf
│ └── outputs.tf
│
├── k8s/ # Kubernetes manifests
│ ├── deployment.yaml
│ └── service.yaml
│
├── app/
├── docker/
├── .gitignore
└── README.md


---

## 🧱 Terraform Architecture (Very Important Concept)

Terraform is designed in **two layers**:

### Layer 1: Backend Infrastructure (Run Once)
Creates:
- S3 bucket for state
- DynamoDB table for locking

This layer uses **local state**.

### Layer 2: Main Infrastructure
Uses:
- Remote backend (S3 + DynamoDB)
- Modular Terraform code
- Creates VPC + EKS + Node Groups

📌 **Terraform backend must exist BEFORE it is used.**

---

## 🔐 Terraform Backend (State & Locking)

### Why Remote Backend?
- Prevents state loss
- Enables collaboration
- Avoids concurrent applies
- Secures infrastructure metadata

### Backend Resources
- **S3** → Stores `terraform.tfstate`
- **DynamoDB** → State locking

### Backend Configuration (Root `backend.tf`)
```hcl
terraform {
  backend "s3" {
    bucket         = "terraform-eks-s3-bucket-ums"
    key            = "eks/terraform.tfstate"
    region         = "us-east-1"
    dynamodb_table = "terraform-state-locks-ums"
    encrypt        = true
  }
}

🚫 Terraform State & Git (Important Rule)

Terraform state files must NEVER be committed.

Root .gitignore
terraform/.terraform/
terraform/.terraform.lock.hcl
terraform/**/*.tfstate
terraform/**/*.tfstate.backup


📌 Interview rule:

“Terraform state should never be committed to Git.”

🧩 Modular Terraform Design (Core Concept)
Why Modules?

Reusability

Clean separation

Easier debugging

Scalable design

Modules Used
Module	Responsibility
VPC	Networking (subnets, NAT, routing)
EKS	Cluster + Node Groups
🌐 VPC Module – Key Concepts
What the VPC Module Creates

VPC

Public subnets

Private subnets

Internet Gateway

NAT Gateway

Route tables

EKS-required subnet tags

Important EKS Tags
"kubernetes.io/cluster/<cluster-name>" = "shared"
"kubernetes.io/role/elb" = "1"
"kubernetes.io/role/internal-elb" = "1"


📌 Without these tags, LoadBalancers do not work.

☸️ EKS Module – Key Concepts
IAM Roles (Common Failure Point)

Two IAM roles are required:

EKS Cluster Role

EKS Node Group Role

Required Policies
Role	Policies
Cluster	AmazonEKSClusterPolicy, AmazonEKSServicePolicy
Node	WorkerNode, CNI, ECRReadOnly

Missing any policy can cause EKS creation to fail.

❌ Problems Faced During EKS Creation (And Fixes)
❌ Problem 1: EKS creation failed randomly

Cause:

Missing AmazonEKSServicePolicy

Fix:

Attach required IAM policy

❌ Problem 2: Node Group failed to join cluster

Cause:

IAM policies not fully attached before node group creation

Fix:

Explicit depends_on for IAM attachments

❌ Problem 3: Cluster created but nodes not ready

Cause:

No explicit security group

VPC ambiguity

Fix:

Create and attach cluster security group using vpc_id

❌ Problem 4: Terraform backend confusion

Cause:

Trying to create backend and use backend in same config

Fix:

Separate backend infrastructure folder

Run backend first

🧠 Root Terraform Module (Orchestration)

The root main.tf:

Configures provider

Uses remote backend

Invokes VPC module

Passes outputs to EKS module

This ensures correct dependency flow:

VPC → EKS

🚀 Deploying Application to EKS
Step 1: Configure kubectl
aws eks update-kubeconfig \
  --region us-east-1 \
  --name <cluster-name>

Step 2: Verify Nodes
kubectl get nodes

📦 Kubernetes Deployment
Deployment (deployment.yaml)

Defines desired pods

Uses Docker image from registry

Ensures high availability

Service (service.yaml)
type: LoadBalancer


This creates an AWS ELB automatically.

🌍 Accessing the Application
kubectl get svc


Open in browser:

http://<EXTERNAL-IP>/health

🔁 Traffic Flow
Browser
 → AWS ELB
 → Kubernetes Service
 → Pod
 → Container

🧹 Cleanup (Cost Safety)
kubectl delete -f k8s/
terraform destroy


📌 Always destroy unused infrastructure.

##########################################################

# Deploy Application to AWS EKS (Post-Terraform)

## 📌 Overview

This document explains the **step-by-step procedure to deploy a containerized application to AWS EKS** after the infrastructure (VPC + EKS cluster + Node Groups) has been successfully created using **Terraform**.

This follows **real-world DevOps best practices** and is suitable for **future revision and interview discussion**.

---

## 🧠 Prerequisites

Ensure the following are already completed:

- ✅ AWS account configured
- ✅ EKS cluster created using Terraform
- ✅ Worker nodes are in `Ready` state
- ✅ Docker image pushed to Docker Hub
- ✅ `kubectl` and `aws` CLI installed locally
- ✅ Kubernetes manifests (`deployment.yaml`, `service.yaml`) available

---

## 📂 Repository Structure (Relevant)

├── terraform/ # Terraform IaC (EKS already created)
├── k8s/ # Kubernetes manifests
│ ├── deployment.yaml
│ └── service.yaml
├── app/
├── docker/
└── README.md


---

## 🚀 Step 1: Connect kubectl to EKS Cluster

Terraform creates the EKS cluster, but `kubectl` must be explicitly configured.

### 🔹 Update kubeconfig

```bash
aws eks update-kubeconfig \
  --region us-east-1 \
  --name <EKS_CLUSTER_NAME>


Example:

aws eks update-kubeconfig \
  --region us-east-1 \
  --name ums-eks-cluster

🔹 Verify current context
kubectl config current-context


Expected output:

arn:aws:eks:us-east-1:xxxx:cluster/ums-eks-cluster

✅ Step 2: Verify EKS Cluster Health
🔹 Check nodes
kubectl get nodes


Expected:

STATUS: Ready

🔹 Check system pods
kubectl get pods -n kube-system


You should see pods like:

coredns

kube-proxy

aws-node

This confirms the cluster is healthy.

📦 Step 3: Prepare Kubernetes Manifests
3.1 Deployment Manifest (k8s/deployment.yaml)
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
          image: <dockerhub-username>/user-management-service:latest
          imagePullPolicy: Always
          ports:
            - containerPort: 8000


📌 Notes:

Image is pulled from Docker Hub

replicas: 2 ensures high availability

3.2 Service Manifest (k8s/service.yaml)
apiVersion: v1
kind: Service
metadata:
  name: ums-service
spec:
  type: LoadBalancer
  selector:
    app: ums
  ports:
    - port: 80
      targetPort: 8000


📌 Notes:

LoadBalancer is required for AWS EKS

AWS automatically provisions an ELB

🚀 Step 4: Deploy Application to EKS

From the project root directory:

kubectl apply -f k8s/

🔍 Step 5: Verify Deployment
🔹 Check deployments and pods
kubectl get deployments
kubectl get pods


Pods should be in:

STATUS: Running

🔹 Check service
kubectl get svc


Output example:

ums-service   LoadBalancer   <CLUSTER-IP>   <EXTERNAL-IP>   80:xxxxx/TCP


⚠️ EXTERNAL-IP may show <pending> for 1–3 minutes.

🌍 Step 6: Access Application in Browser
🔹 Get LoadBalancer endpoint
kubectl get svc ums-service


Example:

EXTERNAL-IP: a1b2c3d4e5.elb.amazonaws.com

🔹 Open in browser
http://a1b2c3d4e5.elb.amazonaws.com/health


🎉 The application is now live on AWS EKS.

🔁 Traffic Flow (Conceptual)
Browser
  ↓
AWS Load Balancer (ELB)
  ↓
Kubernetes Service
  ↓
Pod
  ↓
Container (FastAPI App)

🧪 Troubleshooting
🔹 Pods not running
kubectl describe pod <pod-name>
kubectl logs <pod-name>

🔹 LoadBalancer stuck in <pending>
kubectl describe svc ums-service


Possible reasons:

Missing subnet tags

AWS quota issues

🧹 Cleanup (Important to Avoid Cost)

When practice is complete:

kubectl delete -f k8s/
terraform destroy

🗣️ Interview-Ready Summary

“I provisioned AWS EKS using Terraform, configured kubectl access, deployed a containerized application using Kubernetes Deployments, and exposed it via a LoadBalancer service to access it through a public URL.”