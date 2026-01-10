import os
from fastapi import FastAPI
import psutil
import psycopg2

app = FastAPI()

# ---------------- CPU / Memory Config ----------------
CPU_THRESHOLD = int(os.getenv("CPU_THRESHOLD", 80))
MEMORY_THRESHOLD = int(os.getenv("MEMORY_THRESHOLD", 80))

# ---------------- Database Config ----------------
DB_HOST = os.getenv("DB_HOST")
DB_PORT = os.getenv("DB_PORT")
DB_NAME = os.getenv("DB_NAME")
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")


@app.get("/health")
def health_check():
    cpu_usage = psutil.cpu_percent(interval=1)
    memory_usage = psutil.virtual_memory().percent

    status = "UP"
    if cpu_usage > CPU_THRESHOLD or memory_usage > MEMORY_THRESHOLD:
        status = "DOWN"

    return {
        "status": status,
        "cpu_usage": cpu_usage,
        "memory_usage": memory_usage,
        "cpu_threshold": CPU_THRESHOLD,
        "memory_threshold": MEMORY_THRESHOLD
    }


@app.get("/db-check")
def db_check():
    """
    Simple DB connectivity test.
    """
    try:
        connection = psycopg2.connect(
            host=DB_HOST,
            port=DB_PORT,
            dbname=DB_NAME,
            user=DB_USER,
            password=DB_PASSWORD,
            connect_timeout=3
        )
        connection.close()
        return {"db_status": "CONNECTED"}
    except Exception as e:
        return {
            "db_status": "NOT CONNECTED",
            "error": str(e)
        }
