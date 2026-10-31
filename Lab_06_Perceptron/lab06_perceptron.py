import numpy as np


class Perceptron:
    def __init__(self, learning_rate=0.1, epochs=20):
        self.learning_rate = learning_rate
        self.epochs = epochs
        self.weights = None
        self.bias = 0

    def activation(self, x):
        return np.where(x >= 0, 1, 0)

    def fit(self, X, y):
        samples, features = X.shape
        self.weights = np.zeros(features)

        for epoch in range(self.epochs):
            errors = 0

            for i in range(samples):
                linear_output = np.dot(X[i], self.weights) + self.bias
                prediction = self.activation(linear_output)
                update = self.learning_rate * (y[i] - prediction)

                self.weights += update * X[i]
                self.bias += update

                if update != 0:
                    errors += 1

            print(f"Epoch {epoch + 1}: Errors = {errors}")

            if errors == 0:
                break

    def predict(self, X):
        linear_output = np.dot(X, self.weights) + self.bias
        return self.activation(linear_output)


X = np.array([
    [0, 0],
    [0, 1],
    [1, 0],
    [1, 1]
])

gates = {
    "AND": np.array([0, 0, 0, 1]),
    "OR": np.array([0, 1, 1, 1])
}

for name, y in gates.items():
    print(f"\n{name} Gate")
    model = Perceptron()
    model.fit(X, y)

    predictions = model.predict(X)

    print("Weights:", model.weights)
    print("Bias:", model.bias)
    print("Predictions:", predictions)
    print("Actual:", y)
