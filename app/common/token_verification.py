from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from firebase_admin import auth

security = HTTPBearer()


def verify_firebase_token(credentials: HTTPAuthorizationCredentials = Depends(security)):
    token = credentials.credentials
    try:
        decoded = auth.verify_id_token(id_token=token)
        return decoded
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail="Invalid authentication credentials")
