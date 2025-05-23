import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'

from app.routes.action_prediction_routes import router as action_router
from app.routes.face_routes import router as face_router
from app.routes.auth_routes import router as auth_router
from app.routes.dashboard_routes import router as dashboard_router
from app.routes.goal_routes import router as goal_router

app = FastAPI()

# ✅ Add CORS Middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # ⚡ For testing allow all. For production, list your frontend domain e.g., ["http://localhost:19006"]
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ✅ Now include routers
app.include_router(action_router)
app.include_router(face_router)
app.include_router(auth_router)
app.include_router(dashboard_router)
app.include_router(goal_router)

# Set random port for local use (for Docker or local development)
port = os.getenv("PORT", 8000)  # Default to 8000 if no PORT environment variable is set
print(f"Starting server on port {port}...")
