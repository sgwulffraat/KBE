import os
import pickle
import time
import numpy as np
from math import ceil
from multiprocessing import Pool
import pandas as pd
from shapely.geometry import Polygon, MultiPolygon, Point
import evolutionary
import greedy
import reversible
import shape_functions
from circle import Circle
from common_algorithm_functions import get_time_since, visualize_boxplot_for_data_sequence, print_if_allowed, \
    visualize_plot, visualize_bar_plot, add_newlines_by_spaces, get_stats
from ellipse import Ellipse
from problem_solution import Item, Container, Problem, Solution


def execute_algorithm_with_params(params):

    """Execute the algorithm specified in the first of the passed parameters with the rest of parameters, and return the solution, value and elapsed time"""

    # unpack the algorithm and its parameters
    algorithm, algorithm_name, problem, show_solution_plot, solution_plot_save_path, calculate_times, calculate_value_evolution = params

    start_time = time.time()
    value_evolution = None
    times_dict = None
    if calculate_value_evolution:
        if algorithm == evolutionary.solve_problem:
            if calculate_times:
                solution, times_dict, value_evolution = algorithm(problem, calculate_times=calculate_times, return_population_fitness_per_generation=calculate_value_evolution)
            else:
                solution, value_evolution = algorithm(problem, calculate_times=calculate_times, return_population_fitness_per_generation=calculate_value_evolution)
        else:
            if calculate_times:
                solution, times_dict, value_evolution = algorithm(problem, calculate_times=calculate_times, return_value_evolution=calculate_value_evolution)
            else:
                solution, value_evolution = algorithm(problem, calculate_times=calculate_times, return_value_evolution=calculate_value_evolution)
    elif calculate_times:
        solution, times_dict = algorithm(problem, calculate_times=calculate_times)
    else:
        solution = algorithm(problem)
    elapsed_time = get_time_since(start_time)

    if solution and (show_solution_plot or solution_plot_save_path):
        solution.visualize(show_plot=show_solution_plot, save_path=solution_plot_save_path)

    return solution, solution.value, value_evolution, elapsed_time, times_dict

def execute_algorithm(algorithm, algorithm_name, problem, show_solution_plot=False, solution_plot_save_path=None, calculate_times=False, calculate_fitness_stats=False, execution_num=1, process_num=1):

    """Execute the passed algorithm as many times as specified (with each execution in a different CPU process if indicated), returning (at least) lists with the obtained solutions, values and elapsed times (one per execution)"""

    # encapsulate the algorithm and its parameters in a tuple for each execution (needed for multi-processing)
    param_tuples = [(algorithm, algorithm_name, problem, show_solution_plot, solution_plot_save_path, calculate_times, calculate_fitness_stats) for _ in range(execution_num)]

    solutions, values, value_evolutions, times, time_divisions = [], [], [], [], []

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

max_weight = np.inf
container_shape = Polygon([(0.0, 0.0), (100.0, 0.0), (100.0, 100.0), (0.0, 100.0)])
execution_num = 10
process_num = 1
calculate_internal_times = True
calculate_value_evolution = True
# algorithm_name = "Greedy"
# algorithm = greedy.solve_problem
# algorithm_name = "Reversible"
# algorithm = reversible.solve_problem
algorithm_name = "Evolutionary"
algorithm = evolutionary.solve_problem

# del parapy.geom.Polygon

container = Container(max_weight, container_shape)
items = [Item(Polygon([(0.0, 0.0), (86.1, 0.0), (86.1, 15.2), (0, 15.2)]), 1, 1),
         Item(Polygon([(0.0, 0.0), (86.1, 0.0), (86.1, 15.2), (0, 15.2)]), 1, 1),
         Item(Polygon([(0.0, 0.0), (86.1, 0.0), (86.1, 15.2), (0, 15.2)]), 1, 1),
         Item(Polygon([(0.0, 0.0), (86.1, 0.0), (86.1, 15.2), (0, 15.2)]), 1, 1),
         Item(Polygon([(0.0, 0.0), (55.6, 0.0), (55.6, 15.2), (0, 15.2)]), 1, 1),
         Item(Polygon([(0.0, 0.0), (55.6, 0.0), (55.6, 15.2), (0, 15.2)]), 1, 1),
         Item(Polygon([(0.0, 0.0), (55.6, 0.0), (55.6, 15.2), (0, 15.2)]), 1, 1),
         Item(Polygon([(0.0, 0.0), (55.6, 0.0), (55.6, 15.2), (0, 15.2)]), 1, 1)]
problem = Problem(container, items)

solutions, values, value_evolutions, times, time_divisions = execute_algorithm(algorithm=algorithm, algorithm_name=algorithm_name, problem=problem,
                                                                               execution_num=execution_num, process_num=process_num, calculate_times=calculate_internal_times,
                                                                               calculate_fitness_stats=calculate_value_evolution)

for i in range(0,execution_num):
    solutions[i].visualize()