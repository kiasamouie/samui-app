import strawberry
import uvicorn
from datetime import datetime, timedelta, timezone
from fastapi import FastAPI, status, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from Model.user import User
from Service.user import UserService
from schema import Token
from typing import Annotated
from config import DatabaseSession

from Graphql.query import Query
from Graphql.mutation import Mutation

from strawberry.fastapi import GraphQLRouter

db = DatabaseSession()

app = FastAPI(
    title="Samui Dashboard",
    description="An API for all of our music related applications",
    version="0.0.1"
)

@app.post("/token")
async def login_for_access_token(form_data: Annotated[OAuth2PasswordRequestForm, Depends()]) -> Token:
    user = await UserService.authenticate_user(form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(hours=UserService.ACCESS_TOKEN_EXPIRE_HOURS)
    token_expires_at = (datetime.now() + access_token_expires).strftime('%Y/%m/%d %H:%M:%S')
    access_token = UserService.create_access_token(data={"sub": user.username}, expires_delta=access_token_expires)
    return Token(access_token=access_token, token_type="bearer", token_expires_at=token_expires_at)

@app.get("/users/me/", response_model=User)
async def read_users_me(current_user: Annotated[User, Depends(UserService.get_current_active_user)]):
    return current_user

@app.get("/users/me/items/")
async def read_own_items(current_user: Annotated[User, Depends(UserService.get_current_active_user)]):
    return [{"item_id": "Foo", "owner": current_user.username}]

@app.on_event("startup")
async def startup():
    await db.create_all()

@app.on_event("shutdown")
async def shutdown():
    await db.close()

@app.get('/')
def home():
    return "<h1>welcome home!</h1>"

# add graphql endpoint
schema = strawberry.Schema(query=Query, mutation=Mutation)
graphql_app = GraphQLRouter(schema)

app.include_router(graphql_app, prefix="/graphql")

if __name__ == '__main__':
    uvicorn.run("main:app", host="localhost", port=8888, reload=True)
