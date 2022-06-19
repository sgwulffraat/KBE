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
import numpy as np
import sys
sys.path.append('source')


class InitialSolution(GeomBase):
    # Load shapely Polygon as it will not work with parapy Polygon
    from shapely.geometry import Polygon

    # Specify parameters for the initial solution
    population_size = Input(100)
    item_specialization_iter_proportion = Input(0.5)
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
    initial_solution_generations = Input(500)

    # Create problem to solve so solution is a solution to the total problem
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

        pop = Solution(problem)
        print(self.connector_parts)
        print(self.items[0])

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
                        print(rotation)
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
                        print(rotation)
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
                        print(rotation)
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
                        print(rotation)
                        pop.placed_items[index] = PlacedShape(shape=shape, position=(x, y), rotation=rotation)
                        pop.value = pop.value + self.items[index].value
                        pop.weight = pop.weight + self.items[index].weight
                        index = index + 1

            # Empty solutions in population are altered to contain the manual solution
            for i in range(self.population_size):
                population[i] = pop

        return population


class Optimization(GeomBase):
    """By choosing optimization options the optimization problem is defined. When set to "Inputs",
    the user is working on finalizing input. When set to "KnapsackPacking", the input provided by the
    user is the complete set of connectors that should be placed on a given bracket. """
    optimization_options = ["Inputs", "KnapsackPacking"]
    optimization = Input("Inputs",
                         label="Optimization Setting",
                         widget=Dropdown(optimization_options, labels=["Working on Inputs", "Optimize!"]))

    solution_directory = ""
    number_of_different_solutions = Input(1)
    generations = Input(1)
    connector_height = Input(2)
    manual_initial_solution = Input(True, widget=Dropdown([True, False], labels=['True', 'False']))
    rotation_step = Input(30)

    @Attribute
    def optimized(self):
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

        if self.optimization == "KnapsackPacking":
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
            placed_items_faces = []
            cog = []
            rotation = []
            number_n1 = number_n2 = number_n3 = number_n4 = \
                area_connectors1 = area_connectors2 = area_connectors3 = area_connectors4 = 0
            print("placed_item_index:", placed_item_index)
            item_index = list(placed_item_index.keys())
            item_index.sort()

            for i in item_index:
                placed_item_coor = []
                for j in range(len(placed_items[i]["x_coor"])):
                    placed_coor = Point(placed_items[i]["x_coor"][j], placed_items[i]["y_coor"][j], 0)
                    placed_item_coor.append(placed_coor)
                placed_items_faces.append(Face(Polygon(placed_item_coor), color="red"))

                if i in range(self.bracket.to_manipulate.n1_problem):
                    number_n1 = number_n1 + 1
                    if number_n1 == 1:
                        row = 0
                    area_connectors1 = area_connectors1 + self.bracket.to_manipulate.optimize_items[1][0] / \
                        self.bracket.to_manipulate.n1_problem
                    worksheet.write(1, 0, self.bracket.to_manipulate.type1)
                    worksheet.write(1, 1, number_n1)
                    worksheet.write(1, 2, area_connectors1)
                    connector1.write(row, 0, str(placed_item_coor))
                    row = row + 1
                    rotation.append(placed_items[i]["rotation"])
                    cog.append([placed_items[i]["centroid"].x, placed_items[i]["centroid"].y])

                elif i in range(self.bracket.to_manipulate.n1_problem,
                                self.bracket.to_manipulate.n1_problem+self.bracket.to_manipulate.n2_problem):
                    number_n2 = number_n2 + 1
                    if number_n2 == 1:
                        row = 0
                    area_connectors2 = area_connectors2 + self.bracket.to_manipulate.optimize_items[1][1] / \
                        self.bracket.to_manipulate.n2_problem
                    worksheet.write(2, 0, self.bracket.to_manipulate.type2)
                    worksheet.write(2, 1, number_n2)
                    worksheet.write(2, 2, area_connectors2)
                    connector2.write(row, 0, str(placed_item_coor))
                    row = row + 1
                    rotation.append(placed_items[i]["rotation"])
                    cog.append([placed_items[i]["centroid"].x, placed_items[i]["centroid"].y])

                elif i in range(self.bracket.to_manipulate.n1_problem+self.bracket.to_manipulate.n2_problem,
                                self.bracket.to_manipulate.n1_problem + self.bracket.to_manipulate.n2_problem +
                                self.bracket.to_manipulate.n3_problem):
                    number_n3 = number_n3 + 1
                    if number_n3 == 1:
                        row = 0
                    area_connectors3 = area_connectors3 + self.bracket.to_manipulate.optimize_items[1][2] / \
                        self.bracket.to_manipulate.n3_problem
                    worksheet.write(3, 0, self.bracket.to_manipulate.type3)
                    worksheet.write(3, 1, number_n3)
                    worksheet.write(3, 2, area_connectors3)
                    connector3.write(row, 0, str(placed_item_coor))
                    row = row + 1
                    rotation.append(placed_items[i]["rotation"])
                    cog.append([placed_items[i]["centroid"].x, placed_items[i]["centroid"].y])

                elif i in range(self.bracket.to_manipulate.n1_problem + self.bracket.to_manipulate.n2_problem +
                                self.bracket.to_manipulate.n3_problem,
                                self.bracket.to_manipulate.n1_problem + self.bracket.to_manipulate.n2_problem +
                                self.bracket.to_manipulate.n3_problem + self.bracket.to_manipulate.n4_problem):
                    number_n4 = number_n4 + 1
                    if number_n4 == 1:
                        row = 0
                    area_connectors4 = area_connectors4 + self.bracket.to_manipulate.optimize_items[1][3] / \
                        self.bracket.to_manipulate.n4_problem
                    worksheet.write(4, 0, self.bracket.to_manipulate.type4)
                    worksheet.write(4, 1, number_n4)
                    worksheet.write(4, 2, area_connectors4)
                    connector4.write(row, 0, str(placed_item_coor))
                    row = row + 1
                    rotation.append(placed_items[i]["rotation"])
                    cog.append([placed_items[i]["centroid"].x, placed_items[i]["centroid"].y])

            area_connectors = area_connectors1 + area_connectors2 + area_connectors3 + area_connectors4
            type1 = f"{number_n1} of {self.bracket.to_manipulate.type1} were placed"
            type2 = f"{number_n2} of {self.bracket.to_manipulate.type2} were placed"
            type3 = f"{number_n3} of {self.bracket.to_manipulate.type3} were placed"
            type4 = f"{number_n4} of {self.bracket.to_manipulate.type4} were placed"

            worksheet.write(5, 0, 'Total:')
            worksheet.write(5, 1, number_n1+number_n2+number_n3+number_n4)
            worksheet.write(6, 0, 'Utilized area:')
            worksheet.write(6, 1, area_connectors/self.bracket.to_manipulate.bracket_area)

            msg = f"""{number_n1} of {self.bracket.to_manipulate.type1} were placed, 
{number_n2} of {self.bracket.to_manipulate.type2} were placed,
{number_n3} of {self.bracket.to_manipulate.type3} were placed, 
{number_n4} of {self.bracket.to_manipulate.type4} were placed.
Total available area: {self.bracket.to_manipulate.bracket_area} [mm^2],
Area of connectors: {area_connectors} [mm^2],
Area utilization: {area_connectors / self.bracket.to_manipulate.bracket_area * 100} %"""
            warnings.warn(msg)
            generate_warning("Optimization complete:", msg)
            workbook.close()
            print(cog)
            return number_n1, number_n2, number_n3, number_n4, cog, rotation, placed_items_faces, \
                type1, type2, type3, type4

    @Attribute(in_tree=True)
    def optimized_bracket(self):
        connector = []
        for i in self.bracket.to_manipulate.connectors:
            if i.shape == "square" or "rectangle":
                for j in i.rectangle_connector:
                    print(j)
                    connector.append(j.local_bbox.box)

            print(i)
        print(connector)
        return SubtractedSolid(shape_in=self.bracket.to_manipulate.bracket_box, tool=connector)  # tool=[self.optimized_connectors1.square_connector[0],self.optimized_connectors1.square_connector[1]])

    @Part
    def optimized_connectors(self):
        return Sequence(type=Connector,
                        quantify=self.optimized[0]+self.optimized[1]+self.optimized[2]+self.optimized[3],
                        c_type=([self.bracket.to_manipulate.type1]*self.optimized[0] +
                               [self.bracket.to_manipulate.type2]*self.optimized[1] + #
                               [self.bracket.to_manipulate.type3]*self.optimized[2] +
                               [self.bracket.to_manipulate.type4]*self.optimized[3])[child.index],
                        cog=self.optimized[4][child.index])

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
                               #connector_part1=self.bracket.to_manipulate.connector_part1,
                               #connector_part2=self.bracket.to_manipulate.connector_part2,
                               #connector_part3=self.bracket.to_manipulate.connector_part3,
                               #connector_part4=self.bracket.to_manipulate.connector_part4)

    @Part
    def bracket(self):
        return ManipulateAnything(to_manipulate=Bracket(n1=1, n1_problem=2,
                                                        n2=1, n2_problem=2,
                                                        n3=1, n3_problem=2,
                                                        n4=1, n4_problem=2),
                                  label='initial_bracket',
                                  pts_container=self.bracket.to_manipulate.pts_container)

    #@Part
    #def optimized_bracket(self):
    #    return ManipulateAnything(to_manipulate=Bracket(n1=self.optimized[0], n2=self.optimized[1],
    #                                                    n3=self.optimized[2], n4=self.optimized[3]))

    @Part
    def optimized_connectors1(self):
        return Connector(c_type=self.bracket.to_manipulate.type1,
                         df=self.bracket.to_manipulate.df,
                         n=self.optimized[0],
                         cog=self.optimized[4][0:self.optimized[0]],
                         rotation=self.optimized[5][0:self.optimized[0]],
                         deg=True,
                         color='green',
                         bracket_height=self.bracket.to_manipulate.height)

    @Part
    def optimized_connectors2(self):
        return Connector(c_type=self.bracket.to_manipulate.type2,
                         df=self.bracket.to_manipulate.df,
                         n=self.optimized[1],
                         cog=self.optimized[4][self.optimized[0]:self.optimized[0] + self.optimized[1]],
                         rotation=self.optimized[5][self.optimized[0]:self.optimized[0] + self.optimized[1]],
                         deg=True,
                         color='green',
                         bracket_height=self.bracket.to_manipulate.height)

    @Part
    def optimized_connectors3(self):
        return Connector(c_type=self.bracket.to_manipulate.type3,
                         df=self.bracket.to_manipulate.df,
                         n=self.optimized[2],
                         cog=self.optimized[4][self.optimized[0] + self.optimized[1]:
                                               self.optimized[0] + self.optimized[1] + self.optimized[2]],
                         rotation=self.optimized[5][self.optimized[0] + self.optimized[1]:
                                                    self.optimized[0] + self.optimized[1] + self.optimized[2]],
                         deg=True,
                         color='green',
                         bracket_height=self.bracket.to_manipulate.height)

    @Part
    def optimized_connectors4(self):
        return Connector(c_type=self.bracket.to_manipulate.type4,
                         df=self.bracket.to_manipulate.df,
                         n=self.optimized[3],
                         cog=self.optimized[4][self.optimized[0] + self.optimized[1] + self.optimized[2]:
                                               self.optimized[0] + self.optimized[1] + self.optimized[2] +
                                               self.optimized[3]],
                         rotation=self.optimized[5][self.optimized[0] + self.optimized[1] + self.optimized[2]:
                                                    self.optimized[0] + self.optimized[1] + self.optimized[2] +
                                                    self.optimized[3]],
                         deg=True,
                         color='green',
                         bracket_height=self.bracket.to_manipulate.height)

    @Part
    def step_writer(self):
        return STEPWriter(trees=[self.bracket, self.connectors])


if __name__ == "__main__":
    from parapy.gui import display
    obj = Optimization(label='Optimization')

    display(obj)
