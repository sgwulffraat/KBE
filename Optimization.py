import xlsxwriter
from parapy.geom import *
from parapy.core import *
from parapy.core.widgets import Dropdown
from Bracket import Bracket, generate_warning
from working_testing import perform_experiments
from parapy.exchange import *
from parapy.geom.generic.utilities import vector_angle
import math
from source.evolutionary import generate_population
from working_testing import create_knapsack_packing_problem
from source.problem_solution import PlacedShape, Solution, Container, Item
from Manipulation2 import ManipulateAnything
from connector import Connector
from warnings_and_functions import show, pol_conn, overlap_check
import numpy as np
import sys
sys.path.append('source')


class InitialSolution(GeomBase):
    # Load shapely Polygon as it will not work with parapy Polygon
    from shapely.geometry import Polygon

    # Specify inputs for the initial solution
    population_size = Input(100)
    initial_solution_generations = Input(500)
    manual_initial_solution = Input(False)
    container = Input(Container(np.inf, Polygon([(0, 0), (1, 0), (1, 1), (0, 1)])))
    items = Input(Item(Polygon([(0, 0), (1, 0), (1, 1), (0, 1)]), 1, 0))

    type1 = Input("MIL/20-A")
    type2 = Input("MIL/24-A")
    type3 = Input("EN-2")
    type4 = Input("EN-4")

    n1_problem = Input(0)
    n2_problem = Input(0)
    n3_problem = Input(0)
    n4_problem = Input(0)
    connector_parts = Input([])


    # Create problem to solve so solution is a solution to the correct overall problem
    @Attribute
    def problem(self):
        problems, problem_names, manual_solutions = create_knapsack_packing_problem(self.container, self.items)
        return problems, problem_names, manual_solutions

    # Create initial solution
    @Attribute
    def initial_solution(self):

        # Generate an initial solution or generate empty solution set to be extended using manual connector placements
        for i, (problem, problem_name, solution) in enumerate(zip(self.problem[0], self.problem[1], self.problem[2])):
            if not self.manual_initial_solution:
                population = generate_population(problem,
                                                 self.population_size,
                                                 initial_solution_generations=self.initial_solution_generations)
            else:
                population = [Solution(problem)]*self.population_size

        # Generate an empty solution append
        pop = Solution(problem)

        # If True, manual solution is generated based on placement of connectors
        if self.manual_initial_solution:
            print("Into initial solution loop")

            # Add first connector type to initial solution in population with correct placement and rotation
            index = 0
            for i in self.connector_parts:
                if i.c_type == self.type1:
                    if i.shape == "square" or i.shape == "rectangle":
                        j = i.rectangle_connector
                    elif i.shape == "circle":
                        j = i.circular_connector
                    for k in range(len(j)):
                        shape = self.items[index].shape
                        x, y = j[k].cog[0], j[k].cog[1]
                        rotation = vector_angle(j[k].orientation[0], Vector(1, 0, 0), False) / math.pi * 180
                        pop.placed_items[index] = PlacedShape(shape=shape, position=(x, y), rotation=rotation)
                        pop.value = pop.value + self.items[index].value
                        pop.weight = pop.weight + self.items[index].weight
                        index = index + 1

            # Add second connector type to initial solution in population with correct placement and rotation
            index = self.n1_problem
            for i in self.connector_parts:
                if i.c_type == self.type2:
                    if i.shape == "square" or i.shape == "rectangle":
                        j = i.rectangle_connector
                    elif i.shape == "circle":
                        j = i.circular_connector
                    for k in range(len(j)):
                        shape = self.items[index].shape
                        x, y = j[k].cog[0], j[k].cog[1]
                        rotation = vector_angle(j[k].orientation[0], Vector(1, 0, 0), False) / math.pi * 180
                        pop.placed_items[index] = PlacedShape(shape=shape, position=(x, y), rotation=rotation)
                        pop.value = pop.value + self.items[index].value
                        pop.weight = pop.weight + self.items[index].weight
                        index = index + 1

            # Add third connector type to initial solution in population with correct placement and rotation
            index = self.n1_problem + self.n2_problem
            for i in self.connector_parts:
                if i.c_type == self.type3:
                    if i.shape == "square" or i.shape == "rectangle":
                        j = i.rectangle_connector
                    elif i.shape == "circle":
                        j = i.circular_connector
                    for k in range(len(j)):
                        shape = self.items[index].shape
                        x, y = j[k].cog[0], j[k].cog[1]
                        rotation = vector_angle(j[k].orientation[0], Vector(1, 0, 0), False) / math.pi * 180
                        pop.placed_items[index] = PlacedShape(shape=shape, position=(x, y), rotation=rotation)
                        pop.value = pop.value + self.items[index].value
                        pop.weight = pop.weight + self.items[index].weight
                        index = index + 1

            # Add fourth connector type to initial solution in population with correct placement and rotation
            index = self.n1_problem + self.n2_problem + self.n3_problem
            for i in self.connector_parts:
                if i.c_type == self.type4:
                    if i.shape == "square" or i.shape == "rectangle":
                        j = i.rectangle_connector
                    elif i.shape == "circle":
                        j = i.circular_connector
                    for k in range(len(j)):
                        shape = self.items[index].shape
                        x, y = j[k].cog[0], j[k].cog[1]
                        rotation = vector_angle(j[k].orientation[0], Vector(1, 0, 0), False) / math.pi * 180
                        pop.placed_items[index] = PlacedShape(shape=shape, position=(x, y), rotation=rotation)
                        pop.value = pop.value + self.items[index].value
                        pop.weight = pop.weight + self.items[index].weight
                        index = index + 1

            # Alter empty solutions in population to contain the generated manual solution for full population size.
            for i in range(self.population_size):
                population[i] = pop

        return population


