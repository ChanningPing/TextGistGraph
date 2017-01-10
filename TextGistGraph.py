from flask import Flask, flash, redirect, render_template, request, session, abort,url_for, json,jsonify
import os
import nltk
import pickle
import codecs
import time
import helper


app = Flask(__name__)
#starting point:  http://127.0.0.1:5000/uploadPasteText

@app.route("/")#receive pasted text from users, jump to /visualizeSingleDoc
def index():
    return render_template('UploadPasteText.html')


@app.route('/visualizeSingleDoc', methods=['POST'])
def visualizeSingleDoc():
    # 1. get data from the upload page
    title = request.form['title']#get title of the paper
    content = request.form['content']#get content of the paper
    year = request.form['year']#get year of the paper
    month = request.form['month']#get month of the paper
    print('year='+str(year)+',month='+str(month))

    # 2. process and generate visualization data using helper function
    final_result = helper.JsonResult(content)#use json to store intermediate data
    name = 'data_paragraph' # json data file name
    return render_template('GistGraph.html', name=name, title=title, final_result=json.dumps(final_result))






if __name__ == "__main__":
    app.run()