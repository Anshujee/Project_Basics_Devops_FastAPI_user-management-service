import os
from fastapi import FastAPI
import psutil

app = FastAPI()

CPU_THRESHOLD = int(os.getenv("CPU_THRESHOLD", 80))
MEMORY_THRESHOLD = int(os.getenv("MEMORY_THRESHOLD", 80))

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
