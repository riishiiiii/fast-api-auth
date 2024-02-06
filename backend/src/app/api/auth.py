from fastapi import APIRouter, Depends
from service.user_service import UserService
from schema.user import UserCreate, UserLogin


router = APIRouter()


@router.post("/register")
async def register(user: UserCreate, service : UserService = Depends(UserService)):
    return await service.register_user(user = user)

@router.post("/login")
async def login(user: UserLogin, service: UserService = Depends(UserService)):
    return await service.login_user(user=user)