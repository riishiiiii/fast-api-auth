from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from fastapi import Request, HTTPException
import jwt
import os
import dotenv
import time
import datetime
from passlib.hash import bcrypt
from models import models
from schema.user import UserLogin, UserFields
from sqlalchemy.orm import Session

# dotenv.load_dotenv(dotenv.find_dotenv(".env"))
dotenv.load_dotenv()

JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY")


class JWTBearer(HTTPBearer):
    def __init__(self, auto_error: bool = True):
        super(JWTBearer, self).__init__(auto_error=auto_error)

    async def __call__(self, request: Request):
        credentials: HTTPAuthorizationCredentials = await super(
            JWTBearer, self
        ).__call__(request)
        if credentials:
            if not credentials.scheme == "Bearer":
                raise HTTPException(
                    status_code=403, detail="Invalid authentication scheme."
                )

            if not self.verify_jwt(credentials.credentials):
                raise HTTPException(
                    status_code=403, detail="Invalid token or expired token."
                )
            return credentials.credentials
        else:
            raise HTTPException(status_code=403, detail="Invalid authorization code.")

    def verify_jwt(self, jwt_token: str) -> bool:
        try:
            payload = self.decode_jwt(jwt_token)
        except:
            payload = None

        if payload:
            is_token_valid = True
        else:
            is_token_valid = False

        return is_token_valid

    def decode_jwt(self, token: str) -> dict:
        try:
            decoded_token = jwt.decode(token, JWT_SECRET_KEY, "HS256")
            return decoded_token if decoded_token["exp"] >= time.time() else None
        except:
            return {}

    async def get_jwt_payload(self, request: Request) -> dict:
        credentials: HTTPAuthorizationCredentials = await self.__call__(request)
        if credentials:
            return self.decode_jwt(credentials)
        else:
            return {}


def validate_user(db: Session, user: UserLogin):
    existing_user = (
        db.query(models.User)
        .filter(models.User.user_name == user.dict()[UserFields.USER_NAME.value])
        .first()
    )
    if existing_user is None:
        raise HTTPException(
            status_code=401, detail="User with this username does not exist"
        )

    if _verify_password(user.password, existing_user.password):
        _access_token = jwt.encode(
            {
                "user_id": str(existing_user.user_id),
                "exp": datetime.datetime.utcnow() + datetime.timedelta(days=60),
                "iat": datetime.datetime.utcnow(),
            },
            JWT_SECRET_KEY.encode(),
            algorithm="HS256",
        )
        _refresh_token = jwt.encode(
            {
                "user_id": str(existing_user.user_id),
                "exp": datetime.datetime.utcnow() + datetime.timedelta(days=90),
                "iat": datetime.datetime.utcnow(),
            },
            JWT_SECRET_KEY.encode(),
            algorithm="HS256",
        )

        return {"access_token": _access_token, "refresh_token": _refresh_token}
    else:
        raise HTTPException(401, detail="Wrong credentials!")


def _verify_password(plain_password, hashed_password):
    return bcrypt.verify(plain_password, hashed_password)
