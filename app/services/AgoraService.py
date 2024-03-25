from fastapi import HTTPException
from dotenv import load_dotenv
from agora_token_builder import RtcTokenBuilder
from app.lib.AgoraDynamicKey.python3.src.ChatTokenBuilder2 import ChatTokenBuilder
from app.lib.AgoraDynamicKey.python3.src.AccessToken2 import AccessToken, ServiceChat
import os
import time

load_dotenv()

def generate_rtc_token(channel_name: str, user_uid: str):
    app_id = os.getenv("AGORA_APP_ID")
    primary_certificate = os.getenv("AGORA_PRIMARY_CERITIFICATE")
    expiration_time_in_seconds = 3600
    current_time = int(time.time())
    privilege_expiration = current_time + expiration_time_in_seconds
    role = 1
    try:
        token = RtcTokenBuilder.buildTokenWithUid(appId=app_id, appCertificate=primary_certificate,
                                                  channelName=channel_name, uid=user_uid, role=role, privilegeExpiredTs=privilege_expiration)
        return {"message": "success", "body": token}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

def generate_app_token():
    app_id = os.getenv("AGORA_APP_ID")
    primary_certificate = os.getenv("AGORA_PRIMARY_CERITIFICATE")
    expiration_time_in_seconds = 3600
    current_time = int(time.time())
    privilege_expiration = current_time + expiration_time_in_seconds
    try:
        token = AccessToken(app_id= app_id, app_certificate=primary_certificate,expire=privilege_expiration)
        service_chat = ServiceChat()
        service_chat.add_privilege(ServiceChat.kPrivilegeApp, expire=privilege_expiration)

        token.add_service(service_chat)
        token = token.build()
        return {"message": "success", "body": token}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

def generate_chat_token(user_id: str):
    app_id = os.getenv("AGORA_APP_ID")
    primary_certificate = os.getenv("AGORA_PRIMARY_CERITIFICATE")
    expireTimeInSeconds = 3600
    currentTimestamp = int(time.time())
    expireTimestamp = currentTimestamp + (expireTimeInSeconds * 24)
    try:
        token = ChatTokenBuilder.build_user_token(
            app_id,
            primary_certificate,
            user_id,
            expireTimestamp
        )
        return {"message": "success", "body": token}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))