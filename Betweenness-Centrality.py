#!/usr/bin/env python3

import re
import itertools

class Graph(object):

	def __init__ (self, vertices, edges, graph_dict):

		self.vertices = vertices
		
		ordered_edges = list(map(lambda x: (min(x), max(x)), edges))
		
		self.edges    = ordered_edges
		self.graph_dict = graph_dict
		

	def min_dist(self, graph_dict, start_node, end_node):

		visited = []
		queue = [start_node]

		if ((start_node == end_node)==True):
			return start_node 

		while queue:
			path = queue.pop(0)
			m=0
			node = path[m-1]
			if ((node in visited)==False):
				neighbours = self.graph_dict[node]
			# go through all adjacent nodes, construct a new path and
			# push it into the queue
				for adjacent in neighbours:
					new_path = list(path)
					new_path.append(adjacent)
					queue.append(new_path)

					if ((adjacent == end_node)!=False):
						route= new_path
						new_route=list(map(int,route))
						num=len(new_route)
						return(num) 



	def all_paths(self, graph_dict, start, end, path=[]):

		paths = []
		path = path + [start]
		if ((start != end)==False):
			return [path]
		#to check for each list in the dictionary
		for node in graph_dict[start]:
			if ((node in path)==False):
				newpaths = self.all_paths(graph_dict, node, end, path)
				for newpath in newpaths:

					paths.append(newpath)
		return paths


	def all_shortest_paths(self,paths):
		
		short_path_list=[]
		Min=10000000
		for i in paths:
			if(len(i)<Min):
				Min=len(i)
		for i in paths:
			if(len(i)==Min):
				short_path_list.append(i)

		return short_path_list


	def betweenness_centrality(self):
		n=len(vertices)
		central=[]
		total=0
		for i in vertices:
			sum=0
			for j in vertices:
				#to check for values that don't contain the node
				if(j!=i):
					for k in vertices:
						if (k>j and k!=i):
							total+=1
							L=graph.all_shortest_paths((graph.all_paths(graph_dict, str(j), str(k))))
							count=0
							x=0
							for l in L:
								x+=1
								if str(i) in l:
									count+=1
					
							sum+=count/x
			
			central.append(sum)

		standard_central=[]
		for i in central:
			standard=(2*i)/((n-1)*(n-2))
			standard_central.append(standard)
		return(standard_central)



	def top_k_betweenness_centrality(self):

		knodes=[]
		standard_central=graph.betweenness_centrality()
		max_node=max(standard_central)

		for i in range(len(standard_central)):
			#to search for the nodes that have the maximum value
			if(standard_central[i]==max_node):
				knodes.append(i+1)
		return(knodes)

		

if __name__ == "__main__":
	vertices = [1, 2, 3, 4, 5, 6]
	edges    = [(1, 2), (1, 4), (2, 3), (2, 5), (3, 4), (3,6), (4, 5), (4, 6)]
	graph_dict={}
	#to form an adjacent matrix
	for i in vertices:
		l=[]
		for j in edges:
			if i in j:
				if j[0]==i:
					l.append(str(j[1]))
				else:
					l.append(str(j[0]))
		graph_dict[str(i)]=l


	graph = Graph(vertices, edges, graph_dict)
	graph.min_dist(graph_dict, '1', '6')
	graph.all_paths(graph_dict, '1', '6')
	graph.all_shortest_paths(graph.all_paths(graph_dict, '1', '6'))
	graph.betweenness_centrality()
	print("Nodes that have the same (max) value:", graph.top_k_betweenness_centrality())