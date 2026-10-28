# LAB 04: Basic Search Strategies for 8-Puzzle, 8-Queens and Tic-Tac-Toe
# Aim: To implement and demonstrate basic search strategies for solving the
# 8-Puzzle, 8-Queens, and Tic-Tac-Toe problems using AI techniques.

from collections import deque
import heapq


# =====================================================================
# PART A: 8-PUZZLE (BFS & A* WITH MANHATTAN DISTANCE)
# =====================================================================

GOAL_STATE_8P = (1, 2, 3, 4, 5, 6, 7, 8, 0)


def count_inversions(state):
    """
    Counts the number of inversions in an 8-puzzle configuration.
    An inversion occurs when a tile with a larger number precedes
    a tile with a smaller number (ignoring the blank tile 0).
    """
    tiles = [tile for tile in state if tile != 0]
    inversions = 0
    for i in range(len(tiles)):
        for j in range(i + 1, len(tiles)):
            if tiles[i] > tiles[j]:
                inversions += 1
    return inversions


def is_solvable(state):
    """
    A 3x3 8-puzzle is solvable if and only if the number of inversions is EVEN.
    """
    return count_inversions(state) % 2 == 0


def manhattan_distance(state):
    """
    Computes the sum of Manhattan distances of all non-zero tiles from their goal positions.
    h(n) = sum(|row - goal_row| + |col - goal_col|)
    """
    distance = 0
    for idx, tile in enumerate(state):
        if tile != 0:
            current_row, current_col = divmod(idx, 3)
            # Goal position for tile t (1 to 8)
            goal_idx = tile - 1
            goal_row, goal_col = divmod(goal_idx, 3)
            distance += abs(current_row - goal_row) + abs(current_col - goal_col)
    return distance


def get_neighbors_8p(state):
    """Generates valid neighbor states by sliding the blank tile (0) Up, Down, Left, or Right."""
    blank_idx = state.index(0)
    row, col = divmod(blank_idx, 3)
    neighbors = []

    moves = [
        ('Up', -1, 0),
        ('Down', 1, 0),
        ('Left', 0, -1),
        ('Right', 0, 1)
    ]

    for move_name, dr, dc in moves:
        new_row, new_col = row + dr, col + dc
        if 0 <= new_row < 3 and 0 <= new_col < 3:
            new_blank_idx = new_row * 3 + new_col
            state_list = list(state)
            # Swap blank with target tile
            state_list[blank_idx], state_list[new_blank_idx] = state_list[new_blank_idx], state_list[blank_idx]
            neighbors.append((move_name, tuple(state_list)))

    return neighbors


def solve_8p_bfs(start_state):
    """Solves 8-puzzle using Breadth First Search (BFS)."""
    if start_state == GOAL_STATE_8P:
        return [("Start", start_state)], 0

    queue = deque([([( "Start", start_state )], start_state)])
    visited = {start_state}
    nodes_explored = 0

    while queue:
        path, current = queue.popleft()
        nodes_explored += 1

        for move, neighbor in get_neighbors_8p(current):
            if neighbor not in visited:
                if neighbor == GOAL_STATE_8P:
                    return path + [(move, neighbor)], nodes_explored
                visited.add(neighbor)
                queue.append((path + [(move, neighbor)], neighbor))

    return None, nodes_explored


def solve_8p_astar(start_state):
    """Solves 8-puzzle using A* Search with Manhattan Distance Heuristic."""
    if start_state == GOAL_STATE_8P:
        return [("Start", start_state)], 0

    # Priority queue stores: (f_score, g_score, counter, path, current_state)
    counter = 0
    initial_h = manhattan_distance(start_state)
    pq = [(initial_h, 0, counter, [("Start", start_state)], start_state)]
    best_g = {start_state: 0}
    nodes_explored = 0

    while pq:
        f_val, g_val, _, path, current = heapq.heappop(pq)
        nodes_explored += 1

        if current == GOAL_STATE_8P:
            return path, nodes_explored

        if g_val > best_g.get(current, float('inf')):
            continue

        for move, neighbor in get_neighbors_8p(current):
            new_g = g_val + 1
            if new_g < best_g.get(neighbor, float('inf')):
                best_g[neighbor] = new_g
                h_val = manhattan_distance(neighbor)
                new_f = new_g + h_val
                counter += 1
                heapq.heappush(pq, (new_f, new_g, counter, path + [(move, neighbor)], neighbor))

    return None, nodes_explored


def print_8p_grid(state):
    """Displays a 3x3 puzzle grid in a human-readable format."""
    for r in range(3):
        row_str = " ".join(str(state[r * 3 + c]) if state[r * 3 + c] != 0 else "_" for c in range(3))
        print(f"      [ {row_str} ]")


