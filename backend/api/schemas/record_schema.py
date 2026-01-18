from pydantic import BaseModel

class RecordCreate(BaseModel):
    patient_id: int
    bmi: float
    bp: float
    s1: float
    s2: float
    s3: float
    s4: float
    s5: float
    s6: float

class RecordOut(RecordCreate):
    id: int
    class Config:
        from_attributes = True
