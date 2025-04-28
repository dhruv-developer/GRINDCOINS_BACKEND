from fastapi import APIRouter, File, UploadFile
from fastapi.responses import JSONResponse
from app.services.prediction_service import predict_posture_from_video

router = APIRouter()

@router.post("/predict-posture")
async def predict_posture(file: UploadFile = File(...)):
    result = await predict_posture_from_video(file)
    if "error" in result:
        return JSONResponse(status_code=400, content=result)
    return result
