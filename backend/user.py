from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
from sqlalchemy import text
from Database import db
import os
from dotenv import load_dotenv
import uvicorn
import bcrypt
from middleware import create_token

#  Load environment variables
load_dotenv()
app = FastAPI(title="Simple App", version="1.0.0")
token_time = int(os.getenv("token_time"))

class Simple(BaseModel):
    name: str = Field(..., example="Olaiya Solomon")
    email: str = Field(..., example="olaiyasolomon@email.com")
    password: str = Field(..., example="olai234")
    userType: str = Field(..., example="student")

@app.get("/", description="This endpoint just return a welcome message")
def root():
 return {"Message": "Welcome to my FastAPI App"}

# Signup endpoint
@app.post("/signup")
def signUp(input: Simple):
   
    try:
        # Check if email exists
        duplicate_query = text("SELECT * FROM user WHERE email = :email")
        existing = db.execute(duplicate_query, {"email": input.email}).fetchone()
       
        if existing:
            raise HTTPException(status_code=400, detail="Email already exists")
        # Hash password
        salt = bcrypt.gensalt()
        hashed_password = bcrypt.hashpw(input.password.encode('utf-8'), salt)
        # Insert new user
        query = text("""
            INSERT INTO user (name, email, password)
            VALUES (:name, :email, :password, :userType)
        """)
        db.execute(query, {"name": input.name, "email": input.email, "password": hashed_password, "userType": input.userType})
        db.commit()
      
        return {
            "message": "User created successfully",
            "data": {"name": input.name, "email": input.email}
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

class LoginRequest(BaseModel):
    email: str = Field(..., example="olaiyasolomon@email.com")
    password: str = Field(..., example="olai234")

@app.post("/login")
def login(input: LoginRequest):
    try:
        query = text("""
            SELECT * FROM user WHERE email = :email
""")
        result = db.execute(query, {"email": input.email}).fetchone()
        if not result:
            raise HTTPException(status_code=404, detail="Invalid email or password")
        
        verified_password = bcrypt.checkpw(input.password.encode('utf-8'), result.password.encode('utf-8'))
        if not verified_password:
          raise HTTPException(status_code=404, detail="Invalid email or password")
       
        create_token(details = {
            "email": result.email,
            "usertype": result.usertype
        }, expiry = token_time)
        
        return {
            "message": "Login successful",
            
        }
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    uvicorn.run(app, host=os.getenv("host"), port=int(os.getenv("port")))

