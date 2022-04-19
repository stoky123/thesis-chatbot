from flask import Flask, render_template, request
import webbrowser
import numpy as np
import tensorflow
from tensorflow import keras
from sklearn.preprocessing import LabelEncoder
import preprocessing
import pickle
import os


gpus = tensorflow.config.experimental.list_physical_devices('GPU')
if gpus:
    try:
        tensorflow.config.experimental.set_virtual_device_configuration(
            gpus[0], [tensorflow.config.experimental.VirtualDeviceConfiguration(memory_limit=1200)])
        pass
    except RuntimeError as e:
        print(e)

ROOT_DIR = os.path.dirname(os.path.abspath(__file__))

model = keras.models.load_model(
    ROOT_DIR + '\\final_model')

with open(ROOT_DIR + '\\tokenizer.pickle', 'rb') as handle:
    tokenizer = pickle.load(handle)

with open(ROOT_DIR + '\\answer_encoder.pickle', 'rb') as enc:
    answer_encoder = pickle.load(enc)

with open(ROOT_DIR + '\\sentiment_encoder.pickle', 'rb') as enc:
    sentiment_encoder = pickle.load(enc)

max_len = 128


def chat(message):
    inp = preprocessing.preprocess(message)

    result = model.predict(keras.preprocessing.sequence.pad_sequences(tokenizer.texts_to_sequences([inp]),
                                                                      truncating='post', maxlen=max_len))

    answer = answer_encoder.inverse_transform([np.argmax(result[0])])
    sentiment = sentiment_encoder.inverse_transform(
        [np.argmax(result[1])]) - message.isupper()

    if max(result[0][0]) < 0.6:
        return "I'm not really sure about that question. Please ask me another one!<septoken>3"

    return answer[0] + "<septoken>" + str(int(sentiment[0]))


app = Flask(__name__)
app.static_folder = 'static'


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/get")
def get_bot_response():
    userText = request.args.get('message')
    return chat(userText)


if __name__ == "__main__":
    webbrowser.open("http://127.0.0.1:5000/")
    app.run()
