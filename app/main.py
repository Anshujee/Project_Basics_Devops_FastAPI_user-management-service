import os
from fastapi import FastAPI
import psut
import psycopg2

app = FastAPI()

# ---------- CPU / Memory Thresholds ----------
CPU_THRESHOLD = int(os.getenv("CPU_THRESHOLD", 80))
MEMORY_THRESHOLD = int(os.getenv("MEMORY_THRESHOLD", 80))

# ---------- Database Config ----------
DB_HOST = os.getenv("DB_HOST")
DB_PORT = os.getenv("DB_PORT")
DB_NAME = os.getenv("DB_NAME")
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")


def check_database_connection():
    """
    Try to connect to PostgreSQL.
    Returns True if successful, False otherwise.
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
        return True
    except Exception:
        return False


@app.get("/health")
def health_check():
    """
    Overall system health:
    - CPU
    - Memory
    - Database connectivity
    """
    cpu_usage = psutil.cpu_percent(interval=1)
    memory_usage = psutil.virtual_memory().percent
    db_connected = check_database_connection()

    status = "UP"

    if (
        cpu_usage > CPU_THRESHOLD
        or memory_usage > MEMORY_THRESHOLD
        or not db_connected
    ):
        status = "DOWN"

    return {
        "status": status,
        "cpu_usage": cpu_usage,
        "memory_usage": memory_usage,
        "db_connected": db_connected,
        "cpu_threshold": CPU_THRESHOLD,
        "memory_threshold": MEMORY_THRESHOLD
    }


@app.get("/db-check")
def db_check():
    """
    Database-only health endpoint.
    Useful for debugging and learning.
    """
    db_connected = check_database_connection()

    if db_connected:
        return {
            "db_status": "UP",
            "message": "Database is reachable"
        }
    else:
        return {
            "db_status": "DOWN",
            "message": "Database is NOT reachable"
        }
