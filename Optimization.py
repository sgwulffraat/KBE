import xlsxwriter
from parapy.geom import *
from parapy.core import *
from parapy.core.widgets import Dropdown, FilePicker
from Bracket import Bracket, generate_warning
from working_testing import perform_experiments
from parapy.exchange import *
import sys
sys.path.append('source')
from source.evolutionary import generate_population
from working_testing import create_knapsack_packing_problem
from source.problem_solution import PlacedShape, Solution, Container, Item
from Manipulation import ManipulateAnything
from connector import Connector
import numpy as np
import sys
sys.path.append('source')


class Initial_Solution(GeomBase):
    from shapely.geometry import Polygon
    population_size = Input(100)
    item_specialization_iter_proportion = Input(0.5)
    manual_initial_solution = Input(False)
    container = Input(Container(np.inf, Polygon([(0, 0), (1, 0), (1, 1), (0, 1)])))
    items = Input(Item(Polygon([(0, 0), (1, 0), (1, 1), (0, 1)]), 1, 0))
    n1_problem = Input(1)
    connector_part = Input(Connector())


    @Attribute
    def problem(self):
        problems, problem_names, manual_solutions = create_knapsack_packing_problem(self.container,self.items)
        return problems, problem_names, manual_solutions

    @Attribute
    def initial_solution(self):
        for i, (problem, problem_name, solution) in enumerate(zip(self.problem[0], self.problem[1], self.problem[2])):
            population = generate_population(problem, self.population_size, self.item_specialization_iter_proportion)

        pop = Solution(problem)

        if self.manual_initial_solution == True:
            for j in range(len(self.connector_part.square_connector)):
                shape = self.items[j].shape
                x,y = self.connector_part.square_connector[j].cog[0],self.connector_part.square_connector[j].cog[1]
                pop.placed_items[j] = PlacedShape(shape=shape,position=(x,y),rotation=0)
                pop.value = pop.value + self.items[j].value
                pop.weight = pop.weight + self.items[j].weight

            for i in range(self.population_size):
                population[i] = pop

        return population

