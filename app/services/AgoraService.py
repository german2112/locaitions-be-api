from dotenv import load_dotenv
from fastapi import HTTPException
from app.lib.AgoraDynamicKey.python3.src.RtcTokenBuilder2 import RtcTokenBuilder
from app.lib.AgoraDynamicKey.python3.src.ChatTokenBuilder2 import ChatTokenBuilder
import time
import os

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
