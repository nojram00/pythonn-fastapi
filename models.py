from bson.objectid import ObjectId
from pymongo import MongoClient
from schema import UserQuery, UserMutation, UserUpdate, UserCredential
from typing import List, Optional, Tuple
from session import *

class User:
    def __init__(self, client : MongoClient):
        self.database = client["freedom-wall"]
        self.collection = self.database["users"]


    def insert(self, user_data : UserMutation) -> Tuple[Optional[str], bool]:
        try:
            result = self.collection.insert_one({
                "username" : user_data.username,
                "password" : user_data.password,
                "role" : user_data.role,
                "email" : user_data.email
            })
            return [str(result.inserted_id), True]
        except Exception as e:
            return [str(e), False]
        
    def update(self, id, user_data : UserUpdate) -> Tuple[Optional[UserQuery], bool]:
        try:

            user = self.collection.find_one({ "_id" : ObjectId(id) })

            if user is None:
                return [None, False]

            result = self.collection.update_one({
                "_id" : ObjectId(str(user["_id"]))
            }, { "$set" : {
                    "username" : user_data.username if not user_data.username is None else user["username"],
                    "password" : user_data.password if not user_data.password is None else user["password"],
                    "email" : user_data.email if not user_data.email is None else user["email"]
                }
            })

            updated = self.collection.find_one({ "_id" : ObjectId(id) })

            return [UserQuery(
                id = str(updated['_id']),
                username = str(updated['username']),
                email=str(updated["email"]),
                role=str(updated["role"])
            ), True]
        except Exception as e:
            print(e)
            return [None, False]

    def find_all(self) -> List[UserQuery]:
        results = self.collection.find({})
        
        return [UserQuery(id=str(doc["_id"]), **doc) for doc in results]
    
    def find(self, id) -> Optional[UserQuery]:
        result = self.collection.find_one({ "_id" : ObjectId(id) })

        if result:
            return UserQuery(
                    id=str(result["_id"]), 
                    username=result["username"],
                    role=result["role"],
                    email=result["email"]
                    )
        return None

    def login(self, creds : UserCredential):
        result = self.collection.find_one({
            "email" : creds.email,
            "password" : creds.password
        })

        if not result is None:
            token = create_access_token({
                "id" : str(result["_id"]),
                "username" : str(result["username"]),
                "email" : str(result["email"]),
                "role" : str(result["role"])
            })
            return token
    
    
if __name__ == '__main__':
    from db import client

    user = User(client)

    # user.insert('nojram', 'password123', 'user', 'nojram@gmail.com')

    # results = user.find_all()

    results = user.find("6717352beb3333b55957d781")
    print(results)