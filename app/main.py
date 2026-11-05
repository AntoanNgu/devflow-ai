from fastapi import FastAPI


app = FastAPI(title="devflow-ai")

@app.get("/health")
def health():
    return {"status": "ok"}