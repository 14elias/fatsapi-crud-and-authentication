from fastapi import HTTPException,Response,APIRouter,Depends
from typing import Optional
from sqlmodel import Session,select
from .data import get_session
from .schema import Book, BookCreate

book_router = APIRouter()



@book_router.get('/get_all_books')
def say_hello(db: Session = Depends(get_session)):
    books = db.exec(select(Book)).all()
    return books 


@book_router.get('/get_a_book/{book_id}')
def greetings(book_id : int, db: Session = Depends(get_session)):
    book = db.get(Book,book_id)
    if not book:
        raise HTTPException(status_code=404, detail="Item not found")
    return book


@book_router.delete("/delete_book/{book_id}")
def delete_book(book_id:int, db: Session = Depends(get_session)):
    book = db.get(Book,book_id)
    if not book:
        raise HTTPException(status_code=404, detail = "no content")
    db.delete(book)
    db.commit()
    return book


@book_router.post("/create_book")
def create_book(book: BookCreate, session: Session = Depends(get_session)):
    book = Book(**book.model_dump())
    session.add(book)
    session.commit()
    session.refresh(book)
    return book


@book_router.patch("/update_book/{book_id}")
def update_book(book_id, book_data: BookCreate, db: Session = Depends(get_session)):
    book = db.get(Book,book_id)
    if not book:
        raise HTTPException (status_code = 404 )
    for field, value in book_data.model_dump().items():
        setattr(book, field, value)

    db.commit()
    db.refresh(book)
    return book