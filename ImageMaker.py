import os
import tensorflow as tf
# import IPython.display as display

import matplotlib.pyplot as plt
import matplotlib as mpl


import numpy as np
import PIL.Image
import time
import ssl
import random

import functools
# Load compressed models from tensorflow_hub
ssl._create_default_https_context = ssl._create_unverified_context

def style_transfer():
    mpl.rcParams['figure.figsize'] = (12, 12)
    mpl.rcParams['axes.grid'] = False
    os.environ['TFHUB_MODEL_LOAD_FORMAT'] = 'COMPRESSED'

def tensor_to_image(tensor):
    tensor = tensor*255
    tensor = np.array(tensor, dtype=np.uint8)
    if np.ndim(tensor)>3:
        assert tensor.shape[0] == 1
        tensor = tensor[0]
  
    return PIL.Image.fromarray(tensor)

def load_img(path_to_img):
    max_dim = 512
    img = tf.io.read_file(path_to_img)
    img = tf.image.decode_image(img, channels=3)
    img = tf.image.convert_image_dtype(img, tf.float32)

    shape = tf.cast(tf.shape(img)[:-1], tf.float32)
    long_dim = max(shape)
    scale = max_dim / long_dim

    new_shape = tf.cast(shape * scale, tf.int32)

    img = tf.image.resize(img, new_shape)
    img = img[tf.newaxis, :]

    return img

def imshow(image, title=None):
    if len(image.shape) > 3:
        image = tf.squeeze(image, axis=0)

    plt.imshow(image)
    if title:
        plt.title(title)
        plt.show()

def start(content_path):

    r = (random.randint(0,1))
    if r ==1 :
        style_path = "/Users/abigailmarks/Downloads/ImageGleaner 2/tree.jpg"
    else:
        style_path = "/Users/abigailmarks/Downloads/ImageGleaner 2/blugrass.jpg"
    content_image = load_img(content_path)
    style_image = load_img(style_path)
   

    import tensorflow_hub as hub
    hub_model = hub.load('https://tfhub.dev/google/magenta/arbitrary-image-stylization-v1-256/2')
    stylized_image = hub_model(tf.constant(content_image), tf.constant(style_image))[0]
    tensor_to_image(stylized_image).save(content_path)
    print("done")

if __name__=="__main__":
    start("sunny.png")