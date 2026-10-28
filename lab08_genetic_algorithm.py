# LAB 08: Genetic Algorithm
# Aim: To implement a Genetic Algorithm in Python to find an optimal solution
# to an optimization problem using natural selection and genetic operators.

"""
=============================================================================
GENETIC ALGORITHM (GA) CONCEPTS & OPERATORS:
-----------------------------------------------------------------------------
1. Chromosome Representation:
   Each candidate solution is encoded as a 5-bit binary string (e.g., '10110').
   Decoded integer x in [0, 31] represents the parameter.

2. Fitness Function:
   f(x) = x^2. The goal is to maximize f(x).
   Theoretical Global Maximum: x = 31 ('11111') with fitness = 31^2 = 961.

3. Selection (Roulette Wheel / Fitness-Proportionate Selection):
   Probability of selecting an individual is proportional to its fitness.
   Fitter individuals have higher chances of passing their genes to offspring.

4. Crossover (Single-Point Recombination):
   With crossover probability P_c, two parents are cut at a random point k
   (1 <= k <= 4) and their tails are swapped to produce two offspring.

5. Mutation (Bit-Flip):
   With small mutation probability P_m, each bit is flipped (0 -> 1 or 1 -> 0)
   to introduce genetic diversity and prevent premature convergence.

6. Elitism:
   The best individual from the current generation is guaranteed to survive
   unchanged into the next generation, preventing loss of the best solution.

NOTE ON STOCHASTIC NATURE:
A Genetic Algorithm is a heuristic stochastic search method. Due to randomized
initialization, selection, and mutation, it is NOT guaranteed to find the global
optimum in every single run, though with proper parameter tuning and elitism it
consistently finds near-optimal or optimal solutions.
=============================================================================
"""

import random


def decode_chromosome(chromosome):
    """Decodes a 5-bit binary string into an integer (0 to 31)."""
    return int(chromosome, 2)


def compute_fitness(chromosome):
    """Calculates fitness: f(x) = x^2."""
    x = decode_chromosome(chromosome)
    return x ** 2


def create_initial_population(pop_size=6, num_bits=5):
    """Generates an initial population of random 5-bit chromosomes."""
    population = []
    for _ in range(pop_size):
        chrom = "".join(random.choice(['0', '1']) for _ in range(num_bits))
        population.append(chrom)
    return population


def roulette_wheel_selection(population, fitness_scores):
    """
    Selects one parent using Roulette Wheel Selection (fitness proportionate).
    """
    total_fitness = sum(fitness_scores)
    if total_fitness == 0:
        return random.choice(population)

    pick = random.uniform(0, total_fitness)
    current = 0.0
    for chrom, score in zip(population, fitness_scores):
        current += score
        if current >= pick:
            return chrom

    return population[-1]


def single_point_crossover(parent1, parent2, crossover_rate=0.8):
    """
    Performs single-point crossover between two parents.
    If crossover occurs, selects a random pivot index (1 to length-1) and swaps tails.
    """
    if random.random() < crossover_rate:
        k = random.randint(1, len(parent1) - 1)
        child1 = parent1[:k] + parent2[k:]
        child2 = parent2[:k] + parent1[k:]
        return child1, child2
    else:
        return parent1, parent2


def bit_flip_mutation(chromosome, mutation_rate=0.05):
    """
    Performs bit-flip mutation on a chromosome.
    Each bit is flipped with probability 'mutation_rate'.
    """
    mutated = []
    for bit in chromosome:
        if random.random() < mutation_rate:
            mutated.append('0' if bit == '1' else '1')
        else:
            mutated.append(bit)
    return "".join(mutated)


