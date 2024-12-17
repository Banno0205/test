import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import pandas as pd
import pprint

my_id = '15e224ff16bf4d60908897bfb087dcd3'
my_secret = '68d3c057a7af489ebdae3ce4b323530f'

# クライアント認証の設定
client_credentials_manager = SpotifyClientCredentials(client_id=my_id, client_secret=my_secret)
sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)

# プレイリストから曲を取得
def get_to_playlist(playlist_id):
    playlist = sp.playlist(playlist_id)
    track_ids = []
    for item in playlist['tracks']['items']:
        track = item['track']
        if not track['id'] in track_ids:
            track_ids.append(track['id'])
    return track_ids

def get_to_playlist(playlist_id):
    playlist = sp.playlist(playlist_id)
    track_ids = []
    for item in playlist['tracks']['items']:
        track = item['track']
        # Noneチェックを追加
        if track is not None and track['id'] is not None:
            track_ids.append(track['id'])
    return track_ids

# 楽曲のオーディオ特性を取得
def getTrackFeatures(id):
    meta = sp.track(id)
    features = sp.audio_features(id)

    name = meta['name']
    album = meta['album']['name']
    artist = meta['album']['artists'][0]['name']
    length = meta['duration_ms']
    popularity = meta['popularity']
    key = features[0]['key']
    mode = features[0]['mode']
    danceability = features[0]['danceability']
    acousticness = features[0]['acousticness']
    energy = features[0]['energy']
    instrumentalness = features[0]['instrumentalness']
    liveness = features[0]['liveness']
    loudness = features[0]['loudness']
    speechiness = features[0]['speechiness']
    tempo = features[0]['tempo']
    time_signature = features[0]['time_signature']
    valence = features[0]['valence']

    track = [name, album, artist, length, popularity, key, mode, danceability, acousticness,
             energy, instrumentalness, liveness, loudness, speechiness, tempo, time_signature, valence]
    return track

# プレイリストの曲情報をCSVに変換
def id_to_csv(track_ids):
    tracks = []
    for track_id in track_ids:
        track = getTrackFeatures(track_id)
        tracks.append(track)

    df = pd.DataFrame(tracks, columns=['name', 'album', 'artist', 'length', 'popularity', 'key', 'mode', 'danceability',
                                       'acousticness', 'energy', 'instrumentalness', 'liveness', 'loudness', 
                                       'speechiness', 'tempo', 'time_signature', 'valence'])
    df.to_csv('myplaylist.csv', encoding='utf-8', index=False)
    print("CSVファイルが作成されました。")

    return df

if __name__ == '__main__':
    ids = get_to_playlist("69lcqXeFoDDGbfKxptVwJF")
    id_to_csv(ids)
