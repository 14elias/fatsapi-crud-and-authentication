from fastapi import FastAPI,HTTPException # Correct capitalization
from typing import Optional
from pydantic import BaseModel
from fastapi import Response


app = FastAPI()  # Correct capitalization

class Book(BaseModel):
    id : int
    title : str
    published_date : str
    author : str

class BookUpdate(BaseModel):
    title : str
    published_date : str
    author : str


books = [
    {
        'id':1,
        'title':"breaking bad",
        'published_date':"2010",
        'author':'ella'
    },
    {
        'id':2,
        'title':"vikings",
        'published_date':"2015",
        'author':'ivar'
    },
    {
        'id':3,
        'title':"friends",
        'published_date':"2001",
        'author':'joey'
    },
]


@app.get('/get_all_books')
def say_hello():
    return books 


@app.get('/get_a_book/{book_id}')
def greetings(book_id : int):
    for book in books:
        if book["id"] == book_id:
            return book
    raise HTTPException(status_code=404, detail="Item not found")


@app.delete("/delete_book/{book_id}")
def delete_book(book_id:int):
    for book in books:
        if book["id"] == book_id:
            books.remove(book)
            return Response (status_code=204)
    raise HTTPException(status_code=404, detail = "no content")


@app.post("/create_book")
def create_book(book : Book):
    for b in books:
        if b["id"] == book.id:
            raise HTTPException(status_code=400, detail="Book ID already exists")
    books.append(book.dict())
    return {"message": "Book created successfully", "book": book}

@app.patch("/update_book/{book_id}")
def update_book(book_id, book : BookUpdate):
    for b in books:
        if b["id"] == book_id:
            b["title"] = book.title
            b["author"] = book.author
            b["published_date"] = book.published_date
            return b
    raise HTTPException (status_code = 404 )