def run_genetic_algorithm(pop_size=8, num_generations=15, crossover_rate=0.8,
                           mutation_rate=0.05, seed=1):
    """
    Executes the Genetic Algorithm workflow across generations.
    """
    random.seed(seed)

    population = create_initial_population(pop_size=pop_size, num_bits=5)
    best_overall_chrom = None
    best_overall_fitness = -1

    print(f"\n[INFO] Configuration:")
    print(f"  Population Size:    {pop_size}")
    print(f"  Number of Bits:     5 (Values: 0 to 31)")
    print(f"  Generations:        {num_generations}")
    print(f"  Crossover Rate:     {crossover_rate * 100:.0f}%")
    print(f"  Bit Mutation Rate:  {mutation_rate * 100:.1f}%")
    print(f"  Random Seed:        {seed} (for reproducible evaluation)")
    print(f"  Theoretical Target: '11111' -> x = 31, Fitness = 31^2 = 961\n")

    print("-" * 75)
    print(" Gen | Best Chromosome | Best x | Best Fitness | Avg Fitness | Population")
    print("-" * 75)

    for gen in range(1, num_generations + 1):
        fitness_scores = [compute_fitness(chrom) for chrom in population]

        # Find best individual in current generation
        gen_best_idx = max(range(len(population)), key=lambda i: fitness_scores[i])
        gen_best_chrom = population[gen_best_idx]
        gen_best_fitness = fitness_scores[gen_best_idx]
        gen_best_x = decode_chromosome(gen_best_chrom)
        avg_fitness = sum(fitness_scores) / len(fitness_scores)

        # Update overall best
        if gen_best_fitness > best_overall_fitness:
            best_overall_fitness = gen_best_fitness
            best_overall_chrom = gen_best_chrom

        pop_preview = ", ".join(population)
        print(f" {gen:3d} |      {gen_best_chrom}      |   {gen_best_x:2d}   |     {gen_best_fitness:4d}     |   {avg_fitness:7.2f}   | [{pop_preview}]")

        # Create next generation
        new_population = []

        # ELITISM: Directly preserve the best individual into next generation
        new_population.append(gen_best_chrom)

        # Generate remaining offspring through selection, crossover, and mutation
        while len(new_population) < pop_size:
            p1 = roulette_wheel_selection(population, fitness_scores)
            p2 = roulette_wheel_selection(population, fitness_scores)

            c1, c2 = single_point_crossover(p1, p2, crossover_rate)

            c1 = bit_flip_mutation(c1, mutation_rate)
            c2 = bit_flip_mutation(c2, mutation_rate)

            new_population.append(c1)
            if len(new_population) < pop_size:
                new_population.append(c2)

        population = new_population

    return best_overall_chrom, decode_chromosome(best_overall_chrom), best_overall_fitness


def main():
    print("=" * 75)
    print(" LAB 08: GENETIC ALGORITHM FOR FUNCTION OPTIMIZATION")
    print(" Optimization Goal: Maximize f(x) = x^2 where x in [0, 31]")
    print("=" * 75)

    best_chrom, best_x, best_fitness = run_genetic_algorithm(
        pop_size=8, num_generations=15, crossover_rate=0.8, mutation_rate=0.05, seed=1
    )

    print("-" * 75)
    print("\n[OPTIMIZATION RESULTS]:")
    print(f"  Best Chromosome Found:  '{best_chrom}'")
    print(f"  Decoded Integer Value x: {best_x}")
    print(f"  Maximum Fitness f(x):    {best_fitness}")
    print(f"  Theoretical Maximum:     961 (at x = 31, '11111')")
    optimal_match = "YES (GLOBAL OPTIMUM REACHED!)" if best_x == 31 else f"No ({best_x}/31)"
    print(f"  Optimal Target Met?      {optimal_match}")

    print("\n[VIVA & DISCUSSION SUMMARY]:")
    print("  1. Natural Selection: Roulette wheel gives higher selection chance to fitter individuals.")
    print("  2. Recombination: Crossover combines useful building blocks (schemas) from two parents.")
    print("  3. Diversity: Mutation prevents premature convergence into a local sub-optimum.")
    print("  4. Elitism: Guarantees fitness monotonicity across generations by preserving the leader.")
    print("  5. Stochastic Nature: Since operators depend on random probability, outcomes may vary")
    print("     across runs with different seeds; convergence is heuristic, not absolute guarantee.")


if __name__ == "__main__":
    main()
