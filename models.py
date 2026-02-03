from sqlalchemy import Column, Integer, String,ForeignKey,Date
from sqlalchemy.orm import relationship
from database import Base
from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from database import Base


class Author(Base):
    __tablename__ = "authors"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    email = Column(String, unique=True, nullable=False)
    password = Column(String, nullable=False)

    books = relationship("Book", back_populates="author")

from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from database import Base

class Book(Base):
    __tablename__ = "books"

    id = Column(Integer, primary_key=True)
    title = Column(String, nullable=False)

    author_id = Column(Integer, ForeignKey("authors.id"), nullable=False)
    theme=Column(String,nullable=False)

    author = relationship("Author", back_populates="books")
    
    


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    email = Column(String, unique=True, nullable=False)
    password = Column(String, nullable=False)
    method=Column(String,nullable=False)


    borrowed_books = relationship("BookLoan", back_populates="user")


class BookLoan(Base):
    __tablename__ = "book_loans"

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    book_id = Column(Integer, ForeignKey("books.id"))

    user = relationship("User", back_populates="borrowed_books")
    book = relationship("Book")
    loan_date = Column(Date, nullable=False)
    



