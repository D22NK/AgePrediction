from PIL import Image
import numpy as np
import os, cv2
import tensorflow as tf
from sklearn.model_selection import train_test_split
from tensorflow.keras.applications import MobileNet
import  tensorflow.keras.layers as L
os.environ['TF_XLA_FLAGS'] = '--tf_xla_enable_xla_devices'
PATH = './content/crop_part1'
paths = os.listdir(PATH)
labels = np.array([ float(path.split('_')[0]) for path in paths])

for label in labels:
    print(label)
    
def format_image(path):
    img = cv2.imread(PATH + '/' + path)
    img = cv2.resize(img,(128,128))
    return img

print('creating data')
data = np.array([format_image(path) for path in paths])
train_x,test_x,train_y,test_y = train_test_split(data,labels,test_size=1)
model = tf.keras.Sequential([
                  MobileNet(
                      input_shape=(128,128,3),
                            include_top=False,
                            pooling='avg',
                            weights='imagenet'),
                             L.Dense(1)
])
model.summary()
print('compiling model')
model.compile(optimizer='adam',loss='mae',metrics='mae')

print('fitting model')
model.fit(
    train_x,
    train_y,
    batch_size=32,
    epochs=20 ,
    validation_data=(test_x,test_y)
)
print('saving model')
model.save("./")

print('Testing image')
model = tf.keras.models.load_model("./")
test_pic = cv2.imread('mark.jpg')
test_pic = cv2.resize(test_pic,(128,128))
test_pic = test_pic.reshape((1,128,128,3))
pred = model.predict(test_pic)
print(pred)