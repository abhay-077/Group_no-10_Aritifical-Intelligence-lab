# LAB 02: DFS, BFS and A* Search Algorithms
# Aim: To implement and understand Depth First Search, Breadth First Search,
# and A* Search for solving search problems using Python.

from collections import deque
import heapq


def get_path_cost(graph, path):
    """
    Calculates total path cost along a list of traversed nodes.
    Returns infinity if any consecutive edge does not exist.
    """
    if not path or len(path) < 2:
        return 0
    total_cost = 0
    for i in range(len(path) - 1):
        u, v = path[i], path[i + 1]
        edge_cost = None
        for neighbor, weight in graph.get(u, []):
            if neighbor == v:
                edge_cost = weight
                break
        if edge_cost is None:
            return float('inf')
        total_cost += edge_cost
    return total_cost


def dfs(graph, start, goal):
    """
    Depth First Search (DFS) implementation using an explicit stack.
    Explores as deep as possible along each branch before backtracking.
    Returns: (path, total_cost) or (None, None) if goal is unreachable.
    """
    # Stack stores tuples of: (current_node, path_so_far)
    stack = [(start, [start])]
    visited = set()

    while stack:
        current, path = stack.pop()

        if current == goal:
            cost = get_path_cost(graph, path)
            return path, cost

        if current not in visited:
            visited.add(current)
            # Add neighbors in reverse order so first neighbor is popped first
            for neighbor, _ in reversed(graph.get(current, [])):
                if neighbor not in visited:
                    stack.append((neighbor, path + [neighbor]))

    return None, None


def bfs(graph, start, goal):
    """
    Breadth First Search (BFS) implementation using a queue.
    Explores the neighbor nodes first before moving to next level neighbors.
    Guarantees finding the path with the fewest edges.
    Returns: (path, total_cost) or (None, None) if goal is unreachable.
    """
    # Queue stores tuples of: (current_node, path_so_far)
    queue = deque([(start, [start])])
    visited = {start}

    while queue:
        current, path = queue.popleft()

        if current == goal:
            cost = get_path_cost(graph, path)
            return path, cost

        for neighbor, _ in graph.get(current, []):
            if neighbor not in visited:
                visited.add(neighbor)
                queue.append((neighbor, path + [neighbor]))

    return None, None


def a_star(graph, heuristics, start, goal):
    """
    A* Search implementation using a Priority Queue (min-heap).
    Evaluation function: f(n) = g(n) + h(n)
      g(n): Actual cost from start node to node n
      h(n): Estimated (heuristic) cost from node n to goal
    Returns: (path, total_cost, nodes_expanded) or (None, None, nodes_expanded)
    """
    # Priority queue stores: (f_score, g_score, current_node, path)
    initial_f = heuristics.get(start, 0)
    pq = [(initial_f, 0, start, [start])]

    # Dictionary to keep track of lowest cost g(n) to reach each node
    best_g = {start: 0}
    nodes_expanded = []

    while pq:
        f_val, g_val, current, path = heapq.heappop(pq)

        # Skip if we already found a strictly better path to current
        if g_val > best_g.get(current, float('inf')):
            continue

        nodes_expanded.append(current)

        if current == goal:
            return path, g_val, nodes_expanded

        for neighbor, weight in graph.get(current, []):
            new_g = g_val + weight
            if new_g < best_g.get(neighbor, float('inf')):
                best_g[neighbor] = new_g
                h_val = heuristics.get(neighbor, 0)
                new_f = new_g + h_val
                heapq.heappush(pq, (new_f, new_g, neighbor, path + [neighbor]))

    return None, None, nodes_expanded


