from icrawler.builtin import BingImageCrawler
import os
import numpy as np
import tensorflow as tf
import glob 
import pandas as pd



labels = ["朝の景色"]

for label in labels:
    path = "/Users/bannotaito/Spotify/images" + label
    crawler = BingImageCrawler(storage={'root_dir': path})
    crawler.crawl(keyword=label, max_num=150)


model = tf.keras.applications.EfficientNetB0(include_top=False, pooling="avg")
 

def image2vec(image_path):
    raw = tf.io.read_file(image_path)
    image = tf.image.decode_jpeg(raw, channels=3)
    image = tf.image.resize(image, [224, 224])
    vec = model.predict(np.array([image.numpy()]))[0]
    return vec

img_list = glob.glob('/Users/bannotaito/Spotify/images'+str(label)+'/*')

df_img_list = pd.DataFrame(index = range(len(img_list)), columns = range(len(image2vec(img_list[1]))))

for i in range(len(img_list)):
    img = img_list[i]
    df_img_list.loc[i] = image2vec(img)

df_img_list.to_csv(str(label)+".csv", index=False)
