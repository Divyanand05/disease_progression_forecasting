from pydantic import BaseModel

class PredictionOut(BaseModel):
    patient_id: int
    predicted_score: float
    risk_level: str
    prediction_id: int

    class Config:
        from_attributes = True
