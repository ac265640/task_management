from fastapi import HTTPException,status,Request
from src.user.dtos import UserSchema , LoginSchema
from sqlalchemy.orm import Session
from src.user.models import UserModel
from pwdlib import PasswordHash
from src.utils.settings import settings 
from datetime import datetime , timedelta
import jwt 
from jwt.exceptions import InvalidTokenError


password_hash=PasswordHash.recommended()


def get_password_hash(password):
    return password_hash.hash(password)

#decrypt and verify pass
def verify_password(plain_password,hashed_password):
    return password_hash.verify(plain_password,hashed_password)

def register(body:UserSchema,db:Session):
    #validate username (checking for duplicates)
    is_user=db.query(UserModel).filter(UserModel.username==body.username).first()
    if is_user:
        raise HTTPException(400,detail="Username already exists...")
    #validate email 
    is_user=db.query(UserModel).filter(UserModel.email==body.email).first()
    if is_user:
        raise HTTPException(400,detail="email already exists...")
    
    #hashing of password 
    hash_password=get_password_hash(body.password)


    new_user=UserModel(
    name=body.name,
    username=body.username,
    hash_password=hash_password,
    email=body.email,
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return new_user


def login_user(body:LoginSchema,db:Session):
    

    user=db.query(UserModel).filter(UserModel.username==body.username).first()

    #here if not as cheching for login info 
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail="You entered wrong username")
    

    if not verify_password(body.password,user.hash_password):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail="You entered wrong password")
    
    #token is only valid upto this exp_time 
    exp_time=datetime.now() + timedelta(minutes=settings.EXP_TIME)
    
    

    #now if both are correct we need to generate one token based on user details 
    #(payload , secret key , algorithm)

    token=jwt.encode({"_id":user.id,"exp":exp_time.timestamp()},settings.SECRET_KEY,settings.ALGORITHM)

    return {"token":token}



# authentication is done via headers 
def is_authenticated(request:Request,db:Session):
    try:
        token=request.headers.get("authorization")
        if not token:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail="YOU ARE UNAUTHORIZED")

        #getting token only 
        token=token.split(" ")[-1]
        #decoding the token 
        data=jwt.decode(token,settings.SECRET_KEY,settings.ALGORITHM)
        user_id=data.get("_id")
        
    
        
        user=db.query(UserModel).filter(UserModel.id==user_id).first()
        if not user:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail="YOU ARE UNAUTHORIZED")



        return user
    #if expiry time is done 
    except InvalidTokenError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail="YOU ARE UNAUTHORIZED")
        
