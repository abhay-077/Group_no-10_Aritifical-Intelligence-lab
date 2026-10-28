# LAB 02B: Best First Search, A*, AO* and Hill Climbing
# Aim: To implement and demonstrate Best First Search, A*, AO*, and
# Hill Climbing algorithms for solving AI search problems.

import heapq


# =====================================================================
# 1. GREEDY BEST FIRST SEARCH & A* SEARCH
# =====================================================================

def greedy_best_first_search(graph, heuristics, start, goal):
    """
    Greedy Best First Search evaluates nodes based ONLY on the heuristic h(n):
    f(n) = h(n).
    It expands the node that appears closest to the goal, ignoring accumulated path cost g(n).
    """
    # Priority Queue stores: (h(n), current_node, path, g_cost)
    pq = [(heuristics.get(start, 0), start, [start], 0)]
    visited = set()
    expanded_order = []

    while pq:
        h_val, current, path, g_cost = heapq.heappop(pq)

        if current in visited:
            continue
        visited.add(current)
        expanded_order.append(current)

        if current == goal:
            return path, g_cost, expanded_order

        for neighbor, weight in graph.get(current, []):
            if neighbor not in visited:
                new_g = g_cost + weight
                h_neigh = heuristics.get(neighbor, 0)
                heapq.heappush(pq, (h_neigh, neighbor, path + [neighbor], new_g))

    return None, float('inf'), expanded_order


def a_star_search(graph, heuristics, start, goal):
    """
    A* Search balances path cost and heuristic estimate:
    f(n) = g(n) + h(n).
    Guarantees the optimal path when h(n) is admissible (never overestimates).
    """
    # Priority Queue stores: (f(n), g(n), current_node, path)
    pq = [(heuristics.get(start, 0), 0, start, [start])]
    best_g = {start: 0}
    expanded_order = []

    while pq:
        f_val, g_cost, current, path = heapq.heappop(pq)

        if g_cost > best_g.get(current, float('inf')):
            continue

        expanded_order.append(current)

        if current == goal:
            return path, g_cost, expanded_order

        for neighbor, weight in graph.get(current, []):
            new_g = g_cost + weight
            if new_g < best_g.get(neighbor, float('inf')):
                best_g[neighbor] = new_g
                f_neigh = new_g + heuristics.get(neighbor, 0)
                heapq.heappush(pq, (f_neigh, new_g, neighbor, path + [neighbor]))

    return None, float('inf'), expanded_order


# =====================================================================
# 2. AO* ALGORITHM (AND-OR GRAPH SEARCH)
# =====================================================================

class AOStarGraph:
    """
    Represents an AND-OR Graph for problem reduction.
    Each node has alternative hyper-branches:
      - 'OR' branch: solving ANY one child is sufficient.
      - 'AND' branch: ALL children must be solved simultaneously.
    """
    def __init__(self, branches, heuristics):
        # branches: { node: [ (type, [children], branch_cost), ... ] }
        self.branches = branches
        # heuristics: { node: estimated_cost }
        self.heuristics = dict(heuristics)
        # solved status for each node
        self.solved = {node: False for node in heuristics}
        # marked best branch for each node: { node: chosen_branch_index }
        self.marked = {}

    def cost_of_branch(self, branch):
        b_type, children, edge_cost = branch
        if b_type == 'OR':
            # For OR branch: edge_cost + h(child)
            child = children[0]
            return edge_cost + self.heuristics[child]
        elif b_type == 'AND':
            # For AND branch: sum(edge_cost + h(child)) for all children
            return len(children) * edge_cost + sum(self.heuristics[c] for c in children)

    def is_branch_solved(self, branch):
        _, children, _ = branch
        return all(self.solved.get(c, False) for c in children)

    def find_best_branch(self, node):
        node_branches = self.branches.get(node, [])
        if not node_branches:
            return None, self.heuristics.get(node, 0)

        best_idx = 0
        min_cost = float('inf')
        for idx, branch in enumerate(node_branches):
            b_cost = self.cost_of_branch(branch)
            b_type, children, edge_cost = branch
            if b_type == 'OR':
                formula = f"{edge_cost} + h({children[0]})"
            else:
                formula = " + ".join(f"{edge_cost} + h({c})" for c in children)
            print(f"    Evaluating Branch {idx} ({b_type} -> {children}): Cost = {formula} = {b_cost}")
            if b_cost < min_cost:
                min_cost = b_cost
                best_idx = idx

        return best_idx, min_cost

    def step(self, node):
        """
        Recursive step of AO*:
        1. If node is leaf/terminal, mark solved if no further branches.
        2. Expand down the marked tree, update costs bottom-up.
        """
        if self.solved.get(node, False):
            return

        node_branches = self.branches.get(node, [])
        if not node_branches:
            # Terminal goal leaf with no further branches
            self.solved[node] = True
            return

        print(f"  [Expanding Node '{node}'] (Current h = {self.heuristics[node]}):")
        # Choose best branch
        best_idx, min_cost = self.find_best_branch(node)
        self.marked[node] = best_idx
        self.heuristics[node] = min_cost
        chosen_branch = node_branches[best_idx]
        print(f"    --> Selected Branch {best_idx} ({chosen_branch[0]} -> {chosen_branch[1]}) with Min Cost = {min_cost}")

        b_type, children, _ = chosen_branch

        # Recursively update children
        for child in children:
            if not self.solved.get(child, False):
                self.step(child)

        # Re-evaluate node cost after child updates
        best_idx, min_cost = self.find_best_branch(node)
        self.marked[node] = best_idx
        self.heuristics[node] = min_cost

        # Mark solved if all children of best branch are solved
        if self.is_branch_solved(node_branches[best_idx]):
            self.solved[node] = True
            print(f"  [SOLVED] Node '{node}' is now completely SOLVED!")

    def run(self, root, max_iterations=15):
        print(f"\n[AO*] Starting search from root '{root}'...")
        iteration = 1
        while not self.solved.get(root, False) and iteration <= max_iterations:
            print(f"\n--- AO* Step {iteration} ---")
            self.step(root)
            iteration += 1

        print(f"\n[AO* Complete] Root '{root}' Solved = {self.solved[root]} | Total Solution Cost = {self.heuristics[root]}")
        return self.get_solution_tree(root)

    def get_solution_tree(self, node):
        """Recursively formats the marked solution subgraph."""
        if node not in self.branches or not self.branches[node]:
            return f"{node} [Leaf Goal, cost=0]"

        b_idx = self.marked.get(node, 0)
        b_type, children, cost = self.branches[node][b_idx]
        child_trees = [self.get_solution_tree(c) for c in children]

        if b_type == 'AND':
            return f"{node} (AND branch, edge_cost={cost}) -> [" + ", ".join(child_trees) + "]"
        else:
            return f"{node} (OR branch, edge_cost={cost}) -> " + child_trees[0]


