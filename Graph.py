#!/usr/bin/python3
# -*- coding: UTF-8 -*-

import copy

# This class represents a directed graph for the component network
class NetworkGraph:
    def __init__(self, vertices):
        # No. of vertices
        #self.V = vertices
        # default dictionary to store graph
        #self.graph = defaultdict(list)
        self.graph = {}
        for vertex in vertices:
            self.graph[vertex] = []

    # function to add an edge to graph
    def addEdge(self, u, v):
        if u in self.graph:
            self.graph[u].append(v)
        else:
            self.graph[u] = []
            self.graph[u].append(v)

    # A recursive function to print/store all paths from 's' to 'e', considering the case when s is equal to e
    # visited[] keeps track of vertices in current path, path[] stores actual vertices and path_index is current index in path[]
    def printAllPaths(self, s, e, step, visited, path):
        visited[s] = True
        path.append(s)
        if s == e and step == 0:
            step = step + 1
            visited[s] = False
            for i in self.graph[s]:
                if visited[i] == False:
                    self.printAllPaths(i, e, step, visited, path)
        elif s == e and step != 0:
            print(path)
        else:
            # If current vertex is not destination, recur for all the vertices adjacent to this vertex
            step = step + 1
            for i in self.graph[s]:
                if visited[i] == False:
                    self.printAllPaths(i, e, step, visited, path)
        # Remove current vertex from path[] and mark it as unvisited
        path.pop()
        visited[s] = False

    def storeAllPaths(self, s, e, step, visited, path, paths):
        visited[s] = True
        path.append(s)
        if s == e and step == 0:
            step = step + 1
            visited[s] = False
            for i in self.graph[s]:
                if visited[i] == False:
                    self.storeAllPaths(i, e, step, visited, path, paths)
        elif s == e and step != 0:
            #print(path)
            paths.append(copy.deepcopy(path))
        else:
            # If current vertex is not destination, recur for all the vertices adjacent to this vertex
            step = step + 1
            for i in self.graph[s]:
                if visited[i] == False:
                    self.storeAllPaths(i, e, step, visited, path, paths)
        # Remove current vertex from path[] and mark it as unvisited
        path.pop()
        visited[s] = False


    # A recursive function to print/store all paths from 's' to 'e', not considering the case that s is equal to e
    def printAllPaths2(self, s, e, visited, path):
        # Mark the current node as visited and store in path
        visited[s] = True
        path.append(s)
        # If current vertex is same as destination, then print current path[]
        if s == e:
            print(path)
        else:
            # If current vertex is not destination, recur for all the vertices adjacent to this vertex
            for i in self.graph[s]:
                if visited[i] == False:
                    self.printAllPaths2(i, e, visited, path)
        # Remove current vertex from path[] and mark it as unvisited
        path.pop()
        visited[s] = False

    def storeAllPaths2(self, s, e, visited, path, paths):
        # Mark the current node as visited and store in path
        visited[s] = True
        path.append(s)
        # If current vertex is same as destination, then print current path[]
        if s == e:
            #print(path)
            paths.append(copy.deepcopy(path))
        else:
            # If current vertex is not destination, recur for all the vertices adjacent to this vertex
            for i in self.graph[s]:
                if visited[i] == False:
                    self.storeAllPaths2(i, e, visited, path, paths)
        # Remove current vertex from path[] and mark it as unvisited
        path.pop()
        visited[s] = False

    def calculatePath(self):
        pass