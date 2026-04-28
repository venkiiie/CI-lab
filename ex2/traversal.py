from queue import Queue
import heapq

def add_node(graph, node):
    if node not in graph:
        graph[node] = []
def delete_node(graph, node):
    if node in graph:
        del graph[node]
        for neighbours in graph.values():
            if node in neighbours:
                neighbours.remove(node)
    else:
        print("\nNode does not exist in the graph.")
def add_edge(graph, x, y, weight=1):
    if x not in graph:
        add_node(graph, x)
    if y not in graph:
        add_node(graph, y)
    if y not in graph[x]:
        graph[x].append(y)
    if x not in graph[y]:
        graph[y].append(x)
    # Store weights for both directions
    weights[(x, y)] = weight
    weights[(y, x)] = weight
def delete_edge(graph, x, y):
    if x in graph and y in graph[x]:
        graph[x].remove(y)
    if y in graph and x in graph[y]:
        graph[y].remove(x)
    # Remove weights
    if (x, y) in weights:
        del weights[(x, y)]
    if (y, x) in weights:
        del weights[(y, x)]
def display_adjlist(graph):
    print("\nAdjacency List:")
    for node in graph:
        print(f'{node}: {graph[node]}')
def bfs(graph, start, goals):
    visited = set([start])
    q = Queue()
    q.put(start)
    result = []
    print("\n\tBFS:")
    while not q.empty():
        print("\nFringe (queue):", list(q.queue))
        current = q.get()
        result.append(current)
        print("\nPath so far:", result)
        if current in goals:
            print("\nGoal found! Path:", result)
            break
        for neighbor in graph.get(current, []):
            if neighbor not in visited:
                q.put(neighbor)
                visited.add(neighbor)

def dfs(graph, start, goals):
    visited = set()
    stack = [start]
    result = []
    print("\n\tDFS Traversal:")
    while stack:
        print("Fringe (stack):", list(stack))
        current = stack.pop()
        if current not in visited:
            result.append(current)
            print("Path so far:", result)
            if current in goals:
                print("Goal found! Path:", result)
                break
            visited.add(current)
            for neighbor in reversed(graph.get(current, [])):  # For consistent order
                if neighbor not in visited:
                    stack.append(neighbor)

def ucs(graph, start, goals):
    visited = set()
    # Priority queue: (cumulative_cost, node, path)
    pq = [(0, start, [start])]
    print("\n\tUCS Traversal:")
    
    while pq:
        print("\nFringe (priority queue - cost, node):", [(cost, node) for cost, node, _ in pq])
        current_cost, current_node, path = heapq.heappop(pq)
        
        if current_node in visited:
            continue
            
        visited.add(current_node)
        print(f"Visiting: {current_node} with cost: {current_cost}")
        print("Path so far:", path)
        
        if current_node in goals:
            print(f"\nGoal found! Path: {path}")
            print(f"Total cost: {current_cost}")
            return path, current_cost
        
        for neighbor in graph.get(current_node, []):
            if neighbor not in visited:
                edge_weight = weights.get((current_node, neighbor), 1)
                new_cost = current_cost + edge_weight
                new_path = path + [neighbor]
                heapq.heappush(pq, (new_cost, neighbor, new_path))
    
    print("\nGoal not found!")
    return None, float('inf')

def a_star_search(graph, start, goals):
    visited = set()
    # Priority queue: (f_cost, g_cost, node, path)
    # f_cost = g_cost + h_cost (evaluation function)
    h_start = heuristics.get(start, 0)
    pq = [(h_start, 0, start, [start])]
    print("\n\tA* Search Traversal:")
    
    while pq:
        print("\nFringe (priority queue - f, g, node):", [(f, g, node) for f, g, node, _ in pq])
        f_cost, g_cost, current_node, path = heapq.heappop(pq)
        
        if current_node in visited:
            continue
            
        visited.add(current_node)
        h_cost = heuristics.get(current_node, 0)
        print(f"Visiting: {current_node} | g(n)={g_cost}, h(n)={h_cost}, f(n)={f_cost}")
        print("Path so far:", path)
        
        if current_node in goals:
            print(f"\nGoal found! Path: {path}")
            print(f"Total cost: {g_cost}")
            return path, g_cost
        
        for neighbor in graph.get(current_node, []):
            if neighbor not in visited:
                edge_weight = weights.get((current_node, neighbor), 1)
                new_g_cost = g_cost + edge_weight
                h_neighbor = heuristics.get(neighbor, 0)
                new_f_cost = new_g_cost + h_neighbor
                new_path = path + [neighbor]
                heapq.heappush(pq, (new_f_cost, new_g_cost, neighbor, new_path))
    
    print("\nGoal not found!")
    return None, float('inf')

