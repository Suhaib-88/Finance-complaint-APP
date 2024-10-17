# main.py
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from backend.src.pipeline.training import TrainingPipeline
from backend.src.config.config_pipeline.training import FinanceConfig
from backend.src.exception import FinanceException



from pydantic import BaseModel
# from finance_complaint.pipeline import TrainingPipeline, PredictionPipeline
# from finance_complaint.config.pipeline.training import FinanceConfig
# from finance_complaint.exception import FinanceException

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Update this to your frontend URL
    allow_credentials=True,
    allow_methods=["*"],  # Allows all HTTP methods (GET, POST, etc.)
    allow_headers=["*"],  # Allows all headers (content-type, authorization, etc.)
)

# # Request model for submitting complaints
# class ComplaintRequest(BaseModel):
#     text: str

# @app.post("/api/complaints")
# async def submit_complaint(complaint: ComplaintRequest):
#     # Logic for handling complaint submission
#     try:
#         # Perform any preprocessing or storage of the complaint if needed
#         result = PredictionPipeline().predict_complaint(complaint.text)
#         return {"complaint": complaint.text, "prediction": result}
#     except Exception as e:
#         raise HTTPException(status_code=500, detail=str(FinanceException(e)))

@app.get("/api/model-status")
async def get_model_status():
    # Return model status (dummy status used here as example)
    return {"training": False, "predicting": False}


@app.post("/api/train")
async def start_training():
    try:
        TrainingPipeline(FinanceConfig()).start()
        return {"status": "Training started"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(FinanceException(e)))

# @app.post("/api/predict")
# async def start_prediction():
#     try:
#         PredictionPipeline().start_batch_prediction()
#         return {"status": "Prediction started"}
#     except Exception as e:
#         raise HTTPException(status_code=500, detail=str(FinanceException(e)))

@app.get("/api/dashboard")
async def fetch_dashboard_data():
    # Mock data for dashboard; replace with actual logic
    return {"total_complaints": 150, "resolved": 100, "pending": 50}

