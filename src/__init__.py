from fastapi import FastAPI
from src.book.route import book_router
from src.book.data import init_db
from src.auth.utility import user_router

version = 'v1'

app = FastAPI(
    version = version
)



app.include_router(book_router, prefix=f'/api/{version}/books')
app.include_router(user_router, prefix=f'/api/{version}/users')


init_db()