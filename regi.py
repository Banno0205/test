import spotipy
from spotipy.oauth2 import SpotifyOAuth

# 認証スコープ（必要に応じて追加）
scope = "user-read-private user-read-email playlist-read-private"

# SpotifyOAuth設定
auth_manager = SpotifyOAuth(
    client_id="YOUR_CLIENT_ID",
    client_secret="YOUR_CLIENT_SECRET",
    redirect_uri="http://localhost:8888/callback",  # リダイレクトURI
    scope=scope
)

# Spotifyオブジェクトの作成
sp = spotipy.Spotify(auth_manager=auth_manager)

# ユーザー情報を取得して確認
try:
    user_info = sp.current_user()
    print("User ID:", user_info['id'])
except Exception as e:
    print("Error:", e)
