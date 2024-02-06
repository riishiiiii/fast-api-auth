from fastapi import APIRouter, Depends
from service.auth_service import AuthService
from service.user_service import UserService
from schema.user import UserCreate, UserLogin
from service.jwtauth import JWTBearerSecurity

router = APIRouter()


@router.post("/register")
async def register(user: UserCreate, service : AuthService = Depends(AuthService)):
    return await service.register_user(user = user)

@router.post("/login")
async def login(user: UserLogin, service: AuthService = Depends(AuthService)):
    return await service.login_user(user=user)


@router.get("/me",  dependencies=[Depends(JWTBearerSecurity())])
async def me(service: UserService = Depends(UserService)):
    return await service.get_user()