
import os
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi

url = os.environ.get('MONGO_URL', "mongodb+srv://petmalumarjon:nojram6969@freedom-app.yoiinpm.mongodb.net/?retryWrites=true&w=majority&appName=freedom-app")

client = MongoClient(url, server_api=ServerApi("1"))


if __name__ == '__main__':
    try:
        client.admin.command('ping')
        print("Pinged your deployment. You successfully connected to MongoDB!")

    except Exception as e:
        print(e)