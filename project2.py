import random
import time
from typing import List, Tuple

class UnionFind:
    """Supports efficient cycle detection for Kruskal's algorithm."""
    def __init__(self, n: int):
        # Initially, each vertex is its own parent
        self.parent = list(range(n))
        self.rank = [0] * n 

    def find(self, x: int) -> int:
        """Find the root of node x with path compression."""
        if self.parent[x] != x:
            self.parent[x] = self.find(self.parent[x])
        return self.parent[x]

    def union(self, x: int, y: int) -> bool:
        """Union two sets; returns True if merged (no cycle), False if already connected."""
        rx = self.find(x)
        ry = self.find(y)
        if rx == ry:
            # x and y already in the same set → adding this edge would create a cycle
            return False
        # Merge smaller tree into larger tree (union by rank)
        if self.rank[rx] < self.rank[ry]:
            self.parent[rx] = ry
        elif self.rank[ry] < self.rank[rx]:
            self.parent[ry] = rx
        else:
            self.parent[ry] = rx
            self.rank[rx] += 1
        return True


# ---------------- Kruskal's Algorithm ----------------
def kruskal(n: int, edges: List[Tuple[int, int, int]]) -> None:
    """
    Run Kruskal's algorithm to find MST.
    """
    uf = UnionFind(n)

    sorted_edges = sorted(edges, key=lambda e: e[2])

    mst_edges = []

    for u, v, w in sorted_edges:
        if uf.union(u, v):
            mst_edges.append((u, v, w))
            if len(mst_edges) == n - 1:
                break


def generate_random_graph(n: int) -> List[Tuple[int, int, int]]:
    """Generate a random connected undirected weighted graph with n vertices."""
    edges = set()

   
    for i in range(n - 1):
        w = random.randint(1, 1000)
        edges.add((i, i + 1, w))

    max_edges = min(n * 2, n * (n - 1) // 2)
    while len(edges) < max_edges:
        u, v = random.sample(range(n), 2)
        w = random.randint(1, 1000)
        u, v = sorted((u, v))
        edges.add((u, v, w))

    return list(edges)

if __name__ == "__main__":
    print(f"{'Vertices':<12}{'Edges':<12}{'Time (ns)':<15}")
    print("-" * 40)
    
    for n in range(4, 26, 2):
        edges = generate_random_graph(n)

        # Measure algorithm execution time with perf_counter_ns() for precision
        start_time = time.perf_counter_ns()
        kruskal(n, edges)
        elapsed = time.perf_counter_ns() - start_time

        # Output vertices, edges, and execution time
        print(f"{n:<12}{len(edges):<12}{elapsed:<15}")