import os
import pickle
import time
import numpy as np
from math import ceil
from multiprocessing import Pool
from source import evolutionary
from source.common_algorithm_functions import get_time_since, print_if_allowed
from source.problem_solution import Container, Problem, Solution
from source.shape_functions import get_shape_exterior_points, get_centroid


def create_knapsack_packing_problem(container, items, can_print=False):

    """Create a set of Knapsack-Packing problem instances that are solved (optimally) with manual placements (using actions available for all the algorithms); both the problems and solutions are returned"""

    problems, solutions = list(), list()

    start_time = time.time()

    # Problem

    max_weight = np.inf
    container_shape = container

    container = Container(max_weight, container_shape)

    connectors = items
    print(items[0].shape)
    problem = Problem(container, connectors)
    problems.append(problem)

    solution = Solution(problem)
    solutions.append(solution)

    print_if_allowed(solution.add_item(0, (5.73, 3.02), 318.), can_print)
    print_if_allowed(solution.add_item(1, (6.3, 4.1), 40.), can_print)
    print_if_allowed(solution.add_item(2, (4.58, 2.5), 315.), can_print)
    print_if_allowed(solution.add_item(3, (1.3, 5.4), 320.), can_print)
    print_if_allowed(solution.add_item(4, (1.4, 1.7), 20.), can_print)
    print_if_allowed(solution.add_item(5, (2.9, 7.9), 180.), can_print)
    print_if_allowed(solution.add_item(6, (8.2, 4), 300.), can_print)
    print_if_allowed(solution.add_item(7, (2.5, 7.4), 340.), can_print)
    print_if_allowed(solution.add_item(8, (7.3, 4.), 320.), can_print)
    print_if_allowed(solution.add_item(9, (2.9, 3.9), 330.), can_print)
    print_if_allowed(solution.add_item(11, (7.8, 4.4), 0.), can_print)
    print_if_allowed(solution.add_item(13, (6.2, 6.8), 0.), can_print)

    # show elapsed time
    elapsed_time = get_time_since(start_time)
    print_if_allowed("Manual elapsed time: {} ms".format(round(elapsed_time, 3)), can_print)

    return problems, [str(i + 1) for i in range(len(problems))], solutions


def create_problems(problem_type,container,items, can_print=False):

    """Create a set of problems of the specified problem type; both the problems and their optimal solutions (or at least optimal solution values) are returned"""

    return create_knapsack_packing_problem(container, items, can_print=False)


    #return None, None, None


def execute_algorithm_with_params(params):

    """Execute the algorithm specified in the first of the passed parameters with the rest of parameters, and return the solution, value and elapsed time"""

    # unpack the algorithm and its parameters
    algorithm, algorithm_name, problem, show_solution_plot, solution_plot_save_path, calculate_times, calculate_value_evolution, generations, initial_solution, rotation_step = params

    start_time = time.time()
    value_evolution = None
    times_dict = None
    if calculate_value_evolution:
        if algorithm == evolutionary.solve_problem:
            if calculate_times:
                solution, times_dict, value_evolution = algorithm(problem, calculate_times=calculate_times, return_population_fitness_per_generation=calculate_value_evolution, max_generation_num = generations, initial_solution = initial_solution, rotation_step = rotation_step)
            else:
                solution, value_evolution = algorithm(problem, calculate_times=calculate_times, return_population_fitness_per_generation=calculate_value_evolution, max_generation_num = generations, initial_solution = initial_solution, rotation_step = rotation_step)
        else:
            if calculate_times:
                solution, times_dict, value_evolution = algorithm(problem, calculate_times=calculate_times, return_value_evolution=calculate_value_evolution, max_generation_num = generations, initial_solution = initial_solution, rotation_step = rotation_step)
            else:
                solution, value_evolution = algorithm(problem, calculate_times=calculate_times, return_value_evolution=calculate_value_evolution, max_generation_num = generations, initial_solution = initial_solution, rotation_step = rotation_step)
    elapsed_time = get_time_since(start_time)

    if solution and (show_solution_plot or solution_plot_save_path):
        solution.visualize(show_plot=show_solution_plot, save_path=solution_plot_save_path)

    return solution, solution.value, value_evolution, elapsed_time, times_dict


