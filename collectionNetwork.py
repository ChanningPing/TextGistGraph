import itertools
def generate_network (paper_scene_list):
    # 1. sort the paper and its scenes by year and month
    paper_scene_list.sort(key=lambda x: (x['year'], x['month']))
    print('after sort')
    print(paper_scene_list)

    # 2. get all nodes
    nodes_dict = {}
    edges_dict = {}
    paper_dict = {}
    curr_entity_id = 0
    curr_paper_id = 0

    for paper in paper_scene_list: # for each paper
        for index, scene in enumerate(paper['sentence_scenes']): # for each scene
            if len(scene) > 1:  # if there are at least 2 entities in a sentence
                for entity in scene:
                    entity = str(entity)
                    if entity not in nodes_dict:
                        entity_info = {}
                        entity_info['nodeName'] = entity
                        entity_info['id'] = curr_entity_id
                        entity_info['group'] = curr_paper_id
                        nodes_dict[entity] = entity_info
                        curr_entity_id += 1
                # generate all pairs of entities of the scene
                all_pairs = list(itertools.combinations(range(len(scene)), 2))  # get all possible index pairs for the characters in teh scene
                for pair in all_pairs:
                    source = nodes_dict[scene[pair[0]]]['id']
                    target = nodes_dict[scene[pair[1]]]['id']
                    sentence = paper['sentence_scenes_info'][index]['text']
                    title = paper['title']
                    sentence_info = {}
                    sentence_info['sentence'] = sentence
                    sentence_info['title'] = title
                    key = str(source) + '_' + str(target)  # source_target

                    if key in edges_dict:
                        edges_dict[key]['value'] += 1

                        edges_dict[key]['sentences'].append(sentence_info)
                    else:
                        pair_entry = {}  # 0=source, 1=target, 2=source_target, 3=frequency
                        pair_entry['source'] = source  # source
                        pair_entry['target'] = target  # target
                        pair_entry['value'] = 1
                        sentences = []
                        sentences.append(sentence_info)
                        pair_entry['sentences'] = sentences
                        edges_dict[key] = pair_entry
        paper_info = {}
        paper_info['id'] = curr_paper_id
        paper_info['title'] = paper['title']
        paper_dict[curr_paper_id] = paper_info
        curr_paper_id += 1



    print('the node dict =')
    print(nodes_dict)
    print('the edge dict = ')
    print(edges_dict)

    nodes = nodes_dict.values()
    edges = edges_dict.values()
    papers = paper_dict.values()
    # sort the nodes based on their ids (d3 force layout only track id based on the order of nodes appear, not by id you give)
    from operator import itemgetter
    nodes = sorted(nodes, key=itemgetter('id'))
    network_data = {}
    network_data['nodes'] = nodes
    network_data['links'] = edges
    network_data['papers'] = papers
    return network_data
