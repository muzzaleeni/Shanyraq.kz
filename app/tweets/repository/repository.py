from datetime import datetime
from typing import List

from bson.objectid import ObjectId
from pymongo.database import Database


class TweetRepository:
    def __init__(self, database: Database):
        self.database = database

    def create_tweet(self, tweet_data: dict) -> str:
        payload = {
            "type": tweet_data["type"],
            "price": tweet_data["price"],
            "address": tweet_data["address"],
            "area": tweet_data["area"],
            "rooms_count": tweet_data["rooms_count"],
            "description": tweet_data["description"],
            "created_at": datetime.utcnow(),
        }

        result = self.database["tweets"].insert_one(payload)
        tweet_id = str(result.inserted_id)
        return tweet_id

    def get_tweet_by_id(self, tweet_id: str) -> dict:
        tweet = self.database["tweets"].find_one({"_id": ObjectId(tweet_id)})
        return tweet

    def update_tweet(self, tweet_id: str, updated_data: dict) -> bool:
        updated_data["updated_at"] = datetime.utcnow()
        result = self.database["tweets"].update_one(
            {"_id": ObjectId(tweet_id)}, {"$set": updated_data})
        return result.modified_count > 0

    def delete_tweet(self, tweet_id: str) -> bool:
        result = self.database["tweets"].delete_one(
            {"_id": ObjectId(tweet_id)})
        return result.deleted_count > 0

    def get_tweet_by_user_id(self, user_id: str) -> List[dict]:
        tweets = self.database["tweets"].find(
            {
                "user_id": ObjectId(user_id),
            }
        )
        result = []
        for tweet in tweets:
            result.append(tweet)

        return result
