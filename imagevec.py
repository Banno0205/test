from icrawler.builtin import BingImageCrawler
import os
import numpy as np
import tensorflow as tf
import glob 
import pandas as pd
from PIL import Image

df_img_limi_list = [None] * 200


label = "夕方の風景"

model = tf.keras.applications.EfficientNetB0(include_top=False, pooling="avg")
 

def image2vec(image_path):
    try:
        raw = tf.io.read_file(image_path)
        image = tf.image.decode_jpeg(raw, channels=3)
        image = tf.image.resize(image, [224, 224])
        image = tf.keras.applications.efficientnet.preprocess_input(image)
        image_batch = tf.expand_dims(image, 0)
        vec = model.predict(image_batch)[0]
        return vec
    except (tf.errors.InvalidArgumentError, IOError, SyntaxError) as e:
        print(f"Error processing {image_path}: {e}")
        return None  # エラーが発生した場合はNoneを返す

img_list = glob.glob('/Users/bannotaito/Spotify/images'+str(label)+'/*')
df_img_list = pd.DataFrame(index = range(len(img_list)), columns = range(len(image2vec(img_list[1]))))

for i in range(len(img_list)):
    img = img_list[i]
    df_img_list.loc[i] = image2vec(img)
df_img_limi_list = df_img_list.head(200)
df_img_limi_list.to_csv(str(label)+".csv", index=False)

label = "夜の風景"

img_list = glob.glob('/Users/bannotaito/Spotify/images'+str(label)+'/*')
df_img_list = pd.DataFrame(index = range(len(img_list)), columns = range(len(image2vec(img_list[1]))))

for i in range(len(img_list)):
    img = img_list[i]
    df_img_list.loc[i] = image2vec(img)
df_img_limi_list = df_img_list.head(200)
df_img_limi_list.to_csv(str(label)+".csv", index=False)


label = "昼の風景"

img_list = glob.glob('/Users/bannotaito/Spotify/images'+str(label)+'/*')
df_img_list = pd.DataFrame(index = range(len(img_list)), columns = range(len(image2vec(img_list[1]))))

for i in range(len(img_list)):
    img = img_list[i]
    df_img_list.loc[i] = image2vec(img)
df_img_limi_list = df_img_list.head(200)
df_img_limi_list.to_csv(str(label)+".csv", index=False)

label = "雨の風景"

img_list = glob.glob('/Users/bannotaito/Spotify/images'+str(label)+'/*')
df_img_list = pd.DataFrame(index = range(len(img_list)), columns = range(len(image2vec(img_list[1]))))

for i in range(len(img_list)):
    img = img_list[i]
    df_img_list.loc[i] = image2vec(img)
df_img_limi_list = df_img_list.head(200)
df_img_limi_list.to_csv(str(label)+".csv", index=False)

label = "晴れの風景"

img_list = glob.glob('/Users/bannotaito/Spotify/images'+str(label)+'/*')
df_img_list = pd.DataFrame(index = range(len(img_list)), columns = range(len(image2vec(img_list[1]))))

for i in range(len(img_list)):
    img = img_list[i]
    df_img_list.loc[i] = image2vec(img)
df_img_limi_list = df_img_list.head(200)
df_img_limi_list.to_csv(str(label)+".csv", index=False)

label = "曇りの風景"

img_list = glob.glob('/Users/bannotaito/Spotify/images'+str(label)+'/*')
df_img_list = pd.DataFrame(index = range(len(img_list)), columns = range(len(image2vec(img_list[1]))))

for i in range(len(img_list)):
    img = img_list[i]
    df_img_list.loc[i] = image2vec(img)
df_img_limi_list = df_img_list.head(200)
df_img_limi_list.to_csv(str(label)+".csv", index=False)

label = "街中の風景"

img_list = glob.glob('/Users/bannotaito/Spotify/images'+str(label)+'/*')
df_img_list = pd.DataFrame(index = range(len(img_list)), columns = range(len(image2vec(img_list[1]))))

for i in range(len(img_list)):
    img = img_list[i]
    df_img_list.loc[i] = image2vec(img)
df_img_limi_list = df_img_list.head(200)
df_img_limi_list.to_csv(str(label)+".csv", index=False)

label = "自然の風景"

img_list = glob.glob('/Users/bannotaito/Spotify/images'+str(label)+'/*')
df_img_list = pd.DataFrame(index = range(len(img_list)), columns = range(len(image2vec(img_list[1]))))

for i in range(len(img_list)):
    img = img_list[i]
    df_img_list.loc[i] = image2vec(img)
df_img_limi_list = df_img_list.head(200)
df_img_limi_list.to_csv(str(label)+".csv", index=False)