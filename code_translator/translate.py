from code_translator.core import generate_explanation
from code_translator.validate import find_vulnerabilities, make_prompt_query_for_enhancement, is_same_vulnerability
from code_translator.utils import save_code_to_tmp_file

import os
import re


main_script_pattern = re.compile('if __name__ == ([\'\"]__main__[\'\"]:)?')


def get_explanation(code, n=3):
    query = '"""\nThe explanation of the Python 3 code above is here:\n1. '
    prompt = f'{code}\n\n{query}'

    candidates = generate_explanation(prompt, num_results=n, max_tokens=384, stop='"""')

    cand_texts = [x.text.split('"""')[0] for x in candidates if x.finish_reason == 'stop' or '"""' in x.text]
    res_texts = [x for x in cand_texts if len(x.strip()) > 0]
    return [f'{query}{x}"""' for x in res_texts]


def get_enhancements(code, vulnerabilities=None, n=3):
    if vulnerabilities is None:
        vulnerabilities = find_vulnerabilities(code)

    results = []
    for v in vulnerabilities:
        prompt = make_prompt_query_for_enhancement(v, code)

        candidates = generate_explanation(prompt, num_results=n, max_tokens=384, stop=['##', '%%'])
        cand_texts = [x.text for x in candidates]
        cand_texts = list(set(cand_texts))

        answers = []
        for cand_text in cand_texts:
            fixed_vuls = find_vulnerabilities(cand_text)

            is_valid_code = all([fv['type'] not in ['error', 'fatal'] for fv in fixed_vuls])
            is_vul_remains = any([is_same_vulnerability(v, fv) for fv in fixed_vuls])
            if is_valid_code and not is_vul_remains:
                answers.append(cand_text)

        results.append((v, answers))

    return results


def get_generation(query, n=3):
    prompt = f'"""\n{query} without any explanations & test code\n"""\n\n'

    candidates = generate_explanation(prompt, num_results=n, max_tokens=512, stop=['##', '# test'])

    # cand_texts = [x.text for x in candidates if x.finish_reason == 'stop' or main_script_pattern.search(x.text) is not None]
    cand_texts = [x.text for x in candidates]
    cand_texts = [re.split(main_script_pattern, x, 1)[0].strip() for x in cand_texts]
    cand_texts = list(set(cand_texts))

    results = []
    for cand_text in cand_texts:
        fixed_vuls = find_vulnerabilities(cand_text)

        is_valid_code = all([fv['type'] not in ['error', 'fatal'] for fv in fixed_vuls])
        if is_valid_code:
            results.append(cand_text)

    return results


def get_modification(code, query, n=3):
    query = f'"""Modify the Python 3 code above as:\n{query}\n"""'
    prompt = f'{code}\n\n{query}\n\n## Modified code\n\n'

    candidates = generate_explanation(prompt, num_results=n, max_tokens=512, stop=['##', '# test'])

    cand_texts = [x.text for x in candidates if x.finish_reason == 'stop' or main_script_pattern.search(x.text) is not None]
    cand_texts = [re.split(main_script_pattern, x, 1)[0].strip() for x in cand_texts]
    cand_texts = list(set(cand_texts))

    # TODO: need to check that the code is modified correctly
    results = []
    for cand_text in cand_texts:
        fixed_vuls = find_vulnerabilities(cand_text)

        is_valid_code = all([fv['type'] not in ['error', 'fatal'] for fv in fixed_vuls])
        if is_valid_code:
            results.append(cand_text)

    return results


def get_test_code(code, n=3):
    query = f'## Test code for the Python 3 code above\n\ndef test():\n'
    prompt = f'{code}\n\n{query}'

    candidates = generate_explanation(prompt, num_results=n, max_tokens=768)
    cand_texts = [f'def test():\n{x.text}' for x in candidates if x.finish_reason == 'stop']
    cand_texts = list(set(cand_texts))

    results = []
    for cand_text in cand_texts:
        fixed_vuls = find_vulnerabilities(cand_text)

        is_runnable_code = all([fv['type'] not in ['fatal'] for fv in fixed_vuls])
        if is_runnable_code:
            results.append(cand_text)

    return results


if __name__ == '__main__':
    code = '''def dijkstra_algorithm(graph, start_node):
    unvisited_nodes = list(graph.get_nodes())
    
    shortest_path = {}
    previous_nodes = {}
    
    max_value = sys.maxsize
    for node in unvisited_nodes:
        shortest_path[node] = max_value
    shortest_path[start_node] = 0
    
    while unvisited_nodes:
        current_min_node = None
        for node in unvisited_nodes: # Iterate over the nodes
            if current_min_node == None:
                current_min_node = node
            elif shortest_path[node] < shortest_path[current_min_node]:
                current_min_node = node
    
        neighbors = graph.get_outgoing_edges(current_min_node)
        for neighbor in neighbors:
            tentative_value = shortest_path[current_min_node] + graph.value(current_min_node, neighbor)
            if tentative_value < shortest_path[neighbor]:
                shortest_path[neighbor] = tentative_value
                previous_nodes[neighbor] = current_min_node
    
        unvisited_nodes.remove(current_min_node)
    
    return previous_nodes, shortest_path'''

    res = get_test_code(code)
    print(res)
