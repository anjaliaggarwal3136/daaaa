import tkinter as tk
from tkinter import messagebox, simpledialog
import networkx as nx
import matplotlib.pyplot as plt
import heapq

def dijkstra(graph, start):
    distances = {node: float('inf') for node in graph}
    distances[start] = 0
    priority_queue = [(0, start)]
    
    while priority_queue:
        current_distance, current_node = heapq.heappop(priority_queue)
        
        if current_distance > distances[current_node]:
            continue
        
        for neighbor, weight in graph[current_node].items():
            distance = current_distance + weight
            
            if distance < distances[neighbor]:
                distances[neighbor] = distance
                heapq.heappush(priority_queue, (distance, neighbor))
    
    return distances

def visualize_graph(graph, start, shortest_paths):
    G = nx.Graph()
    
    for node in graph:
        for neighbor, weight in graph[node].items():
            G.add_edge(node, neighbor, weight=weight)
    
    pos = nx.spring_layout(G)
    labels = nx.get_edge_attributes(G, 'weight')
    
    plt.figure(figsize=(6, 4))
    nx.draw(G, pos, with_labels=True, node_color='lightblue', node_size=2000, edge_color='gray', font_size=10)
    nx.draw_networkx_edge_labels(G, pos, edge_labels=labels)
    
    # Highlight the shortest path from start node
    for node in shortest_paths:
        nx.draw_networkx_nodes(G, pos, nodelist=[node], node_color='red', node_size=2000)
    
    plt.title(f"Shortest Paths from {start}")
    plt.show()

def process_input():
    user_input = entry.get()
    edges = user_input.split(',')
    graph = {}
    
    try:
        for edge in edges:
            node1, node2, weight = edge.strip().split()
            weight = int(weight)
            if node1 not in graph:
                graph[node1] = {}
            if node2 not in graph:
                graph[node2] = {}
            graph[node1][node2] = weight
            graph[node2][node1] = weight
    except ValueError:
        messagebox.showerror("Error", "Invalid input format! Use format: A B 10, B C 5")
        return
    
    start_node = simpledialog.askstring("Input", "Enter the starting node:")
    if start_node not in graph:
        messagebox.showerror("Error", "Invalid starting node!")
        return
    
    result = dijkstra(graph, start_node)
    result_text.set(f"Shortest paths from {start_node}:\n" + "\n".join([f"{key}: {value}" for key, value in result.items()]))
    visualize_graph(graph, start_node, result.keys())

def create_gui():
    global entry, result_text
    root = tk.Tk()
    root.title("Traffic Flow Optimization - Dijkstra")
    
    tk.Label(root, text="Enter roads (format: A B 10, B C 5, ...):").pack()
    entry = tk.Entry(root, width=50)
    entry.pack()
    
    tk.Button(root, text="Run Optimization", command=process_input).pack()
    
    result_text = tk.StringVar()
    tk.Label(root, textvariable=result_text, wraplength=400).pack()
    
    root.mainloop()

if _name_ == "_main_":
    create_gui()
