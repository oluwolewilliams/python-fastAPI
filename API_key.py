from fastapi import FastAPI, HTTPException
import requests
import os

app = FastAPI()

#  Better: use environment variable instead of hardcoding
DOG_API_KEY = os.getenv("x-api-key", "live_lM2XsoNtE5Y9oSok6mgJzg466kXi1frCisyxd7WC7VEVZAw7s5zIj7zQRfvzbwSG")


def get_breed_with_auth(query: str, api_key: str):
    url = "https://api.thedogapi.com/v1/breeds/search"
    params = {"q": query}

    headers = {
        "x-api-key": api_key
    }

    response = requests.get(url, headers=headers, params=params, timeout=10)

    if response.status_code == 200:
        data = response.json()

        if data:
            weight = data[0].get("weight", {}).get("imperial", "Unknown")
            return {"breed": query, "weight": weight}

        return {"error": "Breed not found"}

    elif response.status_code == 404:
        return {"error": "Breed not found"}

    else:
        return {"error": f"API error: {response.status_code}"}


#  FastAPI endpoint
@app.get("/dog/{breed}")
def get_dog_breed(breed: str):
    result = get_breed_with_auth(breed, DOG_API_KEY)

    if "error" in result:
        raise HTTPException(status_code=404, detail=result["error"])

    return result