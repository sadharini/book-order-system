from pydantic import BaseModel

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
