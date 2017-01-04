import nltk
import codecs
import pickle
import os
from settings import APP_STATIC

import MSEntityLinking

def SentenceTokenizationTrain(): #the training is unsupervised. More could be added to the corpus at any time.

    tokenizer = nltk.tokenize.punkt.PunktSentenceTokenizer()
    text = codecs.open(APP_STATIC+'/nlp/corpus/SentenceTokenizationTrainCorpus', "r", "utf8").read()
    tokenizer.train(text)
    out = open(APP_STATIC+'/nlp/corpus/literature.pickle', "wb")
    pickle.dump(tokenizer, out)#Save the pickle
    out.close()
def Paragraph_to_Sentence(paragraph):
    '''
    :param paragraph: a paragraph with multiple sentence
    :return: a list of sentences
    '''
    sent_detector = nltk.data.load(APP_STATIC+'/nlp/corpus/literature.pickle')
    return sent_detector.tokenize(paragraph.strip())


def main():
    #SentenceTokenizationTrain()
    paragraph = '''
    We present Poisson Distribution, a browser-based authoring tool that automatically extracts event data from temporal references in unstructured text documents using natural language processing and encodes them along a visual timeline. Our goal is to facilitate the timeline creation process for journalists and others who tell temporal stories online. Current solutions involve manually extracting and formatting event data from source documents, a process that tends to be tedious and error prone. With TimeLineCurator, a prospective timeline author can quickly identify the extent of time encompassed by a document, as well as the distribution of events occurring along this timeline. Authors can speculatively browse possible documents to quickly determine whether they are appropriate sources of timeline material. TimeLineCurator provides controls for curating and editing events on a timeline, the ability to combine timelines from multiple source documents, and export curated timelines for online deployment. We evaluate TimeLineCurator through a benchmark comparison of entity extraction error against a manual timeline curation process, a preliminary evaluation of the user experience of timeline authoring, a brief qualitative analysis of its visual output, and a discussion of prospective use cases suggested by members of the target author communities following its deployment.
    '''
    sentences = Paragraph_to_Sentence(paragraph)
    print(sentences)
    print(MSEntityLinking.entityOffsets(paragraph))

main()