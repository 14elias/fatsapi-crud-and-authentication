from fastapi import APIRouter,Depends,HTTPException
from .model import Post
from .schema import CreatePost
from ..book.data import get_session
from sqlmodel import Session,select

post_router=APIRouter(tags=['post'])

@post_router.post('/create_post')
async def create_post(post:CreatePost, session:Session =Depends(get_session)):
    new_post = Post(**post.dict())
    session.add(new_post)
    session.commit()
    session.refresh(new_post)
    return new_post

@post_router.get('/get_posts')
async def get_post(session:Session =Depends(get_session)):
    post = session.exec(select(Post)).all()
    return post

@post_router.get('/get_a_post/{post_id}')
async def get_post(post_id:int,session:Session =Depends(get_session)):
    post = session.get(Post,post_id)
    if not post:
        raise HTTPException(status_code=404, detail="Item not found")
    return post


@post_router.patch('/update_post/{post_id}')
async def update_book(post_id:int, data:CreatePost, session:Session=Depends(get_session)):
    post = session.get(Post,post_id)
    if not post:
        raise HTTPException (status_code = 404 )
    for field,value in data.dict().items():
        setattr(post,field,value)
    session.add(post)
    session.commit()
    session.refresh(post)
    return post


@post_router.delete('/delete_post/{post_id}')
async def delete_post(post_id:int, session:Session=Depends(get_session)):
    post = session.get(Post,post_id)
    if not post:
        raise HTTPException(status_code=404, detail = "no content")
    session.delete(post)
    session.commit()
    return {'deleted_post ':post}