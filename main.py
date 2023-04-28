import sys
import json

#Function you can input a node into and itll give bellman_ford distance/path back
def bellman_ford(graph, start):
    distances = {}
    for node in graph:
        distances[node] = float('inf')
    distances[start] = 0

    parents = {v: None for v in graph}
    #u = root node 
    #v = node to path
    for _ in range(len(graph) - 1):
        for u in graph:
            for v in graph[u]['connected']:
                weight = graph[u]['connected'][v]
                if distances[u] + weight < distances[v]:
                    distances[v] = distances[u] + weight
                    parents[v] = u

    for u in graph:
        for v in graph[u]['connected']:
            weight = graph[u]['connected'][v]
            if distances[u] + weight < distances[v]:
                raise ValueError('Graph contains a negative-weight cycle')
    return distances, parents

#Main

#Create graph given the input from config(JSON) file
if len(sys.argv) < 2:
    print("Error: Type command in CLI python main.py <config_file>")
    sys.exit(1)

config_file = sys.argv[1]
fp = open(config_file)
config = json.load(fp)

#'connected' for Connected Nodes with their associated costs
graph = {node: {'connected': {}} for node in config['ROUTERS']['routers']}
for node in graph:
    graph[node]['connected'] = config['ROUTERS']['vertices'][node]

#Add paths for each node in graph to every other node using Bellman Ford Algo
for node in graph:
    distances, parents = bellman_ford(graph, node)
    graph[node]['path_cost'] = distances
    graph[node]['path'] = parents

#Print Statement for graph
for i in graph:
    print( "'" + str(i) + "':" + str(graph[i]))
