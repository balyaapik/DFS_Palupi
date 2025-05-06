import streamlit as st
import time
import networkx as nx
import matplotlib.pyplot as plt

# Setup Streamlit page
st.set_page_config(page_title="DFS Visualization with Stack", layout="centered")
st.title("🔁 DFS Traversal with Stack Visualization")

# Default graph (directed)
default_graph = {
    "Austin": ["Dallas", "Houston"],
    "Dallas": ["Denver", "Austin", "Chicago"],
    "Houston": ["Atlanta"],
    "Chicago": ["Denver"],
    "Denver": ["Chicago", "Atlanta"],
    "Atlanta": ["Washington", "Houston"],
    "Washington": ["Atlanta", "Dallas"]
}

# Sidebar for graph customization
st.sidebar.header("Graph Setup")
custom_graph = st.sidebar.checkbox("Use custom graph?")
if custom_graph:
    graph_input = st.sidebar.text_area(
        "Graph as adjacency list (e.g., A:B,C)",
        value="A:B,C\nB:D,E\nC:F\nD:\nE:F\nF:"
    )
    graph = {}
    for line in graph_input.strip().splitlines():
        if ':' in line:
            node, neighbors = line.split(':')
            graph[node.strip()] = [n.strip() for n in neighbors.split(',') if n.strip()]
else:
    graph = default_graph

start_node = st.sidebar.selectbox("Start Node", list(graph.keys()))

# DFS with Stack Visualization and Bidirectional Arrows
def dfs_with_stack(graph, start):
    visited = set()
    stack = [start]
    traversal = []

    # Create MultiDiGraph to allow bidirectional arrows
    G = nx.MultiDiGraph()
    for node, neighbors in graph.items():
        for neighbor in neighbors:
            G.add_edge(node, neighbor)

    pos = nx.spring_layout(G, seed=42)

    # Initial graph view
    fig, ax = plt.subplots()
    nx.draw_networkx_nodes(G, pos, ax=ax, node_color='lightblue')
    nx.draw_networkx_labels(G, pos, ax=ax)
    nx.draw_networkx_edges(
        G, pos, ax=ax,
        connectionstyle='arc3,rad=0.2',
        arrows=True,
        edge_color='gray'
    )
    st.pyplot(fig)

    while stack:
        current = stack.pop()
        if current not in visited:
            traversal.append(current)
            visited.add(current)

            # Determine node colors
            node_colors = []
            for node in G.nodes():
                if node == current:
                    node_colors.append('red')
                elif node in visited:
                    node_colors.append('green')
                elif node in stack:
                    node_colors.append('orange')
                else:
                    node_colors.append('lightblue')

            # Draw graph with updated colors
            fig, ax = plt.subplots()
            nx.draw_networkx_nodes(G, pos, ax=ax, node_color=node_colors)
            nx.draw_networkx_labels(G, pos, ax=ax)
            nx.draw_networkx_edges(
                G, pos, ax=ax,
                connectionstyle='arc3,rad=0.2',
                arrows=True,
                edge_color='gray'
            )
            st.pyplot(fig)

            # Display status
            st.write(f"🔴 **Current Node**: `{current}`")
            st.write(f"📚 **Stack**: `{stack}`")
            st.write(f"✅ **Visited**: `{list(visited)}`")

            # Push unvisited neighbors to the stack
            for neighbor in reversed(graph[current]):
                if neighbor not in visited:
                    stack.append(neighbor)

            time.sleep(1)

    return traversal

# Run visualization
if st.button("Start DFS Visualization"):
    st.subheader(f"🔍 DFS from `{start_node}`")
    dfs_order = dfs_with_stack(graph, start_node)
    st.success(f"✅ Traversal Order: {' → '.join(dfs_order)}")
