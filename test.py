import string
import nltk
s = "a negative! facdotraiztion: based on , oscar's razors "
print(s.translate(None, string.punctuation))
s = "The concatenated features A outperform the original feature set of B"
tagged_tuples = nltk.pos_tag(nltk.word_tokenize(s.lower()))
print(tagged_tuples)