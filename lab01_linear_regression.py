# LAB 01: Linear Regression Using Gradient Descent
# Aim: To implement Linear Regression using Gradient Descent from scratch
# and understand how model parameters are updated to minimize the cost function.

import numpy as np
import matplotlib.pyplot as plt


def normalize_features(X):
    """
    Performs Z-score feature normalization (standardization).
    Normalized feature = (feature - mean) / standard_deviation.
    This ensures features with large numerical ranges (e.g. sq ft)
    do not dominate features with small numerical ranges (e.g. bedrooms).
    """
    mean = np.mean(X, axis=0)
    std = np.std(X, axis=0)
    # Prevent division by zero if std is zero
    std_replaced = np.where(std == 0, 1.0, std)
    X_norm = (X - mean) / std_replaced
    return X_norm, mean, std_replaced


def compute_cost(X, y, weights, bias):
    """
    Computes Mean Squared Error (MSE) cost:
    J(w, b) = (1 / (2 * m)) * sum((y_pred - y)^2)
    """
    m = len(y)
    predictions = np.dot(X, weights) + bias
    cost = (1.0 / (2.0 * m)) * np.sum((predictions - y) ** 2)
    return cost


def gradient_descent(X, y, weights, bias, learning_rate, iterations):
    """
    Performs batch gradient descent to learn weights and bias:
    w = w - alpha * (dJ/dw)
    b = b - alpha * (dJ/db)
    """
    m = len(y)
    cost_history = []

    for i in range(iterations):
        predictions = np.dot(X, weights) + bias
        errors = predictions - y

        # Compute partial derivatives
        dj_dw = (1.0 / m) * np.dot(X.T, errors)
        dj_db = (1.0 / m) * np.sum(errors)

        # Update parameters simultaneously
        weights = weights - learning_rate * dj_dw
        bias = bias - learning_rate * dj_db

        cost = compute_cost(X, y, weights, bias)
        cost_history.append(cost)

        # Print progress every 100 iterations
        if (i + 1) % 100 == 0 or i == 0:
            print(f"Iteration {i+1:4d} | Cost: {cost:10.4f}")

    return weights, bias, cost_history


def predict(X, weights, bias):
    """
    Computes predictions using linear model: y_pred = X * w + b
    """
    return np.dot(X, weights) + bias


def main():
    print("=" * 60)
    print(" LAB 01: LINEAR REGRESSION USING GRADIENT DESCENT (FROM SCRATCH)")
    print("=" * 60)

    # -------------------------------------------------------------
    # 1. Dataset: House Size (sq ft) & Bedrooms -> Price ($ in thousands)
    # -------------------------------------------------------------
    # Feature 1: House size in square feet
    # Feature 2: Number of bedrooms
    # Target: House price in thousands of dollars
    X_raw = np.array([
        [1000, 2],
        [1250, 2],
        [1500, 3],
        [1800, 3],
        [2000, 4],
        [2300, 4],
        [2600, 4],
        [2900, 5],
        [3200, 5],
        [3500, 5]
    ], dtype=float)

    y = np.array([210, 245, 305, 350, 400, 445, 510, 560, 615, 680], dtype=float)

    print("\n[INFO] Training Dataset (House Size, Bedrooms -> Price in $k):")
    for i in range(len(y)):
        print(f"  Sample {i+1:2d}: Size = {X_raw[i, 0]:4.0f} sq ft, "
              f"Bedrooms = {X_raw[i, 1]:1.0f}  --> Price = ${y[i]:.1f}k")

    # -------------------------------------------------------------
    # 2. Feature Normalization
    # -------------------------------------------------------------
    X_norm, mean, std = normalize_features(X_raw)
    print("\n[INFO] Normalization Statistics:")
    print(f"  Feature Means:        Size = {mean[0]:.2f}, Bedrooms = {mean[1]:.2f}")
    print(f"  Feature Std Deviations: Size = {std[0]:.2f}, Bedrooms = {std[1]:.2f}")

    # -------------------------------------------------------------
    # 3. Model Initialization & Training
    # -------------------------------------------------------------
    num_features = X_norm.shape[1]
    initial_weights = np.zeros(num_features)
    initial_bias = 0.0

    learning_rate = 0.05
    iterations = 500

    print(f"\n[INFO] Hyperparameters: Learning Rate = {learning_rate}, Iterations = {iterations}")
    initial_cost = compute_cost(X_norm, y, initial_weights, initial_bias)
    print(f"  Initial Cost J(w, b): {initial_cost:.4f}\n")

    print("--- Gradient Descent Progress ---")
    learned_weights, learned_bias, cost_history = gradient_descent(
        X_norm, y, initial_weights, initial_bias, learning_rate, iterations
    )

    final_cost = cost_history[-1]
    print("\n[INFO] Training Complete:")
    print(f"  Initial Cost: {initial_cost:.4f}")
    print(f"  Final Cost:   {final_cost:.4f}")
    print(f"  Cost Reduction: {initial_cost - final_cost:.4f} "
          f"({((initial_cost - final_cost) / initial_cost) * 100:.2f}%)")
    print(f"  Learned Weights (w1, w2): [{learned_weights[0]:.4f}, {learned_weights[1]:.4f}]")
    print(f"  Learned Bias (b):         {learned_bias:.4f}")

    # -------------------------------------------------------------
    # 4. Model Predictions on Unseen Samples
    # -------------------------------------------------------------
    test_houses = np.array([
        [1600, 3],  # 1600 sq ft, 3 bedrooms
        [2400, 4],  # 2400 sq ft, 4 bedrooms
        [3100, 5]   # 3100 sq ft, 5 bedrooms
    ], dtype=float)

    # Normalize test houses using training mean and std
    test_houses_norm = (test_houses - mean) / std
    predicted_prices = predict(test_houses_norm, learned_weights, learned_bias)

    print("\n[INFO] Sample Predictions for New Houses:")
    for house, price in zip(test_houses, predicted_prices):
        print(f"  House: {house[0]:4.0f} sq ft, {house[1]:1.0f} BHK "
              f"--> Predicted Price: ${price:.2f}k (${price * 1000:,.0f})")

    # -------------------------------------------------------------
    # 5. Visualization: Cost Function vs. Iterations
    # -------------------------------------------------------------
    plt.figure(figsize=(8, 5))
    plt.plot(range(1, iterations + 1), cost_history, color='royalblue', linewidth=2)
    plt.title("Convergence of Gradient Descent: Cost vs. Iterations", fontsize=13, fontweight='bold')
    plt.xlabel("Iteration Number", fontsize=11)
    plt.ylabel("Cost Function J(w, b) [MSE]", fontsize=11)
    plt.grid(True, linestyle='--', alpha=0.6)
    plt.tight_layout()

    plot_filename = "lab01_cost_curve.png"
    plt.savefig(plot_filename, dpi=150)
    print(f"\n[INFO] Cost curve plot saved successfully to '{plot_filename}'.")

    try:
        plt.show()
    except Exception as e:
        print(f"[NOTE] GUI display skipped ({e}). Plot saved as image.")


if __name__ == "__main__":
    main()
