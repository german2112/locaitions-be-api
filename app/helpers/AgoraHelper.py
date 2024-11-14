from app.lib.AgoraDynamicKey.python3.src.AccessToken2 import AccessToken, ServiceChat
from app.exceptions.InternalServerError import InternalServerError
import os
import time

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
        return token.build()
    except Exception as e:
        raise InternalServerError("Error while getting app token: " + str(e))