from fastapi import FastAPI

from backend.api.routes.health import router as health_router
from backend.api.routes.patient import router as patients_router
from backend.api.routes.records import router as records_router
from backend.api.routes.prediction import router as predictions_router



from backend.DB.database import Base, engine
from backend.DB import models  # important: loads models so tables are created

Base.metadata.create_all(bind=engine)

app = FastAPI(title="Disease Progression Forecast API")


app.include_router(health_router)
app.include_router(patients_router)
app.include_router(records_router)
app.include_router(predictions_router)

