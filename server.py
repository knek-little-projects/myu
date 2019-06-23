import os
from flask import Flask, request, redirect, url_for
from werkzeug.utils import secure_filename
from flask import send_from_directory
from process import mix


UPLOAD_FOLDER = r'uploads'
ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'}

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS


@app.route('/', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        file = request.files['file']
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            savepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(savepath)
            video_path = mix(savepath)
            return redirect(url_for('uploaded_file', filename='out.mp4'))
    return '''
<!doctype html>
<title>Upload image</title>
<h1>Upload image</h1>
<form action="" method=post enctype=multipart/form-data>
  <p><input type=file name=file>
    <input type=submit value="Upload image">
</form>

'''


@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], "out.mp4", as_attachment=True)



if __name__ == '__main__':
    os.makedirs("uploads", exist_ok=True)
    app.run()
