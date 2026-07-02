from pydantic import BaseModel, EmailStr
from typing import Optional, List
from datetime import datetime

# ---------- User Models ----------
class UserCreate(BaseModel):
    username: str
    email: EmailStr
    password: str

class UserOut(BaseModel):
    username: str
    email: EmailStr

class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"

# ---------- Chat Models ----------
class Message(BaseModel):
    role: str
    content: str

class ChatIn(BaseModel):
    title: str
    messages: List[Message]

class ChatOut(BaseModel):
    id: str
    title: str
    messages: List[Message]
    summary: Optional[str] = None
    created_at: datetime