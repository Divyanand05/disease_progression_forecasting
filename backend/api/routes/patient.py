from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from backend.DB.database import SessionLocal
from backend.DB.models import Patient
from backend.api.schemas.patient_schema import PatientCreate, PatientOut

router = APIRouter(prefix="/patients", tags=["Patients"])

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/", response_model=PatientOut)
def create_patient(payload: PatientCreate, db: Session = Depends(get_db)):
    p = Patient(**payload.model_dump())
    db.add(p)
    db.commit()
    db.refresh(p)
    return p

@router.get("/", response_model=list[PatientOut])
def list_patients(db: Session = Depends(get_db)):
    return db.query(Patient).order_by(Patient.id.desc()).all()

@router.get("/{patient_id}", response_model=PatientOut)
def get_patient(patient_id: int, db: Session = Depends(get_db)):
    p = db.query(Patient).filter(Patient.id == patient_id).first()
    if not p:
        raise HTTPException(status_code=404, detail="Patient not found")
    return p
