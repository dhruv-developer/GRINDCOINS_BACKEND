from fastapi import APIRouter, Form
from fastapi.responses import JSONResponse
from app.db.mongodb import db

router = APIRouter()

# MongoDB Collection
goals_collection = db["goals"]

@router.post("/add-goal")
async def add_goal(
    email: str = Form(...),
    title: str = Form(...),
    deadline: str = Form(...),
    duration: str = Form(...)
):
    try:
        goal_data = {
            "email": email,
            "title": title,
            "deadline": deadline,
            "duration": duration
        }
        goals_collection.insert_one(goal_data)
        return {"message": "Goal added successfully!"}
    except Exception as e:
        print(f"Error adding goal: {e}")
        return JSONResponse(status_code=500, content={"error": "Internal Server Error"})

@router.get("/get-goals")
async def get_goals(email: str):
    try:
        goals = list(goals_collection.find({"email": email}, {"_id": 0}))
        return {"goals": goals}
    except Exception as e:
        print(f"Error fetching goals: {e}")
        return JSONResponse(status_code=500, content={"error": "Internal Server Error"})

@router.post("/complete-goal")
async def complete_goal(email: str = Form(...), title: str = Form(...)):
    try:
        goals_collection.update_one(
            {"email": email, "title": title},
            {"$set": {"completed": True}}
        )
        return {"message": "Goal marked as completed!"}
    except Exception as e:
        print(f"Error completing goal: {e}")
        return JSONResponse(status_code=500, content={"error": "Internal Server Error"})
