import numpy as np
import tensorflow as tf
import glob 
import pandas as pd


model = tf.keras.applications.EfficientNetB0(include_top=False, pooling="avg")
 


def image2vec(image_path):
    raw = tf.io.read_file(image_path)
    image = tf.image.decode_jpeg(raw, channels=3)
    image = tf.image.resize(image, [224, 224])
    vec = model.predict(np.array([image.numpy()]))[0]
    return vec

path = input("入力してください")
np.img_list = image2vec(path)

def cos_sim(v1, v2):
    return np.dot(v1, v2) / (np.linalg.norm(v1) * np.linalg.norm(v2))


situ_list = ("自然の風景","街中の風景","昼の風景","夕方の風景","夜の風景","晴れの風景","曇りの風景","雨の風景")
df_result = pd.DataFrame(index = range(200),columns = [0] )
top_list = [None] * 8
result_list = [None] * 3
situ_cal_top50_list = [None] * 50
situ_cal_list = [None] * 50

#各シチュエーションのcsvファイルを開く
for i in range(len(situ_list)):
    ipath = str(situ_list[i])+'.csv'
    df = pd.read_csv(ipath)
    #開いたcsvファイルに入っているデータとのコサイン類似度を計算
    for n in range(len(df.index)):
        np.situ_list = np.array(df.iloc[n, :])
        df_result.iloc[n,:] = cos_sim(np.img_list, np.situ_list)
    #コサイン類似度の上位50個の平均を計算
    df_result_top50 = df_result.sort_values(by=df_result.columns[0], ascending=False).head(50)
    top_list[i] = df_result_top50.iloc[:, 0].sum()/50
    top_list[i]
    #コサイン類似度を計算するためのリセット
    df_result.loc[:,:] = 0

#各シチェーションに対して得られたコサイン類似度の平均を比較するために変数に代入

shizen = top_list[0]
machinaka = top_list[1]
hiru = top_list[2]
yugata = top_list[3]
yoru = top_list[4]
hare = top_list[5]
kumori = top_list[6]
ame = top_list[7]

print(top_list)

#各シチェーションに対して得られたコサイン類似度の平均を比較することで環境を識別

#自然か街中か識別
if(shizen > machinaka):
    result_list[0]='自然'
else:
    result_list[0]='街中'

#時間帯を識別
if(hiru > yugata and hiru > yoru):
    result_list[1]='昼'
elif(yugata > hiru and yugata > yoru):
    result_list[1]='夕方'
elif(yoru > hiru and yoru > yugata):
    result_list[1]='夜'

#気候を識別
if(hare > kumori and hare > ame):
    result_list[2]='晴れ'
elif(kumori > hare and kumori > ame):
    result_list[2]='曇り'
elif(ame > hare and ame > kumori):
    result_list[2]='雨'


print(result_list)





