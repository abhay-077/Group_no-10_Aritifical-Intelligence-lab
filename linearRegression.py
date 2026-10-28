import numpy as np

# Training data
X = np.array([
    [1000, 2],
    [1500, 3],
    [2000, 4],
    [2500, 4],
    [3000, 5]
], dtype=float)

y = np.array([200, 300, 400, 500, 600], dtype=float)

# Number of training examples
m = len(y)

# Initialize parameters
w1 = 0
w2 = 0
b = 0

# Learning rate
alpha = 0.000001

# Number of iterations
iterations = 10000

for i in range(iterations):

    # Prediction
    y_pred = b + w1 * X[:, 0] + w2 * X[:, 1]

    # Error
    error = y_pred - y

    # Cost
    cost = (1 / (2 * m)) * np.sum(error ** 2)

    # Gradients
    dw1 = (1 / m) * np.sum(error * X[:, 0])
    dw2 = (1 / m) * np.sum(error * X[:, 1])
    db = (1 / m) * np.sum(error)

    # Parameter updates
    w1 = w1 - alpha * dw1
    w2 = w2 - alpha * dw2
    b = b - alpha * db

    # Display cost
    if i % 1000 == 0:
        print("Iteration:", i, "Cost:", cost)

print("\nFinal Parameters:")
print("w1 =", w1)
print("w2 =", w2)
print("b =", b)