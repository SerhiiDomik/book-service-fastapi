from fastapi import APIRouter

router = APIRouter()

@router.post("/register")
def register():
    return {"message": "User registered"}

@router.post("/login")
def login():
    return {"message": "User logged in"}
