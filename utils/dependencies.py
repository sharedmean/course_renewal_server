from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from utils import users as user_utils

import config

oauth2_scheme = OAuth2PasswordBearer(tokenUrl=f'{config.USERS_PREFIX}/auth')

async def get_current_user(token: str = Depends(oauth2_scheme)):

    user = await user_utils.get_user_by_token(token)

    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Неверные учётные данные",
            headers = {"WWW-Authenticate": "Bearer"}
        )

    return {**user}