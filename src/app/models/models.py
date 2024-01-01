import uuid
from sqlalchemy import Column, String, DateTime
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class User(Base):
    __tablename__ = "user"

    user_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4())
    user_name = Column(String(255), unique=True)
    email = Column(String(255), unique=True)
    password = Column(String(255))
    sign_up_date = Column(DateTime)