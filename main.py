import networkx as nx
import matplotlib.pyplot as plt

from preprocess import lazy_get_pkg

visited = []
edges = []
total_size = 0


class Node:
    """A node that represents a package."""
    def __init__(self, name: str, size: int) -> None:
        self.name = name
        self.size = size
        self.deps = []

    def add_dep(self, pkg_name: str) -> None:
        """Add a dependency to a package."""
        pkg = self.create_node(pkg_name)
        self.deps.append(pkg)

    @classmethod
    def create_node(cls, pkg_name: str):
        print('Creating package:', pkg_name)
        pkg_info = lazy_get_pkg(pkg_name)
        pkg = cls(pkg_info['name'], pkg_info['size'])
        requires_dist = pkg_info['requires_dist']
        if requires_dist is not None:
            for dist in pkg_info['requires_dist']:
                dist_node = cls.create_node(dist[0])
                pkg.deps.append(dist_node)
        return pkg


def calc_total_size(root: Node) -> int:
    global visited
    global total_size
    visited.append(root.name)
    total_size += root.size

    for node in root.deps:
        edges.append((root.name, node.name))
        if node.name in visited: continue
        visited.append(node.name)
        total_size += node.size
        total_size += calc_total_size(node)

    return total_size


if __name__ == '__main__':
    root = Node.create_node('tensorflow')
    print('total size:', calc_total_size(root))
    print('edges:', edges)
    graph = nx.DiGraph()
    graph.add_nodes_from(visited)
    graph.add_edges_from(edges)

    nx.draw_networkx(graph, with_labels=True, node_size=1500)
    plt.show()
