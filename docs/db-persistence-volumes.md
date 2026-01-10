## Database Persistence Using Docker Volumes (PostgreSQL + Docker Compose)

📘 What this README covers (so you know its value)

This document clearly explains:

✔ Why database persistence is mandatory

✔ Why containers lose data by default

✔ What Docker volumes are (with analogy)

✔ How PostgreSQL stores its data

✔ How volumes solve the persistence problem

✔ Step-by-step Docker Compose changes

✔ Full working docker-compose.yml

✔ How to verify persistence practically

✔ Dangerous commands to avoid (--volumes)

✔ DevOps interview–ready explanations

✔ Real production mindset (immutable infra + persistent data)

This is not tutorial fluff — it’s real DevOps knowledge written for future you.
# 💾 Database Persistence Using Docker Volumes (PostgreSQL + Docker Compose)

This document explains **Database Persistence using Docker Volumes** in a clear, beginner-friendly yet professional DevOps manner.

It captures:

* Why database persistence is required
* What problem exists without volumes
* How Docker volumes work internally
* How PostgreSQL uses volumes
* How persistence was implemented step by step
* How to verify persistence practically
* Common doubts, mistakes, and interview insights

This README is meant for **future revision, real-world understanding, and DevOps interviews**.

---

## 1️⃣ Why Database Persistence Is Required

By default, Docker containers are **ephemeral**.

This means:

* Containers can be stopped
* Containers can be deleted
* Containers can be recreated

👉 **All data inside the container is lost** when this happens.

For databases, this is unacceptable.

In real systems:

* Applications may restart
* Containers may be redeployed
* Servers may reboot

But:

> **Database data must survive all of this**

That is why **database persistence** is mandatory.

---

## 2️⃣ The Problem Without Volumes

Without volumes:

```bash
docker compose down
docker compose up -d
```

Result:

* PostgreSQL container is recreated
* Database files are lost
* Tables and records disappear

This happens because:

* Data was stored inside the container filesystem
* Container filesystem is destroyed on removal

---

## 3️⃣ Real-Life Analogy (Easy to Remember)

* **Container** → Hotel room (temporary)
* **Database data** → Your luggage

When you leave the hotel:

* Room is cleaned
* Your luggage is gone ❌

A **Docker volume** is like:

* A **locker outside the hotel**

Even if:

* You change rooms
* Hotel shuts down

Your luggage remains safe ✅

---

## 4️⃣ What Is a Docker Volume?

A Docker volume is:

* Storage managed by Docker
* Lives outside the container lifecycle
* Can be reused by new containers

Key rule:

> ❌ Containers are temporary
> ✅ Volumes are persistent

---

## 5️⃣ How PostgreSQL Stores Data

PostgreSQL stores all database files at:

```text
/var/lib/postgresql/data
```

If we mount a Docker volume to this path:

* Data moves outside the container
* Data survives container restarts

---

## 6️⃣ Implementing Persistence in Docker Compose

### Step 1: Add Volume Mount to DB Service

```yaml
volumes:
  - postgres_data:/var/lib/postgresql/data
```

This connects:

* `postgres_data` → Docker-managed storage
* `/var/lib/postgresql/data` → PostgreSQL data directory

---

### Step 2: Declare the Volume

At the bottom of `docker-compose.yml`:

```yaml
volumes:
  postgres_data:
```

This tells Docker:

* Create and manage this volume

---

## 7️⃣ Complete docker-compose.yml (With Persistence)

```yaml
version: "3.9"

services:
  app:
    build:
      context: .
      dockerfile: docker/Dockerfile
    image: user-management-service:1.0
    container_name: user-management-app
    ports:
      - "8000:8000"
    env_file:
      - .env
    depends_on:
      db:
        condition: service_healthy
    restart: unless-stopped
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:8000/health"]
      interval: 30s
      timeout: 5s
      retries: 3
      start_period: 15s

  db:
    image: postgres:15
    container_name: postgres-db
    environment:
      POSTGRES_DB: userdb
      POSTGRES_USER: useradmin
      POSTGRES_PASSWORD: userpassword
    ports:
      - "5432:5432"
    volumes:
      - postgres_data:/var/lib/postgresql/data
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U useradmin -d userdb"]
      interval: 10s
      timeout: 5s
      retries: 5

volumes:
  postgres_data:
```

---

## 8️⃣ Running the Stack

```bash
docker compose down
docker compose up -d
```

Important:

* **Do NOT use `--volumes`** unless you want to delete DB data

---

## 9️⃣ Verifying Persistence (Hands-on Proof)

### Step 1: Create Data

```bash
docker exec -it postgres-db psql -U useradmin -d userdb
```

```sql
CREATE TABLE test_data (
  id SERIAL PRIMARY KEY,
  name TEXT
);

INSERT INTO test_data (name) VALUES ('Anshu');
SELECT * FROM test_data;
```

---

### Step 2: Stop Containers

```bash
docker compose down
```

---

### Step 3: Start Again

```bash
docker compose up -d
```

---

### Step 4: Verify Data Still Exists

```bash
docker exec -it postgres-db psql -U useradmin -d userdb
SELECT * FROM test_data;
```

Result:

```text
1 | Anshu
```

🎉 Database persistence confirmed.

---

## 🔥 Important Command to Remember

```bash
docker compose down --volumes
```

⚠️ This command will:

* Stop containers
* Delete volumes
* Permanently remove database data

Use **only when intentionally resetting the DB**.

---

## 🧠 Key Concepts Learned

* Containers are ephemeral
* Databases must use persistent storage
* Docker volumes survive container recreation
* Data lifecycle ≠ container lifecycle
* Persistence is mandatory for production systems

---

## 🎯 Interview-Ready Explanation

> "Database persistence in Docker is achieved by mounting a Docker volume to the database’s data directory so that data survives container restarts and redeployments."

---

## 🏁 Final Notes

This setup mirrors real-world DevOps practices where:

* Applications are redeployed frequently
* Databases retain state
* Infrastructure is immutable

This document serves as a **long-term DevOps reference** and prepares the foundation for:

* Database migrations
* Backups
* Kubernetes Persistent Volumes

---

✅ *Learning by doing. Understanding by persisting.*
