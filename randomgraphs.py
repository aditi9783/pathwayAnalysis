#!/usr/bin/python

import random

nG = 1;
MIN = 0.75; # probability to not have an edge between two nodes

def recursive_dfs(graph, start, path=[]):
	'''recursive depth first search from start'''
	path=path+[start]
	
	for node in graph[start]:
		print node, "::";
		if not node in path:
			print node, "not in ", path;
			path=recursive_dfs(graph, node, path)
	return path

for i in range(nG):
	nn = random.randrange(5, 10);
	g = {};	
	# initialize adj list for all nodes
	for a in range(nn):
		g[str(a)] = [];

	for a in range(nn):
		for b in range(a+1,nn):
			if (random.random() > MIN): # add edge to adjacency list of both nodes
				g[str(a)].append(str(b));
				g[str(b)].append(str(a));
	print g;
	print recursive_dfs(g, "0");
		#print a, ":", ",".join(list);
	#print "\n";
	
#graph = {'A':['B','C'],'B':['D','E'],'C':['D','E'],'D':['E'],'E':['A']}
#print 'recursive dfs ', recursive_dfs(graph, 'A')
