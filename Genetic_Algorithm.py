
# LAB 08: Implement the Genetic Algorithm
# Aim: To implement a Genetic Algorithm (GA) in Python to find an
# optimal solution using natural selection and genetic operators.

import random

# Problem: Maximize f(x) = x^2, where 0 <= x <= 31.
# Each solution is represented by a 5-bit binary chromosome.

POPULATION_SIZE = 10
GENERATIONS = 30
MUTATION_RATE = 0.05

random.seed(42)


def create_chromosome():
    """Generate a random 5-bit chromosome."""
    return format(random.randint(0, 31), "05b")


def decode(chromosome):
    """Convert a binary chromosome into an integer."""
    return int(chromosome, 2)


def fitness(chromosome):
    """Calculate fitness: f(x) = x^2."""
    x = decode(chromosome)
    return x ** 2


def initialize_population():
    """Create the initial population."""
    return [
        create_chromosome()
        for _ in range(POPULATION_SIZE)
    ]


def selection(population):
    """Tournament selection: choose the fitter of two candidates."""
    first = random.choice(population)
    second = random.choice(population)

    if fitness(first) >= fitness(second):
        return first
    return second


def crossover(parent1, parent2):
    """Single-point crossover."""
    point = random.randint(1, 4)

    child1 = parent1[:point] + parent2[point:]
    child2 = parent2[:point] + parent1[point:]

    return child1, child2


def mutation(chromosome):
    """Flip each bit with the specified mutation probability."""
    bits = list(chromosome)

    for i in range(len(bits)):
        if random.random() < MUTATION_RATE:
            bits[i] = "1" if bits[i] == "0" else "0"

    return "".join(bits)


def genetic_algorithm():
    population = initialize_population()

    for generation in range(GENERATIONS + 1):
        # Find the best individual in this generation.
        best = max(population, key=fitness)

        print(
            f"Generation {generation:02d} | "
            f"Chromosome: {best} | "
            f"x: {decode(best):2d} | "
            f"Fitness: {fitness(best)}"
        )

        # Stop if the global optimum is found.
        if decode(best) == 31:
            print("\nOptimal solution found!")
            break

        # Preserve the best individual (elitism).
        new_population = [best]

        # Generate the remaining individuals.
        while len(new_population) < POPULATION_SIZE:
            parent1 = selection(population)
            parent2 = selection(population)

            child1, child2 = crossover(parent1, parent2)

            child1 = mutation(child1)
            child2 = mutation(child2)

            new_population.append(child1)

            if len(new_population) < POPULATION_SIZE:
                new_population.append(child2)

        population = new_population

    best = max(population, key=fitness)

    print("\nFinal Best Solution")
    print("Chromosome:", best)
    print("Decoded value:", decode(best))
    print("Fitness:", fitness(best))
    print("Theoretical maximum fitness:", 31 ** 2)


if __name__ == "__main__":
    genetic_algorithm()
