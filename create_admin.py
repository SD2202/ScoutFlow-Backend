import asyncio
from motor.motor_asyncio import AsyncIOMotorClient
from app.core.config import settings

async def create_admin():
    print("⏳ Connecting to MongoDB Atlas...")
    client = AsyncIOMotorClient(settings.MONGODB_URL)
    db = client[settings.DATABASE_NAME]
    
    # Define your admin user
    admin_user = {
        "username": "sparsh",
        "password": "SSD",  # Note: In production you should hash this!
        "name": "Sparsh Dwivedi",
        "role": "admin"
    }
    
    # Check if user already exists
    existing = await db.users.find_one({"username": admin_user["username"]})
    if existing:
        print(f"✅ User '{admin_user['username']}' already exists in the cloud!")
    else:
        result = await db.users.insert_one(admin_user)
        print(f"🚀 Successfully created user '{admin_user['username']}' with ID: {result.inserted_id}")
    
    client.close()

if __name__ == "__main__":
    asyncio.run(create_admin())
