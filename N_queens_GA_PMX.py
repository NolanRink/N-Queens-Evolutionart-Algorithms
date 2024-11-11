import random
import time
import os
import csv
# Uncomment the line below if you wish to see progress bars
# from tqdm import tqdm

def fitness(individual):
    n = len(individual)
    conflicts = 0
    # Total number of pairs of queens: n(n-1)/2
    total_pairs = n * (n - 1) // 2

    for i in range(n):
        for j in range(i + 1, n):
            if abs(individual[i] - individual[j]) == abs(i - j):
                conflicts += 1
    return total_pairs - conflicts

# Tournament selection
def selection(population, fitnesses, population_size):
    tournament_size = max(2, population_size // 5)  # Ensure at least two individuals are selected
    selected = random.sample(list(zip(population, fitnesses)), tournament_size)
    selected.sort(key=lambda x: x[1], reverse=True)
    return selected[0][0]

# Partially Mapped Crossover
def pmx_crossover(parent1, parent2):
    size = len(parent1)
    child1, child2 = parent1.copy(), parent2.copy()
    # Choose crossover points
    cx_point1 = random.randint(0, size - 2)
    cx_point2 = random.randint(cx_point1 + 1, size - 1)
    # Apply PMX between cx_point1 and cx_point2
    for i in range(cx_point1, cx_point2):
        val1, val2 = child1[i], child2[i]
        idx1, idx2 = child1.index(val2), child2.index(val1)
        child1[i], child1[idx1] = child1[idx1], child1[i]
        child2[i], child2[idx2] = child2[idx2], child2[i]
    return child1, child2

# Mutate an individual by swapping two positions.
def mutate(individual, mutation_rate):
    if random.random() < mutation_rate:
        idx1, idx2 = random.sample(range(len(individual)), 2)
        individual[idx1], individual[idx2] = individual[idx2], individual[idx1]
    return individual

# Display the board with queens positions.
def display_board(individual):
    n = len(individual)
    for row in range(n):
        line = ''
        for col in range(n):
            if individual[row] == col:
                line += 'Q '
            else:
                line += '. '
        print(line.strip())

# Main function to run the genetic algorithm.
def genetic_algorithm(n, population_size, generations, mutation_rate, verbose=False):
    start_time = time.time()
    # Initialize population
    population = [random.sample(range(n), n) for _ in range(population_size)]
    best_fitness = 0
    best_individual = None
    generations_run = 0

    if verbose:
        from tqdm import tqdm
        progress_bar = tqdm(range(generations), desc='Generations')
    else:
        progress_bar = range(generations)

    for generation in progress_bar:
        generations_run += 1
        fitnesses = [fitness(individual) for individual in population]
        new_population = []

        for _ in range(population_size // 2):
            # Selection
            parent1 = selection(population, fitnesses, population_size)
            parent2 = selection(population, fitnesses, population_size)
            # Crossover
            child1, child2 = pmx_crossover(parent1, parent2)
            # Mutation
            child1 = mutate(child1, mutation_rate)
            child2 = mutate(child2, mutation_rate)
            new_population.extend([child1, child2])

        population = new_population

        # Update best individual
        fitnesses = [fitness(individual) for individual in population]
        max_fitness = max(fitnesses)
        if max_fitness > best_fitness:
            best_fitness = max_fitness
            best_individual = population[fitnesses.index(max_fitness)]

        # Check for solution
        if best_fitness == n * (n - 1) // 2:
            end_time = time.time()
            time_taken = end_time - start_time
            if verbose:
                print(f"\nTime taken to find a solution: {time_taken:.6f} seconds")
                print(f"Best Individual: {best_individual}")
                display_board(best_individual)
            result = {
                'n': n,
                'population_size': population_size,
                'generations': generations_run,
                'mutation_rate': mutation_rate,
                'solution_found': True,
                'time_taken': time_taken,
                'best_fitness': best_fitness,
                'best_individual': best_individual
            }
            return result

    end_time = time.time()
    time_taken = end_time - start_time
    if verbose:
        print(f"\nTime taken: {time_taken:.6f} seconds")
        print("No solution found.")
        print(f"Best Individual: {best_individual}")
        display_board(best_individual)
    result = {
        'n': n,
        'population_size': population_size,
        'generations': generations_run,
        'mutation_rate': mutation_rate,
        'solution_found': False,
        'time_taken': time_taken,
        'best_fitness': best_fitness,
        'best_individual': best_individual
    }
    return result

def run_experiments():
    # Define the CSV file path
    csv_file = 'experiment_results.csv'
    # Check if the file exists to determine if we need to write the header
    file_exists = os.path.isfile(csv_file)

    # Open the CSV file in append mode
    with open(csv_file, 'a', newline='') as csvfile:
        fieldnames = ['n', 'population_size', 'generations', 'mutation_rate', 'solution_found', 'time_taken', 'best_fitness', 'best_individual']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

        # Write the header only if the file does not exist
        if not file_exists:
            writer.writeheader()

        # Define the mutation rates and population sizes to test
        mutation_rates = [0.05, 0.1, 0.15]
        population_sizes = [25, 50, 100]
        generations = 5000  # Keep generations fixed for this experiment

        for N in range(100, 101):
            print(f"Running experiments for N = {N}")
            results = []

            # Loop over all combinations of mutation rates and population sizes
            for mutation_rate in mutation_rates:
                for population_size in population_sizes:
                    print(f"  Testing mutation rate: {mutation_rate}, population size: {population_size}")
                    result = genetic_algorithm(N, population_size, generations, mutation_rate, verbose=False)
                    results.append(result)
                    # Write the result to the CSV file
                    result_copy = result.copy()
                    result_copy['best_individual'] = str(result_copy['best_individual'])
                    writer.writerow(result_copy)
                    csvfile.flush()  # Ensure data is written to disk

        # No need to return results since they are written to the file after each N
        print("All experiments completed and results saved.")

if __name__ == "__main__":
    run_experiments()
