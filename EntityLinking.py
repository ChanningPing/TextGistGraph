# -*- coding: utf-8 -*-
'''
TODO:
1. Given text, record chapter offsets
2. Given text, record sentence offsets
3. Given text, record entity offsets
4. Given sentence offsets and entity offsets, decide whether the entities are in same sentence

'''

content = '''
In probability theory and statistics, #the Poisson distribution (French pronunciation [pwasɔ̃]; #in English usually /ˈpwɑːsɒn/), named after French mathematician Siméon Denis Poisson, #is a discrete probability distribution that expresses the probability of a given number of events occurring in a fixed interval of time and/or space if these events occur with a known average rate and independently of the time since the last event.[1] #The Poisson distribution can also be used for the number of events in other specified intervals such as distance, area or volume.
'''
def findChapterOffsets(content):
    '''
    :param content: all content of a document with '#' as chapter start
    :return:
    '''
    offsets = findOccurences(content, '#')
    content = content.replace('#','')
    i = 0
    for offset in offsets:
        offset = offset - i
        #print(content[offset:-1])
        i += 1
    return offsets

def findOccurences(content, chapterStart):
        return [i for i, letter in enumerate(content) if letter == chapterStart]

def main():
    findChapterOffsets(content)

main()