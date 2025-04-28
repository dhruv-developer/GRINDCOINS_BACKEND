from fastapi import APIRouter, UploadFile, Form, File
from fastapi.responses import JSONResponse
from app.services.goal_service import complete_goal_with_video

router = APIRouter()

@router.post("/complete-goal-video")
async def complete_goal_video(
    email: str = Form(...),
    title: str = Form(...),
    video: UploadFile = File(...)
):
    print("\n✅ /complete-goal-video called")
    print(f"Email: {email}, Goal Title: {title}, Video: {video.filename}\n")

    result = await complete_goal_with_video(email, title, video)

    if "error" in result:
        return JSONResponse(status_code=400, content=result)

    return result
