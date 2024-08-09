#login route to get the token
from fastapi.security import OAuth2PasswordBearer,OAuth2PasswordRequestForm
from fastapi import APIRouter,Depends,HTTPException,status
from typing import Annotated
from sqlalchemy.orm import Session
from .. import database,models,hashing,user_token,schemas
from datetime import timedelta

router = APIRouter(
    prefix='/my-portfolio',
    tags=['Authentication'],
)

Hashed = hashing.Hash
ACCESS_TOKEN_EXPIRE_HOUR = 2


#one of the login for testing
#username: precious@gmail.com
#password: 12345678

@router.post('/login',
             summary="Login and generate JWT token",
             description="Authenticate a user by checking the email and password against the database. If valid, generate and return a JWT access token with an expiration time.",
             responses={
                 404: {"description": "Invalid credentials or password"}
             }
             )
#pass in the database and the oauth2request form for the login
def login(user:Annotated[OAuth2PasswordRequestForm,Depends()],db:Session=Depends(database.get_db)):
    """Get the useremail and password check it in the database and create and return a jwt token and expire time"""
    #check if the username enter is in the database
    user_details = db.query(models.User).filter(models.User.email == user.username).first()

    #if the user email is not in the database
    if not user_details:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Invalid Credentials')
    
    #verify the password
    if not Hashed.verify(user_details.password,user.password):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Invalid password')
    
    #if the useremail is in the database and the password is verified
    #set the time the token will exipre after 1hr 
    access_token_expire = timedelta(hours=ACCESS_TOKEN_EXPIRE_HOUR) #then the user will have to login again
    # #generate the jwt token
    # #by passing in the data and the expire token time
    access_token = user_token.create_access_token(data={'sub':user.username},expires_delta=access_token_expire)
    return schemas.Token(access_token=access_token,token_type="bearer") #return the access token and the token type





 
