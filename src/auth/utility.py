from datetime import datetime, timedelta, timezone
from typing import Annotated, Optional, List
import jwt
from fastapi import Depends, APIRouter, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jwt.exceptions import InvalidTokenError
from passlib.context import CryptContext
from sqlmodel import Session, select
from .model import User
from src.book.data import get_session
from .schema import TokenData, Token, UserOut, UserRegistration, UserResponse
from ..config import setting

SECRET_KEY = setting.secret_key
ALGORITHM = setting.algorithm
ACCESS_TOKEN_EXPIRE_MINUTES = setting.access_token_expire_minutes


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/users/token")

user_router = APIRouter(tags=["user"])


def verify_password(password,hash_password):
    return pwd_context.verify(password,hash_password)

def get_password_hash(password):
    return pwd_context.hash(password)

def create_access_token(data:dict, expire_time:datetime | None = None):
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + (expire_time or timedelta(minutes=15))
    to_encode.update({"exp":expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

def get_user_by_username(username:str, session:Session):
    statement = select(User).where(User.username==username)
    return session.exec(statement).first()

def authenticate_user(username:str,password:str, session:Session):
    user = get_user_by_username(username, session)
    if not user:
        return False
    if not verify_password(password,user.hashed_password):
        return False
    return user

async def get_current_user(
    token:Annotated[str, Depends(oauth2_scheme)],session:Session=Depends(get_session)
):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

    try:
        payload = jwt.decode(token,SECRET_KEY,algorithms=[ALGORITHM])
        username = payload.get('sub')
        if username is None:
            raise credentials_exception
        token_data = TokenData(username = username)
    except InvalidTokenError:
        raise credentials_exception
    
    user = get_user_by_username(token_data.username, session)
    if user is None:
        raise credentials_exception
    return user
    
async def get_current_active_user(
        current_user:User = Depends(get_current_user)
):
    if current_user.disabled:
        raise HTTPException(status_code=400, detail="Inactive user")
    return current_user



@user_router.post("/token", response_model=Token)
async def login_for_access_token(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
    session: Session = Depends(get_session),
):
    user = authenticate_user(form_data.username, form_data.password, session)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.username}, expire_time=access_token_expires
    )
    return Token(access_token=access_token, token_type="bearer")

@user_router.get("/me/", response_model=UserOut)
async def read_users_me(current_user: Annotated[User, Depends(get_current_active_user)]):
    return current_user

@user_router.post('/register-user',response_model =UserOut )
async def user_register(user:UserRegistration, session:Session = Depends(get_session)):
    existing_user = session.query(User).filter(User.username == user.username).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="user already registered")
    new_user = User(
        username=user.username, email = user.email,
        hashed_password=get_password_hash(user.password),
        full_name = user.full_name
    )
    session.add(new_user)
    session.commit()
    session.refresh(new_user)
    return new_user

@user_router.get('/all_users', response_model =List[UserResponse])
async def get_all_users(user:User = Depends(get_current_user),session:Session=Depends(get_session) ):
    if not user.role == 'admin':
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="not allowed")
    return session.exec(select(User)).all()