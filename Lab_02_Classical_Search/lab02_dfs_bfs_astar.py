import heapq
from collections import deque

graph = {
    'A': [('B', 1), ('C', 4)],
    'B': [('D', 2), ('E', 5)],
    'C': [('F', 3)],
    'D': [('G', 3)],
    'E': [('G', 1)],
    'F': [('G', 2)],
    'G': []
}

heuristic = {
    'A': 6,
    'B': 4,
    'C': 4,
    'D': 2,
    'E': 1,
    'F': 2,
    'G': 0
}


def dfs(start, goal):
    stack = [(start, [start])]
    visited = set()

    while stack:
        node, path = stack.pop()

        if node == goal:
            return path

        if node not in visited:
            visited.add(node)

            for neighbor, _ in reversed(graph[node]):
                if neighbor not in visited:
                    stack.append((neighbor, path + [neighbor]))

    return None


def bfs(start, goal):
    queue = deque([(start, [start])])
    visited = {start}

    while queue:
        node, path = queue.popleft()

        if node == goal:
            return path

        for neighbor, _ in graph[node]:
            if neighbor not in visited:
                visited.add(neighbor)
                queue.append((neighbor, path + [neighbor]))

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
                priority = new_cost + heuristic[neighbor]
                heapq.heappush(
                    pq,
                    (priority, new_cost, neighbor, path + [neighbor])
                )

    return None, float('inf')


start = 'A'
goal = 'G'

print("DFS Path:", dfs(start, goal))
print("BFS Path:", bfs(start, goal))

path, cost = astar(start, goal)
print("A* Path:", path)
print("A* Total Cost:", cost)
