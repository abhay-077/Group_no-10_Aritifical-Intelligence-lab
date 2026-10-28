#include <stdio.h>
#include <math.h>

#define N 6
#define LR 0.1
#define EPOCHS 1000

double sigmoid(double z)
{
    return 1.0 / (1.0 + exp(-z));
}

int main()
{
    double X[N] = {1, 2, 3, 4, 5, 6};
    double Y[N] = {0, 0, 0, 1, 1, 1};

    double w = 0;
    double b = 0;

    for (int epoch = 0; epoch < EPOCHS; epoch++)
    {
        double dw = 0;
        double db = 0;
        double cost = 0;

        for (int i = 0; i < N; i++)
        {
            double z = w * X[i] + b;
            double p = sigmoid(z);

            cost += -(Y[i] * log(p) + (1 - Y[i]) * log(1 - p));

            dw += (p - Y[i]) * X[i];
            db += p - Y[i];
        }

        dw /= N;
        db /= N;
        cost /= N;

        w = w - LR * dw;
        b = b - LR * db;
    }

    printf("Trained w = %.4f\n", w);
    printf("Trained b = %.4f\n", b);

    double x;

    printf("Enter new input: ");
    scanf("%lf", &x);

    double z = w * x + b;
    double probability = sigmoid(z);

    printf("Probability = %.4f\n", probability);

    if (probability >= 0.5)
        printf("Class = 1\n");
    else
        printf("Class = 0\n");

    return 0;
}