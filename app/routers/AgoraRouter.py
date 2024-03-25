from fastapi import APIRouter, Body, status
from app.utils import TypeUtilities as typeUtilities
from app.services import AgoraService as agoraService
from fastapi.responses import JSONResponse

agoraRouter = APIRouter(prefix="/agora")


@agoraRouter.post("/generate-rtc-token", response_description="Token generated for agora's live functions")
def generate(payload=Body(...)):
    response = typeUtilities.parse_json(
        agoraService.generate_rtc_token(channel_name=payload["channel_name"], user_uid=payload["user_uid"]))
    return JSONResponse(status_code=status.HTTP_201_CREATED, content=response)


@agoraRouter.post("/generate-app-token", response_description="Token generated for agora's chat api")
def generate():
    response = typeUtilities.parse_json(
        agoraService.generate_app_token())
    return JSONResponse(status_code=status.HTTP_201_CREATED, content=response)


@agoraRouter.post("/generate-chat-token", response_description="Token generated for agora's live chat functions")
def generate(payload=Body(...)):
    response = typeUtilities.parse_json(
        agoraService.generate_chat_token(user_id=payload["user_id"]))
    return JSONResponse(status_code=status.HTTP_201_CREATED, content=response)
