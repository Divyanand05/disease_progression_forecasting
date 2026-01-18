from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from backend.DB.database import SessionLocal
from backend.DB.models import ClinicalRecord, Prediction
from backend.ai.predictor import predict_progression

router = APIRouter(prefix="/predict", tags=["Predictions"])

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def get_risk(score: float):
    if score < 120:
        return "LOW"
    elif score < 200:
        return "MEDIUM"
    return "HIGH"

@router.post("/{patient_id}")
def predict(patient_id: int, db: Session = Depends(get_db)):
    record = (
        db.query(ClinicalRecord)
        .filter(ClinicalRecord.patient_id == patient_id)
        .order_by(ClinicalRecord.id.desc())
        .first()
    )
    if not record:
        raise HTTPException(status_code=404, detail="No clinical record found")

    score = predict_progression(
        record.bmi, record.bp,
        record.s1, record.s2, record.s3, record.s4, record.s5, record.s6
    )

    risk = get_risk(score)

    pred = Prediction(patient_id=patient_id, predicted_score=score, risk_level=risk)
    db.add(pred)
    db.commit()
    db.refresh(pred)

    return {
        "patient_id": patient_id,
        "prediction_id": pred.id,
        "predicted_score": score,
        "risk_level": risk
    }

@router.get("/history/{patient_id}")
def history(patient_id: int, db: Session = Depends(get_db)):
    preds = db.query(Prediction).filter(Prediction.patient_id == patient_id).order_by(Prediction.id.desc()).all()
    return preds
