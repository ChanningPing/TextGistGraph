from flask import Flask, flash, redirect, render_template, request, session, abort,url_for, json,jsonify
import os
import nltk
import pickle
import codecs
import time
import helper
import string
import collectionNetwork
from settings import APP_STATIC


app = Flask(__name__)
title = ''
file_title = ''
content = ''
year = ''
month = ''
user_defined_entities = ''
final_result = {}
comparative_info = {}
paper_scene_list = []



#starting point:  http://127.0.0.1:5000/uploadPasteText

@app.route("/")#initial upload page, has 2 versions, with or without the options of visualing collections
def index():
    return render_template('UploadShowTable.html')





@app.route('/visualizeSingleDoc', methods=['POST']) #visualize one paper in unit of paragraphs
def visualizeSingleDoc():
    # 1. get data from the upload page
    global title, file_title, content, year, month, user_defined_entities, \
        final_result, comparative_info, sentence_scenes,sentence_scenes_info, \
        paper_scene_list
    title = request.form['title']#get title of the paper
    content = request.form['content']#get content of the paper
    year = request.form['year']#get year of the paper
    month = request.form['month']#get month of the paper
    user_defined_entities = request.form['user_defined_entities']


    # get accumulated data
    file_title = str(title).translate(None, string.punctuation) #title without punctuations


    # 2. process and generate visualization data using helper function
    final_result = helper.JsonResult(content, user_defined_entities, file_title)#use json to store intermediate data

    # 3. store the cooccurrence sentences into a global variable
    paper_scenes = {}
    paper_scenes['sentence_scenes'] = final_result['scenes']
    paper_scenes['sentence_scenes_info'] = final_result['sentence_scenes_info']
    paper_scenes['year'] = year
    paper_scenes['month'] = month
    paper_scenes['title'] = file_title
    paper_scene_list.append(paper_scenes)





    # 4. visualize the paper by paragraph
    name = file_title + '_paragraphs'  # json data file name
    return render_template('GistGraph.html', name=name, title=title,final_result=json.dumps(final_result))

@app.route('/visualizeSentences', methods=['POST'])#visualize one paper in unit of sentences
def visualizeSentences(): #visualize the paper by sentences
    name = file_title + '_sentences'
    return render_template('SentenceGistGraph.html', name=name, title=title, final_result=json.dumps(final_result))


@app.route('/visualizeCollectionNetwork', methods=['POST'])
def visualizeCollectionNetwork():
    #print(paper_scene_list)
    network_data = collectionNetwork.generate_network(paper_scene_list)
    #especially for test
    #with open(APP_STATIC + '/data/' +'All_LDA_Paper_network.json') as data_file:
        #network_data = json.load(data_file)

    return render_template('CollectionGraphNetwork.html', title=title, network_data = json.dumps(network_data))

@app.route('/visualizeCollectionArcDiagram', methods=['POST'])
def visualizeCollectionArcDiagram():
    #print(paper_scene_list)
    network_data = collectionNetwork.generate_network(paper_scene_list)
    return render_template('CollectionGraph.html', title=title, network_data = json.dumps(network_data))

if __name__ == "__main__":

    app.run()