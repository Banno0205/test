from flask import Flask, request, redirect, render_template, flash, url_for
from werkzeug.utils import secure_filename
import os

UPLOAD_FOLDER = "static/uploads"
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.secret_key = 'secret_key'  # Flashメッセージ用

# アップロード先のフォルダが存在しない場合は作成
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

# 許可されたファイルの確認
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/', methods=['GET', 'POST'])
def upload_file():
    message = ""
    show_text_input = False
    filepath_url = ""

    if request.method == 'POST':
        if 'file' in request.files and request.form.get('stage') == '1':
            # ファイルアップロードの処理
            file = request.files['file']
            if file.filename == '' or not allowed_file(file.filename):
                flash('有効なファイルを選択してください')
                return redirect(request.url)

            filename = secure_filename(file.filename)
            save_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(save_path)

            # URLをWeb用の形式に修正
            filepath_url = url_for('static', filename=f'uploads/{filename}')
            show_text_input = True  # 次のステップを表示

        elif request.form.get('stage') == '2':
            # テキスト入力の確認処理
            text_input = request.form.get('text_input', '').strip()
            message = "yes" if text_input else "no"

    return render_template("appindex.html", show_text_input=show_text_input, message=message, filepath=filepath_url)

if __name__ == "__main__":
    app.run(debug=True)

