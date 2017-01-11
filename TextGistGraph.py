from flask import Flask, flash, redirect, render_template, request, session, abort,url_for, json,jsonify
import os
import nltk
import pickle
import codecs
import time
import helper


app = Flask(__name__)
title = ''
content = ''
year = ''
month = ''
user_defined_entities = ''
final_result = {}
comparative_info = {}



#starting point:  http://127.0.0.1:5000/uploadPasteText

@app.route("/")#initial upload page, has 2 versions, with or without the options of visualing collections
def index():
    return render_template('UploadShowTable.html')





@app.route('/visualizeSingleDoc', methods=['POST']) #visualize one paper in unit of paragraphs
def visualizeSingleDoc():
    # 1. get data from the upload page
    global title, content, year, month, user_defined_entities, final_result, comparative_info
    title = request.form['title']#get title of the paper
    content = request.form['content']#get content of the paper
    year = request.form['year']#get year of the paper
    month = request.form['month']#get month of the paper
    user_defined_entities = request.form['user_defined_entities']
    print('year='+str(year)+',month='+str(month))

    # 2. process and generate visualization data using helper function
    final_result = helper.JsonResult(content, user_defined_entities)#use json to store intermediate data

    # 3. store the comparative sentences into a global variable
    #TODO: extract entities and relations of comparative sentences, and use arc diagram to visualize
    #comparative_info = get_comparative_triples(final_result['all_comparative_sentences'])

    # 4. visualize the paper by paragraph
    name = 'data_paragraph' # json data file name
    return render_template('GistGraph.html', name=name, title=title,final_result=json.dumps(final_result))

@app.route('/visualizeSentences', methods=['POST'])#visualize one paper in unit of sentences
def visualizeSentences():
    name = 'data_sentence'
    return render_template('SentenceGistGraph.html', name=name, title=title, final_result=json.dumps(final_result))


@app.route('/visualizeCollection', methods=['POST'])
def visualizeCollection():
    return render_template('CollectionGraph.html', title=title, final_result=json.dumps(final_result))


if __name__ == "__main__":

    app.run()