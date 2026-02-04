from fastapi import FastAPI
from database import engine, Base
import models
from sqlalchemy.orm import Session
from sqlalchemy import func, select
from datetime import date

Base.metadata.create_all(bind=engine)

app = FastAPI()

@app.get("/")
def root():
    return {"message": "Book Management System"}

from fastapi import FastAPI, Depends

app = FastAPI()

from fastapi import HTTPException
from sqlalchemy.orm import Session

from database import get_db

from models import User, Author, Book, BookLoan


from schemas import (
    UserCreate,
    AuthorCreate,
    BookCreate,
    GetUserDetails,
    BookDetailsResponse

)
from schemas import LendingDetails
from schemas import FavouriteTheme
from schemas import AuthorTheme
from schemas import AuthorMaxTheme
from schemas import UserMaxTheme
from schemas import AuthorEmailUpdate
from schemas import BookNotReturned


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

@app.get("/details", response_model=list[BookDetailsResponse])
def get_book_details(db: Session = Depends(get_db)):

    rows = (
        db.query(
            Book.id.label("book_id"),
            Book.title.label("title"),
            Author.email.label("author_email")
        )
        .join(Author, Book.author_id == Author.id)
        .all()
    )

    return rows
@app.get("/lendingdetails/{date}",response_model=list[LendingDetails])
def get_lending_details(date:date,db:Session=Depends(get_db)):
    rows=(
        db.query(
            BookLoan.user_id.label("user_id"),
            BookLoan.book_id.label("book_id"),
            BookLoan.loan_date.label("loan_date"),
            Book.title.label("title")

        )
        .join(Book, BookLoan.book_id == Book.id)
        .filter(BookLoan.loan_date==date)
        .all()
    )
    return rows
@app.get("/themes/{user}", response_model=list[FavouriteTheme])
def get_theme_details(user:int,db: Session = Depends(get_db)):

    rows = (
        db.query(
            Book.theme.label("book_theme"),
            User.email.label("user_email")
        )
        .join(BookLoan, Book.id == BookLoan.book_id)
        .join(User,User.id==BookLoan.user_id)
        .filter(BookLoan.user_id==user)
        .all()
    )

    return rows
    
@app.get("/authorthemes/{author}", response_model=list[AuthorTheme])
def get_theme_details(author:int,db: Session = Depends(get_db)):

    rows = (
        db.query(
            Book.theme.label("book_theme"),
            Book.title.label("book_title"),
            Author.name.label("author_name")
        )
        .join(Author, Author.id == Book.author_id)
        .filter(Author.id==author)
        .all()
    )

    return rows

@app.get("/authormaxthemes/{author}", response_model=list[AuthorMaxTheme])
def author_max_theme(author:int,db: Session = Depends(get_db)):

    rows =(
        db.query(
            Book.theme.label("book_theme"),
            func.count(Book.id).label("max_theme")
        )
        .group_by(Book.theme)
        .filter(Book.author_id==author)
        .order_by(func.count(Book.id).desc())
        .limit(1)
        .all()
    )

    return rows
    
@app.get("/usermaxthemes/{user}", response_model=list[UserMaxTheme])
def user_max_theme(user:int,db: Session = Depends(get_db)):

    rows =(
        db.query(
            Book.theme.label("book_theme"),
            func.count(Book.id).label("max_theme")
        )
        .group_by(Book.theme)
        .join(BookLoan,BookLoan.book_id==Book.id)
        .filter(BookLoan.user_id==user)
        .order_by(func.count(Book.id).desc())
        .limit(1)
        .all()
    )

    return rows

@app.put("/authoremailupdate/{author_id}")
def author_email_update(author_id:int,data:AuthorEmailUpdate,db:Session=Depends(get_db)):
    author=db.query(Author).filter(Author.id==author_id).first()
    author.email=data.email
    db.commit()
    db.refresh(author)

    return{
        "message":"author email updated"
    }
@app.get("/booksnotreturned/{user_id}",response_model=list[BookNotReturned])
def book_not_returned(user_id:int,db:Session=Depends(get_db)):
    books=db.query(Book.title.label("Book_title")).join(BookLoan,Book.id==BookLoan.book_id).filter(BookLoan.user_id==user_id,BookLoan.book_returned==False).all()
    return books
print("for testing")






