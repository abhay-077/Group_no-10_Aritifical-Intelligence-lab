#include <stdio.h>

#define MAX 100

int adj[MAX][MAX];
int visited[MAX];
int n;

int queue[MAX];
int front = -1, rear = -1;

void enqueue(int v) {
    if (front == -1) front = 0;
    queue[++rear] = v;
}

int dequeue() {
    int item = queue[front++];
    if (front > rear) front = rear = -1;
    return item;
}

int isQueueEmpty() {
    return front == -1;
}

void bfs(int start) {
    visited[start] = 1;
    enqueue(start);

    while (!isQueueEmpty()) {
        int current = dequeue();
        printf("%d ", current);

        for (int i = 0; i < n; i++) {
            if (adj[current][i] == 1 && !visited[i]) {
                visited[i] = 1;
                enqueue(i);
            }
        }
    }
}

int main() {
    int edges, u, v, start;

    printf("Enter number of vertices: ");
    scanf("%d", &n);

    printf("Enter number of edges: ");
    scanf("%d", &edges);

    for (int i = 0; i < n; i++) {
        visited[i] = 0;
        for (int j = 0; j < n; j++) {
            adj[i][j] = 0;
        }
    }

    printf("Enter edges (u v), 0-indexed:\n");
    for (int i = 0; i < edges; i++) {
        scanf("%d %d", &u, &v);
        adj[u][v] = 1;
        adj[v][u] = 1;
    }

    printf("Enter starting vertex: ");
    scanf("%d", &start);

    printf("BFS traversal: ");
    bfs(start);
    printf("\n");

    return 0;
}