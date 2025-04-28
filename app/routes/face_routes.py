from fastapi import APIRouter, File, UploadFile, Form
from fastapi.responses import JSONResponse
from app.services.face_service import register_face, recognize_face

router = APIRouter()

@router.post("/register-face")
async def register(file: UploadFile = File(...), name: str = Form(...)):
    result = await register_face(file, name)
    if "error" in result:
        return JSONResponse(status_code=400, content=result)
    return result

@router.post("/recognize-face")
async def recognize(file: UploadFile = File(...)):
    result = await recognize_face(file)
    if "error" in result:
        return JSONResponse(status_code=400, content=result)
    return result