graph = {}
weights = {}  # Dictionary to store edge weights
heuristics = {}  # Dictionary to store heuristic values for A*
n = int(input("Enter number of nodes: "))
print("Enter Nodes:")
for _ in range(n):
    node = input()
    add_node(graph, node)

e = int(input("Enter number of edges: "))
print("Enter Edges (x y weight) or (x y) for weight=1:")
for _ in range(e):
    edge_input = input().split()
    if len(edge_input) == 3:
        x, y, w = edge_input[0], edge_input[1], int(edge_input[2])
        add_edge(graph, x, y, w)
    else:
        x, y = edge_input[0], edge_input[1]
        add_edge(graph, x, y)
display_adjlist(graph)
print("\n\t----Menu----\n0.Exit\n1.BFS\n2.DFS\n3.UCS\n4.Add node\n5.Add edge\n6.Delete node\n7.Delete edge\n8.Display adjacency list\n9.A* Search\n")
while True:
    ch = int(input("\nEnter choice (0-9): "))
    if ch == 1:
        start = input("Enter Start node: ")
        k = int(input("Enter number of goal nodes: "))
        print("Enter Goal nodes:")
        goals = set(input() for _ in range(k))
        bfs(graph, start, goals)
    elif ch == 2:
        start = input("Enter Start node: ")
        k = int(input("Enter number of goal nodes: "))
        print("Enter Goal nodes:")
        goals = set(input() for _ in range(k))
        dfs(graph, start, goals)
    elif ch == 3:
        start = input("Enter Start node: ")
        k = int(input("Enter number of goal nodes: "))
        print("Enter Goal nodes:")
        goals = set(input() for _ in range(k))
        ucs(graph, start, goals)
    elif ch == 4:
        n = int(input("Enter number of nodes: "))
        print("Enter Nodes:")
        for _ in range(n):
            node = input()
            add_node(graph, node)
    elif ch == 5:
        e = int(input("Enter number of edges: "))
        print("Enter Edges (x y weight) or (x y) for weight=1:")
        for _ in range(e):
            edge_input = input().split()
            if len(edge_input) == 3:
                x, y, w = edge_input[0], edge_input[1], int(edge_input[2])
                add_edge(graph, x, y, w)
            else:
                x, y = edge_input[0], edge_input[1]
                add_edge(graph, x, y)
    elif ch == 6:
        n = int(input("Enter number of nodes: "))
        print("Enter Nodes:")
        for _ in range(n):
            node = input()
            delete_node(graph, node)
    elif ch == 7:
        e = int(input("Enter number of edges: "))
        print("Enter Edges (x y):")
        for _ in range(e):
            x, y = input().split()
            delete_edge(graph, x, y)
    elif ch == 8:
        display_adjlist(graph)
    elif ch == 9:
        print("\n--- A* Search ---")
        # Set heuristics first
        print("\nSet Heuristic Values (estimated cost to goal):")
        n = int(input("Enter number of nodes to set heuristics: "))
        print("Enter Node and Heuristic value (node h_value):")
        heuristics.clear()  # Clear previous heuristics
        for _ in range(n):
            node_h = input().split()
            node = node_h[0]
            h_value = int(node_h[1])
            heuristics[node] = h_value
        print("\nHeuristics set:", heuristics)
        
        # Now run A* search
        start = input("\nEnter Start node: ")
        k = int(input("Enter number of goal nodes: "))
        print("Enter Goal nodes:")
        goals = set(input() for _ in range(k))
        a_star_search(graph, start, goals)
    elif ch == 0:
        break
    else:
        print("\nInvalid Choice.")
