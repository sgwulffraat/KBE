from working_testing import perform_experiments

KNAPSACK_PACKING_PROBLEM_TYPE = "KnapsackPacking"
KNAPSACK_PACKING_PROBLEM_DIR = "../Output/Problems/CustomKnapsackPacking/Test/"
problem_type, output_dir = KNAPSACK_PACKING_PROBLEM_TYPE, KNAPSACK_PACKING_PROBLEM_DIR
load_experiments = False


if __name__ == "__main__":
    container, placed_connectors = perform_experiments(KNAPSACK_PACKING_PROBLEM_TYPE,KNAPSACK_PACKING_PROBLEM_DIR,load_experiments)
    print(container,placed_connectors)