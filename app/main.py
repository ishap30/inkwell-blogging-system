from fastapi import FastAPI
from app.routers import users, chats

app = FastAPI(title="Inkwell API", description="Chat summarization backend")

app.include_router(users.router, prefix="/users", tags=["users"])
app.include_router(chats.router, prefix="/chats", tags=["chats"])

@app.get("/")
async def root():
    return {"message": "Welcome to Inkwell API"}