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

            # 画像をモデルに渡して予測する
            img = image.load_img(filepath, target_size=(image_size, image_size))
            img = image.img_to_array(img) / 255.0
            data = np.array([img])
            result = model.predict(data)[0]

            # データベースとコサイン類似度の計算
            df = pd.read_csv("/Users/bannotaito/Spotify/test/allplaylist.csv")
            num_rows = len(df)
            np_all_list = np.zeros((num_rows, 4))  # 4列分の配列

            result_2 = pd.DataFrame(index=range(len(df.index)), columns=['類似度'])
            for n in range(num_rows):
                np_all_list[n, :] = np.array(df.iloc[n, 3:7])
                result_2.loc[n, '類似度'] = np.mean(cos_sim(np_all_list[n], result))

            # 上位50曲を抽出
            df['類似度'] = result_2['類似度'].values
            df_top50 = df.sort_values(by='類似度', ascending=False).head(51)

            # 表示用データ
            df_top_2 = df_top50.iloc[:, [1, 0]].values.tolist()
            top = df_top_2[:11]

            # データを一時保存 (プレイリスト作成用に渡す)
            df_top50.to_csv('static/df_top50_temp.csv', index=False)

            return render_template("index2.html", top=top, getimage=True, imagefile=filepath)

    return render_template("index2.html")


@app.route('/create_playlist', methods=['POST'])
def create_playlist():
    # 一時保存したデータを読み込む
    df_top50 = pd.read_csv('static/df_top50_temp.csv')

    # プレイリスト作成
    user_id = sp.current_user()['id']
    playlist = sp.user_playlist_create(user=user_id, name='今聴きたい曲', public=True, description='説明文')
    playlist_id = playlist['id']

    # トラックを追加
    track_ids = df_top50.iloc[:50, 2].tolist()
    sp.playlist_add_items(playlist_id, track_ids)

    # プレイリストURL
    URL = f"https://open.spotify.com/playlist/{playlist_id}"
    return render_template("index2.html", answer=URL)
