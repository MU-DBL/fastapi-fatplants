import openai
from fastapi import APIRouter
from auth.credentials import open_api_credentials


apikey=open_api_credentials["key"]
openai.api_key = apikey

router = APIRouter(
    tags=["kegg_pathway"],
    # dependencies=[Depends(jwt.JWTBearer())],
    responses={404: {"description": "Error in calling kegg pathway API"}},
)

@router.get('/chatgpt/')
async def getresponse_chatgpt(content,role="user"):
    
    completion = openai.ChatCompletion.create(
    model="gpt-3.5-turbo",
    messages = [{"role": role, "content": content}],
    max_tokens = 1024,
    temperature = 0.8)

    return completion
    

