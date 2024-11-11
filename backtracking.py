import time
import os
import csv

# Backtracking Algorithm

def is_valid(perm, row):
    for i in range(row):
        if perm[i] == perm[row] or abs(perm[i] - perm[row]) == row - i:
            return False
    return True

def solve_nqueens_backtracking(n):
    def backtrack(perm, row):
        if row == n:
            return perm[:]
        
        for col in range(n):
            perm[row] = col
            if is_valid(perm, row):
                solution = backtrack(perm, row + 1)
                if solution:
                    return solution
        return None
    
    perm = [-1] * n
    return backtrack(perm, 0)


# Experiment Runner

def run_experiments():
    csv_file = 'nqueens_results.csv'
    file_exists = os.path.isfile(csv_file)

    with open(csv_file, 'a', newline='') as csvfile:
        fieldnames = ['n', 'algorithm', 'solution_found', 'time_taken', 'best_fitness', 'best_individual']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

        if not file_exists:
            writer.writeheader()

        for N in range(4, 41):
            print(f"Running for N = {N}")

            # Backtracking
            start_time = time.time()
            solution = solve_nqueens_backtracking(N)
            end_time = time.time()

            writer.writerow({
                'n': N,
                'algorithm': 'Backtracking',
                'solution_found': solution is not None,
                'time_taken': end_time - start_time,
                'best_fitness': N * (N - 1) // 2 if solution else None,
                'best_individual': solution if solution else None
            })
            # Ensure data is written to disk after each run
            csvfile.flush()


    print("Experiments completed and results saved to CSV.")

if __name__ == "__main__":
    run_experiments()
