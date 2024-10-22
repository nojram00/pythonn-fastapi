from fastapi import FastAPI, HTTPException, Request, Response
from models import User
from db import client
from schema import UserMutation, UserCredential, UserUpdate
from session import Auth, verify_token


app = FastAPI()
user = User(client)

@app.get('/')
def hello():
    return {
        "message" : "Hello World!"
    }

@app.get('/users')
@Auth
def users(request : Request):
    return user.find_all()

@app.post('/add-user')
def add_user(user_create : UserMutation):
    user_data = user.insert(user_create)

    if user_data[1]:
        return Response({
            "message" : "User created.",
            "id" : user_data[0]
        }, status_code=200)

    return Response({
        "message" : "User not created."
    }, status_code=500)

@app.patch('/update-user/{uid}')
@Auth
def update_user(request : Request, uid : str, user_update : UserUpdate):

    payload = request

    if payload["role"] == "user":
        raise HTTPException(status_code=401, detail="Updating users must be an admin...")

    user_data = user.update(uid, user_update)

    if user_data[1] == True:
        return Response({
            "message" : "User updated.",
            "id" : user_data[0]
        }, status_code=200)

    return Response({
        "message" : "User not updated.",
        "error" : user_data[0]
    }, status_code=500)

@app.patch('/update-profile')
@Auth
def update_profile(request : Request, user_update : UserUpdate):
    user_data = user.update(request["id"], user_update)

    print(user_data[0])
    if user_data[1] == True:
        return Response({
            "message" : "User updated.",
            "user" : {
                "id" : user_data[0].id,
                "username" : user_data[0].username,
                "email" : user_data[0].email
            }
        }, status_code=200)

    return Response({
        "message" : "User not updated.",
        "error" : user_data[0]
    }, status_code=500)

@app.post('/login')
def login(cred : UserCredential):
    u=user.login(cred)

    return {
        "token" : u 
    }

@app.post('/verify-token')
@Auth
def verify(request : Request):

    if request:
        return {
            "message" : "Token verified!",
            "payload" : request
        }
    

@app.get('/user/{uid}')
def search(uid):
    result = user.find(uid)

    return {
        "data" : result
    }