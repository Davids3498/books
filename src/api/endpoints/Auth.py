from datetime import datetime, timedelta
from fastapi import APIRouter, Depends, status
from fastapi.responses import JSONResponse
from src.models.User import UserBooksModel, UserCreateModel, UserModel, UserLoginModel
from src.services.UserService import UserService
from src.db.database import get_session
from sqlmodel.ext.asyncio.session import AsyncSession
from fastapi.exceptions import HTTPException
from src.utils.Utils import create_access_token, verify_password
from src.api.dependencies.dependency import RefreshTokenBearer, AccessTokenBearer, RoleChecker
from src.db.redis import add_jti_to_block_list
from src.api.dependencies.dependency import get_current_user

auth_router = APIRouter(tags=["user"])
user_service = UserService()
role_checker = RoleChecker(["admin","user"])

REFRESH_TOKEN_EXPIERY = 2


@auth_router.post('/signup', response_model=UserModel, status_code=status.HTTP_201_CREATED)
async def sign_up(user_data: UserCreateModel, session: AsyncSession = Depends(get_session)):
    email = user_data.email

    is_user_exists = await user_service.is_email_exist(email, session)
    if is_user_exists:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="Email exists.")

    new_user = await user_service.create_user(user_data, session)

    return new_user


@auth_router.post('/login', response_model=UserModel)
async def login_up(login_data: UserLoginModel, session: AsyncSession = Depends(get_session)):
    email = login_data.email
    password = login_data.password

    user = await user_service.get_user_by_email(email, session)
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="No such user.")

    password_valid = verify_password(password, user.password_hash)
    if not password_valid:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="Password is incorrect.")

    access_token = create_access_token(
        user_data={'email': user.email, 'user_uid': str(user.uid), "role": user.role})

    refresh_token = create_access_token(
        user_data={'email': user.email, 'user_uid': str(
            user.uid), "role": user.role},
        expiry=timedelta(days=REFRESH_TOKEN_EXPIERY), refresh=True)

    return JSONResponse(content={
        "message": "Login successfull",
        "access_token": access_token,
        "refresh_token": refresh_token,
        "user": {'email': user.email, 'uid': str(user.uid)}
    })


@auth_router.get("/refresh")
async def get_new_access_token(token_details: dict = Depends(RefreshTokenBearer())):
    expire_time_stamp = token_details['exp']

    if datetime.fromtimestamp(expire_time_stamp) > datetime.now():
        new_access_token = create_access_token(user_data=token_details['user'])

        return JSONResponse(content={"access_token": new_access_token})

    raise HTTPException(status.HTTP_400_BAD_REQUEST)


@auth_router.get("/logout")
async def logout(token_details: dict = Depends(AccessTokenBearer())):
    jti = token_details['jti']
    await add_jti_to_block_list(jti)
    return JSONResponse(content={
        "message": "Logged out."
    }, status_code=status.HTTP_200_OK)


@auth_router.get("/me",response_model=UserBooksModel)
async def get_current_user(user=Depends(get_current_user), _: bool = Depends(role_checker)):
    return user
