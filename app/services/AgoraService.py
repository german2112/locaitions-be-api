from fastapi import HTTPException
from dotenv import load_dotenv
from app.lib.AgoraDynamicKey.python3.src.RtcTokenBuilder2 import RtcTokenBuilder
from app.lib.AgoraDynamicKey.python3.src.ChatTokenBuilder2 import ChatTokenBuilder
from app.lib.AgoraDynamicKey.python3.src.AccessToken2 import AccessToken, ServiceChat
import os
import time

load_dotenv()

def generate_rtc_token(channelName: str, agoraLiveVideoUser: int, role: int):
    appId = os.getenv("AGORA_APP_ID")
    primaryCertificate = os.getenv("AGORA_PRIMARY_CERITIFICATE")
    expirationTimeInSeconds = 3600
    currentTime = int(time.time())
    privilegeExpiration = currentTime + expirationTimeInSeconds
    try:
        token = RtcTokenBuilder.build_token_with_uid(app_id=appId, app_certificate=primaryCertificate,
                                                  channel_name=channelName, uid=agoraLiveVideoUser, role=role, token_expire= 600, privilege_expire=privilegeExpiration)
        return {
            'token': token
        }
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
