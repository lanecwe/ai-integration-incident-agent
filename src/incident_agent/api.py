from fastapi import FastAPI

app = FastAPI(
    title="AI Integration Incident Agent",
    description="API for investigating integration incidents",
    version="0.1.0",
)


@app.get("/health")
def health_check():
    return {
        "status": "healthy",
        "service": "incident-agent",
    }