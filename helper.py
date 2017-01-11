import nltk
import json
import codecs
import pickle
import os
import string
import collections
import MSEntityLinking
import ComparativeSentenceClassification
from settings import APP_STATIC

daily_limit = 10000
max_heading_length = 200


def get_structured_content (content, c):
    '''
    :param content: the raw content submitted by user
    :param c: the symbol to denote the beginning of a chapter title, e.g. '#'
    :return: a structured content, with 2 attributes:
    (1) chapters: a list of chapters, each chapter has (1) rank; (2) id; (3) heading
    (2) all_paragraphs: a list of paragraphs, each paragraph is a list of sentences, each sentence has (1) rank; (2) id; (3) text; (4) IsComparative
    '''
    #prepare for the dict  and classifier used in comparative sentence
    classfier_file_name = APP_STATIC + '/nlp/CSR/classifier.sav'
    rule_dict_file_name = APP_STATIC + '/nlp/CSR/CSR_rules.csv'
    predict_tools = ComparativeSentenceClassification.predict_initiation(classfier_file_name, rule_dict_file_name)
    print(predict_tools['dict'])
    print(predict_tools['classifier'])




    printable = set(string.printable)
    content =  filter(lambda x: x in printable, content)
    content = content.replace ('{', '<').replace('}','>').replace('[','<').replace(']','>')
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
    all_comparative_sentences = []
    for i, p in enumerate(paragraphs):
        structured_paragraph = {}
        paragraph_info = {}
        sentences = []
        paragraph_count += 1
        paragraph_comparative_number = 0

        ss = segmenter.tokenize(p)
        for j, s in enumerate(ss):
            sentence = {}


            if s[0:1] == c and len(s) < max_heading_length:
                ss[j] = s[1:]
                chapter = {}
                chapter['sentence_rank'] = str(sentence_count)
                chapter['sentence_id'] = 's_' + str(sentence_count)
                chapter['paragraph_rank'] = i
                chapter['paragraph_id'] = 'p_' + str(i)
                chapter['text'] = ss[j]
                chapters.append(chapter)

            sentence['rank'] = sentence_count
            sentence['id'] = 'st_' + str(sentence_count)
            sentence['text'] = ss[j]
            sentence['IsComparative'] = 0 #TODO: call function to test if ss[j] is comparative or not
            sentence['IsComparative'] = ComparativeSentenceClassification.predict_comparative(ss[j] , predict_tools['dict'],predict_tools['classifier'])
            if sentence['IsComparative'] == '1':
                paragraph_comparative_number += 1
                all_comparative_sentences.append(sentence['text'])
            sentences.append(sentence)
            sentence_count += 1
        paragraph_info['rank'] = i
        paragraph_info['id'] = 'p_' + str(i)
        paragraph_info['entities'] = []
        paragraph_info['paragraph_comparative_number'] = paragraph_comparative_number
        paragraph_info['text'] = ('').join([s['text'] for s in sentences])
        structured_paragraph['paragraph_info'] = paragraph_info
        structured_paragraph['sentences'] = sentences
        all_paragraphs.append(structured_paragraph)

    structured_content['chapters'] = chapters
    structured_content['all_paragraphs'] = all_paragraphs
    structured_content['all_comparative_sentences'] = all_comparative_sentences



    return structured_content

