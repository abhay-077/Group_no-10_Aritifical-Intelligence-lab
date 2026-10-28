
# import heapq
# import time

# GOAL = (1, 2, 3, 4, 5, 6, 7, 8, 0)

# GOAL_POS = {
#     tile: divmod(i, 3)
#     for i, tile in enumerate(GOAL)
# }


# # Heuristic 1: Misplaced tiles
# def misplaced(state):
#     count = 0

#     for i, tile in enumerate(state):
#         if tile != 0 and tile != GOAL[i]:
#             count += 1

#     return count


# # Heuristic 2: Manhattan distance
# def manhattan(state):
#     total = 0

#     for i, tile in enumerate(state):
#         if tile != 0:
#             r, c = divmod(i, 3)
#             gr, gc = GOAL_POS[tile]

#             total += abs(r - gr) + abs(c - gc)

#     return total


# # Check whether the puzzle is solvable
# def solvable(state):
#     values = [x for x in state if x != 0]

#     inversions = 0

#     for i in range(len(values)):
#         for j in range(i + 1, len(values)):
#             if values[i] > values[j]:
#                 inversions += 1

#     return inversions % 2 == 0


# # Generate all possible next states
# def neighbors(state):
#     zero = state.index(0)
#     r, c = divmod(zero, 3)

#     moves = [(-1, 0), (1, 0), (0, -1), (0, 1)]

#     for dr, dc in moves:
#         nr, nc = r + dr, c + dc

#         if 0 <= nr < 3 and 0 <= nc < 3:
#             new_zero = nr * 3 + nc

#             new_state = list(state)
#             new_state[zero], new_state[new_zero] = (
#                 new_state[new_zero], new_state[zero]
#             )

#             yield tuple(new_state)


# # A* search algorithm
# def astar(start, heuristic):
#     if not solvable(start):
#         return None, 0, 0

#     begin = time.perf_counter()

#     pq = [(heuristic(start), 0, start)]

#     parent = {start: None}
#     best_g = {start: 0}

#     expanded = 0

#     while pq:
#         _, g, state = heapq.heappop(pq)

#         if g != best_g.get(state):
#             continue

#         if state == GOAL:
#             path = []
#             current = state

#             while current is not None:
#                 path.append(current)
#                 current = parent[current]

#             path.reverse()

#             return path, expanded, time.perf_counter() - begin

#         expanded += 1

#         for nxt in neighbors(state):
#             new_g = g + 1

#             if new_g < best_g.get(nxt, float("inf")):
#                 best_g[nxt] = new_g
#                 parent[nxt] = state

#                 f = new_g + heuristic(nxt)

#                 heapq.heappush(pq, (f, new_g, nxt))

#     return None, expanded, time.perf_counter() - begin


# # Display the board
# def show(state):
#     for r in range(3):
#         row = state[r * 3:r * 3 + 3]

#         print(" ".join(
#             "_" if x == 0 else str(x)
#             for x in row
#         ))

#     print()


# # Main function
# def main():
#     print("Enter the initial board row by row.")
#     print("Use 0 for the blank tile.")

#     nums = []

#     for i in range(3):
#         nums.extend(
#             map(int, input(f"Row {i + 1}: ").split())
#         )

#     if len(nums) != 9 or sorted(nums) != list(range(9)):
#         print("Invalid board.")
#         return

#     start = tuple(nums)

#     heuristics = [
#         ("Misplaced Tiles", misplaced),
#         ("Manhattan Distance", manhattan)
#     ]

#     for name, heuristic in heuristics:
#         path, expanded, seconds = astar(start, heuristic)

#         print("\nHeuristic:", name)

#         if path is None:
#             print("Puzzle is unsolvable.")
#             continue

#         print("Solution moves:", len(path) - 1)
#         print("Expanded nodes:", expanded)
#         print("Execution time:", round(seconds, 6), "seconds")

#         for step, state in enumerate(path):
#             print("Step", step)
#             show(state)


# if __name__ == "__main__":
#     main()


# import random
# import time


# # 1. Generate a random board arrangement
# def create_board(n):
#     board = list(range(n))
#     random.shuffle(board)
#     return board


# # 2. Calculate fitness: maximum possible score = n * (n - 1) // 2
# def fitness(board):
#     n = len(board)
#     score = 0

#     for i in range(n):
#         for j in range(i + 1, n):
#             # Queens attack diagonally if these differences are equal
#             if abs(board[i] - board[j]) != abs(i - j):
#                 score += 1

#     return score


