from fastapi import FastAPI
from pydantic import BaseModel,Field  
from dotenv import load_dotenv
import uvicorn
import os


load_dotenv()

app= FastAPI(title="Simple FastAPI App ", version="1.0.0")
data = [{"Name": "Sam Larry", "age": 20, "track": "AI Developer"},
        {"Name": "bahubili", "age": 21, "track": "Backend Developer"},
        {"Name": "John Doe", "age": 22, "track": "Frontend Developer"}]

class Item(BaseModel):
    name: str = Field(..., example="perpetual")
    age: int = Field(..., example= 25)
    track: str = Field(..., example= "Fullstack")

@app.get("/", description= "This end point just reyurned a welcome message")
def root():
    return {"Message": "Welcome to my fastAPI application"}

app.get("/get-data")
def get_data():
    return data

@app.post("/create-data")
def create_data(req: Item):
    print(data)
    return {"Message": "Data Recieved", "Data": data}

@app.put("/update-data/{id}")
def update_data(id: int, req: Item):
    data[id] = req.dict()
    print (data)
    return {"Message": "Data Updated", "Data": data}


if __name__ == "__main__":
    print(os.getenv("host"))
    print(os.getenv("port"))
    uvicorn.run(app, host=os.getenv("host"), port=int(os.getenv("port")))