# Artificial Intelligence Lab

A comprehensive repository containing complete implementations of Artificial Intelligence laboratory practicals and algorithms. The implementations are developed from scratch using clean algorithmic principles, mathematical foundations, and first principles without relying on black-box machine learning libraries (such as scikit-learn). Both comprehensive Python practicals and foundational C implementations are included.

---

## Contributors

1. **Abhay Verma** — `2024BITE077`
2. **Surya Dev Singh** — `2024BITE075`
3. **Millend Manhas** — `2024BITE033`
4. **Vinay Kumar** — `2024BITE079`

---

## Table of Contents

1. [Project Overview](#project-overview)
2. [Laboratory Experiments Summary](#laboratory-experiments-summary)
3. [Prerequisites & Dependencies](#prerequisites--dependencies)
4. [Lab Details & Execution Instructions](#lab-details--execution-instructions)
   - [Lab 01: Linear Regression Using Gradient Descent](#lab-01-linear-regression-using-gradient-descent)
   - [Lab 02: DFS, BFS, and A* Search Algorithms](#lab-02-dfs-bfs-and-a-search-algorithms)
   - [Lab 02B: Best-First Search, A*, AO*, and Hill Climbing](#lab-02b-best-first-search-a-ao-and-hill-climbing)
   - [Lab 03: Logistic Regression Using Gradient Descent](#lab-03-logistic-regression-using-gradient-descent)
   - [Lab 04: Basic Search Strategies (8-Puzzle, 8-Queens, Tic-Tac-Toe)](#lab-04-basic-search-strategies-8-puzzle-8-queens-tic-tac-toe)
   - [Lab 05: Minimax Algorithm for Game Playing](#lab-05-minimax-algorithm-for-game-playing)
   - [Lab 06: Single-Layer Neural Network (Perceptron)](#lab-06-single-layer-neural-network-perceptron)
   - [Lab 07: Forward Chaining and Backward Chaining](#lab-07-forward-chaining-and-backward-chaining)
   - [Lab 08: Genetic Algorithm for Function Optimization](#lab-08-genetic-algorithm-for-function-optimization)
5. [Additional Implementations](#additional-implementations)
   - [Companion Python Scripts](#companion-python-scripts)
   - [C Source Implementations](#c-source-implementations)
6. [Project Folder Structure](#project-folder-structure)
7. [General Coding & Design Standards](#general-coding--design-standards)

---

## Project Overview

This repository hosts laboratory practicals designed to explore the core paradigms of Artificial Intelligence:
- **Uninformed & Informed State-Space Search**: Depth-First Search, Breadth-First Search, Greedy Best-First Search, A* Search, AO* (AND-OR Graphs), and Hill Climbing.
- **Problem Solving & Constraint Satisfaction**: 8-Puzzle problem (with solvability parity checking), N-Queens backtracking solver, and Tic-Tac-Toe.
- **Adversarial Game Playing**: Minimax algorithm with depth-aware utility evaluation.
- **Supervised Learning from Scratch**: Univariate and multivariate Linear Regression, Logistic Regression (binary cross-entropy loss), and Rosenblatt's Perceptron learning rule.
- **Logical Inference & Expert Systems**: Forward Chaining (data-driven) and Backward Chaining (goal-driven) with cycle detection.
- **Evolutionary Computation**: Genetic Algorithm with binary chromosome encoding, roulette wheel selection, single-point crossover, bit-flip mutation, and elitism.

---

## Laboratory Experiments Summary

| Lab | Filename | Topic | Key Concepts & Techniques |
| :--- | :--- | :--- | :--- |
| **01** | `lab01_linear_regression.py` | Linear Regression | Gradient Descent, Feature Normalization (Z-score), MSE Cost, Cost Curve Plotting |
| **02** | `lab02_dfs_bfs_astar.py` | Classical Search | DFS (Stack), BFS (Queue), A* Search ($f = g + h$), Adjacency Graph Traversal |
| **02B** | `lab02b_best_first_ao_astar_hill_climbing.py` | Advanced Search | Greedy Best First, A*, AO* (AND-OR Graph), Hill Climbing & Local Optima |
| **03** | `lab03_logistic_regression.py` | Binary Classification | Sigmoid Function, Binary Cross-Entropy (Log Loss), Gradient Descent |
| **04** | `lab04_puzzle_queens_tictactoe.py` | Problem Solving | 8-Puzzle (Inversions & Manhattan A*), 8-Queens (Backtracking), Tic-Tac-Toe Minimax |
| **05** | `lab05_minimax.py` | Adversarial Search | Minimax Algorithm, Recursive Game Tree Exploration, Utility Functions |
| **06** | `lab06_perceptron.py` | Neural Networks | Single-Layer Perceptron, Step Function, Perceptron Learning Rule, AND/OR Gates |
| **07** | `lab07_forward_backward_chaining.py` | Logical Inference | Forward Chaining (Data-driven), Backward Chaining (Goal-driven, Cycle Safe) |
| **08** | `lab08_genetic_algorithm.py` | Evolutionary Computing | Genetic Algorithm, Binary Chromosomes, Roulette Selection, Crossover, Elitism |

---

## Prerequisites & Dependencies

### Python Environment
- Python 3.8 or higher
- Required packages: `numpy`, `matplotlib`

Install dependencies using:
```bash
pip install -r requirements.txt
```

### C Environment (Optional for C implementations)
- GCC (GNU Compiler Collection) or Clang

---

## Lab Details & Execution Instructions

### Lab 01: Linear Regression Using Gradient Descent

- **File**: `lab01_linear_regression.py`
- **Aim**: To implement Linear Regression using Gradient Descent from scratch and understand how model parameters are updated to minimize the cost function.
- **Algorithm Overview**:
  - Implements Z-score feature normalization ($z = \frac{x - \mu}{\sigma}$) to handle differing feature dimensions.
  - Uses Mean Squared Error (MSE): $J(w, b) = \frac{1}{2m} \sum (\hat{y}^{(i)} - y^{(i)})^2$.
  - Computes partial derivatives manually and updates parameters via batch gradient descent.
  - Generates convergence plot saved as `lab01_cost_curve.png`.
- **Command to Run**:
  ```bash
  python3 lab01_linear_regression.py
  ```

---

### Lab 02: DFS, BFS, and A* Search Algorithms

- **File**: `lab02_dfs_bfs_astar.py`
- **Aim**: To implement and understand Depth First Search, Breadth First Search, and A* Search for solving search problems using Python.
- **Algorithm Overview**:
  - **DFS**: Uses an explicit LIFO stack to explore along deep branches before backtracking.
  - **BFS**: Uses a FIFO queue (`collections.deque`) to explore level-by-level, guaranteeing the shallowest path.
  - **A* Search**: Uses a min-heap priority queue (`heapq`) combining cumulative path cost $g(n)$ with admissible heuristic $h(n)$ ($f(n) = g(n) + h(n)$) to guarantee optimal path cost.
  - Gracefully handles unreachable targets.
- **Command to Run**:
  ```bash
  python3 lab02_dfs_bfs_astar.py
  ```

---

### Lab 02B: Best-First Search, A*, AO*, and Hill Climbing

- **File**: `lab02b_best_first_ao_astar_hill_climbing.py`
- **Aim**: To implement and analyze heuristic search algorithms: Greedy Best-First Search, A*, AO*, and Hill Climbing in Python.
- **Algorithm Overview**:
  - **Greedy Best-First Search**: Guides exploration purely based on heuristic values $h(n)$.
  - **A* Search**: Evaluates $f(n) = g(n) + h(n)$ balancing known cost and estimated distance.
  - **AO* Search**: Finds optimal cost hyper-trees in AND-OR graphs with bottom-up cost revision.
  - **Hill Climbing**: Iteratively transitions to highest-value neighbors; analyzes plateau and local maximum limitations.
- **Command to Run**:
  ```bash
  python3 lab02b_best_first_ao_astar_hill_climbing.py
  ```

---

### Lab 03: Logistic Regression Using Gradient Descent

- **File**: `lab03_logistic_regression.py`
- **Aim**: To implement Logistic Regression from scratch using Python for binary classification and understand the Sigmoid activation and Log Loss function.
- **Algorithm Overview**:
  - Maps real-valued linear predictions into probabilities via Sigmoid activation:
    $$\sigma(z) = \frac{1}{1 + e^{-z}}$$
  - Measures classification penalty using Binary Cross-Entropy Loss:
    $$J(\mathbf{w}, b) = -\frac{1}{m} \sum \left[ y \log(\hat{y}) + (1 - y) \log(1 - \hat{y}) \right]$$
  - Derives gradients analytically and applies updates iteratively.
  - Evaluates student exam pass/fail classification accuracy and outputs predicted probabilities.
- **Command to Run**:
  ```bash
  python3 lab03_logistic_regression.py
  ```

---

### Lab 04: Basic Search Strategies (8-Puzzle, 8-Queens, Tic-Tac-Toe)

- **File**: `lab04_puzzle_queens_tictactoe.py`
- **Aim**: To implement and demonstrate basic search strategies for solving the 8-Puzzle, 8-Queens, and Tic-Tac-Toe problems using AI techniques.
- **Algorithm Overview**:
  - **Part A (8-Puzzle)**: Evaluates parity of inversions to mathematically identify unsolvable states prior to search. Implements BFS and A* with Manhattan distance heuristic ($h(n) = \sum (|r - r_{goal}| + |c - c_{goal}|)$), reconstructing step-by-step boards.
  - **Part B (8-Queens)**: Uses backtracking depth-first search on an $8 \times 8$ board. Verifies that row and diagonal attack constraints are strictly satisfied.
  - **Part C (Tic-Tac-Toe)**: Formulates game as a state space, generates valid child states, and identifies optimal move decisions.
- **Command to Run**:
  ```bash
  python3 lab04_puzzle_queens_tictactoe.py
  ```

---

### Lab 05: Minimax Algorithm for Game Playing

- **File**: `lab05_minimax.py`
- **Aim**: To implement the Minimax algorithm for game playing and determine the optimal move for a player by exploring the game tree.
- **Algorithm Overview**:
  - Explores complete recursive game trees for Tic-Tac-Toe.
  - Assigns terminal utilities: $+10 - \text{depth}$ for MAX win, $-10 + \text{depth}$ for MIN win, and $0$ for Draw.
  - Evaluates all candidate moves from a given board state and selects the optimal path.
- **Command to Run**:
  ```bash
  python3 lab05_minimax.py
  ```

---

### Lab 06: Single-Layer Neural Network (Perceptron)

- **File**: `lab06_perceptron.py`
- **Aim**: To implement a single-layer neural network (Perceptron) for binary classification using Python.
- **Algorithm Overview**:
  - Computes weighted sum $z = \mathbf{w} \cdot \mathbf{x} + b$ and applies Heaviside step activation.
  - Updates weights and bias via Rosenblatt's learning rule:
    $$\mathbf{w} \leftarrow \mathbf{w} + \eta (y - \hat{y}) \mathbf{x}$$
    $$b \leftarrow b + \eta (y - \hat{y})$$
  - Trains on logical AND and OR gates to $100\%$ accuracy. Explains the linearly separable boundary constraint and why single-layer perceptrons fail on XOR.
- **Command to Run**:
  ```bash
  python3 lab06_perceptron.py
  ```

---

### Lab 07: Forward Chaining and Backward Chaining

- **File**: `lab07_forward_backward_chaining.py`
- **Aim**: To implement Forward Chaining and Backward Chaining algorithms in Artificial Intelligence for logical reasoning and inference using facts and rules.
- **Algorithm Overview**:
  - **Part A (Forward Chaining)**: Data-driven inference engine starting with known facts $A, B$ and repeatedly firing satisfied rules ($A \land B \implies C$, $C \implies D$) to deduce $D$.
  - **Part B (Backward Chaining)**: Goal-driven recursive proof engine working backward from target $E$ through rules ($D \implies E$, $C \implies D$, $A \land B \implies C$).
  - Incorporates cycle detection to prevent infinite recursion on circular rules ($P \implies Q, Q \implies P$) and handles unknown facts safely.
- **Command to Run**:
  ```bash
  python3 lab07_forward_backward_chaining.py
  ```

---

### Lab 08: Genetic Algorithm for Function Optimization

- **File**: `lab08_genetic_algorithm.py`
- **Aim**: To implement a Genetic Algorithm in Python to find an optimal solution to an optimization problem using natural selection and genetic operators.
- **Algorithm Overview**:
  - Maximizes $f(x) = x^2$ for $x \in [0, 31]$ using 5-bit binary chromosomes ($00000_2$ to $11111_2$).
  - Implements:
    1. **Fitness Evaluation**: $f(x) = x^2$.
    2. **Selection**: Roulette wheel (fitness-proportionate) selection.
    3. **Crossover**: Single-point crossover with tail swapping.
    4. **Mutation**: Bit-flip mutation with configured probability $P_m$.
    5. **Elitism**: Preserves the best candidate across generations.
  - Reproducible with fixed random seed and provides theoretical discussion on stochastic convergence.
- **Command to Run**:
  ```bash
  python3 lab08_genetic_algorithm.py
  ```

---

## Additional Implementations

### Companion Python Scripts

- **`Genetic_Algorithm.py`**: A concise, standalone implementation of the Genetic Algorithm maximizing $f(x) = x^2$.
  ```bash
  python3 Genetic_Algorithm.py
  ```
- **`linearRegression.py`**: Compact multi-variable Linear Regression script demonstrating gradient updates.
  ```bash
  python3 linearRegression.py
  ```
- **`tutorial_sheet.py`**: Tutorial implementation exploring 8-puzzle heuristics (misplaced tiles and Manhattan distance) and state space representations.
  ```bash
  python3 tutorial_sheet.py
  ```

### C Source Implementations

Foundational C programs illustrating core search and optimization algorithms:

| File | Description | Compilation & Execution |
| :--- | :--- | :--- |
| `A* search.c` | A* search implementation on an adjacency matrix | `gcc -O2 "A* search.c" -o Astar && ./Astar` |
| `BFS.c` | Breadth-First Search graph traversal | `gcc -O2 BFS.c -o BFS && ./BFS` |
| `DFS.c` | Depth-First Search graph traversal | `gcc -O2 DFS.c -o DFS && ./DFS` |
| `BinarySearch.c` | Iterative Binary Search algorithm | `gcc -O2 BinarySearch.c -o BinarySearch && ./BinarySearch` |
| `linearSearch.c` | Linear Search algorithm | `gcc -O2 linearSearch.c -o linearSearch && ./linearSearch` |
| `linearRegression.c` | Linear regression using gradient descent in C | `gcc -O2 linearRegression.c -o linearRegression -lm && ./linearRegression` |
| `logisticRegression.c` | Logistic regression using sigmoid activation in C | `gcc -O2 logisticRegression.c -o logisticRegression -lm && ./logisticRegression` |
| `lab07.c` | 8-Puzzle BFS solver in C | `gcc -O2 lab07.c -o lab07 && ./lab07` |

---

## Project Folder Structure

```text
Artificial Intelligence Lab/
├── README.md
├── requirements.txt
├── .gitignore
├── lab01_cost_curve.png
├── lab01_linear_regression.py
├── lab02_dfs_bfs_astar.py
├── lab02b_best_first_ao_astar_hill_climbing.py
├── lab03_logistic_regression.py
├── lab04_puzzle_queens_tictactoe.py
├── lab05_minimax.py
├── lab06_perceptron.py
├── lab07_forward_backward_chaining.py
├── lab08_genetic_algorithm.py
├── Genetic_Algorithm.py
├── linearRegression.py
├── tutorial_sheet.py
├── A* search.c
├── BFS.c
├── BinarySearch.c
├── DFS.c
├── lab07.c
├── linearRegression.c
├── linearSearch.c
└── logisticRegression.c
```

---

## General Coding & Design Standards

- **Strict Lab Aim Comments**: Every lab practical file starts with a clear aim comment block defining the problem and objectives.
- **No Black-box ML**: All algorithms (regression, neural networks, inference engines, search) are implemented manually without high-level library shortcuts.
- **Edge Case Robustness**: Includes handling for unreachable nodes, unsolvable puzzle boards, numerical stability in logarithms and exponents, and circular rule dependencies.