# # 3. Select a parent using tournament selection
# def tournament_selection(population, tournament_size=3):
#     contestants = random.sample(
#         population,
#         min(tournament_size, len(population))
#     )

#     return max(contestants, key=fitness)


# # 4. Combine two parents to produce a child
# def crossover(parent1, parent2):
#     n = len(parent1)

#     if n < 2:
#         return parent1[:]

#     point = random.randint(1, n - 1)

#     child = parent1[:point]
#     child += [gene for gene in parent2 if gene not in child]

#     return child


# # 5. Mutate a board by swapping two queen rows
# def mutate(board, mutation_rate):
#     board = board[:]

#     if random.random() < mutation_rate and len(board) >= 2:
#         i, j = random.sample(range(len(board)), 2)
#         board[i], board[j] = board[j], board[i]

#     return board


# # 6. Display the chessboard
# def display_board(board):
#     n = len(board)

#     for row in range(n):
#         line = []

#         for col in range(n):
#             if board[col] == row:
#                 line.append("Q")
#             else:
#                 line.append(".")

#         print(" ".join(line))


# # 7. Run the genetic algorithm
# def genetic_algorithm(
#     n=8,
#     population_size=100,
#     mutation_rate=0.1,
#     max_generations=1000
# ):
#     if n < 1:
#         raise ValueError("N must be at least 1.")

#     if population_size < 1:
#         raise ValueError("Population size must be at least 1.")

#     if not 0 <= mutation_rate <= 1:
#         raise ValueError("Mutation rate must be between 0 and 1.")

#     population = [create_board(n) for _ in range(population_size)]
#     max_fitness = n * (n - 1) // 2

#     start_time = time.perf_counter()

#     for generation in range(max_generations + 1):
#         best = max(population, key=fitness)
#         best_score = fitness(best)

#         if best_score == max_fitness:
#             return best, generation, time.perf_counter() - start_time

#         if generation == max_generations:
#             break

#         # Elitism: preserve the best board
#         new_population = [best[:]]

#         while len(new_population) < population_size:
#             parent1 = tournament_selection(population)
#             parent2 = tournament_selection(population)

#             child = crossover(parent1, parent2)
#             child = mutate(child, mutation_rate)

#             new_population.append(child)

#         population = new_population

#     best = max(population, key=fitness)
#     return best, max_generations, time.perf_counter() - start_time


# # 8. Main program
# def main():
#     print("Genetic Algorithm for N-Queens")

#     n = int(input("Enter number of queens (N): "))
#     population_size = int(input("Enter population size (e.g. 100): "))
#     mutation_rate = float(input("Enter mutation rate (e.g. 0.1): "))
#     max_generations = int(input("Enter maximum generations (e.g. 1000): "))

#     best_board, generations, elapsed = genetic_algorithm(
#         n=n,
#         population_size=population_size,
#         mutation_rate=mutation_rate,
#         max_generations=max_generations
#     )

#     max_fitness = n * (n - 1) // 2
#     best_score = fitness(best_board)

#     print("\nBest board arrangement:", best_board)
#     print("Fitness:", best_score, "/", max_fitness)
#     print("Generations:", generations)
#     print("Execution time:", round(elapsed, 6), "seconds")

#     if best_score == max_fitness:
#         print("Solution found!")
#     else:
#         print("No solution found within the generation limit.")

#     print("\nChessboard:")
#     display_board(best_board)


# if __name__ == "__main__":
#     main()

import math
import time

HUMAN = "X"
AI = "O"
EMPTY = " "


# 1. Display the board
def display_board(board):
    print()
    for i in range(0, 9, 3):
        print(" " + " | ".join(board[i:i + 3]))
        if i < 6:
            print("---+---+---")
    print()


# 2. Check whether a player has won
def winner(board):
    win_positions = [
        (0, 1, 2), (3, 4, 5), (6, 7, 8),
        (0, 3, 6), (1, 4, 7), (2, 5, 8),
        (0, 4, 8), (2, 4, 6)
    ]

    for a, b, c in win_positions:
        if board[a] == board[b] == board[c] != EMPTY:
            return board[a]

    return None


# 3. Generate all legal moves
def legal_moves(board):
    return [i for i in range(9) if board[i] == EMPTY]


# 4. Check whether the game is over
def terminal(board):
    return winner(board) is not None or EMPTY not in board


# 5. Evaluate a board from the AI's perspective
def evaluate(board):
    result = winner(board)

    if result == AI:
        return 10
    elif result == HUMAN:
        return -10
    else:
        return 0


