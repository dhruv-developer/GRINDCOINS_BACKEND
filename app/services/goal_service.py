import os
from fastapi import UploadFile
from app.database import users_db, goals_db
import shutil

async def complete_goal_with_video(email: str, title: str, video: UploadFile):
    user = users_db.get(email)
    if not user:
        return {"error": "User not found."}

    goal_key = f"{email}:{title}"
    goal = goals_db.get(goal_key)

    if not goal:
        return {"error": "Goal not found."}

    if goal["completed"]:
        return {"error": "Goal already completed."}

    # 🛠 Save the uploaded video proof
    save_dir = f"uploads/{email.replace('@', '_at_')}/"
    os.makedirs(save_dir, exist_ok=True)
    video_path = os.path.join(save_dir, f"{title}_proof.mp4")

    with open(video_path, "wb") as buffer:
        shutil.copyfileobj(video.file, buffer)

    # 🎯 Mark goal as completed
    goal["completed"] = True

    # 🎯 Increase user's coins by 10
    user["coins"] = user.get("coins", 0) + 10

    print(f"✅ Goal '{title}' marked completed for user {email} (+10 coins)")

    return {"message": "Goal completed and verified successfully! 🎯"}
