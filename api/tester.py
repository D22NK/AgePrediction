from PIL import Image
import numpy as np
import os, cv2
import tensorflow as tf


os.environ['TF_XLA_FLAGS'] = '--tf_xla_enable_xla_devices'
model = tf.keras.models.load_model("./")
test_pic = cv2.imread('../../victor.png')
test_pic = cv2.resize(test_pic,(128,128))
test_pic = test_pic.reshape((1,128,128,3))
pred = model.predict(test_pic)
print(pred)