import requests
from fastapi import APIRouter, HTTPException
from auth.credentials import open_api_credentials

apikey=open_api_credentials["key"]

OPENROUTER_URL = "https://openrouter.ai/api/v1/chat/completions"

router = APIRouter(
    tags=["chatgpt"],
    # dependencies=[Depends(jwt.JWTBearer())],
    responses={404: {"description": "Error in calling chatgpt API"}},
)

@router.get('/api/chatgpt/')
async def getresponse_chatgpt(content, role="user"):
    try:
        response = requests.post(
            OPENROUTER_URL,
            headers={"Authorization": f"Bearer {apikey}"},
            json={
                "model": "openai/gpt-oss-120b",
                "messages": [{"role": role, "content": content}],
                "max_tokens": 1024,
                "temperature": 0.8,
            },
        )
        response.raise_for_status()
    except requests.RequestException as e:
        raise HTTPException(status_code=502, detail=f"Error calling ChatGPT API: {str(e)}")

    return response.json()["choices"][0]["message"]["content"]
