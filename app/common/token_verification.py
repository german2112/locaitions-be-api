from fastapi import Depends, HTTPException, status, Request
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from firebase_admin import auth
import asyncio

security = HTTPBearer()


async def verify_firebase_token(credentials: HTTPAuthorizationCredentials = Depends(security)):
    token = credentials.credentials
    try:
        loop = asyncio.get_event_loop()
        decoded = await loop.run_in_executor(None, auth.verify_id_token, token)
        return decoded
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail="Invalid authentication credentials")
