def print_board(board):
    for i in range(0, 9, 3):
        print(" | ".join(board[i:i + 3]))
        if i < 6:
            print("---------")


def check_winner(board, player):
    winning_positions = [
        (0, 1, 2), (3, 4, 5), (6, 7, 8),
        (0, 3, 6), (1, 4, 7), (2, 5, 8),
        (0, 4, 8), (2, 4, 6)
    ]

    for a, b, c in winning_positions:
        if board[a] == board[b] == board[c] == player:
            return True

    return False


def minimax(board, depth, maximizing):
    if check_winner(board, 'X'):
        return 10 - depth

    if check_winner(board, 'O'):
        return depth - 10

    if ' ' not in board:
        return 0

    if maximizing:
        best = -float('inf')

        for i in range(9):
            if board[i] == ' ':
                board[i] = 'X'
                score = minimax(board, depth + 1, False)
                board[i] = ' '
                best = max(best, score)

        return best

    best = float('inf')

    for i in range(9):
        if board[i] == ' ':
            board[i] = 'O'
            score = minimax(board, depth + 1, True)
            board[i] = ' '
            best = min(best, score)

    return best


def find_best_move(board):
    best_score = -float('inf')
    best_position = -1

    for i in range(9):
        if board[i] == ' ':
            board[i] = 'X'
            score = minimax(board, 0, False)
            board[i] = ' '

            if score > best_score:
                best_score = score
                best_position = i

    return best_position


board = [' '] * 9

print("Initial Board:")
print_board(board)

while True:
    try:
        position = int(input("\nEnter your move (1-9): ")) - 1

        if position < 0 or position >= 9 or board[position] != ' ':
            print("Invalid move. Try again.")
            continue

        board[position] = 'O'

        if check_winner(board, 'O'):
            print_board(board)
            print("You win!")
            break

        if ' ' not in board:
            print_board(board)
            print("Draw!")
            break

        computer_move = find_best_move(board)
        board[computer_move] = 'X'

        print("\nComputer's Move:")
        print_board(board)

        if check_winner(board, 'X'):
            print("Computer wins!")
            break

        if ' ' not in board:
            print("Draw!")
            break

    except ValueError:
        print("Enter a valid number.")
