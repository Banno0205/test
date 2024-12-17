            playlist = sp.user_playlist_create(user=user_id, name='今聴きたい曲', public=True, description='説明文')
            playlist_id = playlist['id']
            print("https://open.spotify.com/playlist/"+str(playlist_id))
            
            URL = "https://open.spotify.com/playlist/"+str(playlist_id)
            sp.playlist_add_items(playlist_id, track_ids)



            def get_to_playlist(playlist_id):
    playlist = sp.playlist(playlist_id)
    track_ids = []
    for item in playlist['tracks']['items']:
        track = item['track']
        # Noneチェックを追加
        if track is not None and track['id'] is not None:
            track_ids.append(track['id'])
    return track_ids