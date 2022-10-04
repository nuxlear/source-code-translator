import openai
import os


def generate_explanation(prompt, model='text-davinci-002', temperature=0.5, max_tokens=256, num_results=3,
                         frequency_penalty=0., presence_penalty=0.):

    openai.api_key = os.getenv("OPENAI_API_KEY")

    res = openai.Completion.create(
        model=model,
        prompt=prompt,
        temperature=temperature,
        max_tokens=max_tokens,
        top_p=1.0,
        n=num_results,
        frequency_penalty=frequency_penalty,
        presence_penalty=presence_penalty,
    )
    return res.choices


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

    prompt = f'{code}\n\n"""\nThe explanation of the Python 3 code above is here:\n1. '
    results = generate_explanation(prompt)
    print(results)
