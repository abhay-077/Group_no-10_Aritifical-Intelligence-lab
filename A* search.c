#include <stdio.h>

#define N 6
#define INF 9999

int graph[N][N] = {
    {0, 2, 4, 0, 0, 0},
    {2, 0, 1, 7, 0, 0},
    {4, 1, 0, 3, 5, 0},
    {0, 7, 3, 0, 2, 4},
    {0, 0, 5, 2, 0, 1},
    {0, 0, 0, 4, 1, 0}
};

int h[N] = {8, 6, 5, 3, 1, 0};

void aStar(int start, int goal)
{
    int g[N], f[N];
    int visited[N] = {0};
    int parent[N];

    for (int i = 0; i < N; i++) {
        g[i] = INF;
        f[i] = INF;
        parent[i] = -1;
    }

    g[start] = 0;
    f[start] = h[start];

    for (int count = 0; count < N; count++) {

        int current = -1;

        for (int i = 0; i < N; i++) {
            if (!visited[i] &&
                (current == -1 || f[i] < f[current])) {
                current = i;
            }
        }

        if (current == -1)
            break;

        visited[current] = 1;

        if (current == goal)
            break;

        for (int i = 0; i < N; i++) {
            if (graph[current][i] > 0 && !visited[i]) {

                int newG = g[current] + graph[current][i];

                if (newG < g[i]) {
                    g[i] = newG;
                    f[i] = g[i] + h[i];
                    parent[i] = current;
                }
            }
        }
    }

    int path[N];
    int len = 0;
    int current = goal;

    while (current != -1) {
        path[len++] = current;
        current = parent[current];
    }

    printf("Shortest path: ");

    for (int i = len - 1; i >= 0; i--)
        printf("%d ", path[i]);

    printf("\nCost = %d\n", g[goal]);
}

int main()
{
    aStar(0, 5);
    return 0;
}