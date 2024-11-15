from datetime import datetime, timedelta
import uuid
from passlib.context import CryptContext
import jwt
import logging

from src.config import Config
password_context = CryptContext(schemes=['bcrypt'])
ACCESS_TOKEN_EXPIRY = 3600


def generate_password_hash(password: str) -> str:
    hash = password_context.hash(password)
    return hash


def verify_password(password: str, hash: str) -> bool:
    return password_context.verify(password, hash)


def create_access_token(user_data: dict, expiry: timedelta = None, refresh: bool = False):
    payload = {}

    payload["user"] = user_data
    payload["exp"] = datetime.now() + (
        expiry if expiry is not None else timedelta(
            seconds=ACCESS_TOKEN_EXPIRY)
    )
    payload["jti"] = str(uuid.uuid4())

    payload['refresh'] = refresh

    token = jwt.encode(
        payload=payload, key=Config.JWT_SECRET, algorithm=Config.JWT_ALGORITHM
    )

    return token


def decode_token(token: str) -> dict:
    print(token)
    try:
        token_data = jwt.decode(
            jwt=token, key=Config.JWT_SECRET, algorithms=[Config.JWT_ALGORITHM]
        )
        return token_data

    except jwt.ExpiredSignatureError:
        logging.exception("111111 Token has expired")
        return None

    except jwt.DecodeError:
        logging.exception("111111 Invalid token")
        return None

    except jwt.PyJWKError as e:
        logging.exception("111111 JWK error occurred during token decoding")
        return None

    except Exception as e:
        logging.exception(f"111111 Unexpected error: {str(e)}")
        return None