import pytest
import os
from src.main import *
import sys
import platform

graph_1 = 'test_source/test_graph_1.txt'
real_graph_1 = {'1': ['12', '13'],
                '12': ['121', '122', '123'],
                '13': ['131', '132'],
                '131': ['1311'],
                '1311': ['13111']}

STORAGE = 'test_source/'


def test_read_graph():
    print("\n", os.getcwd(), "____________===______________")
    print("\n_____________________________")
    print("\t", platform.system())
    print("\t", sys.platform)
    print("\t", sys.path)
    print("_____________________________\n")
    assert os.path.exists(graph_1)
    graph = gr.read_graph(graph_1)
    for node, neighbors in graph:
        assert real_graph_1[node].sort() == neighbors.sort()


def test_graph_builder():
    graph = graph_builder(graph_1)
    for node, neighbors in graph.adj.items():
        if node in real_graph_1:
            assert real_graph_1[node].sort() == list(neighbors).sort()


def test_bfs():
    graph = graph_builder(graph_1)
    try:
        bfs_path = list(bfs(graph, '1'))
        for i in range(len(bfs_path) - 1):
            assert len(bfs_path[i]) <= len(bfs_path[i + 1])
    except ValueError:
        assert False


def test_dfs():
    graph = graph_builder(graph_1)
    try:
        dfs_path = list(dfs(graph, '1'))
        real_nodes_1 = set()
        for node, neigbors in real_graph_1.items():
            real_nodes_1.add(node)
            real_nodes_1.update(set(neigbors))

        for node in list(real_nodes_1):
            assert node in dfs_path
    except ValueError:
        assert False


def test_dfs_2():
    graph = graph_builder(graph_1)
    try:
        dfs_path = list(dfs(graph, 'A'))
    except ValueError:
        assert True


def test_create_gif_1():
    algorithm = 'bfs'
    fig = plt.figure()
    camera = Camera(fig)
    graph = graph_builder(graph_1)
    assert create_gif(graph, camera, func=algorithm, start='1', source=graph_1, storage=STORAGE)
    file_name = STORAGE + algorithm + FILE_NAME_TEMPLATE + '(' + graph_1.replace('/', '.') + ')' + EXTENSION
    assert os.path.exists(file_name)


def test_create_gif_2():
    algorithm = 'bfs'
    fig = plt.figure()
    camera = Camera(fig)
    graph = graph_builder(graph_1)
    assert not create_gif(graph, camera, func=algorithm, start='A', source=graph_1, storage=STORAGE)


def test_main_1():
    algorithm = 'dfs'
    assert main(start='1', file_path=graph_1, algorithm=algorithm, storage=STORAGE)
    file_name = STORAGE + algorithm + FILE_NAME_TEMPLATE + '(' + graph_1.replace('/', '.') + ')' + EXTENSION
    print(file_name)
    assert os.path.exists(file_name)


def test_main_2():
    algorithm = 'dfs'
    assert not main(start='A', file_path=graph_1, algorithm=algorithm, storage=STORAGE)
