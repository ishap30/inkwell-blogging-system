from fastapi import APIRouter, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from fastapi import Depends
from app.database import db
from app.models import UserCreate, UserOut, Token
from app.auth import hash_password, verify_password, create_access_token

router = APIRouter()

@router.post("/register", response_model=UserOut)
async def register(user: UserCreate):
    existing = await db["users"].find_one({"username": user.username})
    if existing:
        raise HTTPException(status_code=400, detail="Username already taken")

    hashed_pw = hash_password(user.password)
    new_user = {
        "username": user.username,
        "email": user.email,
        "password": hashed_pw
    }
    await db["users"].insert_one(new_user)
    return UserOut(username=user.username, email=user.email)


@router.post("/login", response_model=Token)
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    user = await db["users"].find_one({"username": form_data.username})
    if not user or not verify_password(form_data.password, user["password"]):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password"
        )

    access_token = create_access_token(data={"sub": user["username"]})
    return Token(access_token=access_token)