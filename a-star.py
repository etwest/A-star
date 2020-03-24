#! /usr/local/bin/python3.7

# enforce some basic typing on the functions
from __future__ import annotations
from typing import List, Dict

import math
import queue
import sys
import unittest

class node:
    identity = None
    neighbors = []
    # plot on the graph
    x = 0
    y = 0
    dist = sys.maxsize # distance from the start
    cameFrom = None
    visited = False

    def __init__(self, identity: int, data: List[float]) -> None:
        self.identity  = identity
        self.neighbors = data[2:]
        self.x         = data[0]
        self.y         = data[1]

    # function to calculate the distance between two points
    # arguments: two points, only the data of which the first two
    #            elements are x and y coordinates
    # returns: the distance between the nodes (float)
    def calc_dist(self, other: node) -> float:
        x_diff = self.x - other.x
        y_diff = self.y - other.y
        return math.sqrt(math.pow(x_diff, 2) + math.pow(y_diff, 2))


    def __str__(self) -> str:
        ret = "Identity: " + str(self.identity) + "\n"
        ret += " x:" + str(self.x) + "\n"
        ret += " y:" + str(self.y) + "\n"
        ret += " neighbors:" + str(self.neighbors) + "\n"
        ret += " cameFrom:" + str(self.cameFrom) + "\n"
        ret += " distance from start: " + str(self.dist)
        return ret

# read in the adjacency list
# argument: the name of a file to read from
# returns: the adjacency list of the graph (dictionary)
def readAdj(fileName: str) -> Dict[int, node]:
    # each node will be stored here in the following format
    # x, y, neighbor nodes(zero or more)
    graph = {}
    with open(fileName) as file:
        line = file.readline()
        while line != "":
            if line[0] != '#':
                line = line.rstrip()
                line = line.split("\t")
                element = node(int(line[0]), [float(x) for x in line[1:]])
                graph[int(line[0])] = element
            line = file.readline()

    return graph

# function to loop through the graph and reset all the
# nodes to their initial state so that we can run the a-star
# algorithm across it again
# argument: graph to reset
# returns: void
def resetGraph(graph: Dict[int, node]) -> None:
    for node in graph.values():
        node.cameFrom = None
        node.visited  = False
        node.dist     = sys.maxsize

# function which implements the a star algorithm
# Our heuristic h is calculated as the distance between 
# the points a and b
# arguments: graph, start node, end node
# returns: a string which contains the length of the best path and the
#          specification of that path
def a_star(graph: Dict[int, node], start: int, end: int) -> str:
    pq = queue.PriorityQueue()
    # we must start with start so stick that in the queue with value 0
    pq.put((0, start))
    graph[start].dist = 0
    graph[start].visited = True
    current = None
    while not pq.empty() and current != end:
        pair     = pq.get()
        path_len = pair[0]
        current  = pair[1]

        cur_data = graph[current]
        # set visited for the current node
        cur_data.visited = True
        print(float(current), "chosen from queue.", "g+h =", path_len)
        for neighbor in cur_data.neighbors:
            neighbor_data = graph[neighbor]
            if not neighbor_data.visited:
                # calculate the cost to get to the neighbor
                # this is the distance from one node to another
                dist = cur_data.dist + cur_data.calc_dist(neighbor_data)
                if dist < neighbor_data.dist:
                    neighbor_data.dist = dist
                    # calculate the cost including the estimate of the cost
                    # to the end which we calculate by the cost directly 
                    # from n to end
                    dist = neighbor_data.dist + neighbor_data.calc_dist(graph[end])
                    pq.put((dist, neighbor))
                    neighbor_data.cameFrom = current
                    # print("placed in queue:", "distance:", dist, neighbor_data)
    if current != end:
        return "Did not find a path from start: " + str(start) + " to end: " + str(end)

    current = graph[current] # set current to its data for the purpose of extraction
    ret = "path length = " + str(current.dist)
    # current is end
    path = []
    while current.cameFrom != None:
        path.append(current.identity)
        current = graph[current.cameFrom]
    path.append(start)
    path.reverse()
    return ret + "\npath = " + str(path)



# main function to run the A* tests
if __name__ == "__main__":
    print("loading graphs . . .")
    small_graph = readAdj("small_test")
    large_graph = readAdj("large_test")
    print("done")
    # class for unit testing purposes
    class testAStart(unittest.TestCase):
        def test_a0_8(self):
            print("\ntesting path on small graph from", 0, "to", 8)
            expected  = "path length = 10.509164910466922\npath = [0, 1, 9, 8]"
            best_path = a_star(small_graph, 0, 8)
            resetGraph(small_graph)
            print(best_path)
            self.assertTrue(expected == best_path, msg="\n" + best_path + "\ndoes not match:\n" + expected)
        def test_a4_9(self):
            print("\ntesting path on small graph from", 4, "to", 9)
            expected  = "path length = 9.129965246854832\npath = [4, 7, 8, 9]"
            best_path = a_star(small_graph, 4, 9)
            resetGraph(small_graph)
            print(best_path)
            self.assertTrue(expected == best_path, msg="\n" + best_path + "\ndoes not match:\n" + expected)
        def test_a2_9(self):
            print("\ntesting path on small graph from", 2, "to", 9)
            expected  = "path length = 7.256856116503386\npath = [2, 1, 9]"
            best_path = a_star(small_graph, 2, 9)
            resetGraph(small_graph)
            print(best_path)
            self.assertTrue(expected == best_path, msg="\n" + best_path + "\ndoes not match:\n" + expected)
        def test_b0_80(self):
            print("\ntesting path on large graph from", 0, "to", 80)
            expected  = "path length = 1450.8565674129345\npath = [0, 6264, 2326, 80]"
            best_path = a_star(large_graph, 0, 80)
            resetGraph(large_graph)
            print(best_path)
            self.assertTrue(expected == best_path, msg="\n" + best_path + "\ndoes not match:\n" + expected)
        def test_b7000_573(self):
            print("\ntesting path on large graph from", 7000, "to", 573)
            expected  = "path length = 2197.8002783634197\npath = [7000, 9968, 7441, 573]"
            best_path = a_star(large_graph, 7000, 573)
            resetGraph(large_graph)
            print(best_path)
            self.assertTrue(expected == best_path, msg="\n" + best_path + "\ndoes not match:\n" + expected)
    
    # run the tests
    unittest.main(verbosity=2)
