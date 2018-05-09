import os
import zipfile
import io
import pathlib
import requests
#from io import BytesIO
from flask import Flask, render_template, request, redirect, url_for, send_file
from werkzeug.utils import secure_filename
from keyframe import keyframe
#from flask.ext.bootstrap import Bootstrap
#from flask.ext.wtf import Form
#from wtforms import FileField, SubmitField, ValidationError


app = Flask(__name__)

APP_ROOT = os.path.dirname(os.path.abspath(__file__))

@app.route("/")
def main():
    return render_template('index.html')

@app.route('/return-file/')
def return_file():
    base_path = pathlib.Path('keyframes')
    data = io.BytesIO()
    with zipfile.ZipFile(data, mode='w') as z:
        for f_name in base_path.iterdir():
            z.write(f_name)
    data.seek(0)
    return send_file(
        data,
        mimetype='application/zip',
        as_attachment=True,
        attachment_filename='keyframe.zip'
    )

@app.route('/return-file1/')
def return_file1():
    base_path = pathlib.Path('images')
    data = io.BytesIO()
    with zipfile.ZipFile(data, mode='w') as z:
        for f_name in base_path.iterdir():
            z.write(f_name)
    data.seek(0)
    return send_file(
        data,
        mimetype='application/zip',
        as_attachment=True,
        attachment_filename='frames.zip'
    )
#@app.route("/upload")
#def file_download():
#    return render_template('downloads.html')

@app.route('/upload', methods=['POST'])
def upload():
    target = os.path.join(APP_ROOT, 'videos/')
    print(target)

    if not os.path.isdir(target):
    	os.mkdir(target)

    for file in request.files.getlist("file"):
    	print(file)
    	filename = file.filename
    	destination= "/".join([target, filename])
        #target =target + filename
    	print(destination)
    	file.save(destination)
    print(destination)
    keyframe(destination)

    return render_template('complete.html')

if __name__ == "__main__":
	app.run(port= 8000, debug = True)
