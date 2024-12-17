import pandas as pd

# CSVファイルの読み込み
df = pd.read_csv('myplaylist.csv')

# パラメータのリスト
parameters = ['danceability', 'acousticness', 'energy', 'instrumentalness', 
              'liveness', 'loudness', 'speechiness', 'tempo', 'valence']

# 各パラメータのトップ5を格納するためのリスト
top5_tracks = []

# 各パラメータのトップ5を取得してリストに追加
for param in parameters:
    top5 = df[['name', 'artist', param]].sort_values(by=param, ascending=False).head(5)
    top5['parameter'] = param  # パラメータ名を追加
    top5_tracks.append(top5)

# 全てのトップ5データを1つのDataFrameにまとめる
top5_df = pd.concat(top5_tracks)

# CSVファイルに出力
top5_df.to_csv('top5_parameters.csv', index=False, encoding='utf-8')
print("トップ5の各パラメータが 'top5_parameters.csv' に保存されました。")

