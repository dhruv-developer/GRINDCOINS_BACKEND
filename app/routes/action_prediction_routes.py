from fastapi import APIRouter, File, UploadFile
from fastapi.responses import JSONResponse
from app.services.action_prediction_service import predict_action_from_video

router = APIRouter()  # ✅ This must exist

@router.post("/predict-action")
async def predict_action(file: UploadFile = File(...)):
    result = await predict_action_from_video(file)
    if "error" in result:
        return JSONResponse(status_code=400, content=result)
    return result
