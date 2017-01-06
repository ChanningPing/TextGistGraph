import nltk
import json
import codecs
import pickle
import os
import string
import MSEntityLinking
from settings import APP_STATIC

daily_limit = 10000
max_heading_length = 200
characters_dict = {}

def get_structured_content (content, c):
    '''
    :param content: the raw content submitted by user
    :param c: the symbol to denote the beginning of a chapter title, e.g. '#'
    :return: a structured content, with 2 attributes:
    (1) chapters: a list of chapters, each chapter has (1) rank; (2) id; (3) heading
    (2) all_paragraphs: a list of paragraphs, each paragraph is a list of sentences, each sentence has (1) rank; (2) id; (3) text; (4) IsComparative
    '''

    printable = set(string.printable)
    content =  filter(lambda x: x in printable, content)
    # 1. remove extra line breaks
    paragraphs = content.split('\n') # break full text into natural paragraphs
    for index, paragraph in enumerate(paragraphs):
        paragraphs[index] = paragraphs[index].replace('\n', '').strip()  # remove extra '\n' in paragraphs
    paragraphs = [p for i, p in enumerate(paragraphs) if p != '']  # keeps only the non-empty paragraphs after strip()

    # 2. segment paragraphs into sentences, and store sentence and chapter information
    segmenter = nltk.data.load(APP_STATIC + '/nlp/corpus/literature.pickle')
    structured_content = {}
    chapters = []
    all_paragraphs = []
    sentence_count = 0
    paragraph_count = 0
    for i, p in enumerate(paragraphs):
        structured_paragraph = {}
        paragraph_info = {}
        sentences = []
        paragraph_count += 1

        ss = segmenter.tokenize(p)
        for j, s in enumerate(ss):
            sentence = {}
            sentence_count += 1

            if s[0:1] == c and len(s) < max_heading_length:
                ss[j] = s[1:]
                chapter = {}
                chapter['sentence_rank'] = sentence_count
                chapter['sentence_id'] = 's_' + str(sentence_count)
                chapter['paragraph_rank'] = paragraph_count
                chapter['paragraph_id'] = 'p_' + str(paragraph_count)
                chapter['text'] = ss[j]
                chapters.append(chapter)

            sentence['rank'] = sentence_count
            sentence['id'] = 'st_' + str(sentence_count)
            sentence['text'] = ss[j]
            sentence['IsComparative'] = 0 #TODO: call function to test if ss[j] is comparative or not
            sentences.append(sentence)
        paragraph_info['entities'] = []
        paragraph_info['text'] = ('').join([s['text'] for s in sentences])
        structured_paragraph['paragraph_info'] = paragraph_info
        structured_paragraph['sentences'] = sentences
        all_paragraphs.append(structured_paragraph)
    structured_content['chapters'] = chapters
    structured_content['all_paragraphs'] = all_paragraphs
    return structured_content

def get_entity_cooccurrence_in_paragraph(structured_content):
    #TODO: combine paragraphs into 10k block for saving Microsoft Entity linking service limits
    paragraphs = structured_content['all_paragraphs']

    block = ''
    prevOffset = 0

    for p in paragraphs:  # for each paragraph
        if len(block + p['paragraph_info']['text']) <= daily_limit:
            block += p['paragraph_info']['text']
            print('block='+block)
            continue
        else:
            getEntityDictionary(block, prevOffset)
            prevOffset = len(block)
            block = p['paragraph_info']['text']
    getEntityDictionary(block, prevOffset)
    characters = []
    for key, value in characters_dict.iteritems():
        character = {}
        character['id'] = key
        character['affiliation'] = value['affiliation']
        character['name'] = value['name']
        character['offsets'] = value['offsets']
        character['frequency'] = value['frequency']
        characters.append(character)
    print('characters=')
    print(characters)
        # 2. put characters co-occurring in a paragraph into a scene
        # 3. get all data needed

        # print(entities)

def getEntityDictionary(block, prevOffset):
    '''
    :param block:  a block of combination of multiple paragraphs
    :param currOffset: the current length of the last block
    :return: modify the dict
    '''
    print('execute block!' + block +', with offset='+str(prevOffset))
    entities = MSEntityLinking.entityOffsets(block)  # get all its entities
    print('entities')
    print(entities)
    if entities != 'error-001:invalid-characters':
        entities = json.loads(entities)  # transfer string into a json object
        json_entities = entities['entities']
        if json_entities:
            # 1. get all characters, by storing entities into a dict
            for entity in json_entities:
                entity_key = entity['wikipediaId'].replace(' ', '_')
                # if this is the first time the entity appears
                if entity_key in characters_dict:
                    frequency = 0
                    for m in entity['matches']:
                        for e in m['entries']:
                            characters_dict[entity_key]['offsets'].append(e['offset'] + prevOffset)
                            frequency += 1
                    characters_dict[entity_key]['frequency'] += frequency
                else:  # otherwise
                    entity_value = {}
                    entity_value['affiliation'] = 'light'
                    entity_value['name'] = entity['name']
                    offsets = []
                    frequency = 0
                    for m in entity['matches']:
                        for e in m['entries']:
                            offsets.append(e['offset'] + prevOffset)
                            frequency += 1
                    entity_value['offsets'] = offsets
                    entity_value['frequency'] = frequency
                    characters_dict[entity_key] = entity_value


def JsonResult(content):
    '''
    :param content: full text of a paper
    :return:
    '''

    structured_content = get_structured_content (content, '#')
    print('succeed to get structured content...')
    get_entity_cooccurrence_in_paragraph(structured_content)
    print('succeed to get entity offsets on paragraph level...')

    return structured_content
