from Model.user import User
from Repository.user import UserRepository
from schema import UserInput, UserType, TokenData

from fastapi import FastAPI, status, Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm

from datetime import datetime, timedelta, timezone
from jose import JWTError, jwt

from passlib.context import CryptContext

from typing import Annotated

class UserService:

    pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
    SECRET_KEY = "872cbabb3e7ef5ce4c66ea1f8d6ddcbec72b00ee319713a3fbc23b13b6977b21"
    ALGORITHM = "HS256"
    ACCESS_TOKEN_EXPIRE_HOURS = 24


    @staticmethod
    async def get_all_users():
        users = await UserRepository.get_all()
        return [UserType(id=user.id,email=user.email, full_name=user.full_name, username=user.username) for user in users]

    @staticmethod
    async def get_by_id(id: int):
        user = await UserRepository.get_by_id(id)
        return UserType(id=user.id,email=user.email, full_name=user.full_name, username=user.username)
    
    @staticmethod
    async def add_user(user_data: UserInput):
        user = User()
        user.full_name = user_data.full_name
        user.email = user_data.email
        user.username = user_data.username
        user.hashed_password = UserService.get_password_hash(user_data.password)
        await UserRepository.create(user)
        return UserType(id=user.id,email=user.email, full_name=user.full_name, username=user.username)

    @staticmethod
    async def update(id:int, user_data: UserInput):
        user = User()
        user.full_name = user_data.full_name
        user.email = user_data.email
        user.username = user_data.username
        await UserRepository.update(id,user)
        return f'Successfully updated data by id {id}'
    
    @staticmethod
    async def delete(id: int):
        await UserRepository.delete(id)
        return f'Successfully deleted data by id {id}'
        
    @staticmethod
    def verify_password(plain_password, hashed_password):
        return UserService.pwd_context.verify(plain_password, hashed_password)
    
    @staticmethod
    def get_password_hash(password):
        return UserService.pwd_context.hash(password)
        
    @staticmethod
    async def authenticate_user(username: str, password: str):
        user = await UserRepository.get_by_username(username)
        if not user:
            return False
        if not UserService.verify_password(password, user.hashed_password):
            return False
        return user
    
    @staticmethod
    def create_access_token(data: dict, expires_delta: timedelta | None = None):
        to_encode = data.copy()
        if expires_delta:
            expire = datetime.now(timezone.utc) + expires_delta
        else:
            expire = datetime.now(timezone.utc) + timedelta(minutes=15)
        to_encode.update({"exp": expire})
        encoded_jwt = jwt.encode(to_encode, UserService.SECRET_KEY, algorithm=UserService.ALGORITHM)
        return encoded_jwt
    
    @staticmethod
    async def get_current_user(token: Annotated[str, Depends(OAuth2PasswordBearer(tokenUrl="token"))]):
        credentials_exception = HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
        try:
            payload = jwt.decode(token, UserService.SECRET_KEY, algorithms=[UserService.ALGORITHM])
            username: str = payload.get("sub")
            if username is None:
                raise credentials_exception
            token_data = TokenData(username=username)
        except JWTError:
            raise credentials_exception
        user = await UserRepository.get_by_username(username)
        if user is None:
            raise credentials_exception
        return user
    
    @staticmethod
    async def get_current_active_user(current_user: Annotated[User, Depends(get_current_user)]):
        current_user = await current_user
        if current_user.disabled:
            raise HTTPException(status_code=400, detail="Inactive user")
        return current_user