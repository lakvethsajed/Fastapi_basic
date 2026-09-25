from pydantic import BaseModel,EmailStr, Field ,field_validator
from typing import Optional
from datetime import datetime
class BookBase(BaseModel):
    title : str
    author : str
    genre : str
    available : bool = True 
    description : Optional[str] = None 
    total_copies : int = 1
    available_copies : int = 1

class Addbook(BookBase):
    pass

class BookResponse(BookBase):
    id : int
    created_at : datetime
    class config:
        orm_mode = True

class Registeruser(BaseModel):
    name : str
    username : str
    email : EmailStr
    password : str = Field(max_length=72)

    @field_validator("username")
    def validate_username(cls, value):
        if not value.replace("_", "").isalnum():
            raise ValueError("Username can contain only letters, numbers and underscore")
        if len(value) < 3:
            raise ValueError("Username must contain at least 3 characters")
        if len(value) > 20:
            raise ValueError("Username must not exceed 20 characters")
        return value

    @field_validator("password")
    def validate_password(cls, value):
        if len(value) < 8:
            raise ValueError("Password must contain at least 8 characters")
        if not any(char.isupper() for char in value):
            raise ValueError("Password must contain at least one uppercase letter")
        if not any(char.islower() for char in value):
            raise ValueError("Password must contain at least one lowercase letter")
        if not any(char.isdigit() for char in value):
            raise ValueError("Password must contain at least one number")
        if not any(not char.isalnum() for char in value):
            raise ValueError("Password must contain at least one special character")
        return value

class responseuser(BaseModel):
    name : str
    username : str
    email : EmailStr


    class config:
        orm_mode = True

class loginuser(BaseModel):
    username : str
    password: str

class Token_valid(BaseModel):
    access_token : str
    token_type : str

class Tokendata(BaseModel):
    id : int

class Issuebooks(BaseModel):
    book_id : int

class ResponseBook(BaseModel):
    id : int
    book_id : int
    user_id : int
    issued_at : datetime
    due_date : datetime
    returned_at : Optional[datetime] = None

    class config:
        orm_mode = True

class MyBookResponse(BaseModel):

    issue_id: int

    user_id: int
    user_name: str

    book_id: int
    book_name: str

    issued_at: datetime
    due_date: datetime

    returned_at: Optional[datetime] = None