from fastapi import Depends
from models.db import get_db
from sqlalchemy.orm import Session
from models import models
import uuid
import datetime
from fastapi import HTTPException, status
from sqlalchemy.exc import IntegrityError
from passlib.hash import bcrypt
import jwt
import os
import dotenv
from .jwtauth import validate_user

from schema.user import UserCreate, UserFields, UserLogin
from service.jwtauth import JWTBearerSecurity

dotenv.load_dotenv(dotenv.find_dotenv(".env"))


class AuthService:
    def __init__(self, db: Session = Depends(get_db)):
        self.db = db
        self.JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY")
      


    async def register_user(self, user: UserCreate):
        try:
            user_dict = self._create_user_create_dict(user=user)
            user = models.User(**user_dict)
            self.db.add(user)
            self.db.commit()
            return user_dict
        except IntegrityError as e:
            self.db.rollback()
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="User with this value already exists. Please provide unique values.",
            )
        except Exception as e:
            self.db.rollback()
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="An error occurred while registering the user.",
            )

    def _create_user_create_dict(self, user: UserCreate):
        user_dict = user.dict(exclude_unset=True)
        user_id = uuid.uuid4()
        user_dict[UserFields.PASSWORD.value] = bcrypt.hash(
            user_dict[UserFields.PASSWORD.value]
        )
        user_dict[UserFields.USER_ID.value] = user_id
        user_dict[UserFields.SIGN_UP_DATE.value] = datetime.datetime.today().date()

        return user_dict


    async def login_user(self, user: UserLogin):
        return validate_user(self.db, user)


    async def get_user(self):
        user = self.db.query(models.User).filter(models.User.user_id == self.user_id).first()
        if user is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found",
            )
        return user.user_name