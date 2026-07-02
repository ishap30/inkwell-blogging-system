import asyncio
from app.database import db

async def test():
    collections = await db.list_collection_names()
    print("Connected! Collections:", collections)

asyncio.run(test())