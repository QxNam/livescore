from fastapi import Depends,APIRouter,HTTPException,HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from model import User
from jose import  jwt
from datetime import datetime, timedelta
from dotenv import dotenv_values
import hashlib
import os

if os.path.exists('.env'):
    configs = dotenv_values(".env")
else:
    configs = os.environ

router = APIRouter()
ACCESS_TOKEN_SECRET = configs['ACCESS_TOKEN_SECRET']
ALGORITHM = configs['ALGORITHM']
# ACCESS_TOKEN_EXPIRE_MINUTES = os.getenv('ACCESS_TOKEN_EXPIRE_MINUTES')

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

def hash_password(password: str):
    hashed_password = hashlib.sha256(password.encode()).hexdigest()
    return hashed_password

def create_access_token(user: str) -> str:
    to_encode = {"user": user}
    expiry = datetime.now() + timedelta(minutes=15)  
    to_encode.update({"exp": expiry})
    encoded_jwt = jwt.encode(to_encode, ACCESS_TOKEN_SECRET, algorithm=ALGORITHM)
    return encoded_jwt

@router.post('/token', tags=["Auth"])
async def login(user: User):
    state = {
        "user": configs['USER'],
        "password": hash_password(configs['PASSWORD'])
    }
    if state['user'] != user.user:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="The account does not exist")
    if state['password'] != hash_password(user.password):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Incorrect password")
    return {"access_token": create_access_token(user.user)}

@router.get('/check', tags=["Auth"])
def check(token: str = Depends(oauth2_scheme)):
    try:
        payload = jwt.decode(token, ACCESS_TOKEN_SECRET, algorithms=[ALGORITHM])
        return {"user": payload}
    except:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token")