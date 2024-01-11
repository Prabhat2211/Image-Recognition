import cv2
from flask import Flask, render_template, request,  url_for, Response, redirect
from flask_socketio import SocketIO
import tensorflow as tf
from keras.models import load_model
import keras.utils as image
import keras
import numpy as np
import os
from PIL import Image
import base64
import time
from threading import Thread


app = Flask(__name__, template_folder='templates', static_folder='static')

model = load_model('img_rec.h5')
model_zomato = load_model('img_rec_zomato.h5')
app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app)

camera = cv2.VideoCapture(0)
frame = None
UPLOAD_FOLDER = 'static/uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

def preprocess_image(img):
    img = cv2.resize(img,(150, 150))  # Resize image to fit model input
    img = image.img_to_array(img)
    img = np.expand_dims(img, axis=0)
    return img

def classify_image(image):
     prediction = model.predict(image)
     p = {1:'human_detected',0:'no human detected'}
     result = p[round(prediction[0][0])]
     if result == 'human_detected':
         predictionz = model_zomato.predict(image)
         pz = {1:'zomato_delivery_boy',0:'others'}
         result = (result, pz[round(predictionz[0][0])])
     return result
	
def video_feed():
    global frame
    while True:
        success, frame = camera.read()
        if not success:
            break
        else:
            # Perform classification on the captured frame
            image = preprocess_image(frame)
            result = classify_image(image)

            # Display the result on the frame
            cv2.putText(frame, f"Class: {result}", (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
            
            ret, buffer = cv2.imencode('.jpg', frame)
            frame = base64.b64encode(buffer).decode('utf-8')
            time.sleep(10)


@app.route('/', methods=['GET', 'POST'])
def main():
    if request.method == 'POST' and 'file' in request.files:
        uploaded_file = request.files['file']
        # file.save(os.path.join(app.config['UPLOAD_FOLDER'], uploaded_file))
        # image_path = url_for('static', filename=f'uploads/{uploaded_file}')

        img = np.array(Image.open(uploaded_file).resize((150,150)))
        img = img / 255.0  
        img = np.expand_dims(img, axis=0)
        result1 = classify_image(img)

        return render_template('result.html', prediction=result1)

    return render_template('index4.html', image=frame)
	
if __name__ == '__main__':
    video_thread = Thread(target=video_feed)
    video_thread.daemon = True
    video_thread.start()
    socketio.run(app)
