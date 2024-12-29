import os
from flask import Flask, request, redirect, render_template, flash
from werkzeug.utils import secure_filename
from tensorflow.keras.models import Sequential, load_model
from tensorflow.keras.preprocessing import image

import numpy as np

import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import pandas as pd
import tensorflow as tf
from spotipy.oauth2 import SpotifyOAuth

classes = ["奏","One more time, One more chance","恋音と雨空","I'm a mess","Good Time","たしかなこと","瞳をとじて",
           "The Beginning","別の人の彼女になったよ","サクラキミワタシ","ブルーベリー・ナイツ","I WANNA BE YOUR SLAVE",
           "Bling-Bang-Bang-Born","Dance With Me","恋するフォーチュンクッキー"]
image_size = 150

UPLOAD_FOLDER = "static/uploads"
ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg', 'gif'])

app = Flask(__name__)

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def cos_sim(v1, v2):
    """
    スケールの影響を除外したコサイン類似度を計算
    Parameters:
        v1, v2: np.ndarray - 入力ベクトル
    Returns:
        float - コサイン類似度
    """
    # Zスコア正規化
    v1 = (v1 - np.mean(v1)) / np.std(v1) if np.std(v1) != 0 else v1
    v2 = (v2 - np.mean(v2)) / np.std(v2) if np.std(v2) != 0 else v2
    
    # コサイン類似度計算
    return np.dot(v1, v2) / (np.linalg.norm(v1) * np.linalg.norm(v2))

model = load_model('./model.h5')#学習済みモデルをロード

my_id = '15e224ff16bf4d60908897bfb087dcd3'
my_secret = '37a7614b9dc647e6b6f89e94f8487d7e'


# ユーザー認証に変更
sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id=my_id,
                                               client_secret=my_secret,
                                               redirect_uri="http://localhost:8888/callback",
                                               scope="playlist-modify-public,user-read-private"))


@app.route('/', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST' and 'file' in request.files:
        if 'file' not in request.files:
            flash('ファイルがありません')
            return redirect(request.url)
        file = request.files['file']
        if file.filename == '':
            flash('ファイルがありません')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(UPLOAD_FOLDER, filename))
            filepath = os.path.join(UPLOAD_FOLDER, filename)
            print(filepath)

            #受け取った画像を読み込み、np形式に変換
            # img = image.load_img(filepath, grayscale=True, target_size=(image_size,image_size))
            img = image.load_img(filepath,target_size=(image_size,image_size))
            img = image.img_to_array(img)
            img = img / 255.0 
            #img = np.expand_dims(img, axis=0)
            #print(img)
            data = np.array([img])
            #print(data)
            #変換したデータをモデルに渡して予測する
                #受け取った画像を読み込み、np形式に変換
            # img = image.load_img(filepath, grayscale=True, target_size=(image_size,image_size))
            img = image.load_img(filepath,target_size=(image_size,image_size))
            img = image.img_to_array(img)
            img = img / 255.0 
            #img = np.expand_dims(img, axis=0)
            #print(img)
            data = np.array([img])
            #print(data)
            #変換したデータをモデルに渡して予測する
            print(model.predict(data))
            result = model.predict(data)[0]
            print(result)

            np_all_list_2 = [1, 1, 1, 1]
            np_get_list_2 = [1, 1, 1, 1]

            getimage = True

            df_top20=pd.DataFrame()

            df_standard = pd.read_csv("/Users/bannotaito/Spotify/test/standard_playlist.csv")
            num_rows = len(df_standard)
            num_cols = len(df_standard.iloc[0, 3:7])  # 列数を計算
            np_standard_list = np.zeros((num_rows, num_cols))  # 2 次元配列として初期化
            for e in range(len(df_standard.index)):
                np_standard_list[e, :] =  np.array(df_standard.iloc[e, 3:7])
                

            np_get_list_0 = np_standard_list * result[:, np.newaxis]
            np_get_list = np.sum(np_get_list_0, axis=0)


            #allplylist.csvに入っているデータとのコサイン類似度を計算
            df = pd.read_csv("/Users/bannotaito/Spotify/test/allplaylist.csv")

            result_2 = pd.DataFrame(index=range(len(df.index)), columns=range(1))
            result_2.columns = ['類似度']
            num_rows_2 = len(df)
            num_cols_2 = len(df.iloc[0, 3:7])  # 列数を計算
            np_all_list = np.zeros((num_rows_2, num_cols_2))  # 2 次元配列として初期化

            for n in range(len(df.index)):
                np_all_list[n, :] = np.array(df.iloc[n, 3:7])
                np_all_list_2 = np_all_list[n]
                result_2.loc[n,'類似度'] = np.mean(cos_sim(np_all_list_2, np_get_list))


            #計算した類似度をdfに追加し上位50曲に絞る
            df['類似度'] = result_2['類似度'].values
            df_top50 = df.sort_values(by='類似度', ascending=False).head(51)


            df_top_2 = df_top50.iloc[:, [1, 0]].values.tolist()  # リストに変換
            top = df_top_2[:11]
            # 一時保存（再利用用）
            df_top50.to_csv('static/df_top50_temp.csv', index=False)
            return render_template("index.html", top=top, getimage=True, imagefile=filepath)


    if request.method == 'POST' and 'create_playlist' in request.form:
        df_top50 = pd.read_csv('static/df_top50_temp.csv')
        #空のプレイリストを作成し上で作成した上位20曲を入れる
        track_ids = [None] * 50
        user_id = sp.current_user()['id']
        playlist = sp.user_playlist_create(user=user_id, name='今聴きたい曲', public=True, description='説明文')
        playlist_id = playlist['id']
        for t in range(50):
            track_ids[t] = df_top50.iloc[t,2]
        print("https://open.spotify.com/playlist/"+str(playlist_id))
        URL = "https://open.spotify.com/playlist/"+str(playlist_id)
        sp.playlist_add_items(playlist_id, track_ids)
        URLready = True
        return render_template("index.html", answer=URL, URLready=URLready, getimage=True)

    return render_template("index.html",answer="")

if __name__ == "__main__":
    port = int(os.environ.get('PORT', 8080))
    app.run(host ='0.0.0.0',port = port)