class Optimization(GeomBase):
    from parapy.geom import Polygon, Point
    """By choosing optimization options the optimization problem is defined. When set to "Inputs",
    the user is working on finalizing input. When set to "KnapsackPacking", the input provided by the
    user is the complete set of connectors that should be placed on a given bracket. """
    optimization_options = ["Inputs", "KnapsackPacking"]
    optimization = Input("Inputs", label="Optimization Setting", widget=Dropdown(optimization_options, labels=["Working on Inputs","Optimize!"]))

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
        worksheet.write(0, 0,'Connector Type')
        worksheet.write(0, 1,'Quantity')
        worksheet.write(0, 2,'Area')
        worksheet.write(0, 3,'Position')
        connector1 = workbook.add_worksheet("Connector 1")
        connector2 = workbook.add_worksheet("Connector 2")
        connector3 = workbook.add_worksheet("Connector 3")
        connector4 = workbook.add_worksheet("Connector 4")

        if self.optimization == "KnapsackPacking":
            placed_item_index, placed_items = perform_experiments(self.optimization,
                                                                  self.solution_directory,
                                                                  load_experiments=False,
                                                                  container=self.initial_solution.bracket.to_manipulate.optimize_container,
                                                                  items=self.initial_solution.bracket.to_manipulate.optimize_items[0],
                                                                  num_experiments = self.number_of_different_solutions,
                                                                  gens = self.generations,
                                                                  initial_solution = self.initial_solution.initial_solution,
                                                                  rotation_step = self.rotation_step)
            placed_items_faces = []
            number_n1 = number_n2 = number_n3 = number_n4 = area_connectors1 = area_connectors2 = area_connectors3 = area_connectors4 = 0
            cog = []
            rotation = []
            print("placed_item_index:", placed_item_index)
            for i in placed_item_index:
                print(placed_items[i]["centroid"])
                rotation.append(placed_items[i]["rotation"])
                print("rotation:", rotation)
                cog.append([placed_items[i]["centroid"].x,placed_items[i]["centroid"].y])
                print(cog)
                placed_item_coor = []
                for j in range(len(placed_items[i]["x_coor"])):
                    placed_coor = Point(placed_items[i]["x_coor"][j],placed_items[i]["y_coor"][j],0)
                    placed_item_coor.append(placed_coor)
                placed_items_faces.append(Face(Polygon(placed_item_coor),color="red"))

                if i in range(self.bracket.to_manipulate.n1_problem):
                    number_n1 = number_n1 + 1
                    if number_n1 == 1:
                        row = 0
                    area_connectors1 = area_connectors1 + self.bracket.to_manipulate.optimize_items[1][0]/self.bracket.to_manipulate.n1_problem
                    worksheet.write(1,0,self.bracket.to_manipulate.type1)
                    worksheet.write(1,1,number_n1)
                    worksheet.write(1,2,area_connectors1)
                    connector1.write(row,0,str(placed_item_coor))
                    row = row + 1

                elif i in range(self.bracket.to_manipulate.n1_problem,
                                self.bracket.to_manipulate.n1_problem+self.bracket.to_manipulate.n2_problem):
                    number_n2 = number_n2 + 1
                    if number_n2 == 1:
                        row = 0
                    area_connectors2 = area_connectors2 + self.bracket.to_manipulate.optimize_items[1][1]/self.bracket.to_manipulate.n2_problem
                    worksheet.write(2, 0, self.bracket.to_manipulate.type2)
                    worksheet.write(2, 1, number_n2)
                    worksheet.write(2, 2, area_connectors2)
                    connector2.write(row, 0, str(placed_item_coor))
                    row = row + 1

                elif i in range(self.bracket.to_manipulate.n1_problem+self.bracket.to_manipulate.n2_problem,
                                self.bracket.to_manipulate.n1_problem + self.bracket.to_manipulate.n2_problem+self.bracket.to_manipulate.n3_problem):
                    number_n3 = number_n3 + 1
                    if number_n3 == 1:
                        row = 0
                    area_connectors3 = area_connectors3 + self.bracket.to_manipulate.optimize_items[1][2]/self.bracket.to_manipulate.n3_problem
                    worksheet.write(3, 0, self.bracket.to_manipulate.type3)
                    worksheet.write(3, 1, number_n3)
                    worksheet.write(3, 2, area_connectors3)
                    connector3.write(row, 0, str(placed_item_coor))
                    row = row + 1

                elif i in range(self.bracket.to_manipulate.n1_problem+self.bracket.to_manipulate.n2_problem+self.bracket.to_manipulate.n3_problem,
                                self.bracket.to_manipulate.n1_problem+self.bracket.to_manipulate.n2_problem+self.bracket.to_manipulate.n3_problem+self.bracket.to_manipulate.n4_problem):
                    number_n4 = number_n4 + 1
                    if number_n4 == 1:
                        row = 0
                    area_connectors4 = area_connectors4 + self.bracket.to_manipulate.optimize_items[1][3]/self.bracket.to_manipulate.n4_problem
                    worksheet.write(4, 0, self.bracket.to_manipulate.type4)
                    worksheet.write(4, 1, number_n4)
                    worksheet.write(4, 2, area_connectors4)
                    connector4.write(row, 0, str(placed_item_coor))
                    row = row + 1

            area_connectors = area_connectors1 + area_connectors2 + area_connectors3 + area_connectors4
            type1 = f"{number_n1} of {self.bracket.to_manipulate.type1} were placed"
            type2 = f"{number_n2} of {self.bracket.to_manipulate.type2} were placed"
            type3 = f"{number_n3} of {self.bracket.to_manipulate.type3} were placed"
            type4 = f"{number_n4} of {self.bracket.to_manipulate.type4} were placed"

            worksheet.write(5, 0, 'Total:')
            worksheet.write(5, 1, number_n1+number_n2+number_n3+number_n4)
            worksheet.write(6, 0, 'Utilized area:')
            worksheet.write(6,1,area_connectors/self.bracket.to_manipulate.bracket_area)

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
            return number_n1, number_n2, number_n3, number_n4, cog, rotation, placed_items_faces, type1, type2, type3, type4


    @Part
    def initial_solution(self):
        return Initial_Solution(manual_initial_solution=self.manual_initial_solution,
                                container=self.bracket.to_manipulate.optimize_container,
                                items=self.bracket.to_manipulate.optimize_items[0],
                                n1_problem=self.bracket.to_manipulate.n1_problem,
                                connector_part=self.bracket.to_manipulate.connector_part)

    @Part
    def bracket(self):
        return ManipulateAnything(to_manipulate=Bracket(n1=2,n1_problem=9), pts_container=Bracket().pts_container,
                                  label='bracket: right-click to manipulate')

    @Part
    def optimized_connectors(self):
        return Connector(c_type=self.bracket.to_manipulate.type1,
                         df=self.bracket.to_manipulate.df,
                         n=self.optimized[0],
                         cog=self.optimized[4],
                         rotation=self.optimized[5],
                         deg=True,
                         color='green')


    @Part
    def step_writer(self):
        return STEPWriter(trees = [self.bracket,self.connectors])

if __name__ == "__main__":
    from parapy.gui import display
    obj = Optimization(label = 'Optimization')

    display(obj)

