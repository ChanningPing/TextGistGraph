from nltk.stem.snowball import SnowballStemmer
import nltk
import string

stemmer = SnowballStemmer("english")
print(stemmer.stem('gain'))
sentence = 'Since PLSIQ can not take much advantage from the term weighting scheme PLSIUPLSIU performs slightly better in this case'
print(nltk.pos_tag(nltk.word_tokenize(sentence.lower())))
print(string.punctuation)