def log(string): 
    l = (len(string) + 8)
    print()
    print('  ' + ('-' * l))
    print('  |   ' + string + '   |')
    print('  ' + ('-' * l))
    print()

log("Importing modules")

import keras.models as keras
import tensorflow as tf
from PIL import Image
from io import BytesIO
import numpy as np
import base64
import flask
import os

app = flask.Flask(__name__)

log("Loading model")

model = keras.load_model('Model.h5') # Load Keras model 
model._make_predict_function()
graph = tf.get_default_graph()

if not os.path.exists('images'):  os.makedirs('images') # Create images folder if it doesn't exist

images = [None] * (len(next(os.walk('images'))[2]) + 1) # Create empty array with size of number of images in 'images' folder. 


# --------------
#     Routes
# --------------

@app.route('/js/<path:path>')
def send_js(path):
    return flask.send_from_directory('web_client/js', path)


@app.route('/css/<path:path>')
def send_css(path):
    return flask.send_from_directory('web_client/css', path)


@app.route('/images/<path:path>')
def send_image(path):
    return flask.send_from_directory('web_client/images', path)


@app.route('/audio/<path:path>')
def send_audio(path):
    return flask.send_from_directory('web_client/audio', path)



@app.route("/")
def root():
    return flask.send_file('web_client/html/predict.html')


@app.route("/results", methods=['POST'])
def process():

    id = len(images)

    images.append('Processing')

    b64 = flask.request.form["image"]
    b64 = b64.replace('data:image/png;base64,', '')

    b64 = base64.b64decode(b64)

    file = 'images/image_' + format(id, '03') + '.png'

    img = Image.open(BytesIO(b64))

    img = img.crop((80, 0, 480, 480))
    img = img.resize((128, 128))

    img = img.convert('RGB')

    img.save(file, 'png')

    img = np.array(img) / 255
    img = np.expand_dims(img, axis = 0)

    with graph.as_default():
        pred = float(model.predict(img))
        
        log('Prediction for image ' + format(id, '03') + ': ' + str(round(pred, 3)))

        if pred <= 0.5:  return flask.send_file('web_client/html/ok.html')
        else:            return flask.send_file('web_client/html/infected.html')


if __name__ == "__main__": 
    log("Server started!")
    app.run(port = 8080)

