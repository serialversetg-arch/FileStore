import motor.motor_asyncio
from config import Config

class Database:
    def __init__(self, uri, database_name):
        self._client = motor.motor_asyncio.AsyncIOMotorClient(uri)
        self.db = self._client[database_name]
        self.col = self.db.users

    async def add_user(self, id):
        if not await self.col.find_one({'id': id}):
            await self.col.insert_one({'id': id})

    async def get_all_users(self):
        return self.col.find({})

    async def total_users_count(self):
        return await self.col.count_documents({})

db = Database(Config.DB_URL, "FileStoreBot")