def execute_algorithm(algorithm, algorithm_name, problem, show_solution_plot=False, solution_plot_save_path=None, calculate_times=False, calculate_fitness_stats=False, execution_num=1, process_num=1, gens = 30, initial_solution = 1, rotation_step = 30):

    """Execute the passed algorithm as many times as specified (with each execution in a different CPU process if indicated), returning (at least) lists with the obtained solutions, values and elapsed times (one per execution)"""

    # encapsulate the algorithm and its parameters in a tuple for each execution (needed for multi-processing)
    param_tuples = [(algorithm, algorithm_name, problem, show_solution_plot, solution_plot_save_path, calculate_times, calculate_fitness_stats, gens, initial_solution, rotation_step) for _ in range(execution_num)]

    solutions, values, value_evolutions, times, time_divisions = list(), list(), list(), list(), list()

    # if possible, perform each execution in a separate CPU process (in parallel)
    if process_num > 1:

        process_pool = Pool(process_num)
        batch_num = ceil(execution_num / process_num)
        for batch in range(batch_num):
            results = process_pool.map(execute_algorithm_with_params, param_tuples[batch * process_num: batch * process_num + process_num])
            batch_solutions, batch_values, batch_value_evolutions, batch_times, batch_time_divisions = [result[0] for result in results], [result[1] for result in results], [result[2] for result in results], [result[3] for result in results], [result[4] for result in results]
            solutions.extend(batch_solutions)
            values.extend(batch_values)
            value_evolutions.extend(batch_value_evolutions)
            times.extend(batch_times)
            time_divisions.extend(batch_time_divisions)
            '''process_pool.terminate()
            process_pool.join()'''

    # perform the calculation sequentially if multi-processing is not allowed
    else:

        for i in range(execution_num):

            solution, value, value_evolution, elapsed_time, time_division = execute_algorithm_with_params(param_tuples[i])
            solutions.append(solution)
            values.append(value)
            value_evolutions.append(value_evolution)
            times.append(elapsed_time)
            time_divisions.append(time_division)

    return solutions, values, value_evolutions, times, time_divisions


