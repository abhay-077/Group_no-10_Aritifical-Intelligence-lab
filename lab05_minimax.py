# LAB 05: Minimax Algorithm for Game Playing
# Aim: To implement the Minimax algorithm for game playing and determine
# the optimal move for a player by exploring the game tree.

"""
=============================================================================
MINIMAX ALGORITHM CONCEPT AND UTILITY VALUES EXPLANATION:
-----------------------------------------------------------------------------
1. Game Tree:
   Each node represents a distinct board state. The root is the current state.
   Branches from a node represent valid legal moves. Terminal nodes are states
   where the game ends (Win, Loss, or Draw).

2. MAX and MIN Players:
   - MAX ('X'): Strives to choose the move leading to the HIGHEST utility score.
   - MIN ('O'): Strives to choose the move leading to the LOWEST utility score.

3. Meaning of Utility Values:
   - (+10 - depth): MAX wins. Subtracting 'depth' penalizes longer paths so
     the algorithm prefers faster wins (e.g., winning in 1 move scores +9,
     while winning in 3 moves scores +7).
   - (-10 + depth): MIN wins. Adding 'depth' makes MIN prefer postponing loss
     if defeat is inevitable.
   - 0: Draw / Tie game.
=============================================================================
"""


def check_terminal_state(board):
    """
    Checks if current state is terminal.
    Returns:
      'X' if player X has three in a row,
      'O' if player O has three in a row,
      'Draw' if board is completely filled without a winner,
      None if the game is still active.
    """
    win_conditions = [
        (0, 1, 2), (3, 4, 5), (6, 7, 8),  # Rows
        (0, 3, 6), (1, 4, 7), (2, 5, 8),  # Columns
        (0, 4, 8), (2, 4, 6)              # Diagonals
    ]

    for c1, c2, c3 in win_conditions:
        if board[c1] != ' ' and board[c1] == board[c2] == board[c3]:
            return board[c1]

    if ' ' not in board:
        return 'Draw'

    return None


def get_available_moves(board):
    """Returns a list of empty board cell indices (0 to 8)."""
    return [i for i, cell in enumerate(board) if cell == ' ']


def evaluate_terminal_utility(terminal_status, depth, max_player='X', min_player='O'):
    """
    Assigns utility scores to terminal game states.
    - MAX win: +10 - depth
    - MIN win: -10 + depth
    - Draw:    0
    """
    if terminal_status == max_player:
        return 10 - depth
    elif terminal_status == min_player:
        return -10 + depth
    elif terminal_status == 'Draw':
        return 0
    return 0


def minimax(board, depth, is_maximizing, max_player='X', min_player='O'):
    """
    Recursive implementation of Minimax:
    Explores the entire game tree down to terminal leaves.
    Returns the minimax value of the board.
    """
    terminal_status = check_terminal_state(board)
    if terminal_status is not None:
        return evaluate_terminal_utility(terminal_status, depth, max_player, min_player)

    legal_moves = get_available_moves(board)

    if is_maximizing:
        # MAX player's turn: maximize utility
        max_utility = -float('inf')
        for move in legal_moves:
            board[move] = max_player
            utility = minimax(board, depth + 1, False, max_player, min_player)
            board[move] = ' '
            max_utility = max(max_utility, utility)
        return max_utility
    else:
        # MIN player's turn: minimize utility
        min_utility = float('inf')
        for move in legal_moves:
            board[move] = min_player
            utility = minimax(board, depth + 1, True, max_player, min_player)
            board[move] = ' '
            min_utility = min(min_utility, utility)
        return min_utility


def find_best_move(board, current_player, max_player='X', min_player='O'):
    """
    Evaluates all possible legal moves from current state using Minimax.
    Returns: (best_move_index, move_evaluations_dict)
    """
    legal_moves = get_available_moves(board)
    is_maximizing = (current_player == max_player)
    move_evaluations = {}

    if is_maximizing:
        best_score = -float('inf')
        best_move = None
        for move in legal_moves:
            board[move] = max_player
            score = minimax(board, depth=0, is_maximizing=False,
                            max_player=max_player, min_player=min_player)
            board[move] = ' '
            move_evaluations[move] = score
            if score > best_score:
                best_score = score
                best_move = move
    else:
        best_score = float('inf')
        best_move = None
        for move in legal_moves:
            board[move] = min_player
            score = minimax(board, depth=0, is_maximizing=True,
                            max_player=max_player, min_player=min_player)
            board[move] = ' '
            move_evaluations[move] = score
            if score < best_score:
                best_score = score
                best_move = move

    return best_move, move_evaluations


