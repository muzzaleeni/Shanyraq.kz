from datetime import datetime

from bson.objectid import ObjectId
from pymongo.database import Database

from ..utils.security import hash_password


class AuthRepository:
    def __init__(self, database: Database):
        self.database = database

    def create_user(self, user: dict):
        payload = {
            "email": user["email"],
            "password": hash_password(user["password"]),
            "created_at": datetime.utcnow(),
            "name": "NA",
            "phone": "NA",
            "city": "NA",
        }

        self.database["users"].insert_one(payload)

    def get_user_by_id(self, user_id: str) -> dict | None:
        user = self.database["users"].find_one(
            {
                "_id": ObjectId(user_id),
            }
        )
        return user

    def get_user_by_email(self, email: str) -> dict | None:
        user = self.database["users"].find_one(
            {
                "email": email,
            }
        )
        return user

    def update_user(self, user: dict):
        self.database["users"].update_one(
            {"_id": ObjectId(user["_id"])},
            {"$set": user}
        )

    def add_tweet_to_favorites(self, user_id: str, tweet_id: str):
        user_id_object = ObjectId(user_id)
        self.database["users"].update_one(
            {"_id": user_id_object},
            {"$addToSet": {"favorites": tweet_id}},
            upsert=True
        )

    def get_favorite_tweet_ids(self, user_id: str):
        user = self.database["users"].find_one({"_id": ObjectId(user_id)})
        if user and "favorites" in user:
            tweet_ids = user.get("favorites", [])  # Use .get() to handle missing key gracefully
            return tweet_ids
        else:
            return []
