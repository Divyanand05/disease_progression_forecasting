from fastapi import APIRouter

router = APIRouter(tags=["Health"])

@router.get("/")
def root():
    return {"status": "ok", "message": "API running"}
