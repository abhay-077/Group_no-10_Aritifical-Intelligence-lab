import heapq
from collections import deque


def puzzle_bfs(start, goal):
    queue = deque([(start, [])])
    visited = {start}

    while queue:
        state, path = queue.popleft()
        path = path + [state]

        if state == goal:
            return path

        zero = state.index(0)
        row, col = divmod(zero, 3)

        for dr, dc in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
            nr, nc = row + dr, col + dc

            if 0 <= nr < 3 and 0 <= nc < 3:
                new_pos = nr * 3 + nc
                new_state = list(state)
                new_state[zero], new_state[new_pos] = (
                    new_state[new_pos], new_state[zero]
                )
                new_state = tuple(new_state)

                if new_state not in visited:
                    visited.add(new_state)
                    queue.append((new_state, path))

    return None


def manhattan(state, goal):
    distance = 0

    for i, tile in enumerate(state):
        if tile == 0:
            continue

        j = goal.index(tile)
        r1, c1 = divmod(i, 3)
        r2, c2 = divmod(j, 3)
        distance += abs(r1 - r2) + abs(c1 - c2)

    return distance


def puzzle_astar(start, goal):
    pq = [(manhattan(start, goal), 0, start, [])]
    best = {start: 0}

    while pq:
        _, cost, state, path = heapq.heappop(pq)

        if state == goal:
            return path + [state]

        if cost > best[state]:
            continue

        zero = state.index(0)
        row, col = divmod(zero, 3)

        for dr, dc in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
            nr, nc = row + dr, col + dc

            if 0 <= nr < 3 and 0 <= nc < 3:
                new_pos = nr * 3 + nc
                new_state = list(state)
                new_state[zero], new_state[new_pos] = (
                    new_state[new_pos], new_state[zero]
                )
                new_state = tuple(new_state)
                new_cost = cost + 1

                if new_cost < best.get(new_state, float('inf')):
                    best[new_state] = new_cost
                    priority = new_cost + manhattan(new_state, goal)
                    heapq.heappush(
                        pq,
                        (priority, new_cost, new_state, path + [state])
                    )

    return None


def solve_n_queens(n):
    board = [-1] * n
    solutions = []

    def backtrack(row):
        if row == n:
            solutions.append(board.copy())
            return

        for col in range(n):
            valid = True

            for prev in range(row):
                if board[prev] == col or abs(board[prev] - col) == abs(prev - row):
                    valid = False
                    break

            if valid:
                board[row] = col
                backtrack(row + 1)
                board[row] = -1

    backtrack(0)
    return solutions


def print_board(board):
    for row in range(3):
        print(board[row * 3:row * 3 + 3])
    print()


def check_winner(board, player):
    wins = [
        (0, 1, 2), (3, 4, 5), (6, 7, 8),
        (0, 3, 6), (1, 4, 7), (2, 5, 8),
        (0, 4, 8), (2, 4, 6)
    ]

    return any(all(board[i] == player for i in line) for line in wins)


def minimax(board, maximizing):
    if check_winner(board, 'O'):
        return 1

    if check_winner(board, 'X'):
        return -1

    if ' ' not in board:
        return 0

    if maximizing:
        best = -float('inf')

        for i in range(9):
            if board[i] == ' ':
                board[i] = 'O'
                best = max(best, minimax(board, False))
                board[i] = ' '

        return best

    best = float('inf')

    for i in range(9):
        if board[i] == ' ':
            board[i] = 'X'
            best = min(best, minimax(board, True))
            board[i] = ' '

    return best


def best_move(board):
    best_score = -float('inf')
    move = None

    for i in range(9):
        if board[i] == ' ':
            board[i] = 'O'
            score = minimax(board, False)
            board[i] = ' '

            if score > best_score:
                best_score = score
                move = i

    return move


start = (1, 2, 3, 4, 0, 6, 7, 5, 8)
goal = (1, 2, 3, 4, 5, 6, 7, 8, 0)

bfs_path = puzzle_bfs(start, goal)
astar_path = puzzle_astar(start, goal)

print("8-Puzzle BFS Moves:", len(bfs_path) - 1 if bfs_path else "No solution")
print("8-Puzzle A* Moves:", len(astar_path) - 1 if astar_path else "No solution")

print("\n8-Puzzle A* Solution:")
if astar_path:
    for state in astar_path:
        print_board(state)

solutions = solve_n_queens(8)
print("8-Queens Total Solutions:", len(solutions))
print("First 8-Queens Solution:", solutions[0])

board = [' '] * 9
move = best_move(board)
print("\nTic-Tac-Toe Best Move for O:", move)
