from fastapi import FastAPI

app = FastAPI(title="Email Summarizer Agent")


@app.get("/health")
def health_check():
    return {"status": "ok"}