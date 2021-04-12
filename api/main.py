# Importeren van alle benodigde modules voor Tensorflow
from typing import List
import shutil
from PIL import Image
import numpy as np
import os, cv2
import tensorflow as tf

# Importeren van alle benodigde modules voor de API (Application Programming Interface)
from fastapi import FastAPI, File, UploadFile
from fastapi.responses import HTMLResponse
from fastapi.middleware.cors import CORSMiddleware
import uuid

# Het aanmaken van een api Instance.
app = FastAPI()


# Het instellen van een paar server opties, onderandere de toegestane IP 
# adressen waar verzoeken van zullen worden geaccepeteerd.
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

# Alle verzoeken op /upload worden
@app.post("/upload/")
async def create_upload_files(files: List[UploadFile] = File(...)):
    # Voor elke afbeelding in het verzoek wordt dit stuk uitgevoerd. 
    # In dit geval is het altijd amar een afbeelding.
    for image in files:
        # Er wordt een nieuwe naam id gegenereerd.
        new_name = str(uuid.uuid4())
        # De map voor uploads wordt geopend.
        with open("uploads/" + image.filename, "wb") as buffer:
            shutil.copyfileobj(image.file, buffer)
        # De afbeelding krijgt zijn nieuwe naam.
        shutil.move("uploads/" + image.filename,
                    "uploads/" + new_name + ".jpg")
        # De bestandsnaam & locatie
        filename = new_name + ".jpg"
        filelocation = "./uploads/" + filename
        # Omgevingsvariabele wordt gezet voor de computer.
        os.environ['TF_XLA_FLAGS'] = '--tf_xla_enable_xla_devices'
        # Het getrained ai model wordt geladen
        model = tf.keras.models.load_model("./")
        # De afbeelding wordt geopend
        test_pic = cv2.imread(filelocation)
        # De afbeelding krijgt het juiste formaat
        test_pic = cv2.resize(test_pic,(128,128))
        # De afbeeldingsvorm wordt aangepast
        test_pic = test_pic.reshape((1,128,128,3))
        # Het model wordt gebruikt om de leeftijd te schatten.
        pred = model.predict(test_pic)
        # Het resultaat wordt in een lijst gezet
        age = pred.tolist()\
    # De api stuurt een antwoord op het verzoek van de gebruiker
    return  {"UploadedFileName": filename, "age": round(age[0][0], 0)}

