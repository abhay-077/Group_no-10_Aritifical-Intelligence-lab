# LAB 03: Logistic Regression Using Gradient Descent
# Aim: To implement Logistic Regression using Gradient Descent for binary classification.

import numpy as np


def sigmoid(z):
    """
    Computes the sigmoid activation function:
    sigma(z) = 1 / (1 + e^(-z))
    Clips z values to avoid numerical overflow in exp(-z).
    """
    z_clipped = np.clip(z, -500, 500)
    return 1.0 / (1.0 + np.exp(-z_clipped))


def compute_cost(X, y, weights, bias):
    """
    Computes Binary Cross-Entropy (Log Loss):
    J(w, b) = - (1 / m) * sum( y * log(y_hat) + (1 - y) * log(1 - y_hat) )
    Adds an epsilon (1e-15) to prevent log(0) domain errors.
    """
    m = len(y)
    z = np.dot(X, weights) + bias
    y_hat = sigmoid(z)

    eps = 1e-15
    y_hat = np.clip(y_hat, eps, 1.0 - eps)

    cost = - (1.0 / m) * np.sum(y * np.log(y_hat) + (1.0 - y) * np.log(1.0 - y_hat))
    return cost


def gradient_descent(X, y, weights, bias, learning_rate, epochs):
    """
    Performs batch gradient descent for Logistic Regression:
    dj_dw = (1 / m) * X.T * (y_hat - y)
    dj_db = (1 / m) * sum(y_hat - y)
    """
    m = len(y)
    cost_history = []

    for epoch in range(epochs):
        z = np.dot(X, weights) + bias
        y_hat = sigmoid(z)
        errors = y_hat - y

        # Gradients
        dj_dw = (1.0 / m) * np.dot(X.T, errors)
        dj_db = (1.0 / m) * np.sum(errors)

        # Update weights and bias
        weights = weights - learning_rate * dj_dw
        bias = bias - learning_rate * dj_db

        cost = compute_cost(X, y, weights, bias)
        cost_history.append(cost)

        if (epoch + 1) % 200 == 0 or epoch == 0:
            print(f"Epoch {epoch+1:4d} | Cross-Entropy Loss: {cost:.5f}")

    return weights, bias, cost_history


def predict_probability(X, weights, bias):
    """Returns continuous probability P(y = 1 | x)."""
    z = np.dot(X, weights) + bias
    return sigmoid(z)


def predict_class(X, weights, bias, threshold=0.5):
    """Returns discrete binary prediction: 1 if prob >= threshold else 0."""
    probabilities = predict_probability(X, weights, bias)
    return (probabilities >= threshold).astype(int)


def evaluate_accuracy(y_true, y_pred):
    """Calculates classification accuracy percentage."""
    correct = np.sum(y_true == y_pred)
    return (correct / len(y_true)) * 100.0


def main():
    print("=" * 65)
    print(" LAB 03: LOGISTIC REGRESSION USING GRADIENT DESCENT (FROM SCRATCH)")
    print("=" * 65)

    # -------------------------------------------------------------
    # 1. Dataset: Student Exam 1 & Exam 2 Scores -> Pass (1) / Fail (0)
    # -------------------------------------------------------------
    X_raw = np.array([
        [30, 42],  # Fail
        [34, 45],  # Fail
        [40, 52],  # Fail
        [45, 48],  # Fail
        [52, 58],  # Pass
        [60, 50],  # Pass
        [68, 72],  # Pass
        [75, 80],  # Pass
        [82, 88],  # Pass
        [90, 95]   # Pass
    ], dtype=float)

    y = np.array([0, 0, 0, 0, 1, 1, 1, 1, 1, 1], dtype=float)

    print("\n[INFO] Training Dataset (Exam 1, Exam 2 -> Result):")
    for i in range(len(y)):
        label = "Pass (1)" if y[i] == 1 else "Fail (0)"
        print(f"  Student {i+1:2d}: Exam 1 = {X_raw[i, 0]:2.0f}, "
              f"Exam 2 = {X_raw[i, 1]:2.0f} --> {label}")

    # -------------------------------------------------------------
    # 2. Feature Standardization (Z-score)
    # -------------------------------------------------------------
    mean = np.mean(X_raw, axis=0)
    std = np.std(X_raw, axis=0)
    X_norm = (X_raw - mean) / std

    # -------------------------------------------------------------
    # 3. Model Training
    # -------------------------------------------------------------
    num_features = X_norm.shape[1]
    initial_weights = np.zeros(num_features)
    initial_bias = 0.0

    learning_rate = 0.1
    epochs = 1000

    print(f"\n[INFO] Hyperparameters: Learning Rate = {learning_rate}, Epochs = {epochs}")
    initial_loss = compute_cost(X_norm, y, initial_weights, initial_bias)
    print(f"  Initial Cross-Entropy Loss: {initial_loss:.5f}\n")

    print("--- Gradient Descent Training Progress ---")
    weights, bias, cost_history = gradient_descent(
        X_norm, y, initial_weights, initial_bias, learning_rate, epochs
    )

    final_loss = cost_history[-1]
    print("\n[INFO] Training Summary:")
    print(f"  Initial Loss: {initial_loss:.5f}")
    print(f"  Final Loss:   {final_loss:.5f}")
    print(f"  Learned Weights: w1 = {weights[0]:.4f}, w2 = {weights[1]:.4f}")
    print(f"  Learned Bias:    b  = {bias:.4f}")

    # -------------------------------------------------------------
    # 4. In-Sample Predictions & Accuracy Evaluation
    # -------------------------------------------------------------
    pred_probs = predict_probability(X_norm, weights, bias)
    pred_classes = predict_class(X_norm, weights, bias)
    accuracy = evaluate_accuracy(y, pred_classes)

    print("\n[INFO] Prediction Results on Training Data:")
    print("  Student | Actual | Pred Prob | Pred Class | Status")
    print("  " + "-" * 48)
    for i in range(len(y)):
        actual_str = "Pass" if y[i] == 1 else "Fail"
        pred_str = "Pass" if pred_classes[i] == 1 else "Fail"
        match_str = "CORRECT" if y[i] == pred_classes[i] else "WRONG"
        print(f"     {i+1:2d}   |  {actual_str:4s}  |  {pred_probs[i]:.4f}   |   {pred_str:4s}   | {match_str}")

    print(f"\n[EVALUATION] Training Accuracy: {accuracy:.2f}%")

    # -------------------------------------------------------------
    # 5. Predictions on New (Unseen) Students
    # -------------------------------------------------------------
    test_students = np.array([
        [32, 38],  # Expected Fail
        [55, 62],  # Expected Pass
        [78, 85]   # Expected Pass
    ], dtype=float)

    test_norm = (test_students - mean) / std
    test_probs = predict_probability(test_norm, weights, bias)
    test_preds = predict_class(test_norm, weights, bias)

    print("\n[INFO] Predictions for New Candidate Students:")
    for i, student in enumerate(test_students):
        outcome = "PASS" if test_preds[i] == 1 else "FAIL"
        print(f"  Candidate {i+1}: Scores = ({student[0]:.0f}, {student[1]:.0f}) "
              f"--> Probability = {test_probs[i]:.4f} | Decision: {outcome}")


if __name__ == "__main__":
    main()
