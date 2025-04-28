from fastapi import APIRouter, File, UploadFile, Form
from fastapi.responses import JSONResponse
from app.services.auth_service import signup_user, verify_otp, login_user

router = APIRouter()

@router.post("/signup")
async def signup(file: UploadFile = File(...), email: str = Form(...), name: str = Form(...)):
    print("\n✅ /signup called")
    print(f"Email: {email}")
    print(f"Name: {name}")
    print(f"File: {file.filename}\n")
    
    result = await signup_user(file, email, name)
    if "error" in result:
        return JSONResponse(status_code=400, content=result)
    return result

@router.post("/verify-otp")
async def verify(email: str = Form(...), otp: str = Form(...)):
    print("\n✅ /verify-otp called")
    print(f"Email: {email}")
    print(f"OTP: {otp}\n")
    
    result = await verify_otp(email, otp)
    if "error" in result:
        return JSONResponse(status_code=400, content=result)
    return result

@router.post("/login")
async def login(file: UploadFile = File(...), email: str = Form(...)):
    print("\n✅ /login called")
    print(f"Email: {email}")
    print(f"File: {file.filename}\n")
    
    result = await login_user(file, email)
    if "error" in result:
        return JSONResponse(status_code=400, content=result)

    # 🔥 THIS IS THE FINAL PIECE YOU WERE MISSING 🔥
    return {
        "message": result["message"],
        "name": result["name"],   # ✅ Send name
        "email": email             # ✅ Send email
    }
