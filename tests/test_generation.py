from code_translator import *


if __name__ == '__main__':
    res = get_generation('Python 3 code for Dijkstra\'s Algorithm')
    print(res)

    res = get_modification(res[0], 'Remove all comments')
    print(res)