# =====================================================================
# PART B: 8-QUEENS PROBLEM (BACKTRACKING SEARCH)
# =====================================================================

def is_safe_queen(queens, row, col):
    """
    Checks if a queen can be safely placed at (row, col) without being attacked
    by any previously placed queens in columns 0 .. col-1.
    """
    for c in range(col):
        r = queens[c]
        # Same row check
        if r == row:
            return False
        # Diagonal check: |row - r| == |col - c|
        if abs(r - row) == abs(col - c):
            return False
    return True


def solve_8_queens_backtracking(queens, col=0):
    """
    Solves 8-Queens using Backtracking (Depth First Search on state space).
    queens[c] stores the row index of the queen in column c.
    """
    if col == 8:
        # All 8 queens safely placed
        return True

    for row in range(8):
        if is_safe_queen(queens, row, col):
            queens[col] = row
            if solve_8_queens_backtracking(queens, col + 1):
                return True
            # Backtrack
            queens[col] = -1

    return False


def verify_queens_solution(queens):
    """Verifies that no two queens attack each other on the 8x8 chessboard."""
    if len(queens) != 8 or any(r < 0 or r >= 8 for r in queens):
        return False

    for c1 in range(8):
        for c2 in range(c1 + 1, 8):
            r1, r2 = queens[c1], queens[c2]
            if r1 == r2 or abs(r1 - r2) == abs(c1 - c2):
                return False
    return True


def print_queens_board(queens):
    """Prints the 8x8 chessboard showing Queens (Q) and empty squares (.)."""
    print("      a b c d e f g h")
    print("    +" + "-" * 17 + "+")
    for r in range(8):
        row_str = f"  {8 - r} | "
        for c in range(8):
            row_str += "Q " if queens[c] == r else ". "
        row_str += f"| {8 - r}"
        print(row_str)
    print("    +" + "-" * 17 + "+")
    print("      a b c d e f g h")


# =====================================================================
# PART C: TIC-TAC-TOE (MINIMAX STATE-SPACE SEARCH)
# =====================================================================

def check_tic_tac_toe_winner(board):
    """
    Evaluates Tic-Tac-Toe board state.
    Returns: 'X' (X won), 'O' (O won), 'Draw' (board full with no winner), or None (ongoing).
    """
    win_lines = [
        [0, 1, 2], [3, 4, 5], [6, 7, 8],  # Rows
        [0, 3, 6], [1, 4, 7], [2, 5, 8],  # Columns
        [0, 4, 8], [2, 4, 6]              # Diagonals
    ]

    for line in win_lines:
        if board[line[0]] != ' ' and board[line[0]] == board[line[1]] == board[line[2]]:
            return board[line[0]]

    if ' ' not in board:
        return 'Draw'

    return None


def get_tic_tac_toe_moves(board):
    """Returns list of open square indices (0-8)."""
    return [i for i in range(9) if board[i] == ' ']


def minimax_ttt(board, is_maximizing, max_player='X', min_player='O'):
    """
    Minimax recursive evaluation function.
    Returns: (best_score, best_move_index)
      +10 for MAX win, -10 for MIN win, 0 for draw.
    """
    status = check_tic_tac_toe_winner(board)
    if status == max_player:
        return 10, None
    elif status == min_player:
        return -10, None
    elif status == 'Draw':
        return 0, None

    legal_moves = get_tic_tac_toe_moves(board)

    if is_maximizing:
        best_score = -float('inf')
        best_move = legal_moves[0]
        for move in legal_moves:
            board[move] = max_player
            score, _ = minimax_ttt(board, False, max_player, min_player)
            board[move] = ' '
            if score > best_score:
                best_score = score
                best_move = move
        return best_score, best_move
    else:
        best_score = float('inf')
        best_move = legal_moves[0]
        for move in legal_moves:
            board[move] = min_player
            score, _ = minimax_ttt(board, True, max_player, min_player)
            board[move] = ' '
            if score < best_score:
                best_score = score
                best_move = move
        return best_score, best_move


def print_ttt_board(board):
    """Prints a formatted 3x3 Tic-Tac-Toe board."""
    for r in range(3):
        row_vals = [board[r * 3 + c] for c in range(3)]
        print(f"        {row_vals[0]} | {row_vals[1]} | {row_vals[2]}")
        if r < 2:
            print("       ---+---+---")


# =====================================================================
# MAIN DRIVER FUNCTION
# =====================================================================

