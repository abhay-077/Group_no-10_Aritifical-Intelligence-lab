# LAB 06: Single-Layer Neural Network for Classification
# Aim: To implement a single-layer neural network (Perceptron) for binary
# classification using Python.

import numpy as np


class Perceptron:
    """
    Single-layer Perceptron for binary classification.
    Implements Rosenblatt's Perceptron learning rule.
    """
    def __init__(self, learning_rate=0.1, max_epochs=20):
        self.learning_rate = learning_rate
        self.max_epochs = max_epochs
        self.weights = None
        self.bias = 0.0

    @staticmethod
    def step_activation(z):
        """
        Heaviside step activation function:
        f(z) = 1 if z >= 0 else 0
        """
        return 1 if z >= 0 else 0

    def predict_single(self, x):
        """
        Calculates weighted sum and applies step activation for a single sample:
        z = sum(w_i * x_i) + b = w . x + b
        y_hat = step_activation(z)
        """
        weighted_sum = np.dot(self.weights, x) + self.bias
        return self.step_activation(weighted_sum)

    def predict(self, X):
        """Generates predictions for an array of input samples."""
        return np.array([self.predict_single(x) for x in X])

    def train(self, X, y, verbose=True):
        """
        Trains the perceptron using the perceptron learning rule:
          error = y - y_hat
          weights = weights + eta * error * x
          bias = bias + eta * error
        """
        num_features = X.shape[1]
        self.weights = np.zeros(num_features)
        self.bias = 0.0

        if verbose:
            print(f"[INFO] Initial Weights: {self.weights}, Initial Bias: {self.bias}")
            print(f"[INFO] Learning Rate: {self.learning_rate}, Max Epochs: {self.max_epochs}\n")

        for epoch in range(1, self.max_epochs + 1):
            total_errors = 0

            for i in range(len(X)):
                x_i = X[i]
                target = y[i]

                # Forward pass: weighted sum + activation
                prediction = self.predict_single(x_i)
                error = target - prediction

                if error != 0:
                    total_errors += 1
                    # Perceptron parameter update rule
                    self.weights += self.learning_rate * error * x_i
                    self.bias += self.learning_rate * error

            if verbose:
                print(f"  Epoch {epoch:2d} | Misclassifications: {total_errors} | "
                      f"Weights: [{self.weights[0]:.2f}, {self.weights[1]:.2f}] | Bias: {self.bias:.2f}")

            # Early stopping: if linearly separable and 0 misclassifications reached
            if total_errors == 0:
                if verbose:
                    print(f"\n[CONVERGENCE] Perfectly separated training data at Epoch {epoch}!")
                break


def evaluate_accuracy(y_true, y_pred):
    """Calculates classification accuracy percentage."""
    return (np.sum(y_true == y_pred) / len(y_true)) * 100.0


def main():
    print("=" * 68)
    print(" LAB 06: SINGLE-LAYER NEURAL NETWORK (PERCEPTRON CLASSIFIER)")
    print("=" * 68)

    # -------------------------------------------------------------
    # Experiment 1: Learning the Logical AND Gate
    # -------------------------------------------------------------
    print("\n" + "=" * 68)
    print(" EXPERIMENT 1: CLASSIFYING LOGICAL AND GATE")
    print("=" * 68)

    X_and = np.array([
        [0, 0],
        [0, 1],
        [1, 0],
        [1, 1]
    ], dtype=float)

    y_and = np.array([0, 0, 0, 1], dtype=int)

    print("\n[INFO] Logical AND Truth Table:")
    print("  Input X1 | Input X2 | Target Y")
    print("  ---------+----------+---------")
    for i in range(len(y_and)):
        print(f"     {int(X_and[i, 0])}     |    {int(X_and[i, 1])}     |    {y_and[i]}")

    perceptron_and = Perceptron(learning_rate=0.1, max_epochs=15)
    print("\n--- Training Perceptron on AND Gate ---")
    perceptron_and.train(X_and, y_and, verbose=True)

    predictions_and = perceptron_and.predict(X_and)
    accuracy_and = evaluate_accuracy(y_and, predictions_and)

    print("\n[INFO] Final Trained Parameters for AND Gate:")
    print(f"  Learned Weights: w1 = {perceptron_and.weights[0]:.2f}, w2 = {perceptron_and.weights[1]:.2f}")
    print(f"  Learned Bias:    b  = {perceptron_and.bias:.2f}")
    print(f"  Decision Boundary: {perceptron_and.weights[0]:.2f}*x1 + "
          f"{perceptron_and.weights[1]:.2f}*x2 + ({perceptron_and.bias:.2f}) = 0")

    print("\n[VERIFICATION] Final Evaluation on AND Gate:")
    print("  X1 | X2 | Target | Predicted | Status")
    print("  ---+----+--------+-----------+-------")
    for i in range(len(y_and)):
        status = "CORRECT" if y_and[i] == predictions_and[i] else "INCORRECT"
        print(f"   {int(X_and[i, 0])} |  {int(X_and[i, 1])} |   {y_and[i]}    |     {predictions_and[i]}     | {status}")

    print(f"\n  Final Classification Accuracy: {accuracy_and:.1f}%")

    # -------------------------------------------------------------
    # Experiment 2: Learning the Logical OR Gate
    # -------------------------------------------------------------
    print("\n" + "=" * 68)
    print(" EXPERIMENT 2: CLASSIFYING LOGICAL OR GATE")
    print("=" * 68)

    X_or = np.array([
        [0, 0],
        [0, 1],
        [1, 0],
        [1, 1]
    ], dtype=float)

    y_or = np.array([0, 1, 1, 1], dtype=int)

    perceptron_or = Perceptron(learning_rate=0.1, max_epochs=15)
    print("\n--- Training Perceptron on OR Gate ---")
    perceptron_or.train(X_or, y_or, verbose=True)

    predictions_or = perceptron_or.predict(X_or)
    accuracy_or = evaluate_accuracy(y_or, predictions_or)

    print(f"\n  Final Classification Accuracy for OR Gate: {accuracy_or:.1f}%")

    # -------------------------------------------------------------
    # Theoretical Context for Viva
    # -------------------------------------------------------------
    print("\n[THEORETICAL NOTE - VIVA DISCUSSION]:")
    print("  - Linearly Separable Functions: Perceptron is mathematically guaranteed")
    print("    to converge (Perceptron Convergence Theorem) for linearly separable datasets (AND, OR).")
    print("  - Limitation (XOR Problem): A single-layer perceptron CANNOT solve XOR")
    print("    because XOR outputs cannot be separated by a single straight line (hyperplane).")
    print("    Solving XOR requires a Multi-Layer Perceptron (MLP) with non-linear activation.")


if __name__ == "__main__":
    main()
