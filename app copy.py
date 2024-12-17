import os
from flask import Flask, request, redirect, render_template, flash
from werkzeug.utils import secure_filename
from tensorflow.keras.models import Sequential, load_model
from tensorflow.keras.preprocessing import image

import numpy as np

import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import pandas as pd
import pprint
import tensorflow as tf
import glob 
from spotipy.oauth2 import SpotifyOAuth

classes = ["奏","One more time, One more chance","恋音と雨空","I'm a mess","Good Time","たしかなこと","瞳をとじて",
           "The Beginning","別の人の彼女になったよ","サクラキミワタシ","ブルーベリー・ナイツ","I WANNA BE YOUR SLAVE",
           "Bling-Bang-Bang-Born","Dance With Me","恋するフォーチュンクッキー"]
image_size = 150

UPLOAD_FOLDER = "static/uploads"
ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg', 'gif'])

app = Flask(__name__)
app.secret_key = 'secret_key'  

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def cos_sim(v1, v2):
    return np.dot(v1, v2) / (np.linalg.norm(v1) * np.linalg.norm(v2))

# プレイリストから曲を取得
def get_to_playlist_all_tracks(playlist_id):
    track_ids = []
    offset = 0

    while True:
        response = sp.playlist_tracks(playlist_id, offset=offset)
        for item in response['items']:
            track = item['track']
            # track と track['id'] が有効であるかをチェック
            if track is not None and track['id'] is not None:
                track_ids.append(track['id'])

        offset += len(response['items'])
        if len(response['items']) == 0:  # すべて取得済み
            break

    return track_ids
# 楽曲のオーディオ特性を取得
def getTrackFeatures(id):
    meta = sp.track(id)
    features = sp.audio_features(id)

    name = meta['name']
    artist = meta['album']['artists'][0]['name']
    id = meta['id']
    acousticness = features[0]['acousticness']
    energy = features[0]['energy']
    tempo = features[0]['tempo']
    valence = features[0]['valence']

    track = [name, artist, id, acousticness,
             energy, tempo, valence]
    return track

# プレイリストの曲情報をCSVに変換
def id_to_csv(track_ids):
    tracks = []
    for track_id in track_ids:
        track = getTrackFeatures(track_id)
        tracks.append(track)

    df_make = pd.DataFrame(tracks, columns=['name', 'artist', 'id',
                                       'acousticness', 'energy',
                                        'tempo', 'valence'])
    df_make.to_csv('allplaylist.csv', encoding='utf-8', index=False)
    print("CSVファイルが作成されました。")

    return df_make


model = load_model('./model.h5')#学習済みモデルをロード

my_id = '15e224ff16bf4d60908897bfb087dcd3'
my_secret = '68d3c057a7af489ebdae3ce4b323530f'


# ユーザー認証に変更
sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id=my_id,
                                               client_secret=my_secret,
                                               redirect_uri="http://localhost:8888/callback",
                                               scope="playlist-modify-public,user-read-private"))


@app.route('/', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
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

            if request.form.get('stage') == '1':
                #受け取った画像を読み込み、np形式に変換
                # img = image.load_img(filepath, grayscale=True, target_size=(image_size,image_size))
                img = image.load_img(filepath,target_size=(image_size,image_size))
                img = image.img_to_array(img)
                img = img / 255.0 
                #img = np.expand_dims(img, axis=0)
                data = np.array([img])
                #変換したデータをモデルに渡して予測する
                #受け取った画像を読み込み、np形式に変換
                # img = image.load_img(filepath, grayscale=True, target_size=(image_size,image_size))
                img = image.load_img(filepath,target_size=(image_size,image_size))
                img = image.img_to_array(img)
                img = img / 255.0 
                #img = np.expand_dims(img, axis=0)
                data = np.array([img])
                #変換したデータをモデルに渡して予測する
                print(model.predict(data))
                result = model.predict(data)[0]
                print(result)

                getimage = True
                
                return render_template("index.html", getimage=getimage, imagefile=filepath)

            print("Received stage:", request.form.get('stage'))

            if request.form.get('stage', '').strip() == '2':
                getplaylistid = request.form.get('getplaylistid', '').strip()  # フォームから値を取得
                getplaylist_id = getplaylistid if getplaylistid else "6UOjJK96nz6y4LKToTSIDw"

                
                ids = get_to_playlist_all_tracks(getplaylist_id)
                df_make = id_to_csv(ids)
                print(f"読み込んだ曲数: {len(ids)}")
                
                
                np_all_list_2 = [1, 1, 1, 1]
                np_get_list_2 = [1, 1, 1, 1]

                df_top20=pd.DataFrame()

                df_standard = pd.read_csv("/Users/bannotaito/Spotify/test/standard_playlist.csv")
                num_rows = len(df_standard)
                num_cols = len(df_standard.iloc[0, 3:7])  # 列数を計算
                np_standard_list = np.zeros((num_rows, num_cols))  # 2 次元配列として初期化

                for e in range(len(df_standard.index)):
                    np_standard_list[e, :] =  np.array(df_standard.iloc[e, 3:7])
                

                np_get_list_0 = np_standard_list * result[:, np.newaxis]
                np_get_list = np.sum(np_get_list_0, axis=0)

                print("np_standard_list")
                print(np_standard_list)

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

                print("result_2")
                print(result_2)
                print("np_all_list")
                print(np_all_list)
            

                #計算した類似度をdfに追加し上位50曲に絞る
                df['類似度'] = result_2['類似度'].values
                df_top50 = df.sort_values(by='類似度', ascending=False).head(51)
                print(df_top50)
                print("ここから")
                print(np_get_list_0)
                print(np_get_list)

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
                return render_template("index.html", getimage=False, answer=URL, imagefile=filepath)
                answer = True


        flash("許可されていないファイル形式です。")
        return redirect(request.url)

    return render_template("index.html", answer="")

if __name__ == "__main__":
    port = int(os.environ.get('PORT', 8080))
    app.run(host ='0.0.0.0',port = port)