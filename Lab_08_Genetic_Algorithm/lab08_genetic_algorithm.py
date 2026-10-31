import random


POPULATION_SIZE = 20
CHROMOSOME_LENGTH = 10
MUTATION_RATE = 0.02
GENERATIONS = 100
ELITE_COUNT = 2


def create_chromosome():
    return [random.randint(0, 1) for _ in range(CHROMOSOME_LENGTH)]


def decode(chromosome):
    value = 0

    for bit in chromosome:
        value = value * 2 + bit

    return value


def fitness(chromosome):
    x = decode(chromosome)
    return x * x


def selection(population):
    candidates = random.sample(population, 3)
    return max(candidates, key=fitness)


def crossover(parent1, parent2):
    point = random.randint(1, CHROMOSOME_LENGTH - 1)

    child1 = parent1[:point] + parent2[point:]
    child2 = parent2[:point] + parent1[point:]

    return child1, child2


def mutation(chromosome):
    chromosome = chromosome.copy()

    for i in range(CHROMOSOME_LENGTH):
        if random.random() < MUTATION_RATE:
            chromosome[i] = 1 - chromosome[i]

    return chromosome


def genetic_algorithm():
    population = [
        create_chromosome()
        for _ in range(POPULATION_SIZE)
    ]

    for generation in range(GENERATIONS):
        population.sort(key=fitness, reverse=True)

        best = population[0]

        print(
            f"Generation {generation + 1}: "
            f"x = {decode(best)}, Fitness = {fitness(best)}"
        )

        if decode(best) == 2 ** CHROMOSOME_LENGTH - 1:
            break

        new_population = [
            individual.copy()
            for individual in population[:ELITE_COUNT]
        ]

        while len(new_population) < POPULATION_SIZE:
            parent1 = selection(population)
            parent2 = selection(population)

            child1, child2 = crossover(parent1, parent2)

            new_population.append(mutation(child1))

            if len(new_population) < POPULATION_SIZE:
                new_population.append(mutation(child2))

        population = new_population

    best = max(population, key=fitness)

    print("\nFinal Result")
    print("Best Chromosome:", best)
    print("Optimal x:", decode(best))
    print("Maximum Fitness:", fitness(best))


if __name__ == "__main__":
    random.seed(42)
    genetic_algorithm()
