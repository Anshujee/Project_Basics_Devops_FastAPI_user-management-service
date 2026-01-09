from fastapi import FastAPI
import psutil

app = FastAPI()

@app.get("/health")
def health_check():
    cpu_usage = psutil.cpu_percent(interval=1)
    memory_usage = psutil.virtual_memory().percent

    if cpu_usage < 80 and memory_usage < 80:
        return {
            "status": "UP",
            "cpu_usage": cpu_usage,
            "memory_usage": memory_usage
        }
    else:
        return {
            "status": "DOWN",
            "cpu_usage": cpu_usage,
            "memory_usage": memory_usage
        }
