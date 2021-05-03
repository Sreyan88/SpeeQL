import numpy as np
from flask import Flask, request, jsonify, render_template, redirect, flash
from tqdm import tqdm
import speech_recognition as sr
import speechtotext
import ner
import ocr
import os
import findProduct
import pandas as pd
import quesans
import sys
from werkzeug.utils import secure_filename
import shutil
from transformers import DistilBertTokenizer, DistilBertForQuestionAnswering
import torch
import quesans2

application = Flask(__name__)
application.secret_key = 'super secret key'
application.config['SESSION_TYPE'] = 'filesystem'

@application.route('/')
def home():
    return render_template('index.html')

@application.route('/speech')
def speech():
    return render_template('speechtotext.html')

@application.route('/text')
def text():
    return render_template('text.html')

@application.route('/image')
def image():
    return render_template('image.html')

@application.route('/qna')
def qna():
    return render_template('qna.html')

@application.route('/recom')
def recom():
    return render_template('recom.html')


@application.route('/predict_speech',methods=['POST'])
def predict_speech():
    text = speechtotext.speech()
    entities = ner.sample_analyze_entities(text)
    res, with_brand = findProduct.findProduct(entities)
    to_show = with_brand
    if len(with_brand) == 0:
        to_show = res
    return render_template('speechtotext.html', prediction_text='You have said: {}, Recognised Products are {}'.format(text, entities), tables=[to_show.to_html(classes='data')], titles=to_show.columns.values)

@application.route('/predict_text',methods=['POST'])
def predict_text():
    text = [str(x) for x in request.form.values()][0]
    entities = ner.sample_analyze_entities(text)
    res, with_brand = findProduct.findProduct(entities)
    to_show = with_brand
    if len(with_brand) == 0:
        to_show = res
    return render_template('text.html', prediction_text='You have said: {}, Recognised Products are {}'.format(text, entities), tables=[to_show.to_html(classes='data')], titles=to_show.columns.values)

@application.route('/predict_image',methods=['POST'])
def predict_image():
    folder = r'image'
    file = 'list4.jpg'
    list_products = ocr.ocr(folder, file)
    if list_products:
        entities = ner.sample_analyze_entities(list_products[0])
    if len(list_products)>1:
        for i in list_products[1:]:
            entities += ner.sample_analyze_entities(i)
    try:
        res, with_brand = findProduct.findProduct(entities)
    except IndexError:
        res = pd.DataFrame()
        with_brand = pd.DataFrame()
    to_show = with_brand
    if len(with_brand) == 0:
        to_show = res
    if to_show.empty!=True:
        return render_template('image.html', prediction_text='{}'.format(entities), tables=[to_show.to_html(classes='data')], titles=with_brand.columns.values)
    else:
        return render_template('image.html', predict_text='{}'.format("Sorry we didn't get you. Please try again."))

@application.route('/qna_fun_text',methods=['POST'])
def qna_fun_text():
    question = [str(x) for x in request.form.values()][0]
    answer = quesans2.qna_predict2(question)
    return render_template('qna.html', prediction_text='{}'.format(answer))

@application.route('/qna_fun_speech',methods=['POST'])
def qna_fun_speech():
    question = speechtotext.speech()
    answer = quesans2.qna_predict2(question)
    return render_template('qna.html', prediction_text='{}'.format(answer))

@application.route('/recomend', methods=['POST'])
def recomend():
    cus_id = [int(x) for x in request.form.values()][0]
    cmd = 'python ./retailbox/retailbox/cli.py --customer {} -i --status'.format(cus_id)
    os.system(cmd)
    file = open('output.txt', 'r')
    list = file.read()
    list = list.strip().split('\n')
    df = pd.DataFrame(list, columns={'Products'})
    return render_template('recom.html', tables=[df.to_html(classes='data')], titles=df.columns.values)

@application.route('/upload', methods=['POST'])
def upload():
    if request.method == 'POST':
        # check if the post request has the file part
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']
        # if user does not select file, browser also
        # submit an empty part without filename
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        if file:
            filename = secure_filename(file.filename)
            file.save(os.path.join('./image/', filename))
            if os.path.exists('./image/list4.jpg'):
                os.remove('./image/list4.jpg')
            os.rename('./image/'+filename, './image/list4.jpg')
    return render_template('image.html')

if __name__ == "__main__":
    application.run(debug=True)
