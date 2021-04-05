from typing import List
import shutil
from fastapi import FastAPI, File, UploadFile
from fastapi.responses import HTMLResponse
import uuid

from fastapi.middleware.cors import CORSMiddleware
from PIL import Image
import numpy as np
import os, cv2
import tensorflow as tf

app = FastAPI()


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
        filename = new_name + ".jpg"
        filelocation = "./uploads/" + filename
        os.environ['TF_XLA_FLAGS'] = '--tf_xla_enable_xla_devices'
        model = tf.keras.models.load_model("./")
        test_pic = cv2.imread(filelocation)
        test_pic = cv2.resize(test_pic,(128,128))
        test_pic = test_pic.reshape((1,128,128,3))
        pred = model.predict(test_pic)
        age = pred.tolist()
    return  {"UploadedFileName": filename, "age": round(age[0][0], 0)}

