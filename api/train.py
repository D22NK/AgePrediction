# In dit bestand wordt de ai getrained doormiddel van de circa 10000 test afbeeldingen.


# Importen van alle benodigde modules zoals tensorflow en numpy.
from PIL import Image
import numpy as np
import os, cv2
import tensorflow as tf
from sklearn.model_selection import train_test_split
from tensorflow.keras.applications import MobileNet
import  tensorflow.keras.layers as L

# Een omgevingsvariabele activeren op de computer, dit heeft te maken met het gebruik van de GPU.
os.environ['TF_XLA_FLAGS'] = '--tf_xla_enable_xla_devices'

# De bestandlocaties van de afbeeldingen die gebruikt gaan worden.
PATH = './content/crop_part1'

# Een array maken  met daarin alle namen van de afbeeldingen.
paths = os.listdir(PATH)

# Een array maken met de leeftijds labels van elke afbeelding. 
# Dit wordt gedaan door het deel voor de eerste _ te knippen en aan de array toe te voegen.
labels = np.array([ float(path.split('_')[0]) for path in paths])

# Het laten zien van alle labels in de terminal.
for label in labels:
    print(label)

# De functie die ervoor zorgt dat elke afbeelding het juiste formaat krijgt.
def format_image(path):
    img = cv2.imread(PATH + '/' + path)
    img = cv2.resize(img,(128,128))
    return img

# Een array maken van alle afbeeldingen die geformateerd zijn door de formate_image functie.
data = np.array([format_image(path) for path in paths])

# Instellingen voor de testdata instellen.
train_x,test_x,train_y,test_y = train_test_split(data,labels,test_size=1)

# Het AI model maken met de juiste instellingen.
model = tf.keras.Sequential([
                  MobileNet(
                      input_shape=(128,128,3),
                            include_top=False,
                            pooling='avg',
                            weights='imagenet'),
                             L.Dense(1)
])

# Een samenvatting geven van het model.
model.summary()

# Het model compilen.
model.compile(optimizer='adam',loss='mae',metrics='mae')

# Het model trainen en valideren met de test data.
# batch_size staat hier voor het aantal afbeeldingen dat per keer wordt getest.
# epochs staat voor het aantal trainings rondes dat uitgevoerd moet worden.
model.fit(
    train_x,
    train_y,
    batch_size=32,
    epochs=20 ,
    validation_data=(test_x,test_y)
)

# Het getrainde model opslaan in saved_model.pb
model.save("./")