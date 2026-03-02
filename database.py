import motor.motor_asyncio
from config import Config

class Database:
    def __init__(self, uri, database_name):
        # MongoDB Atlas se connect karne ke liye client setup
        self._client = motor.motor_asyncio.AsyncIOMotorClient(uri)
        self.db = self._client[database_name]
        self.col = self.db.users # Users collection ka naam

    # --- 🆕 New User Check & Add ---
    def new_user(self, id):
        return dict(
            id=id,
            join_date=None # Aap chahein toh date bhi add kar sakte hain
        )

    async def add_user(self, id):
        user = self.new_user(id)
        # Agar user pehle se DB mein nahi hai, toh insert karein
        if not await self.is_user_exist(id):
            await self.col.insert_one(user)

    async def is_user_exist(self, id):
        user = await self.col.find_one({'id': int(id)})
        return True if user else False

    # --- 📊 Stats & Broadcast Helpers ---
    async def total_users_count(self):
        count = await self.col.count_documents({})
        return count

    async def get_all_users(self):
        # Saare users ki list nikalne ke liye (for broadcast)
        all_users = self.col.find({})
        return all_users

    async def delete_user(self, user_id):
        # Agar koi bot ko block karde toh use DB se hatane ke liye
        await self.col.delete_many({'id': int(user_id)})

# Database Instance Create Karein
db = Database(Config.DB_URL, "FileStoreBotV2")
