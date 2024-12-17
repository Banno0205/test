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

    df = pd.DataFrame(tracks, columns=['name', 'artist', 'id',
                                       'acousticness', 'energy',
                                        'tempo', 'valence'])
    df.to_csv('allplaylist.csv', encoding='utf-8', index=False)
    print("CSVファイルが作成されました。")

    return df

if __name__ == '__main__':
    ids = get_to_playlist_all_tracks("6UOjJK96nz6y4LKToTSlDw")
    df = id_to_csv(ids)
    print(f"読み込んだ曲数: {len(ids)}")

