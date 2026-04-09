from fastapi import FastAPI
from pydantic import BaseModel

app=FastAPI()

users=[]

class User(BaseModel):
    name:str
    age:int

@app.get("/")
def home():
    return{"Message":"Welcome Swara"}

@app.get("/users")
def get_users():
    return {"users":users}

@app.post("/add_user")
def add_user(user: User):
    users.append(user)
    return {"message": "User added sucessfully","user":user}