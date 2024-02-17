from fastapi import Security, status
from fastapi.exceptions import HTTPException
from fastapi.security import HTTPBearer

from todo import models

security = HTTPBearer()


def get_user(auth: str = Security(security)) -> models.User:
    try:
        return models.User.objects.get(keys__key=auth.credentials)
    except models.Key.DoesNotExist:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or missing API key.",
        )
