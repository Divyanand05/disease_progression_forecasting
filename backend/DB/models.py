from sqlalchemy import Column, Integer, String, Float, ForeignKey, DateTime
from datetime import datetime
from .database import Base
from sqlalchemy import Column, Integer, Float, ForeignKey, String, DateTime
from datetime import datetime


class Patient(Base):
    __tablename__ = "patients"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    age = Column(Integer, nullable=False)
    gender = Column(String(20), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)

class ClinicalRecord(Base):
    __tablename__ = "clinical_records"

    id = Column(Integer, primary_key=True, index=True)
    patient_id = Column(Integer, ForeignKey("patients.id"), nullable=False)

    bmi = Column(Float, nullable=False)
    bp = Column(Float, nullable=False)
    s1 = Column(Float, nullable=False)
    s2 = Column(Float, nullable=False)
    s3 = Column(Float, nullable=False)
    s4 = Column(Float, nullable=False)
    s5 = Column(Float, nullable=False)
    s6 = Column(Float, nullable=False)

    created_at = Column(DateTime, default=datetime.utcnow)

class Prediction(Base):
    __tablename__ = "predictions"

    id = Column(Integer, primary_key=True, index=True)
    patient_id = Column(Integer, ForeignKey("patients.id"), nullable=False)
    predicted_score = Column(Float, nullable=False)
    risk_level = Column(String(20), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
