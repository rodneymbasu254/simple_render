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

# CORS - during dev allow all; in production restrict origins
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],   # change to your app origin(s)
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

MODEL_PATH = os.environ.get("MODEL_PATH", "model.joblib")
API_KEY = os.environ.get("API_KEY")  # set on Render for security

# load model (pipeline contains vectorizer + classifier)
model = joblib.load(MODEL_PATH)

def verify_api_key(x_api_key: str = Header(None)):
    # If API_KEY env var is not set, skip check (developer convenience)
    if API_KEY and x_api_key != API_KEY:
        raise HTTPException(status_code=401, detail="Invalid API key")

@app.get("/")
def root():
    return {"status": "ok"}

@app.post("/predict", response_model=PredictResponse, dependencies=[Depends(verify_api_key)])
def predict(req: PredictRequest):
    text = req.text
    # model is a pipeline (vectorizer + classifier)
    probs = model.predict_proba([text])[0]  # requires classifier supports predict_proba
    idx = int(probs.argmax())
    label = str(model.classes_[idx])
    score = float(probs[idx])
    return PredictResponse(input=text, prediction=label, score=score)
