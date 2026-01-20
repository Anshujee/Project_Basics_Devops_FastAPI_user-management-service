# 🌐 DNS Setup for DevOps Projects  
## (GoDaddy Domain + AWS Route53 + Real-World Debugging Guide)

This document explains **end-to-end DNS setup** required for DevOps and Cloud projects, including:

- Purchasing a domain from **GoDaddy**
- Connecting the domain to **AWS Route53**
- Understanding DNS delegation
- Verifying DNS using command-line tools
- Debugging real-world DNS issues

This guide is written from a **first-time learner’s perspective** and reflects **actual production troubleshooting**, not just ideal steps.

---

## 📌 Why DNS Is Important in DevOps

DNS is a **foundational requirement** for production systems.

DNS is required for:
- HTTPS (TLS / ACM certificates)
- AWS Load Balancers (ALB / ELB)
- Kubernetes Ingress
- CI/CD pipelines
- Real user traffic via browser

If DNS is not configured correctly:
- ACM certificate validation fails
- HTTPS does not work
- Ingress routing breaks

---

## 🧠 Core DNS Concepts (Must Understand)

| Term | Meaning |
|----|--------|
Domain Registrar | Company where the domain is purchased (GoDaddy) |
DNS Provider | Service that manages DNS records (AWS Route53) |
Nameservers | Decide **who controls DNS for the domain** |
Hosted Zone | DNS database inside Route53 |
ACM | AWS Certificate Manager (TLS certificates) |
`dig` | CLI tool to verify DNS delegation |

📌 **Registrar and DNS provider can be different** — this is normal and common in real projects.

---

## 🏗️ High-Level Architecture

User / Browser
↓
Domain (GoDaddy)
↓
Nameservers (Route53)
↓
DNS Records (Route53)
↓
AWS ALB
↓
Kubernetes Ingress
↓
Service
↓
Pod

---

# 🟦 PART 1 — Buy Domain from GoDaddy

### Step 1: Purchase Domain

1. Go to https://www.godaddy.com
2. Search for a domain (example: `umsdevopsdemo.in`)
3. Complete payment
4. Verify domain ownership via email

At this stage:
- GoDaddy is both **Registrar + DNS provider**
- AWS is **not connected yet**

---

# 🟦 PART 2 — Create Hosted Zone in AWS Route53

### Why Hosted Zone Is Required

Route53 Hosted Zone:
- Stores DNS records
- Enables ACM certificate validation
- Integrates with AWS Load Balancers and Kubernetes

---

### Step 2: Create Hosted Zone

1. Login to **AWS Console**
2. Go to **Route53**
3. Click **Hosted zones → Create hosted zone**
4. Enter:
   - Domain name: `umsdevopsdemo.in`
   - Type: **Public hosted zone**
5. Click **Create**

AWS automatically creates:
- NS (Nameserver) records
- SOA record

---

### Step 3: Copy Route53 Nameservers

Example (your values will differ):

ns-558.awsdns-05.net
ns-1671.awsdns-16.co.uk
ns-1192.awsdns-21.org
ns-476.awsdns-59.com


⚠️ **Do NOT include trailing dots when pasting into GoDaddy**

---

# 🟦 PART 3 — Connect GoDaddy Domain to Route53

This is the **most critical step**.

### Important Rule

> **DNS delegation is controlled ONLY by nameservers, not DNS records.**

---

### Step 4: Change Nameservers in GoDaddy

1. GoDaddy → **My Products**
2. Select your domain (`umsdevopsdemo.in`)
3. Open **Domain Settings**
4. Find **Nameservers**
5. Click **Change**
6. Select:
I'll use my own nameservers
7. Paste Route53 nameservers (one per line)
8. Save

After saving, GoDaddy must show:

Nameservers: Custom


---

# 🟦 PART 4 — Verify DNS Delegation (CRITICAL STEP)

UI confirmation is **not reliable**.  
Always verify DNS using CLI.

---

### Step 5: Verify Using `dig`

Run on your local machine:

```bash
dig NS umsdevopsdemo.in 
if Output is like -- 

ns63.domaincontrol.com
ns64.domaincontrol.com
❌ Incorrect Output (GoDaddy Still Controls DNS)
This means:

DNS is NOT delegated

Route53 is NOT active

✅ Correct Output (SUCCESS)

ns-558.awsdns-05.net
ns-1671.awsdns-16.co.uk
ns-1192.awsdns-21.org
ns-476.awsdns-59.com
This confirms:

Route53 is authoritative

DNS delegation is complete

You can proceed with ACM and HTTPS

Real-World Debugging Scenarios
Issue 1: “Hostname has invalid TLD” in GoDaddy

Cause
Route53 displays nameservers with trailing dots:

ns-558.awsdns-05.net.


Fix
Remove the trailing dot before pasting into GoDaddy:

ns-558.awsdns-05.net

Issue 2: dig still shows domaincontrol.com

Cause

Nameservers edited in wrong section

Change not saved properly

Registrar-side delay

Fix

Ensure Nameservers → Custom

Re-save correctly

Verify again using dig

Issue 3: Waiting Did Not Help

Lesson

If dig output does not change, the delegation was not applied — waiting alone will not fix it.

Registrar support may be required in some cases.

🧠 Key Learnings (Remember Forever)

DNS records ≠ DNS delegation

Nameservers decide DNS authority

dig NS > UI screenshots

Registrar issues are common in real projects

This is real DevOps experience, not failure

🗣️ Interview-Ready Explanation

“I purchased the domain from GoDaddy, delegated DNS to AWS Route53 using custom nameservers, and verified the change using dig NS before proceeding with ACM and HTTPS.”

✅ Final Checklist

✔ Domain purchased from GoDaddy
✔ Route53 hosted zone created
✔ Nameservers updated correctly
✔ dig NS shows awsdns
✔ DNS delegation successfull. 

