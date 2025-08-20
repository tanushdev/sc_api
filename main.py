from fastapi import FastAPI, UploadFile, File
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
import tempfile, shutil, os
import pandas as pd
from pipeline import run_pipeline

app = FastAPI(title="SC API", version="1.0")

# Allow frontend to call API
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

DATASET_PATH = "dataset.csv"

@app.post("/analyze-pdfs/")
async def analyze_pdfs(files: list[UploadFile] = File(...)):
    with tempfile.TemporaryDirectory() as tmpdirname:
        for file in files:
            file_path = os.path.join(tmpdirname, file.filename)
            with open(file_path, "wb") as buffer:
                shutil.copyfileobj(file.file, buffer)

        results = run_pipeline(tmpdirname)
        json_result = results.to_dict(orient="records")

        # Save to dataset.csv
        if os.path.exists(DATASET_PATH):
            dataset = pd.read_csv(DATASET_PATH)
            dataset = pd.concat([dataset, results], ignore_index=True)
        else:
            dataset = results

        dataset.to_csv(DATASET_PATH, index=False)
        return JSONResponse(content={"results": json_result})
