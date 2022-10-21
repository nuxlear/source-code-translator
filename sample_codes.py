exp_sample = '''def dijkstra(graph, start, end):
    table = {}
    for vertex in graph.vertexes:
        table[vertex] = {'distance': float('inf'), 'path': None}
    table[start]['distance'] = 0

    processed_vertexes = set()
    min_heap = MinHeap()
    min_heap.insert(start, 0)
    
    while min_heap:
        distance, vertex = min_heap.extract_min()
        
        if vertex in processed_vertexes:
            continue
        if vertex == end:
            return table

        for edge in graph.vertexes[vertex]:
            if edge.end not in processed_vertexes:
                if edge.weight + table[vertex]['distance'] < table[edge.end]['distance']:
                    table[edge.end]['distance'] = edge.weight + table[vertex]['distance']
                    table[edge.end]['path'] = vertex

                min_heap.insert(edge.end, table[edge.end]['distance'])

        processed_vertexes.add(vertex)

    return table'''

test_sample = '''class SimpleCNN(nn.Module):
    def __init__(self, num_classes=10):
        super(SimpleCNN, self).__init__()
        self.features = nn.Sequential(
            nn.Conv2d(3, 32, kernel_size=5, stride=1, padding=2),
            nn.ReLU(inplace=True),
            nn.MaxPool2d(kernel_size=3, stride=2),
            nn.Conv2d(32, 32, kernel_size=5, stride=1, padding=2),
            nn.ReLU(inplace=True),
            nn.AvgPool2d(kernel_size=3, stride=2),
            nn.Conv2d(32, 64, kernel_size=5, padding=2),
            nn.ReLU(inplace=True),
            nn.AvgPool2d(kernel_size=3, stride=2),
        )
        self.classifier = nn.Sequential(
            nn.Dropout(),
            nn.Linear(64 * 4 * 4, 256),
            nn.ReLU(inplace=True),
            nn.Dropout(),
            nn.Linear(256, 256),
            nn.ReLU(inplace=True),
            nn.Linear(256, num_classes),
        )

    def forward(self, x):
        x = self.features(x)
        x = x.view(x.size(0), 64 * 4 * 4)
        x = self.classifier(x)
        return x
'''


