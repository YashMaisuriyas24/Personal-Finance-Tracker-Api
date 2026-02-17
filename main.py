import uvicorn
from api__.api__ import app

@app.on_event("startup")
async def startup_event():
    print("Starting Finance Tracker API...")

@app.on_event("shutdown")
async def shutdown_event():
    print("Shutting down Finance Tracker API...")


if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True
    )