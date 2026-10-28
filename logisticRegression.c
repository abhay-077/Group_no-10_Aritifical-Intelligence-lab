#include <stdio.h>
#include <math.h>

#define N 6
#define LR 0.1
#define EPOCHS 1000

double sigmoid(double z)
{
    return 1 / (1 + exp(-z));
}

int main()
{
    double x[N] = {1, 2, 3, 4, 5, 6};
    double y[N] = {0, 0, 0, 1, 1, 1};

    double w = 0, b = 0;

    for (int e = 0; e < EPOCHS; e++)
    {
        double dw = 0, db = 0;

        for (int i = 0; i < N; i++)
        {
            double z = w * x[i] + b;
            double p = sigmoid(z);

            dw += (p - y[i]) * x[i];
            db += p - y[i];
        }

        dw /= N;
        db /= N;

        w -= LR * dw;
        b -= LR * db;
    }

    printf("w = %.3f\n", w);
    printf("b = %.3f\n", b);

    double input;

    printf("Enter input: ");
    scanf("%lf", &input);

    double z = w * input + b;
    double probability = sigmoid(z);

    printf("Probability = %.3f\n", probability);

    if (probability >= 0.5)
        printf("Class = 1\n");
    else
        printf("Class = 0\n");

    return 0;
}