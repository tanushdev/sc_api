# main.py
from fastapi import FastAPI, UploadFile, File
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
import tempfile
import shutil
import os
import pandas as pd
from pipeline import run_pipeline  # your existing pipeline

app = FastAPI(title="SC Scoring API", version="1.0")

# Allow CORS for frontend access
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # restrict to your domain in production
    allow_methods=["*"],
    allow_headers=["*"],
)

DATASET_PATH = "dataset.csv"

# Serve HTML frontend
app.mount("/", StaticFiles(directory=".", html=True), name="frontend")

@app.get("/health")
def health():
    return {"status": "OK", "message": "SC API is running"}

@app.post("/analyze-pdfs/")
async def analyze_pdfs(files: list[UploadFile] = File(...)):
    """
    Upload one or more PDFs → process with SC pipeline → return scores
    and save to dataset.csv
    """
    with tempfile.TemporaryDirectory() as tmpdirname:
        for file in files:
            file_path = os.path.join(tmpdirname, file.filename)
            with open(file_path, "wb") as buffer:
                shutil.copyfileobj(file.file, buffer)

        # Run pipeline
        results = run_pipeline(tmpdirname)

        # Convert DataFrame to JSON
        json_result = results.to_dict(orient="records")

        # Save or append to dataset
        if os.path.exists(DATASET_PATH):
            dataset = pd.read_csv(DATASET_PATH)
            dataset = pd.concat([dataset, results], ignore_index=True)
        else:
            dataset = results

        dataset.to_csv(DATASET_PATH, index=False)

        return JSONResponse(content={"results": json_result})

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
