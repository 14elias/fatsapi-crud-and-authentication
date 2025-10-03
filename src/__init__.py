from fastapi import FastAPI
from src.book.data import init_db
from src.auth.utility import user_router
from src.post.route import post_router
from .config import setting

version = 'v1'

app = FastAPI(
    version = version
)



app.include_router(user_router, prefix=f'/api/{version}/users')
app.include_router(post_router)


init_db()