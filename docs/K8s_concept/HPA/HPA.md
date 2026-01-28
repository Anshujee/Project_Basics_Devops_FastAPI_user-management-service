# 📘 Kubernetes HPA (Horizontal Pod Autoscaler)

A complete **revision + interview-ready guide** based on hands-on implementation in this project.

---

## 1️⃣ What is HPA?

**Horizontal Pod Autoscaler (HPA)** is a Kubernetes controller that automatically **scales the number of pods** in a Deployment, ReplicaSet, or StatefulSet based on observed metrics.

👉 In simple terms:

> HPA decides **how many pods should be running** based on application load.

---

## 2️⃣ Why Do We Need HPA?

### ❌ Without HPA

* Fixed number of replicas
* Manual scaling
* Poor handling of traffic spikes
* Risk of downtime
* Resource wastage

Example:

```yaml
replicas: 2
```

If traffic suddenly increases, the application may fail.

---

### ✅ With HPA

* Automatic scaling
* Handles traffic spikes
* Cost-efficient
* Production-grade behavior

📌 **HPA is mandatory in real-world production Kubernetes setups.**

---

## 3️⃣ What Exactly Does HPA Scale?

⚠️ Important clarification:

| Component   | Scaled By              |
| ----------- | ---------------------- |
| Pods        | HPA                    |
| Nodes (EC2) | Cluster Autoscaler     |
| Traffic     | Ingress / LoadBalancer |

👉 HPA **only scales pods**, not nodes.

---

## 4️⃣ Core Components Required for HPA

HPA works only when these components are present:

1. **Metrics Server**
2. **Resource Requests**
3. **HPA Object**
4. **Deployment**

---

### 4.1 Metrics Server

Metrics Server provides CPU and memory metrics.

Without it:

```text
HPA will NOT work
```

---

### 4.2 Resource Requests (Critical)

HPA calculates utilization **based on resource requests**, not limits.

Example:

```yaml
resources:
  requests:
    cpu: "100m"
    memory: "128Mi"
```

❌ If requests are missing, HPA will not scale.

---

## 5️⃣ Types of Autoscaling in Kubernetes

| Type       | Description               |
| ---------- | ------------------------- |
| Horizontal | Pod scaling (HPA)         |
| Vertical   | Pod resource resize (VPA) |
| Cluster    | Node scaling              |

👉 This project uses **Horizontal Pod Autoscaling**.

---

## 6️⃣ How HPA Works (Core Logic)

Example:

* CPU request = 100m
* Target = 50%
* Current usage = 80m

Calculation:

```
80m / 100m = 80%
```

Since 80% > 50%, **HPA scales up pods**.

---

## 7️⃣ HPA Control Loop

HPA runs every ~15 seconds:

1. Reads metrics
2. Compares with target
3. Decides scale up/down
4. Updates replica count

Scaling is **gradual**, not instant.

---

## 8️⃣ HPA API Versions

| Version        | Capability                  |
| -------------- | --------------------------- |
| autoscaling/v1 | CPU only                    |
| autoscaling/v2 | CPU, Memory, Custom metrics |

✅ This project uses **autoscaling/v2**.

---

## 9️⃣ HPA Template (Helm)

```yaml
{{- if .Values.autoscaling.enabled }}
apiVersion: autoscaling/v2
kind: HorizontalPodAutoscaler
metadata:
  name: {{ .Release.Name }}
spec:
  scaleTargetRef:
    apiVersion: apps/v1
    kind: Deployment
    name: {{ .Release.Name }}
  minReplicas: {{ .Values.autoscaling.minReplicas }}
  maxReplicas: {{ .Values.autoscaling.maxReplicas }}
  metrics:
    - type: Resource
      resource:
        name: cpu
        target:
          type: Utilization
          averageUtilization: {{ .Values.autoscaling.targetCPUUtilizationPercentage }}
{{- end }}
```

---

## 🔟 values-prod.yaml (HPA Section)

```yaml
autoscaling:
  enabled: true
  minReplicas: 2
  maxReplicas: 6
  targetCPUUtilizationPercentage: 50
```

Meaning:

* Minimum pods: 2
* Maximum pods: 6
* Scale when CPU > 50%

---

## 1️⃣1️⃣ App Threshold vs HPA (Important Difference)

| Feature           | Purpose            |
| ----------------- | ------------------ |
| CPU_THRESHOLD env | App health logic   |
| HPA CPU target    | Kubernetes scaling |

👉 These are **independent systems**.

---

## 1️⃣2️⃣ How HPA Was Tested (Hands-On)

Load generation:

```bash
kubectl run -i --tty load-generator \
  --image=busybox \
  -n prod \
  -- /bin/sh
```

Inside pod:

```bash
while true; do wget -q -O- http://ums-service/health; done
```

Result:

* CPU increased
* HPA scaled pods automatically

---

## 1️⃣3️⃣ Useful Commands

```bash
kubectl get hpa -n prod
kubectl describe hpa ums -n prod
kubectl get pods -n prod
```

---

## 1️⃣4️⃣ Common HPA Issues

| Issue               | Cause                     |
| ------------------- | ------------------------- |
| HPA not scaling     | Missing resource requests |
| CPU shows <unknown> | Metrics server missing    |
| Helm lint error     | autoscaling block missing |
| No scale-down       | Cooldown period           |

---

## 1️⃣5️⃣ Production Best Practices

✅ Always define requests
✅ Use autoscaling/v2
✅ Set safe min/max replicas
✅ Monitor HPA metrics
✅ Combine with Cluster Autoscaler

---

## 1️⃣6️⃣ Interview-Ready Summary

> HPA is a Kubernetes controller that automatically scales pods based on resource utilization. It relies on metrics-server and resource requests, operates via a control loop, and is essential for production-grade Kubernetes deployments.

---

## ✅ Final Takeaway

HPA enables **resilient, scalable, and cost-efficient applications** in Kubernetes and is a **must-have skill for DevOps Engineers**.

---

📌 **Next Learning Options**

* Cluster Autoscaler
* Custom Metrics HPA (Prometheus)
* KEDA (Event-driven autoscaling)
