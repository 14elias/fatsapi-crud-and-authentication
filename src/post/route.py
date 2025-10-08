from fastapi import APIRouter,Depends,HTTPException
from .model import Post,Likes
from .schema import CreatePost,PostOut,Vote,PostOutVote
from ..book.data import get_session
from ..auth.utility import get_current_user
from ..auth.model import User
from sqlmodel import Session,select,func

post_router=APIRouter(tags=['post'])

@post_router.post('/create_post')
async def create_post(post:CreatePost, session:Session =Depends(get_session),current_user:User =Depends(get_current_user)):
    id = current_user.id
    new_post = Post(**post.dict())
    new_post.owner_id = id
    session.add(new_post)
    session.commit()
    session.refresh(new_post)
    return new_post

@post_router.get('/get_posts',response_model = list[PostOutVote])
async def get_post(session:Session =Depends(get_session), limit:int=10,skip:int=0,search:str=''):
    statement = (
        select(Post, func.count(Likes.post_id).label("likes"))
        .select_from(Post)
        .join(Likes, Post.id == Likes.post_id, isouter=True)  # LEFT JOIN
        .group_by(Post.id)
    )

    if search:
        statement=statement.where(Post.title.contains(search))

    statement = statement.offset(skip).limit(limit)
    print(statement)
    post = session.exec(statement).all()

    return post

@post_router.get('/get_a_post/{post_id}',response_model=PostOutVote)
async def get_post(post_id:int,session:Session =Depends(get_session)):
    statement = (
        select(Post, func.count(Likes.post_id).label("likes"))
        .select_from(Post)
        .join(Likes, Post.id == Likes.post_id, isouter=True)  # LEFT JOIN
        .group_by(Post.id).where(Post.id==post_id)
    )
    post = session.exec(statement).first()
    if not post:
        raise HTTPException(status_code=404, detail="Item not found")
    return post


@post_router.patch('/update_post/{post_id}',response_model=PostOut)
async def update_book(post_id:int, data:CreatePost, session:Session=Depends(get_session),
                      current_user:User=Depends(get_current_user)
):
    owner_id = current_user.id
    statement = select(Post).where((Post.owner_id==owner_id) & (Post.id==post_id))
    post = session.exec(statement).first()
    if not post:
        raise HTTPException (status_code = 404 )
    for field,value in data.dict().items():
        setattr(post,field,value)
    session.add(post)
    session.commit()
    session.refresh(post)
    return post


@post_router.delete('/delete_post/{post_id}',status_code=204)
async def delete_post(post_id:int, session:Session=Depends(get_session),current_user:User=Depends(get_current_user)):
    statement = select(Post).where((Post.owner_id==current_user.id)&(Post.id==post_id))
    post = session.exec(statement).first()
    if not post:
        raise HTTPException(status_code=404, detail = "no content")
    session.delete(post)
    session.commit()
    return {'deleted_post ':post}


@post_router.post('/vote')
async def vote(vote_data:Vote,session:Session=Depends(get_session),current_user:User=Depends(get_current_user)):
    post = session.exec(select(Post).where(Post.id==vote_data.post_id)).first()
    if not post:
        raise HTTPException(status_code=404, detail="no content")

    like = session.exec(select(Likes).where(Likes.post_id==vote_data.post_id,Likes.user_id==current_user.id)).first()

    if vote_data.dir == 1:
        if like:
            raise HTTPException(status_code=409, detail="user already likes")
        
        new_like=Likes(user_id=current_user.id,post_id=vote_data.post_id)
        session.add(new_like)
        session.commit()
        session.refresh(new_like)

        return {"message":"successfully liked"}

    elif vote_data.dir ==0:
        if not like:
            raise HTTPException(status_code=404, detail='like not found')
        session.delete(like)
        session.commit()

        return {"message":"like deleted successfully"}
    else:
        return {"message":"enter valid dir"}