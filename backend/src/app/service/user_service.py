from sqlalchemy.orm import Session
from fastapi import Depends
from models.db import get_db
from service.jwtauth import JWTBearerSecurity   
from models import models 

class UserService:
    def __init__(
        self,
        db: Session = Depends(get_db),
        user_payload: dict = Depends(JWTBearerSecurity()),
    ) -> None:
        self.db = db
        self.user_id = user_payload["user_id"]

    async def get_user(self):
        user = self.db.query(models.User).filter_by(user_id=self.user_id).first()
        if user is None:
            return None
        return {"user_name":user.user_name}