from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from backend.DB.database import SessionLocal
from backend.DB.models import ClinicalRecord, Patient
from backend.api.schemas.record_schema import RecordCreate, RecordOut

router = APIRouter(prefix="/records", tags=["Clinical Records"])

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/", response_model=RecordOut)
def add_record(payload: RecordCreate, db: Session = Depends(get_db)):
    # check patient exists
    patient = db.query(Patient).filter(Patient.id == payload.patient_id).first()
    if not patient:
        raise HTTPException(status_code=404, detail="Patient not found")

    r = ClinicalRecord(**payload.model_dump())
    db.add(r)
    db.commit()
    db.refresh(r)
    return r

@router.get("/{patient_id}", response_model=list[RecordOut])
def get_records(patient_id: int, db: Session = Depends(get_db)):
    return db.query(ClinicalRecord).filter(ClinicalRecord.patient_id == patient_id).all()
