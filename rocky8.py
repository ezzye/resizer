import networkx as nx
import matplotlib.pyplot as plt


def draw_startup_graph(system):
    G = nx.DiGraph()

    if system == "CentOS 7":
        # Linear, more sequential startup
        G.add_edge("Service A", "Service B")
        G.add_edge("Service B", "Service C")
        G.add_edge("Service C", "Service D")
        title = "CentOS 7 (Upstart) Startup Sequence"
    else:
        # Parallel, dependency-based startup
        G.add_edge("Service A", "Service B")
        G.add_edge("Service A", "Service C")
        G.add_edge("Service B", "Service D")
        G.add_edge("Service C", "Service D")
        title = "Rocky Linux 8 (systemd) Startup Sequence"

    pos = nx.spring_layout(G)
    nx.draw(G, pos, with_labels=True, node_color='skyblue', node_size=2000, edge_color='black', linewidths=1,
            font_size=15)
    plt.title(title)
    plt.show()


# Draw the graphs for CentOS 7 and Rocky Linux 8
draw_startup_graph("CentOS 7")
draw_startup_graph("Rocky Linux 8")
