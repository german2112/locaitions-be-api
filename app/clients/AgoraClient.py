import httpx
from app.exceptions.InternalServerError import InternalServerError
from app.helpers.AgoraHelper import generate_app_token

async def create_chatroom(agoraUser: str):
    CREATE_CHATROOM_URL = "http://a41.chat.agora.io/411114815/1299148/chatrooms"
    try:
        token = generate_app_token()
        async with httpx.AsyncClient() as client:
            payload = {
                'name': '',
                'owner': agoraUser,
            }
            headers = {
                'Authorization': f'Bearer {token}'
            }
            response = await client.post(CREATE_CHATROOM_URL, json=payload, headers=headers)
            response.raise_for_status()
            return response.json()
    except Exception as e:
        raise InternalServerError("Error while creating chatroom: " + str(e))
    