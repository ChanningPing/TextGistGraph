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
    title = request.form['title']#get title of the paper
    content = request.form['content']#get content of the paper
    timestamp = time.strftime("%Y%m%d_%H%M%S")#get current system time
    dataFile = 'file_'+timestamp + '.json'#use timestamp as data file name

    result = helper.JsonResult( content)#use json to store intermediate data
    #print(result)

    data = {
        "characters": [
            {
                "id": "EMPTY",
                "name": "",
                "affiliation": "light"
            },
            {
                "id": "R2D",
                "name": "LDA",
                "affiliation": "light"
            },
            {
                "id": "abc1",
                "name": "ABC",
                "affiliation": "light"
            },
            {
                "id": "def2",
                "name": "DEF",
                "affiliation": "light"
            },
            {
                "id": "C3P",
                "name": "Poisson",
                "affiliation": "light"
            },
            {
                "id": "RO1",
                "name": "Rebel Officers",
                "affiliation": "light"
            },
            {
                "id": "ST1",
                "name": "Stormtroopers",
                "affiliation": "dark"
            },
            {
                "id": "DV1",
                "name": "Anakin Skywalker / Darth Vader",
                "affiliation": "vader"
            },
            {
                "id": "PL1",
                "name": "Princess Leia Organa",
                "affiliation": "light"
            },
            {
                "id": "JW1",
                "name": "Jawas",
                "affiliation": "other"
            },
            {
                "id": "LS1",
                "name": "Luke Skywalker",
                "affiliation": "light"
            },
            {
                "id": "OL1",
                "name": "Owen Lars",
                "affiliation": "other"
            },
            {
                "id": "BL1",
                "name": "Beru Lars",
                "affiliation": "other"
            },
            {
                "id": "TR1",
                "name": "Tusken Raiders",
                "affiliation": "other"
            },
            {
                "id": "OB1",
                "name": "Obi-Wan Kenobi",
                "affiliation": "light"
            },
            {
                "id": "GT1",
                "name": "General Tagge",
                "affiliation": "dark"
            },
            {
                "id": "AM1",
                "name": "Admiral Motti",
                "affiliation": "dark"
            },
            {
                "id": "GMT",
                "name": "Grand Moff Tarkin",
                "affiliation": "dark"
            },
            {
                "id": "CB1",
                "name": "Chewbacca",
                "affiliation": "light"
            },
            {
                "id": "HS1",
                "name": "Han Solo",
                "affiliation": "light"
            },
            {
                "id": "GR1",
                "name": "Greedo",
                "affiliation": "other"
            },
            {
                "id": "JTH",
                "name": "Jabba The Hutt",
                "affiliation": "other"
            },
            {
                "id": "GW1",
                "name": "General Willard",
                "affiliation": "light"
            },
            {
                "id": "GJD",
                "name": "General Jan Dodonna",
                "affiliation": "light"
            },
            {
                "id": "JV1",
                "name": "Jon 'Dutch' Vander",
                "affiliation": "light"
            },
            {
                "id": "WA1",
                "name": "Wedge Antilles",
                "affiliation": "light"
            },
            {
                "id": "BD2",
                "name": "Biggs Darklighter",
                "affiliation": "light"
            },
            {
                "id": "GD1",
                "name": "Garven Dreis",
                "affiliation": "light"
            },
            {
                "id": "JP1",
                "name": "Jek Porkins",
                "affiliation": "light"
            },
            {
                "id": "DT1",
                "name": "Dex Tiree",
                "affiliation": "light"
            },
            {
                "id": "DK1",
                "name": "Davish Krail",
                "affiliation": "light"
            },
            {
                "id": "TN1",
                "name": "Theron Nett",
                "affiliation": "light"
            },
            {
                "id": "PN1",
                "name": "Puck Naeco",
                "affiliation": "light"
            }
        ],
        "scenes": [
            [
                "R2D",
                "C3P",
                "DV1",
                "ST1",
                "RO1"
            ],
            ["abc1"],
            [
                "abc1",
                "def2"
            ],
            ["EMPTY"],
            ["EMPTY"],
            ["EMPTY"],
            ["EMPTY"],
            [
                "R2D",
                "C3P",
                "DV1",
                "PL1"
            ],
            [
                "DV1",
                "PL1"
            ],
            [
                "R2D",
                "C3P"
            ],
            [
                "R2D",
                "C3P",
                "ST1",
                "JW1"
            ],
            [
                "R2D",
                "C3P",
                "LS1",
                "OL1",
                "BL1",
                "JW1"
            ],
            [
                "R2D",
                "C3P",
                "LS1"
            ],
            [
                "LS1",
                "OL1",
                "BL1"
            ],
            [
                "LS1",
                "C3P",
                "OL1",
                "BL1",
                ""
            ],
            [
                "LS1",
                "C3P",
                "R2D",
                "TR1"
            ],
            [
                "LS1",
                "OB1",
                "R2D",
                "C3P",
                "TR1"
            ],
            [
                "LS1",
                "OB1",
                "R2D",
                "C3P"
            ],
            [
                "LS1",
                "OB1",
                "R2D",
                "C3P"
            ],
            [
                "GT1",
                "AM1",
                "DV1",
                "GMT"
            ],
            [
                "LS1",
                "OB1",
                "R2D",
                "C3P",
                "OL1",
                "BL1"
            ],
            [
                "DV1",
                "PL1"
            ],
            [
                "LS1",
                "OB1",
                "R2D",
                "C3P"
            ],
            [
                "LS1",
                "OB1",
                "R2D",
                "C3P"
            ],
            [
                "LS1",
                "OB1",
                "R2D",
                "C3P",
                "CB1"
            ],
            [
                "LS1",
                "OB1",
                "CB1",
                "HS1"
            ],
            [
                "HS1",
                "GR1"
            ],
            [
                "DV1",
                "GMT",
                "GT1",
                "AM1",
                "R2D",
                "LS1",
                "OB1",
                "C3P"
            ],
            [
                "HS1",
                "CB1",
                "JTH"
            ],
            [
                "LS1",
                "OB1",
                "R2D",
                "C3P",
                "HS1",
                "CB1",
                "ST1"
            ],
            [
                "GMT",
                "DV1",
                "PL1",
                "AMI"
            ],
            [
                "LS1",
                "OB1",
                "R2D",
                "C3P",
                "HS1",
                "CB1",
                "GMT",
                "DV1",
                ""
            ],
            [
                "HS1",
                "CB1",
                "LS1",
                "OB1",
                "ST1"
            ],
            [
                "DV1",
                "GMT"
            ],
            [
                "DV1",
                "ST1",
                "LS1",
                "HS1",
                "OB1",
                "CB1",
                "R2D",
                "C3P"
            ],
            [
                "LS1",
                "HS1",
                "OB1",
                "CB1",
                "R2D",
                "C3P",
                "ST1"
            ],
            [
                "LS1",
                "HS1",
                "OB1",
                "CB1",
                "DV1"
            ],
            [
                "LS1",
                "HS1",
                "CB1",
                "PL1",
                "ST1"
            ],
            [
                "DV1",
                "GMT"
            ],
            [
                "HS1",
                "LS1",
                "PL1",
                "CB1",
                "C3P",
                "R2D"
            ],
            [
                "LS1",
                "HS1",
                "PL1",
                "CB1"
            ],
            [
                "LS1",
                "HS1",
                "PL1",
                "CB1",
                "C3P",
                "R2D",
                "ST1"
            ],
            [
                "OB1",
                "LS1",
                "HS1",
                "PL1",
                "CB1",
                "ST1"
            ],
            [
                "LS1",
                "PL1",
                "HS1",
                "CB1",
                "R2D",
                "C3P",
                "OB1",
                "ST1"
            ],
            [
                "LS1",
                "PL1"
            ],
            [
                "DV1",
                "LS1",
                "PL1",
                "HS1",
                "CB1",
                "R2D",
                "C3P",
                "OB1",
                "ST1"
            ],
            [
                "DV1",
                "LS1",
                "PL1",
                "HS1",
                "CB1",
                "R2D",
                "C3P",
                "OB1",
                "ST1"
            ],
            [
                "LS1",
                "HS1",
                "PL1",
                "CB1",
                "C3P",
                "R2D"
            ],
            [
                "DV1",
                "GMT"
            ],
            [
                "DV1",
                "GMT",
                "HS1",
                "LS1",
                "PL1",
                "CB1"
            ],
            [
                "LS1",
                "PL1",
                "HS1",
                "CB1",
                "R2D",
                "C3P",
                "RO1",
                "GW1"
            ],
            [
                "DV1",
                "GMT"
            ],
            [
                "GJD",
                "PL1",
                "LS1",
                "HS1",
                "CB1",
                "RO1",
                "JV1",
                "WA1"
            ],
            [
                "DV1",
                "GMT"
            ],
            [
                "HS1",
                "CB1",
                "LS1",
                "C3P",
                "RO1"
            ],
            [
                "LS1",
                "PL1",
                "R2D",
                "C3P",
                "BD2",
                "RO1",
                "GD1"
            ],
            [
                "PL1",
                "C3P",
                "LS1",
                "BD2",
                "JP1",
                "GJD",
                "WA1",
                "R2D",
                "GD1"
            ],
            [
                "DV1"
            ],
            [
                "LS1",
                "GJD",
                "WA1",
                "BD2",
                "PL1",
                "C3P",
                "PN1",
                "TN1",
                "DK1",
                "JV1",
                "DT1",
                "GD1"
            ],
            [
                "LS1",
                "HS1",
                "DV1",
                "CB1",
                "PL1",
                "C3P",
                "GJD"
            ],
            [
                "PL1",
                "HS1",
                "LS1",
                "C3P",
                "CB1",
                "R2D",
                "RO1"
            ],
            [
                "PL1",
                "HS1",
                "LS1",
                "C3P",
                "CB1",
                "R2D",
                "RO1",
                "GJD"
            ]
        ],
        "JustTest": ['haha','hahahaha']

    }

    #TODO:0. get system time for json file; 1. identify entities;2. identify comparative sentences; 3. generate json file
    name = 'data1'


    intervals = {#this is the information for each scene
        'start': [1, 12, 13, 20, 25, 27, 29, 35, 40, 52, 57, 59, 62, 63, 64, 73, 89, 100, 103, 111, 114, 119, 130, 134,
                  145, 151, 172, 193, 204, 215, 221, 235, 263, 274, 275, 281, 282, 293, 314, 325, 341, 342, 355, 364,
                  375, 381, 392, 394, 402, 405, 411, 412, 413, 434, 445, 451, 452, 463, 467, 485, 491,492],
        'id': ['s1', 's12', 's13', 's20', 's25', 's27', 's29', 's35', 's40', 's52', 's57', 's59', 's62', 's63',
               's64', 's73', 's89', 's100', 's103', 's111', 's114', 's119', 's130', 's134', 's145', 's151',
               's172', 's193', 's204', '215s', 's221', 's235', 's263', 's274', 's275', 's281', 's282',
               's293', 's314', 's325', 's341', 's342', 's355', 's364', 's375', 's381', 's391', 's394',
               's402', 's405', 's411', 's412', 's413', 's434', 's445', 's451', 's452', 's463', 's467', 's485',
               's492'],
        'IsComparative': [0, 1, 1, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                          0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
        'sentence': ['sentence1', 'sentence2', 'sentence3', 'sentence4', 'sentence5', 'sentence6', 'sentence7',
                     'sentence8', 'sentence9', 'sentence10', 'sentence11', 'sentence12', 'sentence13', 'sentence14',
                     'sentence15', 'sentence16', 'sentence17', 'sentence18', 'sentence19', 'sentence20', 'sentence21',
                     'sentence22', 'sentence23', 'sentence24', 'sentence25', 'sentence26', 'sentence27', 'sentence28',
                     'sentence29', 'sentence30', 'sentence31', 'sentence32', 'sentence33', 'sentence34', 'sentence35',
                     'sentence36', 'sentence37', 'sentence38', 'sentence39', 'sentence40', 'sentence41', 'sentence42',
                     'sentence43', 'sentence44', 'sentence45', 'sentence46', 'sentence47', 'sentence48', 'sentence49',
                     'sentence50', 'sentence51', 'sentence52', 'sentence53', 'sentence54', 'sentence55', 'sentence56',
                     'sentence57', 'sentence58', 'sentence59', 'sentence60', 'sentence61', 'sentence62']
    }
    texts = [
        'this is the first sentence',
        'this is the 2 sentence',
        'this is the 3 sentence'
    ]
    return render_template('GistGraph.html',name=name, intervals = intervals, data = data)

@app.route("/SingleDocVisualize/<string:name>")
def SingleDocVisualize(name):
    return render_template('GistGraph.html',name=name)



#@app.route("/hello/<string:json_file_name>/")
@app.route("/hello")
def hello():
    return render_template('UploadPasteText.html')




if __name__ == "__main__":
    app.run()