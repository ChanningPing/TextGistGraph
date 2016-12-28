from flask import Flask, flash, redirect, render_template, request, session, abort,url_for, json
import os
import nltk
import pickle
import codecs
import helper

app = Flask(__name__)
#starting point:  http://127.0.0.1:5000/uploadPasteText

@app.route("/uploadPasteText")#receive pasted text from users, jump to /visualizeSingleDoc
def index():
    return render_template('UploadPasteText.html')


@app.route('/visualizeSingleDoc', methods=['POST'])
def visualizeSingleDoc():
    print(request.form['title'])
    print(request.form['content'])
    #TODO:0. get system time for json file; 1. identify entities;2. identify comparative sentences; 3. generate json file
    name = 'data1'
    helper.main()
    return render_template('GistGraph.html',name=name)

@app.route("/SingleDocVisualize/<string:name>")
def SingleDocVisualize(name):
    return render_template('GistGraph.html',name=name)



#@app.route("/hello/<string:json_file_name>/")
@app.route("/hello")
def hello():
    return render_template('UploadPasteText.html')




if __name__ == "__main__":
    app.run()