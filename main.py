from fastapi import FastAPI
from database import engine, Base
import models
from sqlalchemy.orm import Session
from sqlalchemy import func, select

Base.metadata.create_all(bind=engine)

app = FastAPI()

@app.get("/")
def root():
    return {"message": "Book Management System"}

from fastapi import FastAPI, Depends
from config import Settings, get_settings

app = FastAPI()

@app.get("/db-connection-status")
def read_db_status(settings: Settings = Depends(get_settings)):
    db_url = f"postgresql://{settings.database_user}:{settings.database_password}@{settings.database_host}:{settings.database_port}/{settings.database_name}"
    return {"database_host": settings.database_host, "database_name": settings.database_name, "db_url_snippet": db_url[:30] + "..."}

from database import get_db
from schemas import UserCreate
from models import User
from schemas import AuthorCreate
from models import Author
from fastapi import HTTPException
from models import Book, Author
from schemas import BookCreate
from schemas import GetUserDetails



@app.post("/users")
def create_user(user: UserCreate, db: Session = Depends(get_db)):
    new_user = User(
        email=user.email,
        password=user.password,
        method=user.method
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return {
        "message": "user registered successfully"
    }
@app.post("/authors")
def create_author(author: AuthorCreate, db: Session = Depends(get_db)):

    # check duplicate email
    existing_author = db.query(Author).filter(Author.email == author.email).first()
    if existing_author:
        raise HTTPException(
            status_code=400,
            detail="Author email already exists"
        )

    new_author = Author(
        name=author.name,
        email=author.email,
        password=author.password
    )

    db.add(new_author)
    db.commit()
    db.refresh(new_author)

    return {
        "message": "Author registered successfully"
    }

@app.post("/books")
def create_book(book: BookCreate, db: Session = Depends(get_db)):

    # check if author exists
    author = db.query(Author).filter(Author.id == book.author_id).first()
    if not author:
        raise HTTPException(
            status_code=404,
            detail="Author not found"
        )

    new_book = Book(
        title=book.title,
        author_id=book.author_id
    )

    db.add(new_book)
    db.commit()
    db.refresh(new_book)

    return {
        "id": new_book.id,
        "title": new_book.title,
        "author_id": new_book.author_id
    }
@app.get("/method")
def get_users_type(met:GetUserDetails,db:Session=Depends(get_db)):
    users=db.query(User).filter(User.method==met.method).all()
    return users

@app.get("/usercounts")
def get_user_counts(db: Session = Depends(get_db)):
    result = (db.query(User.method,func.count(User.id)).group_by(User.method).order_by(func.count(User.id).desc()).first())

    return {
        "method_with_max_users": result[0],
        "max_count": result[1]
    }

@app.get("/details")
def get_book_details(db: Session = Depends(get_db)):
    book_details=db.query(Book.id,Book.title,Author.email).join(Author,Book.author_id==Author.id).all()
    print(book_details)
    return [
        {
            "book_id": Book.id,
            "title": Book.title,
            "author_email": author.email
        }
        for book_id, title, author_email in book_details
    ]