from typing import Optional

import aiohttp
from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer, OAuth2AuthorizationCodeBearer, OpenIdConnect

from app.core.exceptions import InactiveUserError
from .services.auth import get_user, Admin
from .utils.jwt_manager import JWTManager

# oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/token")

# client_id: 68974572259c426b7f7fa99f564fb21c
oauth2_scheme = OAuth2AuthorizationCodeBearer(
    authorizationUrl='https://kauth.kakao.com/oauth/authorize',
    tokenUrl="https://kauth.kakao.com/oauth/token")

# oauth2_scheme = OAuth2AuthorizationCodeBearer(
#     authorizationUrl='https://accounts.google.com/o/oauth2/auth',
#     tokenUrl='https://oauth2.googleapis.com/token',
#     scopes={
#         'https://www.googleapis.com/auth/userinfo.email': 'email',
#         'https://www.googleapis.com/auth/userinfo.profile': 'profile',
#         'openid': 'openid'
#     })


# oauth2_scheme = OpenIdConnect(
#     openIdConnectUrl='https://accounts.google.com/.well-known/openid-configuration')


async def get_current_user(token: str = Depends(oauth2_scheme)):
    print(token)
    user_id = JWTManager.decode_token(token)
    print(user_id)
    user = get_user(user_id)
    return user


async def get_current_active_user(current_user: Admin = Depends(get_current_user)):
    if current_user.disabled:
        raise InactiveUserError()
    return current_user


async def access_token_info(token: str = Depends(oauth2_scheme)):
    async with aiohttp.ClientSession() as session:
        url = "https://kapi.kakao.com/v1/user/access_token_info"
        headers = {'Authorization': f'Bearer {token}'}
        async with session.get(url=url, headers=headers) as resp:
            response = await resp.json()
            return response