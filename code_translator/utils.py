from code_translator.db import get_db_engine, get_session, CodeTranslateResults
from sqlalchemy.exc import SQLAlchemyError

import os
from pathlib import Path
import uuid
import ast
import json


tmp_input_dir = Path('tmp_input')

obj_node_type = [ast.ClassDef, ast.FunctionDef, ast.AsyncFunctionDef]
valid_node_type = [ast.Import, ast.ImportFrom] + obj_node_type


def save_code_to_tmp_file(code):
    os.makedirs(tmp_input_dir, exist_ok=True)
    filename = f'{uuid.uuid4()}.py'
    file_path = tmp_input_dir / filename

    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(code)

    return file_path


def remove_syntax_error_in_code(code):
    ''' Find function or class block from code, without running scripts '''
    if isinstance(code, str):
        code = code.split('\n')

    for end in range(len(code), 0, -1):
        sub_code = '\n'.join(code[:end])
        try:
            res = ast.parse(sub_code)
            return sub_code
        except SyntaxError as e:
            pass

    return None


def record_user_data(code=None, query=None, candidates=None, results=None):
    if (code, query) == (None, None):
        raise ValueError('One of `code` or `query` must not be None. ')
    candidates = candidates or []
    results = results or []

    d = {
        'code': code,
        'query': query,
        'candidates': [dict(x) for x in candidates],
        'results': results,
    }

    os.makedirs('userdata', exist_ok=True)

    item_id = uuid.uuid4()
    filename = f'{item_id}.json'
    with open(f'userdata/{filename}', 'w', encoding='utf-8') as f:
        json.dump(d, f, indent=4)

    engine = get_db_engine('db_tokens_main.json')
    orm = CodeTranslateResults(filename=filename)
    try:
        with get_session(engine) as session:
            session.add(orm)
            session.commit()
        return filename
    except SQLAlchemyError as e:
        print(e)
        print(e.__traceback__)
        return None


def find_valid_objects_in_code(code):
    lines = code.split('\n')
    sub_code = remove_syntax_error_in_code(lines)

    tree = ast.parse(sub_code)
    obj_tree = [x for x in tree.body if x.__class__ in obj_node_type]
    valid_tree = [x for x in tree.body if x.__class__ in valid_node_type]

    valid_tree = tree.body if len(obj_tree) == 0 else valid_tree

    valid_codes = ['\n'.join(lines[x.lineno-1:x.end_lineno]) for x in valid_tree]
    return '\n\n'.join(valid_codes)


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

    code2 = f'''class Graph:
    def __init__(self, vertices):
        self.V = vertices
        self.graph = [[0 for column in range(vertices)]
                      for row in range(vertices)]

    def printSolution(self, dist):
        print("Vertex \tDistance from Source")
        for node in range(self.V):
            print(node, "\t", dist[node])

    def minDistance(self, dist, sptSet):
        min = float("inf")
        for v in range(self.V):
            if dist[v] < min and sptSet[v] == False:
                min = dist[v]
                min_index = v
        return min_index

    def dijkstra(self, src):
        dist = [float("inf")] * self.V
        dist[src] = 0
        sptSet = [False] * self.V
        for cout in range(self.V):
            u = self.minDistance(dist, sptSet)
            sptSet[u] = True
            for v in range(self.V):
                if self.graph[u][v] > 0 and sptSet[v] == False and dist[v] > dist[u] + self.graph[u][v]:
                    dist[v] = dist[u] + self.graph[u][v]
        self.printSolution(dist)


g = Graph(9)
g.graph = [[0, 4, 0, 0, 0, 0, 0, 8, 0],
           [4, 0, 8, 0, 0, 0, 0, 11, 0],
           [0, 8, 0, 7, 0, 4, 0, 0, 2],
           [0, 0, 7, 0, 9, 14, 0, 0, 0],
           [0, 0, 0, 9, 0, 10, 0, 0, 0],
           [0, 0, 4, 14, 10, 0, 2, 0, 0],
           [0, 0, 0, 0, 0, 2, 0, 1, 6],
           [8, 11, 0, 0, 0, 0, 1, 0, 7],'''

    code3 = f'''a = 2
b = 3
print(a, b, a + b)'''

    res = find_valid_objects_in_code(code)
    res2 = find_valid_objects_in_code(code2)
    res3 = find_valid_objects_in_code(code3)
    print([res, res2, res3])
