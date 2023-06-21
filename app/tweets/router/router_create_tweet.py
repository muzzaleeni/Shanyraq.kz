from dotenv import dotenv_values
import requests
from fastapi import Depends, HTTPException
from app.auth.adapters.jwt_service import JWTData
from app.auth.router.dependencies import parse_jwt_user_data
from pydantic import BaseModel
from ..service import Service, get_service
from . import router


class CreateTweetRequest(BaseModel):
    type: str
    price: int
    address: str
    area: float
    rooms_count: int
    description: str


class CreateTweetResponse(BaseModel):
    tweet_id: str


@router.post("/", response_model=CreateTweetResponse)
def create_tweet(
        tweet_data: CreateTweetRequest,
        jwt_data: JWTData = Depends(parse_jwt_user_data),
        svc: Service = Depends(get_service)
) -> CreateTweetResponse:
    # Extract the user ID from the JWT data
    user_id = jwt_data.user_id

    # Load the environment variables from .env file
    env_vars = dotenv_values(".env")
    herecom_api_key = env_vars.get("HERE_API_KEY")

    # Construct the geocoding API request URL
    geocode_url = f"https://geocode.search.hereapi.com/v1/geocode"
    params = {
        "q": tweet_data.address,
        "apiKey": herecom_api_key
    }

    try:
        # Send the geocoding API request
        response = requests.get(geocode_url, params=params)
        response.raise_for_status()

        # Parse the API response to get the latitude and longitude
        data = response.json()
        latitude = data["items"][0]["position"]["lat"]
        longitude = data["items"][0]["position"]["lng"]
    except (requests.RequestException, KeyError, IndexError) as e:
        raise HTTPException(status_code=500, detail="Failed to retrieve latitude and longitude") from e

    # Create a new ad with the provided data
    temp_tweet_id: str = svc.repository.create_tweet(
        user_id,
        {
            "type": tweet_data.type,
            "price": tweet_data.price,
            "address": tweet_data.address,
            "area": tweet_data.area,
            "rooms_count": tweet_data.rooms_count,
            "description": tweet_data.description,
            "longitude": longitude,
            "latitude": latitude,
        },
    )

    if not temp_tweet_id:
        raise HTTPException(status_code=500, detail="Failed to create tweet")

    # Return the ID of the created ad
    return CreateTweetResponse(tweet_id=temp_tweet_id)
