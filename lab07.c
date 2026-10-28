
#include <stdio.h>
#include <stdlib.h>
#include <stdbool.h>
#include <string.h>

#define MAX_QUEUE 100000

typedef struct Node {
    int board[3][3];
    int zero_row, zero_col;
    int parent_index;
} Node;

Node queue[MAX_QUEUE];
int front = 0, rear = 0;

int visited[MAX_QUEUE][3][3];
int visited_count = 0;
int goal[3][3] = {
    {1, 2, 3},
    {4, 5, 6},
    {7, 8, 0}
};

bool is_equal(int a[3][3], int b[3][3]) {
    for (int i = 0; i < 3; i++) {
        for (int j = 0; j < 3; j++) {
            if (a[i][j] != b[i][j]) return false;
        }
    }
    return true;
}

bool is_visited(int board[3][3]) {
    for (int k = 0; k < visited_count; k++) {
        if (is_equal(visited[k], board)) return true;
    }
    return false;
}

void mark_visited(int board[3][3]) {
    for (int i = 0; i < 3; i++) {
        for (int j = 0; j < 3; j++) {
            visited[visited_count][i][j] = board[i][j];
        }
    }
    visited_count++;
}

void print_board(int board[3][3]) {
    for (int i = 0; i < 3; i++) {
        for (int j = 0; j < 3; j++) {
            if (board[i][j] == 0)
                printf("_ ");
            else
                printf("%d ", board[i][j]);
        }
        printf("\n");
    }
    printf("\n");
}

void print_path(int node_idx) {
    if (node_idx == -1) return;
    print_path(queue[node_idx].parent_index);
    print_board(queue[node_idx].board);
}

void solve_8_puzzle(int start_board[3][3]) {
  
    int dRow[] = {-1, 1, 0, 0};
    int dCol[] = {0, 0, -1, 1};

    int z_row = -1, z_col = -1;
    for (int i = 0; i < 3; i++) {
        for (int j = 0; j < 3; j++) {
            if (start_board[i][j] == 0) {
                z_row = i;
                z_col = j;
            }
        }
    }

    memcpy(queue[rear].board, start_board, sizeof(queue[rear].board));
    queue[rear].zero_row = z_row;
    queue[rear].zero_col = z_col;
    queue[rear].parent_index = -1;
    mark_visited(start_board);
    rear++;

    while (front < rear) {
        int current_idx = front++;
        Node current = queue[current_idx];

        if (is_equal(current.board, goal)) {
            printf("Goal state reached! Solution path:\n\n");
            print_path(current_idx);
            return;
        }

        for (int i = 0; i < 4; i++) {
            int new_r = current.zero_row + dRow[i];
            int new_c = current.zero_col + dCol[i];

            if (new_r >= 0 && new_r < 3 && new_c >= 0 && new_c < 3) {
                int new_board[3][3];
                memcpy(new_board, current.board, sizeof(new_board));

                new_board[current.zero_row][current.zero_col] = new_board[new_r][new_c];
                new_board[new_r][new_c] = 0;

                if (!is_visited(new_board)) {
                    mark_visited(new_board);

                    memcpy(queue[rear].board, new_board, sizeof(queue[rear].board));
                    queue[rear].zero_row = new_r;
                    queue[rear].zero_col = new_c;
                    queue[rear].parent_index = current_idx;
                    rear++;
                }
            }
        }
    }

    printf("No solution found.\n");
}

int main() {
    int start_board[3][3] = {
        {1, 2, 3},
        {4, 0, 6},
        {7, 5, 8}
    };

    printf("Start State:\n");
    print_board(start_board);

    solve_8_puzzle(start_board);

    return 0;
}

