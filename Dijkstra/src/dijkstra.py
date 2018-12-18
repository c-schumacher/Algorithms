from collections import defaultdict
import heapq

def dijkstra(fname):
    def get_adj_list(fname):
        ''' converts a text file in the directory into a digestible format'''
        adj_list = []
        with open(fname) as inputFile:
            next(inputFile)
            for line in inputFile:
                adj_list.append(line.strip('\n').split(' '))
            for row in adj_list:
                row[2] = int(row[2])
        return adj_list
    
    def heap_idx(k):
        ''' returning the index in the heap for accessing different elements of (dist, v) pairs'''
        return zip(*min_heap)[1].index(k) 
    
    def update_key(k, dist):
        ''' updates the key and value pair in the heap. deletes first if already present'''
        if len(min_heap) > 0 and k in zip(*min_heap)[1]:
            min_heap.pop(heap_idx(k))
        heapq.heappush(min_heap, (dist, k))
        
    def in_heap(k):
        ''' checking if a key is in the heap already'''
        if len(min_heap) < 1:
            return False
        elif k in zip(*min_heap)[1]:
            return True
        else: 
            return False
        
    def B_route():
        ''' returns the shortest route from A to B'''
        parents_list = ['B']
        for i in range(len(distances)):
            parent = parents[(parents_list[-1])]
            parents_list.append(parent)
            if parent == 'A':
                break
        return [i for i in reversed(parents_list)]
    

    ''' executing dijkstra's algorithm on a given directed graph'''
    case = get_adj_list(fname)
    edge_dict = defaultdict(list)
    for edge in case:
        edge_dict[edge[0]].append([edge[1], edge[2]])

    parents ={}
    distances = {}
    for i in range(2):
        for j in zip(*case)[i]:
            if j not in parents:
                parents[j] = None
                distances[j] = float('inf')

    distances['A'] = 0
    min_heap = []
    for k in edge_dict.keys():
        update_key(k, distances[k])
        
    while len(min_heap) > 0:                      
        u = heapq.heappop(min_heap)[1]            
        u_neighbors = zip(*edge_dict[u])
        if not u_neighbors:                       
            break
        for w in u_neighbors[0]:                   
            dist_u = distances[u] 
            dist_w = dist_u + u_neighbors[1][u_neighbors[0].index(w)]
            if distances[w] >= dist_w:  
                distances[w] = distances[u] + u_neighbors[1][u_neighbors[0].index(w)]
                parents[w] = u
                update_key(w, distances[w])

    return (distances['B'], B_route())
