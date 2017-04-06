# -*- coding: utf-8 -*-
from __future__ import division
import gensim.models.word2vec as w2v
from settings import APP_STATIC
from nltk.corpus import stopwords
import re
import jieba.posseg as pseg
import nltk
import os

import sys

reload(sys)
sys.setdefaultencoding('utf8')

def prepare_word_embeddings():
    danmu2vec = w2v.Word2Vec.load(APP_STATIC + '/nlp/word_embeddings/literature2vec-test.w2v')
    return danmu2vec

def paper_to_sentences(paper_name):
    nltk.download('punkt')
    segmenter = nltk.data.load(APP_STATIC + '/nlp/corpus/literature.pickle')
    with open(paper_name) as paper:  # read labels and sentences from file
        sentences = segmenter.tokenize(paper.read().replace('\n', ' '))
    return sentences

def query_expansion(query,danmu2vec):
    # transform query into weighted word list
    interrogative_word_tags = ['WP', 'WRB', 'WDT']  # exclude interrogatives
    tagged_tokens = nltk.pos_tag(nltk.word_tokenize(query.lower()))
    keywords = {}
    decay_factor = 0.9
    expansion_threshold = 0.8
    for token, tag in tagged_tokens:  # exclude stopwords, pure non-alphabetics
        if not tag in interrogative_word_tags and (not token in stopwords.words('english')) and (
        re.search('[a-zA-Z]', token)):
            if token in danmu2vec.wv.vocab:
                print(token)
                print(danmu2vec.wv.vocab[token].count)
                keywords[token] = 1 / danmu2vec.wv.vocab[token].count * 1000  # weight words based on idf


    # added begin
    keywords = {}
    keywords_list = sentence_to_phrases(query, danmu2vec)
    for k in keywords_list:
        if k in danmu2vec.wv.vocab:
            print(k)
            print(danmu2vec.wv.vocab[k].count)
            keywords[k] = 1 / danmu2vec.wv.vocab[k].count * 1000  # weight words based on idf
        else:
            keywords[k] = 1/1000
    # added end
    expanded_keywords = keywords.copy()
    for keyword, weight in keywords.iteritems():
        top_n = int(weight)
        if top_n ==0:
            top_n = 1
        if keyword in danmu2vec.wv.vocab:
            top_similar_words = danmu2vec.most_similar(keyword, topn=top_n)
            for word,similarity in top_similar_words:
                if similarity > expansion_threshold:
                    expanded_keywords[word] = (1 / danmu2vec.wv.vocab[word].count * 1000) * decay_factor # weight words based on idf
    print(expanded_keywords)
    return expanded_keywords


def generate_answers(keywords,sentences,danmu2vec):


    answer_set = []
    threshold = len(keywords)*0.4
    for s in sentences:
        tokens = nltk.word_tokenize(s.lower())
        #added begin
        tokens = sentence_to_phrases(s, danmu2vec)
        #added end
        sum_embeddings = 0
        max_words = []
        for k in keywords:
            max_embedding = 0
            max_word = ''
            for t in tokens:
                if t==k:
                    max_embedding = 1
                    max_word = t
                    break
                elif (not t in stopwords.words('english')) and (re.search('[a-zA-Z]',t)) and t in danmu2vec.wv.vocab and k in danmu2vec.wv.vocab:
                    embedding = danmu2vec.wv.similarity(k, t)
                    if embedding > max_embedding:
                        max_embedding = embedding
                        max_word=t
            sum_embeddings = sum_embeddings + max_embedding
            max_words.append(max_word)
        if sum_embeddings >= threshold:
            answer = {}
            answer['sentence'] = s
            answer['max_word'] = max_words
            answer['sum_embedding'] = sum_embeddings
            answer_set.append(answer)
            #print(s)
    from operator import itemgetter
    answer_set = sorted(answer_set, key=itemgetter('sum_embedding'),reverse=True)
    for answer in answer_set:
        print(answer)







def sentence_to_phrases(sentence,danmu2vec):
    from nltk.tokenize import word_tokenize
    from nltk.corpus import stopwords
    import re

    stopwords = set(stopwords.words('english'))

    sentence = word_tokenize(sentence)
    grammar = "NP: {<JJ.*>*<NN.*>+}"
    sentence = nltk.pos_tag(sentence)
    cp = nltk.RegexpParser(grammar)
    result = cp.parse(sentence)

    phrases = []
    for leave in result:
        if isinstance(leave[0], tuple):
            phrase = []
            for pair in leave:
                phrase.append(pair[0])
            phrase = ('_').join(word.lower() for word in phrase)  # concatenate noun phrase
            phrases.append(phrase)
        else:
            if not leave[0] in stopwords and re.search('[a-zA-Z]',
                                                       leave[0]):  # remove stopwords and pure non-alphabetic strings.
                phrases.append(leave[0].lower())
    return phrases

def main():
    danmu2vec = prepare_word_embeddings()
    paper_name = APP_STATIC + '/nlp/corpus/biomed.txt'
    sentences = paper_to_sentences(paper_name)
    #q1 = 'what is the novelty of the paper?'
    # q1 = 'what is the definition of research front?'
    q1 = 'how to accelerate synthesis?'
    q1 = 'what are the methods used in optimization of biological process?'
    #q1 = 'how are pivotal points defined'
    q2 = 'the algorithm proposed outperforms what?'
    q3 = 'what is the length of the hidden layer?'
    q4 = 'what data is used in the experiment?'
    q5 = 'is there any interaction between Video Structure and cartoon ratings?'
    q6 = 'what is the relationship between enjoyment and video structure?'
    #q6 = 'what is the advantage of citespace?'
    q7 ='what is the programming language of citespace?'
    #q3 = 'what why how who where which whom whether'
    keywords = query_expansion(q1,danmu2vec)
    generate_answers(keywords,sentences,danmu2vec)
    #print (danmu2vec.most_similar('first_work', topn=10))
    #print(len(danmu2vec.wv.vocab))
    #print(danmu2vec.wv.similarity('first_work', 'inference'))
    #print(danmu2vec.wv.similarity('first_work', 'first_research'))



main()