# =====================================================================
# 3. HILL CLIMBING ALGORITHM
# =====================================================================

def hill_climbing(objective_function, start_state, step_size=1, bounds=(0, 20)):
    """
    Standard Steepest-Ascent Hill Climbing algorithm.
    Iteratively moves to the neighboring state that yields the greatest increase
    in the objective/heuristic function. Stops when no neighbor is strictly better.
    """
    current_state = start_state
    current_value = objective_function(current_state)
    path = [(current_state, current_value)]

    print(f"\n[Hill Climbing] Starting at x = {current_state}, Value f(x) = {current_value:.2f}")

    while True:
        # Generate valid neighbors within bounds
        candidates = []
        for delta in [-step_size, step_size]:
            nxt = current_state + delta
            if bounds[0] <= nxt <= bounds[1]:
                candidates.append((nxt, objective_function(nxt)))

        # Find best neighbor
        best_neighbor, best_value = max(candidates, key=lambda item: item[1])

        # If neighbor improves current value, climb up
        if best_value > current_value:
            current_state = best_neighbor
            current_value = best_value
            path.append((current_state, current_value))
            print(f"  Climbing to x = {current_state:2d} | Value f(x) = {current_value:6.2f}")
        else:
            # Terminate at peak / local optimum
            print(f"  Reached peak / plateau at x = {current_state} (no neighbor improves f(x)).")
            break

    return current_state, current_value, path


# =====================================================================
# MAIN DRIVER FUNCTION
# =====================================================================

