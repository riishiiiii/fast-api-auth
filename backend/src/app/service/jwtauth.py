from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from fastapi import Request, HTTPException, Depends
import jwt
import os
import dotenv
import time
import datetime
from passlib.hash import bcrypt
from models import models
from schema.user import UserLogin, UserFields
from sqlalchemy.orm import Session

from models.db import get_db

# dotenv.load_dotenv(dotenv.find_dotenv(".env"))
dotenv.load_dotenv()

JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY")


class JWTBearerSecurity(HTTPBearer):
    def __init__(self, auto_error: bool = True, permission: list = []) -> None:
        self.permission = permission
        super(JWTBearerSecurity, self).__init__(auto_error=auto_error)

    async def __call__(self, request: Request, db: Session = Depends(get_db)):
        credentials: HTTPAuthorizationCredentials = await super(
            JWTBearerSecurity, self
        ).__call__(request)

        if not credentials and self.auto_error:
            raise HTTPException(
                status_code=403, detail="Invalid authorization code."
            )

        if credentials:
            if not credentials.scheme == "Bearer":
                raise HTTPException(
                    status_code=403, detail="Invalid authentication scheme."
                )

            try:
                jwt_payload = jwt.decode(
                    credentials.credentials,
                    JWT_SECRET_KEY,
                    algorithms=["HS256"],
                )

            except jwt.ExpiredSignatureError:
                raise HTTPException(
                    status_code=403, detail="Token has expired."
                )

            except jwt.InvalidTokenError:
                raise HTTPException(status_code=403, detail="Invalid token.")

            return jwt_payload

        return credentials.credentials
    

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
