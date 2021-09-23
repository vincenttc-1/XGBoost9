# -*- coding: utf-8 -*-
"""flask.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1iAyiAvlGVEHp_z9Hxbyxm-0LG4GwUSpc"""

# Commented out IPython magic to ensure Python compatibility.
import pandas as pd
from flask import Flask,jsonify,request
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics import accuracy_score
from sklearn.metrics import confusion_matrix
from sklearn.metrics import classification_report
import xgboost
import pickle
from flask_cors import CORS
import json
from Sastrawi.Stemmer.StemmerFactory import StemmerFactory
from Sastrawi.StopWordRemover.StopWordRemoverFactory import StopWordRemoverFactory, StopWordRemover, ArrayDictionary
import re
import string
from flask_cors import CORS
from flask import Flask,jsonify,request,render_template

df2 = pd.DataFrame()
df2['title'] = ['Malaysia Sudutkan RI: Isu Kabut Asap hingga Invasi Babi']

def text_preproc(x):
  #case folding
  x = x.lower()
  #remove double space
  x = re.sub(r'\s{2,}', ' ', x)
  return x

df2['Judul Berita (Bersih)'] = df2['title'].apply(text_preproc)

vectorizer = TfidfVectorizer(binary=True)

#load vectorizer.vocabulary_
kosaKata = pickle.load(open("feature.pkl", "rb"))

#load vectorizer.vocabulary_
xgb_model_loaded = pickle.load(open("xgbmodel.sav", "rb"))

vectorizer.fit(kosaKata)

app = Flask(__name__)
CORS(app)

@app.route("/")
def home():
    return "<h1>Running Flask on Google Colab!</h1>"

@app.route('/api/sentence', methods=["GET"])
def sentece():
    arr_title = []
    title = request.args.get("title")
    arr_title.append(title) 
    clean_arr_title = list(map(text_preproc,arr_title))
    x_sentence = vectorizer.transform(clean_arr_title)
    predict = xgb_model_loaded.predict(x_sentence)
    resp = jsonify({"title":title,"prediction":int(predict[0])})
    return resp

@app.route('/api/file', methods=["POST"])
def byFile():
    request_data = request.get_json()
    print(request_data)
    data_judul = request_data['data']

    arr_text = []

    for f in data_judul :
      arr_text.append(f)

    clean_arr_text = list(map(text_preproc,arr_text))
    x_sentence = vectorizer.transform(clean_arr_text)
    predict = xgb_model_loaded.predict(x_sentence)

    juduls = []
    prediksis = []
    for count,f in enumerate(predict) :
      judul = arr_text[count],
      prediksi = int(f)
      juduls.append(judul)
      prediksis.append(prediksi)

    return jsonify({"text":juduls,"predictions":prediksis})

@app.route('/api/testjson', methods=["POST"])
def postJsonHandler():
    print (request.is_json)
    content = request.get_json()
    print (content)
    return 'JSON posted'

if __name__ == '__main__':
    # Threaded option to enable multiple instances for multiple user access support
    app.run(threaded=True, port=5000)