def main():
    print("=" * 70)
    print(" LAB 02B: BEST FIRST SEARCH, A*, AO*, AND HILL CLIMBING")
    print("=" * 70)

    # -----------------------------------------------------------------
    # Part 1: Greedy Best First Search vs. A* Comparison
    # -----------------------------------------------------------------
    # Graph where Greedy Best First Search is deceived by heuristic,
    # but A* finds the optimal path by taking true path cost into account.
    graph = {
        'S': [('A', 3), ('B', 1)],
        'A': [('G', 10)],
        'B': [('C', 2)],
        'C': [('G', 3)],
        'G': []
    }

    heuristics = {
        'S': 7,
        'A': 2,   # Looks deceptively close to G, but edge A->G costs 10!
        'B': 6,
        'C': 3,
        'G': 0
    }

    print("\n--- COMPARISON: GREEDY BEST FIRST SEARCH VS. A* SEARCH ---")
    print("Graph: S->A (cost 3), S->B (cost 1), A->G (cost 10), B->C (cost 2), C->G (cost 3)")
    print("Heuristics: h(S)=7, h(A)=2, h(B)=6, h(C)=3, h(G)=0")

    gbfs_path, gbfs_cost, gbfs_expanded = greedy_best_first_search(graph, heuristics, 'S', 'G')
    print(f"\n1. Greedy Best First Search (f = h):")
    print(f"   Path: {' -> '.join(gbfs_path)}")
    print(f"   Total Cost: {gbfs_cost} (Suboptimal! Deceived by h(A) = 2)")
    print(f"   Nodes Expanded: {' -> '.join(gbfs_expanded)}")

    astar_path, astar_cost, astar_expanded = a_star_search(graph, heuristics, 'S', 'G')
    print(f"\n2. A* Search (f = g + h):")
    print(f"   Path: {' -> '.join(astar_path)}")
    print(f"   Total Cost: {astar_cost} (Optimal! Finds S -> B -> C -> G)")
    print(f"   Nodes Expanded: {' -> '.join(astar_expanded)}")

    # -----------------------------------------------------------------
    # Part 2: AO* Algorithm on AND-OR Graph
    # -----------------------------------------------------------------
    print("\n" + "=" * 70)
    print(" PART 2: AO* ALGORITHM ON AND-OR GRAPH")
    print("=" * 70)

    # Graph description:
    # A has two options:
    #   Option 1 (OR): Branch to B (edge cost 1)
    #   Option 2 (AND): Branch to both C and D (edge cost 1 each)
    # B has OR branch to Goal G1 (cost 1)
    # C has OR branch to Goal G2 (cost 1)
    # D has OR branch to Goal G3 (cost 1)
    # Goals G1, G2, G3 have h = 0 and are terminals.
    ao_branches = {
        'A': [
            ('OR', ['B'], 1),
            ('AND', ['C', 'D'], 1)
        ],
        'B': [
            ('OR', ['G1'], 1)
        ],
        'C': [
            ('OR', ['G2'], 1)
        ],
        'D': [
            ('OR', ['G3'], 1)
        ],
        'G1': [],
        'G2': [],
        'G3': []
    }

    ao_heuristics = {
        'A': 6,
        'B': 5,
        'C': 2,
        'D': 2,
        'G1': 0,
        'G2': 0,
        'G3': 0
    }

    ao_solver = AOStarGraph(ao_branches, ao_heuristics)
    solution_tree = ao_solver.run('A')
    print("\n[AO* Solution Tree Found]:")
    print(f"  {solution_tree}")

    # -----------------------------------------------------------------
    # Part 3: Hill Climbing & Local Optima Limitations
    # -----------------------------------------------------------------
    print("\n" + "=" * 70)
    print(" PART 3: HILL CLIMBING & ITS LIMITATIONS")
    print("=" * 70)

    # Define a 1D multimodal objective function with:
    #   - Local Maximum at x = 4 (value = 14.0)
    #   - Valley around x = 7-8
    #   - Global Maximum at x = 16 (value = 25.0)
    def landscape(x):
        if x <= 7:
            return 14.0 - float((x - 4) ** 2)
        else:
            return 25.0 - 0.5 * float((x - 16) ** 2)

    print("Objective function has a LOCAL peak at x = 4 (f = 14) and a GLOBAL peak at x = 16 (f = 25).")

    # Run 1: Starting at x = 1 -> gets trapped in Local Maximum
    print("\n--- Test Run 1: Starting near Local Maximum (x = 1) ---")
    stuck_x, stuck_val, _ = hill_climbing(landscape, start_state=1, bounds=(0, 20))
    print(f"Result: Terminated at x = {stuck_x} with f(x) = {stuck_val:.2f} (TRAPPED IN LOCAL MAXIMUM!)")

    # Run 2: Starting at x = 10 -> reaches Global Maximum
    print("\n--- Test Run 2: Starting near Global Maximum (x = 10) ---")
    opt_x, opt_val, _ = hill_climbing(landscape, start_state=10, bounds=(0, 20))
    print(f"Result: Terminated at x = {opt_x} with f(x) = {opt_val:.2f} (GLOBAL OPTIMUM REACHED!)")

    print("\n[THEORETICAL LIMITATIONS OF HILL CLIMBING]:")
    print("  1. Local Optima: The algorithm stops when all immediate neighbors have lower values,")
    print("     failing to find better solutions that lie beyond valleys.")
    print("  2. Plateaux: Flat regions where all neighbors have identical heuristic values,")
    print("     causing the search to wander aimlessly without direction.")
    print("  3. Ridges: Navigating ridges requires sequences of diagonal steps that standard")
    print("     single-variable adjustments cannot follow.")
    print("  Solutions: Random Restart Hill Climbing, Simulated Annealing, Genetic Algorithms.")


if __name__ == "__main__":
    main()
