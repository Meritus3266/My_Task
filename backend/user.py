# from fastapi import FastAPI, HTTPException
# from pydantic import BaseModel, Field
# from sqlalchemy import text
# from Database import db
# import os
# from dotenv import load_dotenv
# import uvicorn
# import bcrypt
# from middleware import create_token, verify_token

# #  Load environment variables
# load_dotenv()
# app = FastAPI(title="Simple App", version="1.0.0")
# token_time = int(os.getenv("token_time"))

# class Simple(BaseModel):
#     name: str = Field(..., example="Olaiya Solomon")
#     email: str = Field(..., example="olaiyasolomon@email.com")
#     password: str = Field(..., example="olai234")
#     userType: str = Field(..., example="student")

# @app.get("/", description="This endpoint just return a welcome message")
# def root():
#  return {"Message": "Welcome to my FastAPI App"}

# # Signup endpoint
# @app.post("/signup")
# def signUp(input: Simple):
   
#     try:
#         # Check if email exists
#         duplicate_query = text("SELECT * FROM user WHERE email = :email")
#         existing = db.execute(duplicate_query, {"email": input.email}).fetchone()
       
#         if existing:
#             raise HTTPException(status_code=400, detail="Email already exists")
#         # Hash password
#         salt = bcrypt.gensalt()
#         hashed_password = bcrypt.hashpw(input.password.encode('utf-8'), salt)
#         # Insert new user
#         query = text("""
#             INSERT INTO user (name, email, password)
#             VALUES (:name, :email, :password, :userType)
#         """)
#         db.execute(query, {"name": input.name, "email": input.email, "password": hashed_password, "userType": input.userType})
#         db.commit()
      
#         return {
#             "message": "User created successfully",
#             "data": {"name": input.name, "email": input.email}
#         }
#     except Exception as e:
#         raise HTTPException(status_code=500, detail=str(e))

# class LoginRequest(BaseModel):
#     email: str = Field(..., example="olaiyasolomon@email.com")
#     password: str = Field(..., example="olai234")

# @app.post("/login")
# def login(input: LoginRequest):
#     try:
#         query = text("""
#             SELECT * FROM user WHERE email = :email
# """)
#         result = db.execute(query, {"email": input.email}).fetchone()
#         if not result:
#             raise HTTPException(status_code=404, detail="Invalid email or password")
        
#         verified_password = bcrypt.checkpw(input.password.encode('utf-8'), result.password.encode('utf-8'))
#         if not verified_password:
#           raise HTTPException(status_code=404, detail="Invalid email or password")
       
#         create_token(details = {
#             "email": result.email,
#             "usertype": result.usertype,
#             "userid": result.userid
#         }, expiry = token_time)
        
#         return {
#             "message": "Login successful",
#             "token": encoded_token
#         }
    
#     except Exception as e:
#         raise HTTPException(status_code=500, detail=str(e))
    

#     class courseRequest(BaseModel):
#         title: str = Field(..., example="Backend Course")
#         level: str = Field(..., example="Beginner")

#     @app.post("/courses")
#     def addcourses(input: courseRequest, user_data = Depends(verify_token)):
#         try:
#             query = text("""
#                 INSERT INTO courses (title, level)
#                 VALUES (:title, :level)
#             """)
#             db.execute(query, {"title": input.title, "level": input.level})
#             db.commit()
#             return {
#                 "message": "Course added successfully",
#                 "data": {
#                     "title": input.title,
#                     "level": input.level
#                       }
#             }
#         except Exception as e:
#             raise HTTPException(status_code=500, detail=str(e))

# if __name__ == "__main__":
#     uvicorn.run(app, host=os.getenv("host"), port=int(os.getenv("port")))











from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
from sqlalchemy import text
from Database import db
import os
from dotenv import load_dotenv
import uvicorn
import bcrypt
import jwt
from middleware import create_token, verify_token
from fastapi import Depends
#  Load environment variables
load_dotenv()
app = FastAPI(title="Simple App", version="1.0.0")
token_time = int(os.getenv("token_time"))
#  Pydantic model
class Simple(BaseModel):
    name: str = Field(..., example="Ola James")
    email: str = Field(..., example="olajames@email.com")
    password: str = Field(..., example="james123")
@app.get("/")
def read_root():
    return {"message": "Welcome to the User Management API"}
# Signup endpoint
@app.post("/signup")
def signUp(input: Simple):
    try:
        # Check if email exists
        duplicate_query = text("SELECT * FROM users WHERE email = :email")
        existing = db.execute(duplicate_query, {"email": input.email}).fetchone()
        if existing:
            print("Email already exists")
            raise HTTPException(status_code=400, detail="Email already exists")
        # Hash password
        salt = bcrypt.gensalt()
        hashed_password = bcrypt.hashpw(input.password.encode('utf-8'), salt)
        # Insert new user
        query = text("""
            INSERT INTO users (name, email, password)
            VALUES (:name, :email, :password)
        """)
        db.execute(query, {"name": input.name, "email": input.email, "password": hashed_password})
        db.commit()
        return {
            "message": "User created successfully",
            "data": {"name": input.name, "email": input.email}
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
class LoginRequest(BaseModel):
    email: str = Field(..., example="olajames@email.com")
    password: str = Field(..., example="james123")
@app.post("/login")
def login(input: LoginRequest):
    try:
        query = text("""
        SELECT * FROM users WHERE email = :email
""")
        result = db.execute(query, {"email": input.email}).fetchone()
        if not result:
            raise HTTPException(status_code=404, detail="Invalid email or password")
        verified_password = bcrypt.checkpw(input.password.encode('utf-8'), result.password.encode('utf-8'))
        if not verified_password:
            raise HTTPException(status_code=404, detail="Invalid email or password")
        encoded_token = create_token(details={
            "email": result.email,
            "userType": result.userType,
            "userid": result.id
        }, expiry=token_time)
        return {
            "message": "Login successful",
            "token": encoded_token
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
class courseRequest(BaseModel):
    title: str = Field(..., example="backend engineering")
    level: str = Field(..., example="Beginner")
@app.post("/courses")
def addcourses(input: courseRequest, user_data = Depends(verify_token)):
    try:
        print(user_data)
        if user_data.userTyper != "admin":
            raise HTTPException(status_code=401, detail="You are not authorized to add a course")
        query = text("""
            INSERT INTO courses (title, level)
            VALUES (:title, :level)
        """)
        db.execute(query, {"title": input.title, "level": input.level})
        db.commit()
        return {
            "message": "Course added successfully",
            "data": {"title": input.title, "level": input.level}
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
#  Run app
if __name__ == "__main__":
    uvicorn.run(app, host=os.getenv("host"), port=int(os.getenv("port")))
