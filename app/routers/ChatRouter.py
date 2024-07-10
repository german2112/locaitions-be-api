from fastapi import APIRouter, Body, status
from app.services import ChatService as chatService
from fastapi.responses import JSONResponse
from app.utils.ResponseUtils import *

chatRouter = APIRouter(prefix="/chat")


@chatRouter.post("/chatroomId", response_description="Get or generate chatroom Id of a specific client")
async def generate(payload=Body(...)):
    response = await chatService.create_chatroom(agoraUser=payload['agoraChatUser'])
    return JSONResponse(status_code=status.HTTP_200_OK, content=get_successful_response(response))

