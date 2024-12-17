import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import pandas as pd
import pprint
import numpy as np
import tensorflow as tf
import glob 
from spotipy.oauth2 import SpotifyOAuth


my_id = '15e224ff16bf4d60908897bfb087dcd3'
my_secret = '68d3c057a7af489ebdae3ce4b323530f'


# クライアント認証からユーザー認証に変更
sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id=my_id,
                                               client_secret=my_secret,
                                               redirect_uri="http://localhost:8888/callback",
                                               scope="playlist-modify-public,user-read-private"))


def cos_sim(v1, v2):
    return np.dot(v1, v2) / (np.linalg.norm(v1) * np.linalg.norm(v2))


np_get_list = np.array([0.00106, 0.792, 124.997, 0.733])
np_all_list = np.array([1, 1, 1, 1])

df_top20=pd.DataFrame()




#allplylist.csvに入っているデータとのコサイン類似度を計算
df = pd.read_csv("/Users/bannotaito/Spotify/test/allplaylist.csv")
result = pd.DataFrame(index=range(len(df.index)), columns=['類似度'])

for n in range(len(df.index)):
    np_all_list = np.array(df.iloc[n, 3:7])
    result.at[n,'類似度'] = cos_sim(np_all_list, np_get_list)

#計算した類似度をdfに追加し上位20曲に絞る
df['類似度'] = result['類似度'].values
df_top20 = df.sort_values(by='類似度', ascending=False).head(21)
print(df_top20)


#空のプレイリストを作成し上で作成した上位20曲を入れる
track_ids = [None] * 20
user_id = sp.current_user()['id']
playlist = sp.user_playlist_create(user=user_id, name='今聴きたい曲', public=True, description='説明文')
playlist_id = playlist['id']
for t in range(20):
    track_ids[t] = df_top20.iloc[t,2]
print("https://open.spotify.com/playlist/"+str(playlist_id))
sp.playlist_add_items(playlist_id, track_ids)

