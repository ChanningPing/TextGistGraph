from flask import Flask, flash, redirect, render_template, request, session, abort,url_for, json,jsonify
import os
import nltk
import pickle
import codecs
import time
import helper
import string


app = Flask(__name__)
title = ''
file_title = ''
content = ''
year = ''
month = ''
user_defined_entities = ''
final_result = {}
comparative_info = {}
title_dict = {}
number_of_papers = 0
paper_scene_dict = [] # key: integer_paper_id; value: {title, }



#starting point:  http://127.0.0.1:5000/uploadPasteText

@app.route("/")#initial upload page, has 2 versions, with or without the options of visualing collections
def index():
    return render_template('UploadShowTable.html')





@app.route('/visualizeSingleDoc', methods=['POST']) #visualize one paper in unit of paragraphs
def visualizeSingleDoc():
    # 1. get data from the upload page
    global title, file_title, content, year, month, user_defined_entities, \
        final_result, comparative_info, sentence_scenes,sentence_scenes_info, \
        number_of_papers
    title = request.form['title']#get title of the paper
    content = request.form['content']#get content of the paper
    year = request.form['year']#get year of the paper
    month = request.form['month']#get month of the paper
    user_defined_entities = request.form['user_defined_entities']


    # get accumulated data
    file_title = str(title).translate(None, string.punctuation) #title without punctuations
    number_of_papers += 1 # how many papers so far, also paper id
    title_dict[number_of_papers] = file_title # key: paper_id, value: paper_title


    # 2. process and generate visualization data using helper function
    final_result = helper.JsonResult(content, user_defined_entities, file_title)#use json to store intermediate data

    # 3. store the cooccurrence sentences into a global variable
    paper_scenes = {}
    paper_scenes['sentence_scenes'] = final_result['scenes']
    paper_scenes['sentence_scenes_info'] = final_result['sentence_scenes_info']
    paper_scene_list.append()



    # 4. visualize the paper by paragraph
    name = file_title + '_paragraphs'  # json data file name
    return render_template('GistGraph.html', name=name, title=title,final_result=json.dumps(final_result))

@app.route('/visualizeSentences', methods=['POST'])#visualize one paper in unit of sentences
def visualizeSentences(): #visualize the paper by sentences
    name = file_title + '_sentences'
    return render_template('SentenceGistGraph.html', name=name, title=title, final_result=json.dumps(final_result))


@app.route('/visualizeCollection', methods=['POST'])
def visualizeCollection():
    return render_template('CollectionGraph.html', title=title, final_result=json.dumps(final_result))


if __name__ == "__main__":

    app.run()