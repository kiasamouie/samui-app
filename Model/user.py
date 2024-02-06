from sqlmodel import SQLModel, Field
from typing import Optional, Union
from datetime import datetime
from sqlalchemy import Column, DateTime
from sqlalchemy.sql import func


class User(SQLModel, table=True):
    __tablename__ = "users"

    id: Optional[int] = Field(default=None, primary_key=True)
    username: str = Field(index=True, nullable=False)
    email: Union[str, None] = Field(default=None, index=True, nullable=True)
    full_name: Union[str, None] = Field(default=None, nullable=True)
    hashed_password: str = Field(nullable=False)
    disabled: Union[bool, None] = Field(default=False, nullable=True)
    created_at: datetime = Field(default_factory=func.now, sa_column=Column(nullable=False))
    updated_at: datetime = Field(default=None, sa_column=Column(onupdate=func.now))
