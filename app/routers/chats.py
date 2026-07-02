from fastapi import APIRouter, Depends, HTTPException
from bson import ObjectId
from datetime import datetime
from app.database import db
from app.models import ChatIn, ChatOut
from app.auth import get_current_user

router = APIRouter()

def simple_summarize(messages, max_sentences=2):
    """Basic placeholder summarizer - just grabs first user message content."""
    text = " ".join([m["content"] for m in messages if m["role"] == "user"])
    sentences = text.split(". ")
    return ". ".join(sentences[:max_sentences]).strip() + ("..." if len(sentences) > max_sentences else "")


@router.post("/", response_model=dict)
async def create_chat(chat: ChatIn, current_user: str = Depends(get_current_user)):
    chat_doc = {
        "title": chat.title,
        "messages": [m.dict() for m in chat.messages],
        "owner": current_user,
        "created_at": datetime.utcnow(),
        "summary": simple_summarize([m.dict() for m in chat.messages])
    }
    result = await db["chats"].insert_one(chat_doc)
    return {"id": str(result.inserted_id), "message": "Chat saved successfully"}


@router.get("/", response_model=list)
async def get_chats(current_user: str = Depends(get_current_user)):
    chats = []
    cursor = db["chats"].find({"owner": current_user})
    async for chat in cursor:
        chat["id"] = str(chat["_id"])
        del chat["_id"]
        chats.append(chat)
    return chats


@router.get("/{chat_id}", response_model=dict)
async def get_chat(chat_id: str, current_user: str = Depends(get_current_user)):
    chat = await db["chats"].find_one({"_id": ObjectId(chat_id), "owner": current_user})
    if not chat:
        raise HTTPException(status_code=404, detail="Chat not found")
    chat["id"] = str(chat["_id"])
    del chat["_id"]
    return chat


@router.get("/{chat_id}/summary", response_model=dict)
async def get_summary(chat_id: str, current_user: str = Depends(get_current_user)):
    chat = await db["chats"].find_one({"_id": ObjectId(chat_id), "owner": current_user})
    if not chat:
        raise HTTPException(status_code=404, detail="Chat not found")
    return {"chat_id": chat_id, "summary": chat.get("summary", "No summary available")}