# 6. Minimax WITHOUT alpha-beta pruning
def minimax(board, depth, maximizing, stats):
    stats["nodes"] += 1

    if terminal(board) or depth == 0:
        return evaluate(board)

    if maximizing:
        best_score = -math.inf

        for move in legal_moves(board):
            board[move] = AI
            score = minimax(board, depth - 1, False, stats)
            board[move] = EMPTY

            best_score = max(best_score, score)

        return best_score

    else:
        best_score = math.inf

        for move in legal_moves(board):
            board[move] = HUMAN
            score = minimax(board, depth - 1, True, stats)
            board[move] = EMPTY

            best_score = min(best_score, score)

        return best_score


# 7. Order moves: center, corners, then edges
def ordered_moves(board):
    preference = [4, 0, 2, 6, 8, 1, 3, 5, 7]
    return [i for i in preference if board[i] == EMPTY]


# 8. Minimax WITH alpha-beta pruning
def minimax_alpha_beta(board, depth, alpha, beta, maximizing, stats):
    stats["nodes"] += 1

    if terminal(board) or depth == 0:
        return evaluate(board)

    if maximizing:
        best_score = -math.inf

        for move in ordered_moves(board):
            board[move] = AI
            score = minimax_alpha_beta(
                board, depth - 1, alpha, beta, False, stats
            )
            board[move] = EMPTY

            best_score = max(best_score, score)
            alpha = max(alpha, best_score)

            if beta <= alpha:
                stats["pruned"] += 1
                break

        return best_score

    else:
        best_score = math.inf

        for move in ordered_moves(board):
            board[move] = HUMAN
            score = minimax_alpha_beta(
                board, depth - 1, alpha, beta, True, stats
            )
            board[move] = EMPTY

            best_score = min(best_score, score)
            beta = min(beta, best_score)

            if beta <= alpha:
                stats["pruned"] += 1
                break

        return best_score


# 9. Find the AI's best move
def best_move(board, depth, use_pruning=True):
    stats = {"nodes": 0, "pruned": 0}
    chosen_move = None
    best_score = -math.inf

    for move in ordered_moves(board):
        board[move] = AI

        if use_pruning:
            score = minimax_alpha_beta(
                board, depth - 1, -math.inf, math.inf, False, stats
            )
        else:
            score = minimax(board, depth - 1, False, stats)

        board[move] = EMPTY

        if score > best_score:
            best_score = score
            chosen_move = move

    return chosen_move, best_score, stats


# 10. Compare both algorithms
def compare_algorithms(board, depth):
    for name, pruning in [
        ("Minimax without pruning", False),
        ("Minimax with Alpha-Beta pruning", True)
    ]:
        start = time.perf_counter()

        move, score, stats = best_move(board, depth, pruning)

        elapsed = time.perf_counter() - start

        print("\n" + name)
        print("Best move (position 1-9):", move + 1 if move is not None else None)
        print("Evaluation score:", score)
        print("Nodes evaluated:", stats["nodes"])
        print("Pruning cutoffs:", stats["pruned"])
        print("Execution time:", round(elapsed, 6), "seconds")


# 11. Main game
def main():
    board = [EMPTY] * 9

    try:
        depth = int(input("Enter AI search depth (1-9): "))
        if not 1 <= depth <= 9:
            print("Depth must be between 1 and 9.")
            return
    except ValueError:
        print("Please enter an integer.")
        return

    print("\nBoard positions:")
    print(" 1 | 2 | 3")
    print("---+---+---")
    print(" 4 | 5 | 6")
    print("---+---+---")
    print(" 7 | 8 | 9")

    while not terminal(board):
        display_board(board)

        # Human move
        try:
            move = int(input("Choose your position (1-9): ")) - 1

            if move not in legal_moves(board):
                print("Invalid or occupied position. Try again.")
                continue

        except ValueError:
            print("Enter a number from 1 to 9.")
            continue

        board[move] = HUMAN

        if terminal(board):
            break

        # AI move
        move, score, stats = best_move(board, depth, True)
        board[move] = AI

        print("AI chose position:", move + 1)
        print("AI evaluated nodes:", stats["nodes"])

    display_board(board)

    result = winner(board)

    if result == HUMAN:
        print("You win!")
    elif result == AI:
        print("AI wins!")
    else:
        print("It's a draw!")

    print("\nPerformance comparison for the current board:")
    if not terminal(board):
        compare_algorithms(board, depth)
    else:
        print("Game ended; comparison is demonstrated separately by the function.")


if __name__ == "__main__":
    main()
