from typing import List
import shutil
from fastapi import FastAPI, File, UploadFile
from fastapi.responses import HTMLResponse
import uuid

from fastapi.middleware.cors import CORSMiddleware

from pymongo import MongoClient
import datetime

app = FastAPI()
# client = MongoClient(
#     'mongodb+srv://AIGANG:Ez6DFjF8XJttNMLF@dk-1.sflh5.mongodb.net/AIGANG?retryWrites=true&w=majority')
# db = client.AIGANG
# collection = db.AIGANG

origins = [
    "http://localhost:8000",
    "http://localhost:3000",

]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.post("/upload/")
async def create_upload_files(files: List[UploadFile] = File(...)):
    for image in files:
        new_name = str(uuid.uuid4())
        with open("uploads/" + image.filename, "wb") as buffer:
            shutil.copyfileobj(image.file, buffer)
        shutil.move("uploads/" + image.filename,
                    "uploads/" + new_name + ".jpg")
        item = {
            "id": new_name,
            "date": datetime.datetime.utcnow(),
            "age": 0,
            "status": "Uploaded"
        }
        # collection.insert_one(item)
    return {"UploadedFileName": new_name + ".jpg", "age": item['age']}


# @app.get("/info/{id}")
# def getInfo(id):
#     return collection.find_one({"id": id}, {'_id': 0})


@app.get("/")
def home():
    return {"Ageprediction API": "Welcome"}
