import numpy as np


class LogisticRegression:
    def __init__(self, learning_rate=0.1, iterations=2000):
        self.learning_rate = learning_rate
        self.iterations = iterations
        self.weights = None
        self.bias = 0

    def sigmoid(self, z):
        z = np.clip(z, -500, 500)
        return 1 / (1 + np.exp(-z))

    def fit(self, X, y):
        m, n = X.shape
        self.weights = np.zeros(n)

        for _ in range(self.iterations):
            linear = np.dot(X, self.weights) + self.bias
            predictions = self.sigmoid(linear)

            dw = np.dot(X.T, predictions - y) / m
            db = np.sum(predictions - y) / m

            self.weights -= self.learning_rate * dw
            self.bias -= self.learning_rate * db

    def predict_proba(self, X):
        return self.sigmoid(np.dot(X, self.weights) + self.bias)

    def predict(self, X, threshold=0.5):
        return (self.predict_proba(X) >= threshold).astype(int)


X = np.array([
    [1, 2], [2, 3], [2, 1], [3, 4],
    [4, 3], [5, 5], [6, 5], [7, 7],
    [8, 6], [9, 8]
], dtype=float)

y = np.array([0, 0, 0, 0, 0, 1, 1, 1, 1, 1])

model = LogisticRegression(learning_rate=0.1, iterations=2000)
model.fit(X, y)

predictions = model.predict(X)
probabilities = model.predict_proba(X)

accuracy = np.mean(predictions == y) * 100

print("Logistic Regression")
print("-------------------")
print("Weights:", model.weights)
print("Bias:", model.bias)
print("Probabilities:", probabilities)
print("Predicted Classes:", predictions)
print("Actual Classes:", y)
print("Accuracy:", accuracy, "%")