def display_board(board):
    """Prints the 3x3 game board."""
    print("         Col 0   Col 1   Col 2")
    for r in range(3):
        row_cells = [board[r * 3 + c] if board[r * 3 + c] != ' ' else '.' for c in range(3)]
        print(f"  Row {r}:     {row_cells[0]}   |   {row_cells[1]}   |   {row_cells[2]} ")
        if r < 2:
            print("        -------+-------+-------")


def display_reference_indices():
    """Prints board grid cell numbers (0-8) for reference."""
    print("      Cell Index Mapping:")
    print("        0 | 1 | 2")
    print("       ---+---+---")
    print("        3 | 4 | 5")
    print("       ---+---+---")
    print("        6 | 7 | 8")


def main():
    print("=" * 68)
    print(" LAB 05: MINIMAX ALGORITHM FOR GAME PLAYING (TIC-TAC-TOE)")
    print("=" * 68)

    display_reference_indices()

    # -------------------------------------------------------------
    # Scenario 1: Immediate Winning Opportunity for MAX (X)
    # -------------------------------------------------------------
    # Board layout:
    #   X | O | X
    #   O | X | .
    #   . | . | O
    # X can win immediately by playing at index 8 (Row 2, Col 2) via diagonal,
    # or block/make other moves. Minimax will identify the optimal move.
    sample_board_1 = [
        'X', 'O', 'X',
        'O', 'X', ' ',
        ' ', ' ', 'O'
    ]

    print("\n" + "=" * 68)
    print(" SCENARIO 1: SAMPLE INTERMEDIATE BOARD")
    print(" Player MAX ('X') turn to move.")
    print("=" * 68)
    display_board(sample_board_1)

    best_move, move_scores = find_best_move(sample_board_1, current_player='X', max_player='X', min_player='O')

    print("\n[INFO] Minimax Tree Evaluation of Available Legal Moves:")
    for move_idx, score in move_scores.items():
        row, col = divmod(move_idx, 3)
        print(f"  Option: Move to cell {move_idx} (Row {row}, Col {col}) --> Minimax Utility: {score:+2d}")

    row, col = divmod(best_move, 3)
    print(f"\n[DECISION] Optimal Move for 'X': Cell {best_move} (Row {row}, Col {col}) with Utility: {move_scores[best_move]:+2d}")

    # Apply move
    sample_board_1[best_move] = 'X'
    print("\nBoard State after playing optimal move:")
    display_board(sample_board_1)
    status_1 = check_terminal_state(sample_board_1)
    print(f"Game Status: {status_1} (Player 'X' won the game!)")

    # -------------------------------------------------------------
    # Scenario 2: Blocking Opponent's Winning Threat
    # -------------------------------------------------------------
    # Board layout:
    #   O | O | .   <-- Opponent 'O' threatens to win at index 2!
    #   X | X | O
    #   . | . | .
    # MAX ('X') MUST choose index 2 to block 'O' from winning.
    sample_board_2 = [
        'O', 'O', ' ',
        'X', 'X', 'O',
        ' ', ' ', ' '
    ]

    print("\n" + "=" * 68)
    print(" SCENARIO 2: DEFENSIVE PLAY (BLOCKING OPPONENT WIN)")
    print(" Player MAX ('X') turn to move.")
    print("=" * 68)
    display_board(sample_board_2)

    best_move_2, move_scores_2 = find_best_move(sample_board_2, current_player='X', max_player='X', min_player='O')

    print("\n[INFO] Minimax Tree Evaluation of Available Legal Moves:")
    for move_idx, score in move_scores_2.items():
        row, col = divmod(move_idx, 3)
        note = " (BLOCKS OPPONENT WIN!)" if move_idx == 2 else ""
        print(f"  Option: Move to cell {move_idx} (Row {row}, Col {col}) --> Utility: {score:+2d}{note}")

    r2, c2 = divmod(best_move_2, 3)
    print(f"\n[DECISION] Optimal Move: Cell {best_move_2} (Row {r2}, Col {c2})")
    sample_board_2[best_move_2] = 'X'
    print("\nBoard State after blocking:")
    display_board(sample_board_2)


if __name__ == "__main__":
    main()
