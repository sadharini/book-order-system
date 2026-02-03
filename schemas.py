from pydantic import BaseModel
from datetime import date

class UserCreate(BaseModel):
    email:str
    password:str
    method:str
class GetUserDetails(BaseModel):
    method:str

class AuthorCreate(BaseModel):
    name: str
    email: str
    password:str

class BookCreate(BaseModel):
    title: str
    author_id: int


class BookDetailsResponse(BaseModel):
    book_id: int
    title: str
    author_email: str

class LendingDetails(BaseModel):
    user_id:int
    book_id:int
    title:str
    loan_date:date

class FavouriteTheme(BaseModel):
    book_theme:str
    user_email:str

class AuthorTheme(BaseModel):
    book_theme:str
    author_name:str
    book_title:str
class AuthorMaxTheme(BaseModel):
    book_theme:str
    max_theme:int

class UserMaxTheme(BaseModel):
    book_theme:str
    max_theme:int