import heapq

graph = {
    'A': [('B', 2), ('C', 4)],
    'B': [('D', 3), ('E', 5)],
    'C': [('F', 2)],
    'D': [('G', 2)],
    'E': [('G', 1)],
    'F': [('G', 3)],
    'G': []
}

heuristic = {
    'A': 6, 'B': 4, 'C': 3,
    'D': 2, 'E': 1, 'F': 2, 'G': 0
}


def best_first_search(start, goal):
    pq = [(heuristic[start], start, [start])]
    visited = set()

    while pq:
        _, node, path = heapq.heappop(pq)

        if node == goal:
            return path

        if node in visited:
            continue

        visited.add(node)

        for neighbor, _ in graph[node]:
            if neighbor not in visited:
                heapq.heappush(
                    pq,
                    (heuristic[neighbor], neighbor, path + [neighbor])
                )

    return None


def astar(start, goal):
    pq = [(heuristic[start], 0, start, [start])]
    best_cost = {start: 0}

    while pq:
        _, cost, node, path = heapq.heappop(pq)

        if node == goal:
            return path, cost

        if cost > best_cost[node]:
            continue

        for neighbor, weight in graph[node]:
            new_cost = cost + weight

            if new_cost < best_cost.get(neighbor, float('inf')):
                best_cost[neighbor] = new_cost
                heapq.heappush(
                    pq,
                    (new_cost + heuristic[neighbor],
                     new_cost, neighbor, path + [neighbor])
                )

    return None, float('inf')


def ao_star(graph, start):
    costs = {}
    solution = {}

    def solve(node, visiting):
        if node not in graph or not graph[node]:
            costs[node] = 0
            return 0

        if node in visiting:
            return float('inf')

        if node in costs:
            return costs[node]

        visiting = visiting | {node}
        best = float('inf')
        best_option = None

        for option in graph[node]:
            if isinstance(option, list):
                value = sum(
                    weight + solve(child, visiting)
                    for child, weight in option
                )
            else:
                child, weight = option
                value = weight + solve(child, visiting)

            if value < best:
                best = value
                best_option = option

        costs[node] = best
        solution[node] = best_option
        return best

    total = solve(start, set())
    return total, solution


def hill_climbing(values, start):
    current = start

    while True:
        neighbors = [
            i for i in (current - 1, current + 1)
            if 0 <= i < len(values)
        ]

        if not neighbors:
            break

        best = max(neighbors, key=lambda i: values[i])

        if values[best] <= values[current]:
            break

        current = best

    return current, values[current]


ao_graph = {
    'A': [[('B', 1), ('C', 1)], [('D', 2)]],
    'B': [('E', 2)],
    'C': [('F', 3)],
    'D': [('G', 1)],
    'E': [],
    'F': [],
    'G': []
}

values = [1, 3, 5, 7, 9, 8, 6, 4, 2]

print("Greedy Best First Search:", best_first_search('A', 'G'))

path, cost = astar('A', 'G')
print("A* Path:", path)
print("A* Cost:", cost)

cost, solution = ao_star(ao_graph, 'A')
print("AO* Minimum Cost:", cost)
print("AO* Solution Choices:", solution)

index, value = hill_climbing(values, 0)
print("Hill Climbing Maximum:", value)
print("Maximum Position:", index)
