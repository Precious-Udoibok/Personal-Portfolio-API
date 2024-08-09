from datetime import datetime, timedelta, timezone,date
import jwt
from jwt.exceptions import  InvalidTokenError
from . import schemas
import secrets
from json import dumps

# # Generate a secure random secret key
# secret_key = secrets.token_hex(32)
# print(secret_key)


SECRET_KEY="658b1e7468b000d8cf21371bea9aef57b1462929888ebadca668ebc5ac72f6ad"
ALGORITHM = "HS256"

#This function is handles serialization of obj into a format that can be converted into JSON.
def json_serial(obj):
    """JSON serializer for objects not serializable by default json code"""

    if isinstance(obj, (datetime, date)): #check if the object is in datetime or date format
        return obj.isoformat() #convert it to a JSon serialization format
    raise TypeError ("Type %s not serializable" % type(obj))


#create access token
def create_access_token(data:dict,expires_delta:timedelta| None = None):
    to_encode = data.copy() #copying the data

    # if the expire_delta time is provvided
    if expires_delta:
        #set the expire time to the current time plus expire time(30mins)
        # Converts the result to a JSON-serializable format 
        expire = dumps(datetime.now(timezone.utc) + expires_delta,default=json_serial)

    else:
        #if the expire time is not provided, the current expire time will be 
        #current time plus 15 mins
        # Converts the result to a JSON-serializable format 
        expire = dumps(datetime.now(timezone.utc)+ timedelta(hours=1),default=json_serial) 
    to_encode.update({'expire':expire}) #updating the data to have the expire keyword and expire time
    # encode the data(to_encode)
    encoded_jwt = jwt.encode(to_encode,SECRET_KEY,ALGORITHM)
    return encoded_jwt


#verify the token
def verify_token(token:str,credentials_exceptions):
    try:
        #decode the data using the token, secret key and the algorithm
        payload = jwt.decode(token,SECRET_KEY,algorithms=[ALGORITHM])
        email:str = payload.get('sub') #extracts the username from the payload
        if not email:
            raise credentials_exceptions
        token_data = schemas.TokenData(email=email)
    except InvalidTokenError:
        raise credentials_exceptions