def print_search_result(algorithm_name, start, goal, path, cost, extra_info=None):
    """Utility helper to print formatted search results."""
    print(f"\n--- {algorithm_name} ---")
    print(f"  Start Node: '{start}'  -->  Goal Node: '{goal}'")
    if path:
        print(f"  Path Found: {' -> '.join(path)}")
        print(f"  Total Cost: {cost}")
        if extra_info:
            print(f"  {extra_info}")
    else:
        print(f"  [RESULT] Goal '{goal}' is UNREACHABLE from '{start}'.")


def main():
    print("=" * 65)
    print(" LAB 02: DFS, BFS, AND A* SEARCH ALGORITHMS")
    print("=" * 65)

    # -------------------------------------------------------------
    # 1. Graph Representation: Adjacency List with Edge Costs
    # -------------------------------------------------------------
    # Each entry maps a node to a list of (neighbor, edge_cost) tuples
    graph = {
        'S': [('A', 1), ('B', 4)],
        'A': [('B', 2), ('C', 5), ('D', 12)],
        'B': [('C', 2)],
        'C': [('D', 3), ('G', 4)],
        'D': [('G', 1)],
        'G': [],
        'Z': []  # Disconnected isolated node to test unreachable goal
    }

    # Heuristic estimates h(n) towards Goal 'G' (must be admissible: h(n) <= true cost)
    heuristics = {
        'S': 7,
        'A': 6,
        'B': 4,
        'C': 2,
        'D': 1,
        'G': 0,
        'Z': 10
    }

    print("\n[INFO] Graph Adjacency List (Directed Weighted):")
    for node, edges in graph.items():
        if edges:
            edge_strs = [f"{neighbor} (cost: {cost})" for neighbor, cost in edges]
            print(f"  Node '{node}' -> [{', '.join(edge_strs)}]")
        else:
            print(f"  Node '{node}' -> [No outgoing edges]")

    print("\n[INFO] Heuristic Values h(n) towards Goal 'G':")
    for node, h_val in heuristics.items():
        print(f"  h('{node}') = {h_val}")

    start_node = 'S'
    goal_node = 'G'

    # -------------------------------------------------------------
    # 2. Execute DFS
    # -------------------------------------------------------------
    dfs_path, dfs_cost = dfs(graph, start_node, goal_node)
    print_search_result("Depth First Search (DFS)", start_node, goal_node, dfs_path, dfs_cost)

    # -------------------------------------------------------------
    # 3. Execute BFS
    # -------------------------------------------------------------
    bfs_path, bfs_cost = bfs(graph, start_node, goal_node)
    print_search_result("Breadth First Search (BFS)", start_node, goal_node, bfs_path, bfs_cost,
                        "Note: BFS finds the shallowest path (fewest edges).")

    # -------------------------------------------------------------
    # 4. Execute A* Search
    # -------------------------------------------------------------
    astar_path, astar_cost, expanded = a_star(graph, heuristics, start_node, goal_node)
    print_search_result(
        "A* Search (f = g + h)", start_node, goal_node, astar_path, astar_cost,
        f"Nodes Expanded in order: {' -> '.join(expanded)} (Guaranteed optimal with admissible h)"
    )

    # -------------------------------------------------------------
    # 5. Handle Unreachable Goal Gracefully
    # -------------------------------------------------------------
    unreachable_goal = 'Z'
    print("\n" + "=" * 65)
    print(f" TEST CASE: HANDLING UNREACHABLE GOAL '{unreachable_goal}'")
    print("=" * 65)

    dfs_p, dfs_c = dfs(graph, start_node, unreachable_goal)
    print_search_result("DFS Unreachable Test", start_node, unreachable_goal, dfs_p, dfs_c)

    bfs_p, bfs_c = bfs(graph, start_node, unreachable_goal)
    print_search_result("BFS Unreachable Test", start_node, unreachable_goal, bfs_p, bfs_c)

    a_p, a_c, _ = a_star(graph, heuristics, start_node, unreachable_goal)
    print_search_result("A* Unreachable Test", start_node, unreachable_goal, a_p, a_c)


if __name__ == "__main__":
    main()