def perform_experiments(problem_type, output_dir, load_experiments, container, items, num_experiments, gens, initial_solution, rotation_step):
    if problem_type == "KnapsackPacking":
        print("Optimizing! Please wait for finish")
        """Perform a set of experiments for the problem with the passed index, and producing output in the specified directory (when applicable)"""

        experiment_file_path = output_dir + "experiments.pickle"

        # data structure where to store all the problems, and the experimental results for each algorithm: solutions, final values and times
        experiment_dict = dict()

        # if experiments should be loaded (not repeated), do it if possible
        if load_experiments:
            with open(experiment_file_path, "rb") as _file:
                experiment_dict = pickle.load(_file)

        # perform experiments if pre-existing results were not loaded
        if not experiment_dict:

            # given a problem type, create a set of problem instances that are solved (optimally) with manual placements (using actions available for all the algorithms)
            problems, problem_names, manual_solutions = create_problems(problem_type,container,items)

            if problems and problem_names and manual_solutions:

                # parameters for the experimentation; note: calculating internal times and value evolution can increase the overall time of algorithms (in a slight, almost neglectible way)
                execution_num = num_experiments
                process_num = 10  # 1
                calculate_internal_times = True
                calculate_value_evolution = True

                start_time = time.time()

                # solve each problem with each algorithm
                for i, (problem, problem_name, solution) in enumerate(zip(problems, problem_names, manual_solutions)):

                    experiment_dict[problem_name] = {"problem": problem, "manual_solution": solution, "algorithms": dict()}

                    # solve the problem with different algorithms, executing each one multiple times to gain statistical significance
                    for (algorithm_name, algorithm) in [("Evolutionary", evolutionary.solve_problem)]:
                        solutions, values, value_evolutions, times, time_divisions = execute_algorithm(algorithm=algorithm, algorithm_name=algorithm_name, problem=problem, execution_num=execution_num, process_num=process_num, calculate_times=calculate_internal_times, calculate_fitness_stats=calculate_value_evolution,gens = gens, initial_solution = initial_solution, rotation_step = rotation_step)
                        experiment_dict[problem_name]["algorithms"][algorithm_name] = {"solutions": solutions, "values": values, "value_evolutions": value_evolutions, "times": times, "time_divisions": time_divisions}

                # show the total time spent doing experiments (note that significant overhead can be introduced beyond calculation time if plots are shown or saved to files; for strict time measurements, plotting should be avoided altogether)
                print("Total experimental calculation time: {} s".format(round(get_time_since(start_time) / 1000.), 3))

        if experiment_dict:

            # experiment-saving parameter
            save_experiments = True

            # if possible, save the experiments to a binary file
            if not load_experiments and save_experiments:
                with open(experiment_file_path, "wb") as file:
                    pickle.dump(experiment_dict, file)

            # visualization/saving parameters
            show_problem_stats = False
            save_problem_stats = False  # True
            show_manual_solution_plots = False
            save_manual_solution_plots = False  # True
            show_algorithm_solution_plots = False
            save_algorithm_solution_plots = False  # True
            show_value_evolution_plots = False
            save_value_evolution_plots = False  # True
            show_time_division_plots = False
            save_time_division_plots = False  # True
            show_algorithm_comparison = False
            save_algorithm_comparison = False  # True
            show_aggregated_result_tables = True
            save_aggregated_result_tables = False  # True
            show_best_solution_plot = True
            save_best_solution_plot = False

            # show/save the results of the experiments
            #placed_connectors = visualize_and_save_experiments(experiment_dict, output_dir, can_plots_show_value_and_weight=problem_type == KNAPSACK_PACKING_PROBLEM_TYPE, show_problem_stats=show_problem_stats, save_problem_stats=save_problem_stats, show_manual_solution_plots=show_manual_solution_plots, save_manual_solution_plots=save_manual_solution_plots, show_algorithm_solution_plots=show_algorithm_solution_plots, save_algorithm_solution_plots=save_algorithm_solution_plots, show_value_evolution_plots=show_value_evolution_plots, save_value_evolution_plots=save_value_evolution_plots, show_time_division_plots=show_time_division_plots, save_time_division_plots=save_time_division_plots, show_algorithm_comparison=show_algorithm_comparison, save_algorithm_comparison=save_algorithm_comparison, show_aggregated_result_tables=show_aggregated_result_tables, save_aggregated_result_tables=save_aggregated_result_tables,show_best_solution_plot=show_best_solution_plot,save_best_solution_plot=save_best_solution_plot)

        else:
            print("The experiments cannot be performed (there are no problems available).")

        for problem_name in experiment_dict.keys():

            problem, manual_solution, algorithm_dict = experiment_dict[problem_name].values()

            # create a subdirectory to store the solutions of the problem (if not done yet)
            problem_dir_path = output_dir + problem_name + "/"
            if not os.path.exists(problem_dir_path):
                os.mkdir(problem_dir_path)

            plotted_problem_name = "Problem " + problem_name if len(problem_name) < 5 else problem_name
            for algorithm_name, subdict in algorithm_dict.items():
                max_value = max(subdict["values"])
                for i, solution in enumerate(subdict["solutions"]):
                    if subdict["values"][i] == max_value:
                        placed_connectors = dict()
                        for item_index in range(len(problem.items)):
                            if item_index in solution.placed_items:
                                print("item_index:",item_index)
                                placed_shape = solution.placed_items[item_index]
                                print("actual rotation", placed_shape)
                                rotation = placed_shape.rotation
                                print("rotation working testing:", rotation)
                                print("Problem item rotation:", solution.placed_items[item_index].rotation)
                                shape = placed_shape.shape
                                print("shape=",shape)
                                position_offset = (0, 0)
                                x, y = get_shape_exterior_points(shape, False)
                                if position_offset != (0, 0):
                                    x = [x_i + position_offset[0] for x_i in x]
                                    y = [y_i + position_offset[1] for y_i in y]
                                #rotation = math.atan2(y[1]-y[0],x[1]-x[0])*180/math.pi
                                centroid = get_centroid(shape)
                                print('Centroid:', centroid)
                                value = problem.items[item_index].value
                                if value / int(value) == 1:
                                    value = int(value)
                                weight = problem.items[item_index].weight
                                if weight / int(weight) == 1:
                                    weight = int(weight)
                                placed_connectors[item_index] = {"item_index": item_index, "x_coor": x, "y_coor": y,
                                                             "centroid": centroid, "rotation": rotation, "value": value, "weight": weight}
                                print(placed_connectors[item_index]["rotation"])
                        break

        return solution.placed_items, placed_connectors
    else:
        print("""WARNING, INCORRECT SETTING: Please change "Optimization Setting" to "Connectors fully defined".""")


#
# def main():
#
#     """Main function"""
#
#     # set the type of problem to solve and the output directory
#     # problem_type, output_dir = KNAPSACK_PACKING_PROBLEM_TYPE, KNAPSACK_PACKING_PROBLEM_DIR
#     problem_type, output_dir = KNAPSACK_PACKING_PROBLEM_TYPE, KNAPSACK_PACKING_PROBLEM_DIR
#
#     # whether it should be attempted to load existing experiments, and avoid running new ones
#     load_experiments = False
#
#     # perform (or just load and show) a set of experiments
#     perform_experiments(problem_type, output_dir, load_experiments)
#
#
# if __name__ == "__main__":
#     main()