class Optimization(GeomBase):

    # Specify inputs for optimization, optimization only starts when it is set to KnapsackPacking.
    optimization_options = ["Inputs", "KnapsackPacking"]
    optimization = Input("Inputs",
                         label="optimization_setting",
                         widget=Dropdown(optimization_options, labels=["Working on Inputs", "Optimize!"]))
    solution_directory = ""
    number_of_different_solutions = Input(1)

    # Higher generations results in better solutions, but longer solving time.
    generations = Input(1)
    connector_height = Input(2)

    # Set to True when the user wants to define an initial solution by dragging connectors.
    manual_initial_solution = Input(True, widget=Dropdown([True, False], labels=['True', 'False']))

    # Rotation step used in algorithm in [deg]. Larger angles result in more logical solution, but limits creativity.
    rotation_step = Input(30)

    # Allow pop-up
    popup_gui = Input(True, label="Allow pop-up")

    # Button to start optimization.
    @action(label="click_to_optimize",button_label="OPTIMIZE")
    def optimize(self):
        if overlap_check(connectors=self.bracket.to_manipulate.connectors,
                         tol=self.bracket.to_manipulate.tol) is True:
            msg = "Warning: Overlap present in initial solution. Try removing overlapping " \
                  "connector."
            warnings.warn(msg)
            if self.popup_gui:
                generate_warning("Warning: Invalid action", msg)
        else:
            self.optimization = "KnapsackPacking"

    # Button to show optimized results.
    @action(button_label="SHOW OPTIMIZED SOLUTION")
    def show_optimization(self):
        for i in self.optimized_connectors:
            show(i)
        show(self.optimized_bracket)

    # Optimization loop itself.
    @Attribute
    def optimizing_results(self):

        # Opens Excel sheet to write placement solutions to.
        workbook = xlsxwriter.Workbook('Optimized_bracket.xlsx')
        worksheet = workbook.add_worksheet()
        worksheet.write(0, 0, 'Connector Type')
        worksheet.write(0, 1, 'Quantity')
        worksheet.write(0, 2, 'Area')
        worksheet.write(0, 3, 'Position')
        connector1 = workbook.add_worksheet("Connector 1")
        connector2 = workbook.add_worksheet("Connector 2")
        connector3 = workbook.add_worksheet("Connector 3")
        connector4 = workbook.add_worksheet("Connector 4")

        # Only starts optimization when set to KnapsackPacking.  Done using action.
        if self.optimization == "KnapsackPacking":

            # Runs function to solve problem based on given inputs.
            placed_item_index, placed_items = perform_experiments(
                                            self.optimization,
                                            self.solution_directory,
                                            load_experiments=False,
                                            container=self.initial_solution.bracket.to_manipulate.optimize_container,
                                            items=self.initial_solution.bracket.to_manipulate.optimize_items[0],
                                            num_experiments=self.number_of_different_solutions,
                                            gens=self.generations,
                                            initial_solution=self.initial_solution.initial_solution,
                                            rotation_step=self.rotation_step)

            cog = []
            rotation = []
            number_n1 = number_n2 = number_n3 = number_n4 = \
                area_connectors1 = area_connectors2 = area_connectors3 = area_connectors4 = 0
            item_index = list(placed_item_index.keys())

            # Sorting the order of placed items in the solution to simplify loop.
            item_index.sort()

            for i in item_index:

                # Determine all edge coordinates of placed item i.
                placed_item_coor = []
                for j in range(len(placed_items[i]["x_coor"])):
                    placed_coor = Point(placed_items[i]["x_coor"][j], placed_items[i]["y_coor"][j], 0)
                    placed_item_coor.append(placed_coor)


                if i in range(self.bracket.to_manipulate.n1_problem):

                    # Determine amount of placed connectors of type 1 and used area and write to Excel sheet.
                    number_n1 = number_n1 + 1
                    if number_n1 == 1:
                        row = 0
                    area_connectors1 = area_connectors1 + self.bracket.to_manipulate.optimize_items[1][0] / \
                        self.bracket.to_manipulate.n1_problem
                    worksheet.write(1, 0, self.bracket.to_manipulate.type1)
                    worksheet.write(1, 1, number_n1)
                    worksheet.write(1, 2, area_connectors1)

                    # Writes coordinates of placed item i to Excel sheet of connector type 1.
                    connector1.write(row, 0, str(placed_item_coor))
                    row = row + 1

                    # Determine the rotation and cog of placed item i.
                    rotation.append(placed_items[i]["rotation"])
                    cog.append([placed_items[i]["centroid"].x, placed_items[i]["centroid"].y])

                elif i in range(self.bracket.to_manipulate.n1_problem,
                                self.bracket.to_manipulate.n1_problem+self.bracket.to_manipulate.n2_problem):

                    # Determine amount of placed connectors of type 2 and used area and write to Excel sheet.
                    number_n2 = number_n2 + 1
                    if number_n2 == 1:
                        row = 0
                    area_connectors2 = area_connectors2 + self.bracket.to_manipulate.optimize_items[1][1] / \
                        self.bracket.to_manipulate.n2_problem
                    worksheet.write(2, 0, self.bracket.to_manipulate.type2)
                    worksheet.write(2, 1, number_n2)
                    worksheet.write(2, 2, area_connectors2)

                    # Writes coordinates of placed item i to Excel sheet of connector type 2.
                    connector2.write(row, 0, str(placed_item_coor))
                    row = row + 1

                    # Determine the rotation and cog of placed item i.
                    rotation.append(placed_items[i]["rotation"])
                    cog.append([placed_items[i]["centroid"].x, placed_items[i]["centroid"].y])

                elif i in range(self.bracket.to_manipulate.n1_problem+self.bracket.to_manipulate.n2_problem,
                                self.bracket.to_manipulate.n1_problem + self.bracket.to_manipulate.n2_problem +
                                self.bracket.to_manipulate.n3_problem):

                    # Determine amount of placed connectors of type 3 and used area and write to Excel sheet.
                    number_n3 = number_n3 + 1
                    if number_n3 == 1:
                        row = 0
                    area_connectors3 = area_connectors3 + self.bracket.to_manipulate.optimize_items[1][2] / \
                        self.bracket.to_manipulate.n3_problem
                    worksheet.write(3, 0, self.bracket.to_manipulate.type3)
                    worksheet.write(3, 1, number_n3)
                    worksheet.write(3, 2, area_connectors3)

                    # Writes coordinates of placed item i to Excel sheet of connector type 3.
                    connector3.write(row, 0, str(placed_item_coor))
                    row = row + 1

                    # Determine the rotation and cog of placed item i.
                    rotation.append(placed_items[i]["rotation"])
                    cog.append([placed_items[i]["centroid"].x, placed_items[i]["centroid"].y])

                elif i in range(self.bracket.to_manipulate.n1_problem + self.bracket.to_manipulate.n2_problem +
                                self.bracket.to_manipulate.n3_problem,
                                self.bracket.to_manipulate.n1_problem + self.bracket.to_manipulate.n2_problem +
                                self.bracket.to_manipulate.n3_problem + self.bracket.to_manipulate.n4_problem):

                    # Determine amount of placed connectors of type 4 and used area and write to Excel sheet.
                    number_n4 = number_n4 + 1
                    if number_n4 == 1:
                        row = 0
                    area_connectors4 = area_connectors4 + self.bracket.to_manipulate.optimize_items[1][3] / \
                        self.bracket.to_manipulate.n4_problem
                    worksheet.write(4, 0, self.bracket.to_manipulate.type4)
                    worksheet.write(4, 1, number_n4)
                    worksheet.write(4, 2, area_connectors4)

                    # Writes coordinates of placed item i to Excel sheet of connector type 4.
                    connector4.write(row, 0, str(placed_item_coor))
                    row = row + 1

                    # Determine the rotation and cog of placed item i.
                    rotation.append(placed_items[i]["rotation"])
                    cog.append([placed_items[i]["centroid"].x, placed_items[i]["centroid"].y])

            # Total used area of all placed items.
            area_connectors = area_connectors1 + area_connectors2 + area_connectors3 + area_connectors4

            # Write total number of placed items and the utilized area of the bracket to Excel.
            worksheet.write(5, 0, 'Total:')
            worksheet.write(5, 1, number_n1+number_n2+number_n3+number_n4)
            worksheet.write(6, 0, 'Utilized area:')
            worksheet.write(6, 1, area_connectors/self.bracket.to_manipulate.bracket_area)

            # Generate message to indicate optimization is finished.
            msg = f"""{number_n1} of {self.bracket.to_manipulate.type1} were placed, 
{number_n2} of {self.bracket.to_manipulate.type2} were placed,
{number_n3} of {self.bracket.to_manipulate.type3} were placed, 
{number_n4} of {self.bracket.to_manipulate.type4} were placed.
Total available area: {self.bracket.to_manipulate.bracket_area} [mm^2],
Area of connectors: {area_connectors} [mm^2],
Area utilization: {area_connectors / self.bracket.to_manipulate.bracket_area * 100} %"""
            warnings.warn(msg)
            generate_warning("Optimization complete:", msg)

            # Close Excel sheet.
            workbook.close()

            return number_n1, number_n2, number_n3, number_n4, cog, rotation

    # Generates solids and indicates placement of connectors.
    @Attribute(in_tree=True)
    def optimized_connectors(self):

        # Only useful if optimization happens, otherwise returns empty list.
        if self.optimization == "KnapsackPacking":

            # Specify number of placed items and their locations from attribute optimizing_results.
            number_n1 = self.optimizing_results[0]
            number_n2 = self.optimizing_results[1]
            number_n3 = self.optimizing_results[2]
            number_n4 = self.optimizing_results[3]
            cog = self.optimizing_results[4]
            rotation = self.optimizing_results[5]
            connector = [Connector()]

            # Generate connector solids for all placed items of type 1.
            connector[0] = Connector(c_type=self.bracket.to_manipulate.type1,
                                     df=self.bracket.to_manipulate.df,
                                     n=number_n1,
                                     cog=cog[0:number_n1],
                                     rotation=rotation[0:number_n1],
                                     deg=True,
                                     color='green',
                                     bracket_height=self.bracket.to_manipulate.height,
                                     label=f"Placed {self.bracket.to_manipulate.type1} connectors")

            # Generate connector solids for all placed items of type 2.
            connector.append(Connector(c_type=self.bracket.to_manipulate.type2,
                                       df=self.bracket.to_manipulate.df,
                                       n=number_n2,
                                       cog=cog[number_n1:number_n1+number_n2],
                                       rotation=rotation[number_n1:number_n1+number_n2],
                                       deg=True,
                                       color='green',
                                       bracket_height=self.bracket.to_manipulate.height,
                                       label=f"Placed {self.bracket.to_manipulate.type2} connectors"))

            # Generate connector solids for all placed items of type 3.
            connector.append(Connector(c_type=self.bracket.to_manipulate.type3,
                                       df=self.bracket.to_manipulate.df,
                                       n=number_n3,
                                       cog=cog[number_n1+number_n2:number_n1+number_n2+number_n3],
                                       rotation=rotation[number_n1+number_n2:number_n1+number_n2+number_n3],
                                       deg=True,
                                       color='green',
                                       bracket_height=self.bracket.to_manipulate.height,
                                       label=f"Placed {self.bracket.to_manipulate.type3} connectors"))

            # Generate connector solids for all placed items of type 4.
            connector.append(Connector(c_type=self.bracket.to_manipulate.type4,
                                       df=self.bracket.to_manipulate.df,
                                       n=number_n4,
                                       cog=cog[number_n1+number_n2+number_n3:number_n1+number_n2+number_n3+number_n4],
                                       rotation=rotation[number_n1+number_n2+number_n3:number_n1+number_n2+number_n3+number_n4],
                                       deg=True,
                                       color='green',
                                       bracket_height=self.bracket.to_manipulate.height,
                                       label=f"Placed {self.bracket.to_manipulate.type4} connectors"))

            # Loop to return only the solids of the placed connectors defined above for simplicity.
            connector1 = []
            for i in connector:
                if i.shape == "square" or i.shape == "rectangle":
                    j = i.rectangle_connector
                elif i.shape == "circle":
                    j = i.circular_connector
                for k in range(len(j)):
                    connector1.append(j[k])


            return connector1
        else:
            return []

    # Generates the geometry of the bracket with holes for the connectors.
    @Attribute(in_tree=True)
    def optimized_bracket(self):

        # Only useful if optimization happens, otherwise returns empty list.
        if self.optimization == "KnapsackPacking":

            # Generates solid for bracket irrespective of what the shape the bracket is.
            if self.bracket.to_manipulate.bracketshape == "rectangle":
                bracket = self.bracket.to_manipulate.bracket_box
            elif self.bracket.to_manipulate.bracketshape == 'circle':
                bracket = self.bracket.to_manipulate.bracket_cylinder
            elif self.bracket.to_manipulate.bracketshape == "file":
                bracket = ExtrudedSolid(face_in=self.bracket.to_manipulate.bracket_from_file.children[0].children[0].
                                        children[0].children[0].faces[0],
                                        distance=self.bracket.to_manipulate.height,
                                        direction='z')


            # Generates tools to make holes in the bracket.
            tool = list()
            for i in self.optimized_connectors:
                    tool.append(i.solids[0])
                    print(tool)

            return SubtractedSolid(shape_in=bracket,tool=tool)

        else:
            return []

    # Part defining initial solution for optimization based on given inputs (algorithm or manual placement).
    @Part
    def initial_solution(self):
        return InitialSolution(manual_initial_solution=self.manual_initial_solution,
                               container=self.bracket.to_manipulate.optimize_container,
                               items=self.bracket.to_manipulate.optimize_items[0],
                               n1_problem=self.bracket.to_manipulate.n1_problem,
                               n2_problem=self.bracket.to_manipulate.n2_problem,
                               n3_problem=self.bracket.to_manipulate.n3_problem,
                               n4_problem=self.bracket.to_manipulate.n4_problem,
                               connector_parts=self.bracket.to_manipulate.connectors,
                               type1=self.bracket.to_manipulate.type1,
                               type2=self.bracket.to_manipulate.type2,
                               type3=self.bracket.to_manipulate.type3,
                               type4=self.bracket.to_manipulate.type4)

    # Part defining bracket and allowing manipulation of connector placement.
    @Part
    def bracket(self):
        return ManipulateAnything(to_manipulate=Bracket(n1=1, n1_problem=2,
                                                        n2=1, n2_problem=2,
                                                        n3=1, n3_problem=2,
                                                        n4=1, n4_problem=2),
                                  label='initial_bracket')#,
                                  #pts_container=self.bracket.to_manipulate.pts_container)

    # Part allowing to write step of generated optimized bracket geometry.
    @Part
    def step_writer(self):
        return STEPWriter(trees=self.optimized_bracket)


if __name__ == "__main__":
    from parapy.gui import display
    obj = Optimization(label='Optimization')

    display(obj)