def get_entity_cooccurrence_in_paragraph(structured_content):
    characters_dict = {}
    paragraphs = structured_content['all_paragraphs']

    block = '' # block text consisting of multiple paragraphs
    prevOffset = 0 # length of the previous block
    paragraph_start = 0 #
    sentence_start = 0
    for p in paragraphs:  # for each paragraph
        #calculate the ranges of each paragraph and sentence
        p['paragraph_info']['start'] = paragraph_start
        p['paragraph_info']['end'] = paragraph_start + len(p['paragraph_info']['text'])
        paragraph_start = p['paragraph_info']['end']
        sentences = p['sentences']
        #print('[p_start]=' + str(p['paragraph_info']['start']) + '[p_end]=' + str(p['paragraph_info']['end']) + '[paragraph]=' + p['paragraph_info']['text'])
        for s in sentences:
            s['start'] = sentence_start
            s['end'] = sentence_start + len(s['text'])
            sentence_start = s['end']
            #print('[s_start]=' + str(s['start']) + '[s_end]=' + str(s['end']) + '[sentence]=' + s['text'])

        #merge paragraphs into blocks for saving MS entity linking service limits
        if len(block + p['paragraph_info']['text']) <= daily_limit:
            block += p['paragraph_info']['text']
            continue
        else:
            #print('block=' + block)
            getEntityDictionary(block, prevOffset,characters_dict)
            prevOffset = prevOffset + len(block)
            block = p['paragraph_info']['text']
    getEntityDictionary(block, prevOffset,characters_dict)
    #print('block=' + block)

    # get characters
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


    # 1. get the paragraph_rank and sentence_rank of each entity
    curr_Paragraph_rank = 0 #use the pointer as the start of finding the correct range, so that we don't have to start from begining every time. linear time complexity.
    for c in characters:
        paragraph_occurrences = []
        sentence_occurrences = []
        for offset in c['offsets']:
            for p in paragraphs:
                if p['paragraph_info']['start'] <= offset <= p['paragraph_info']['end']:
                    paragraph_occurrences.append(p['paragraph_info']['rank'])
                    for s in p['sentences']:
                        if s['start'] <= offset <= s['end']:
                            sentence_occurrences.append(s['rank'])
                            break
                    curr_Paragraph_rank = p['paragraph_info']['rank']
                    break
        c['paragraph_occurrences'] = paragraph_occurrences
        #print('paragraph occurrences=')
        #print(paragraph_occurrences)
        c['sentence_occurrences'] = sentence_occurrences
        print('sentence occurrence=')
        print(sentence_occurrences)

    # 2. put characters co-occurring in a paragraph into a scene
    paragraph_scenes_dict = {} #key:paragraph_rank; value: entity_id
    for c in characters:
        for p_o in c['paragraph_occurrences']:
            if p_o in paragraph_scenes_dict:
                paragraph_scenes_dict[p_o].append(c['id'])
            else:
                entity_ids = []
                entity_ids.append(c['id'])
                paragraph_scenes_dict[p_o] = entity_ids

    paragraph_scenes = []
    paragraph_scenes_info = []
    #prepare a paragraph dictionary, for looking up text based on rank
    paragraph_id_text_dict = {}
    for p in paragraphs:
        paragraph_id_text_dict[p['paragraph_info']['rank']] = p['paragraph_info']['text']

    paragraph_scenes_dict = collections.OrderedDict(sorted(paragraph_scenes_dict.items()))
    for key, value in paragraph_scenes_dict.iteritems():#key: paragraph rank; value: character id list
        #print(key)
        #print(value)
        paragraph_scenes.append(list(set(value)))
        scene_info = {}
        scene_info['x'] = key #paragraph rank
        scene_info['text'] = paragraph_id_text_dict[key]
        paragraph_scenes_info.append(scene_info)

    # 3. get all data needed
    final_result ={}
    final_result['characters'] = characters
    final_result['scenes'] = paragraph_scenes
    final_result['paragraph_scenes_info'] = paragraph_scenes_info
    final_result['chapters'] = structured_content['chapters']
    final_result['all_paragraphs'] = paragraphs


    with open(APP_STATIC + '/data/data_paragraph.json', 'w') as fp:
        json.dump(final_result, fp)


    # 4. get sentence scenes
    # put characters co-occurring in a sentence into a scene
    sentence_scenes_dict = {}
    for c in characters:
        for s_o in c['sentence_occurrences']:
            if s_o in sentence_scenes_dict:
                sentence_scenes_dict[s_o].append(c['id'])
            else:
                entity_ids = []
                entity_ids.append(c['id'])
                sentence_scenes_dict[s_o] = entity_ids

    print('the sentence scene dict=')
    print(sentence_scenes_dict)
    sentence_scenes = []
    sentence_scenes_info = []
    #prepare a sentence dictionary, for looking up text based on rank
    sentence_id_text_dict = {}
    for p in paragraphs:
        for s in p['sentences']:
            sentence_id_text_dict[s['rank']] = s['text']


    print('in sentence scene dict, the key and value=')
    sentence_scenes_dict = collections.OrderedDict(sorted(sentence_scenes_dict.items()))
    for key, value in sentence_scenes_dict.iteritems():#key: sentence rank; value: character id list
        print(key)
        print(value)
        sentence_scenes.append(list(set(value)))
        scene_info = {}
        scene_info['x'] = key #paragraph rank
        scene_info['text'] = sentence_id_text_dict[key]
        sentence_scenes_info.append(scene_info)

    print('sentence scenes=')
    print(sentence_scenes)
    print('sentence scene info=')
    print(sentence_scenes_info)
    # 3. get all data needed

    final_result['scenes'] = sentence_scenes
    final_result['sentence_scenes_info'] = sentence_scenes_info


    with open(APP_STATIC + '/data/data_sentence.json', 'w') as fp:
        json.dump(final_result, fp)



    final_result['all_comparative_sentences'] = ['all_comparative_sentences']
    return final_result

def getEntityDictionary(block, prevOffset, characters_dict):
    '''
    get the entities using Microsoft Entity linking, and calculate the offsets of entities
    :param block:  a block of combination of multiple paragraphs
    :param currOffset: the current length of the last block
    :return: modify the dict
    '''
    #print('[execute block!]=' + block +'  [offset]='+str(prevOffset))
    entities = MSEntityLinking.entityOffsets(block)  # get all its entities
    #print('entities')
    #print(entities)
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
    final_result = get_entity_cooccurrence_in_paragraph(structured_content)
    print('succeed to get entity offsets on paragraph level...')

    return final_result
