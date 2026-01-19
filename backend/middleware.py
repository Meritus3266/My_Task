import jwt
from dotenv import load_dotenv
import os
from datetime import datetime, timedelta
from fastapi import Security
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from fastapi import Request

load_dotenv()

secret_key = os.getenv("secret_key")
algorithm = "Hs256"
security = HTTPBearer()

def create_token(details: dict, expiry: int):
    expire = datetime.now() + timedelta(minutes=expiry)
    details.update({"exp": expire})
    encoded_jwt = jwt.encode(details, secret_key, algorithm = algorithm)
     
    return encoded_jwt

bearer = HTTPBearer()
def verify_token(request: HTTPAuthorizationCredentials = Security(bearer)):
    
    token = request.credentials
    verified_token = jwt.decode(token, secret_key, algorithms=["HS256"])
    expiry_time = verified_token.get("exp")

    return {
        "email": verified_token.get["email"],
        "usertype": verified_token.get["usertype"]
   }