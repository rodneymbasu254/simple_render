from fastapi import FastAPI, HTTPException, Header, Depends
from pydantic import BaseModel
import joblib, os
from fastapi.middleware.cors import CORSMiddleware

class PredictRequest(BaseModel):
    text: str

class PredictResponse(BaseModel):
    input: str
    prediction: str
    score: float

app = FastAPI(title="Simple Sentiment API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], 
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

API_KEY = os.environ.get("API_KEY")

model = joblib.load("model.joblib")

def verify_api_key(x_api_key: str = Header(None)):
    if API_KEY and x_api_key != API_KEY:
        raise HTTPException(status_code=401, detail="Invalid API key")

@app.get("/")
def root():
    return {"status": "ok"}

@app.post("/predict", response_model=PredictResponse, dependencies=[Depends(verify_api_key)])
def predict(req: PredictRequest):
    text = req.text
    probs = model.predict_proba([text])[0] 
    idx = int(probs.argmax())
    label = str(model.classes_[idx])
    score = float(probs[idx])
    return PredictResponse(input=text, prediction=label, score=score)
