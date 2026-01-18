from pydantic import BaseModel

class PatientCreate(BaseModel):
    name: str
    age: int
    gender: str

class PatientOut(PatientCreate):
    id: int
    class Config:
        from_attributes = True
