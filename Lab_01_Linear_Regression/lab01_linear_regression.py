import numpy as np

class LinearRegression:
    def __init__(self, learning_rate=0.01, iterations=1000):
        self.learning_rate = learning_rate
        self.iterations = iterations
        self.weights = None
        self.bias = 0

    def fit(self, X, y):
        m, n = X.shape
        self.weights = np.zeros(n)

        for _ in range(self.iterations):
            predictions = np.dot(X, self.weights) + self.bias
            dw = (1 / m) * np.dot(X.T, predictions - y)
            db = (1 / m) * np.sum(predictions - y)

            self.weights -= self.learning_rate * dw
            self.bias -= self.learning_rate * db

    def predict(self, X):
        return np.dot(X, self.weights) + self.bias

    def mse(self, y, predictions):
        return np.mean((y - predictions) ** 2)


X = np.array([[1], [2], [3], [4], [5], [6]], dtype=float)
y = np.array([2, 4, 6, 8, 10, 12], dtype=float)

model = LinearRegression(learning_rate=0.01, iterations=2000)
model.fit(X, y)

predictions = model.predict(X)

print("Linear Regression Using Gradient Descent")
print("-----------------------------------------")
print("Weights:", model.weights)
print("Bias:", model.bias)
print("Predictions:", predictions)
print("Actual Values:", y)
print("Mean Squared Error:", model.mse(y, predictions))

test = np.array([[7]], dtype=float)
print("Prediction for X = 7:", model.predict(test)[0])
