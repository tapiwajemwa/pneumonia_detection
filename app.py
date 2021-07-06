import os
from warnings import filterwarnings
from flask import Flask, flash, request, redirect, url_for,render_template
from werkzeug.utils import secure_filename
from tensorflow.keras.models import load_model
from tensorflow.keras.applications.vgg16 import preprocess_input
import numpy as np
from tensorflow.keras.preprocessing import image
from PIL import Image

UPLOAD_FOLDER = './static/images/'
ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'}
app = Flask(__name__,template_folder='templates')
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['SECRET_KEY'] = 'super secret key'

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':

        # check if the post request has the file part
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)

        file = request.files['file']

        # If the user does not select a file, the browser submits an
        # empty file without a filename.
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            if 'file' in request.files:
                print('tapinda')
                img = Image.open(request.files['file']).convert('L')
                img = img.resize((36,36))
                img = np.asarray(img)
                img = img.reshape((1,36,36,1))
                img = img / 255.0
                model = load_model("models/pneumonia.h5")
                Pred = np.argmax(model.predict(img)[0])
                print(Pred)

                if Pred == 0:
                    prediction = "Result is Normal"
                else:
                    prediction = "Affected By PNEUMONIA"
            
                return render_template('main.html', prediction= prediction)
            else:
                print('hello')
    return render_template('main.html')

if __name__ == '__main__':
    app.run(debug=True)