def main():
    print("=" * 70)
    print(" LAB 04: BASIC SEARCH STRATEGIES (8-PUZZLE, 8-QUEENS, TIC-TAC-TOE)")
    print("=" * 70)

    # -----------------------------------------------------------------
    # Part A: 8-Puzzle Search (BFS, A*, Unsolvability Detection)
    # -----------------------------------------------------------------
    print("\n" + "=" * 70)
    print(" PART A: 8-PUZZLE PROBLEM")
    print("=" * 70)

    # Solvable initial board (few moves from goal for clear display)
    solvable_board = (1, 2, 3, 4, 0, 6, 7, 5, 8)
    inversions_solvable = count_inversions(solvable_board)

    print("\n[Case 1: Solvable Board]")
    print(f"  Configuration: {solvable_board}")
    print_8p_grid(solvable_board)
    print(f"  Inversion Count: {inversions_solvable} (Even -> Solvable: {is_solvable(solvable_board)})")

    # Run A*
    astar_path, astar_explored = solve_8p_astar(solvable_board)
    print(f"\n  [A* Search with Manhattan Distance]:")
    print(f"    Nodes Explored: {astar_explored}")
    print(f"    Solution Length: {len(astar_path) - 1} moves")
    print("    Step-by-step Solution:")
    for step_num, (move, state) in enumerate(astar_path):
        print(f"      Step {step_num}: Move = {move}")
        print_8p_grid(state)

    # Run BFS
    bfs_path, bfs_explored = solve_8p_bfs(solvable_board)
    print(f"\n  [BFS Search]:")
    print(f"    Nodes Explored: {bfs_explored}")
    print(f"    Solution Length: {len(bfs_path) - 1} moves")

    # Unsolvable board test
    unsolvable_board = (1, 2, 3, 4, 5, 6, 8, 7, 0)  # 7 and 8 swapped
    inversions_unsolvable = count_inversions(unsolvable_board)
    print("\n[Case 2: Unsolvable Board Detection]")
    print(f"  Configuration: {unsolvable_board}")
    print_8p_grid(unsolvable_board)
    print(f"  Inversion Count: {inversions_unsolvable} (ODD -> Mathematically Unsolvable!)")
    print(f"  Solvability Check: {is_solvable(unsolvable_board)}")
    print("  [INFO] Unsolvable configuration detected immediately before initiating search.")

    # -----------------------------------------------------------------
    # Part B: 8-Queens Problem (Backtracking Search)
    # -----------------------------------------------------------------
    print("\n" + "=" * 70)
    print(" PART B: 8-QUEENS PROBLEM (BACKTRACKING)")
    print("=" * 70)

    queens_board = [-1] * 8
    success = solve_8_queens_backtracking(queens_board, col=0)

    if success:
        print("\n[INFO] Valid 8-Queens Placement Found:")
        print(f"  Column placements (col 0-7 -> row): {queens_board}")
        print_queens_board(queens_board)

        # Verification check
        is_valid = verify_queens_solution(queens_board)
        print(f"\n  [VERIFICATION]: Solution is valid and conflict-free? -> {is_valid}")
        print("  Checked: No two queens share the same row, column, or diagonal.")
    else:
        print("[ERROR] No solution found.")

    # -----------------------------------------------------------------
    # Part C: Tic-Tac-Toe Minimax State-Space Search
    # -----------------------------------------------------------------
    print("\n" + "=" * 70)
    print(" PART C: TIC-TAC-TOE MOVE SELECTION (MINIMAX)")
    print("=" * 70)

    # Sample intermediate game state:
    # X | O | X
    # O | X |
    #   |   | O
    sample_ttt = [
        'X', 'O', 'X',
        'O', 'X', ' ',
        ' ', ' ', 'O'
    ]

    print("\n[INFO] Sample Game State (Player 'X' to move):")
    print_ttt_board(sample_ttt)

    current_status = check_tic_tac_toe_winner(sample_ttt)
    print(f"  Game Status: {'Ongoing' if current_status is None else current_status}")
    print(f"  Legal Moves (Indices): {get_tic_tac_toe_moves(sample_ttt)}")

    # Minimax evaluation
    best_eval, optimal_move = minimax_ttt(sample_ttt, is_maximizing=True, max_player='X', min_player='O')
    print(f"\n  [Minimax Decision]:")
    print(f"    Optimal Move Index: {optimal_move} (Row {optimal_move // 3}, Col {optimal_move % 3})")
    print(f"    Minimax Score: {best_eval} (+10: X wins, 0: Draw, -10: O wins)")

    # Apply optimal move and display
    sample_ttt[optimal_move] = 'X'
    print("\n[INFO] Board After Executing Optimal Move:")
    print_ttt_board(sample_ttt)
    outcome = check_tic_tac_toe_winner(sample_ttt)
    print(f"  Result After Move: {outcome} (Player 'X' wins!)")


if __name__ == "__main__":
    main()
