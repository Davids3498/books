from abc import ABC, abstractmethod
from typing import Any, List
from fastapi import Depends, HTTPException, Request, status
from fastapi.security import HTTPBearer
from fastapi.security.http import HTTPAuthorizationCredentials
from sqlmodel.ext.asyncio.session import AsyncSession
from src.db.database import get_session
from src.db.models.User import User
from src.services.UserService import UserService
from src.utils.Utils import decode_token
from src.db.redis import is_token_in_block_list

user_service = UserService()


class TokenBearer(HTTPBearer, ABC):
    def __init__(self, auto_error=True):
        super().__init__(auto_error=auto_error)

    async def __call__(self, request: Request) -> HTTPAuthorizationCredentials | None:
        creds = await super().__call__(request)

        token = creds.credentials

        if not self._is_token_valid(token):
            raise HTTPException(status.HTTP_403_FORBIDDEN)

        token_data = decode_token(token)

        if await is_token_in_block_list(token_data['jti']):
            raise HTTPException(status.HTTP_403_FORBIDDEN)

        self.verify_token_data(token_data)

        return token_data

    def _is_token_valid(self, token: str) -> bool:
        return decode_token(token) != None

    @abstractmethod
    def verify_token_data(self, token_data: dict) -> None:
        pass


class AccessTokenBearer(TokenBearer):
    def verify_token_data(self, token_data: dict) -> None:
        if token_data and token_data['refresh']:
            raise HTTPException(status.HTTP_403_FORBIDDEN,
                                detail='Provide a access token.')


class RefreshTokenBearer(TokenBearer):
    def verify_token_data(self, token_data: dict) -> None:
        if token_data and not token_data['refresh']:
            raise HTTPException(status.HTTP_403_FORBIDDEN,
                                detail='Provide a refresh token.')


async def get_current_user(
    token_details: dict = Depends(AccessTokenBearer()),
    session: AsyncSession = Depends(get_session),
):
    user_email = token_details["user"]["email"]

    user = await user_service.get_user_by_email(user_email, session)

    return user


class RoleChecker:
    def __init__(self, allowed_roles: List[str]) -> None:
        self.allowed_roles = allowed_roles

    def __call__(self, current_user: User = Depends(get_current_user)) -> Any:
        if current_user.role in self.allowed_roles:
            return True
        
        raise (HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="User role is not allowed."
        ))
