from parapy.geom import *
from parapy.core import *
from parapy.core.widgets import Dropdown, FilePicker
from parapy.core.validate import *
from parapy.exchange import *
from connector import Connector
from connector_input_converter import connector_input_converter, read_connector_excel
from shapely.geometry import Polygon
from source.circle import Circle
from parapy.geom import TextLabel
from Manipulation import ManipulateAnything
import numpy as np
import sys
from source.evolutionary import generate_population
from source.problem_solution import PlacedShape, Solution, Container, Item
from working_testing import create_knapsack_packing_problem
from warning_pop_up import generate_warning
sys.path.append('source')


class Bracket(GeomBase):
    # Shape input: rectangle, circle or file
    shapeoptions = ["rectangle", "circle", "file"]

    # Connector input: various abbreviated connector types. See 'Connector details.xsl' for reference.
    connectorlabels, df, df2 = read_connector_excel('Connector details.xlsx', 'Connector details',
                                                    'Cavity specific area')

    # Input block bracket generator
    bracketshape = Input("rectangle",
                         widget=Dropdown(shapeoptions, labels=["Rectangular", "Circular",
                                                               "Create from file"]))
    filename = Input(__file__, widget=FilePicker)

    # Widget section connector type selection
    type1 = Input("MIL/20-A", label="Type Connector",
                  widget=Dropdown(connectorlabels))
    n1 = Input(1, label="Placed number of this type", validator=Positive(incl_zero=True))
    n1_problem = Input(0, label="Total number of this type", validator=Positive(incl_zero=True))
    type2 = Input("MIL/24-A", label="Type Connector",
                  widget=Dropdown(connectorlabels))
    n2 = Input(0, label="Placed number of this type", validator=Positive(incl_zero=True))
    n2_problem = Input(0, label="Total number of this type", validator=Positive(incl_zero=True))
    type3 = Input("EN-2", label="Type Connector",
                  widget=Dropdown(connectorlabels))
    n3 = Input(0, label="Placed number of this type", validator=Positive(incl_zero=True))
    n3_problem = Input(0, label="Total number of this type", validator=Positive(incl_zero=True))
    type4 = Input("EN-4", label="Type Connector",
                  widget=Dropdown(connectorlabels))
    n4 = Input(0, label="Placed number of this type", validator=Positive(incl_zero=True))
    n4_problem = Input(0, label="Total number of this type", validator=Positive(incl_zero=True))

    # Specify tolerance between connectors
    tol = Input(3, label="Tolerance", validator=Positive(incl_zero=True))

    # Height or thickness of the to be designed bracket
    height = Input(1, validator=Positive(incl_zero=True), label="Thickness of bracket")

    # Allow pop-up
    popup_gui = Input(True, label="Allow pop-up")

    # Connectors empty list
    connectors_list = []

    # Toggle to generate initial placement of connectors
    generate_initial_placement = Input(False, widget=Dropdown([True, False], labels=['True', 'False']))

    # How many different initial placements should be generated and how
    population_size = Input(1)
    item_specialization_iter_proportion = Input(0.5)
    container = Input(Container(np.inf, Polygon([(0, 0), (1, 0), (1, 1), (0, 1)])))
    items = Input(Item(Polygon([(0, 0), (1, 0), (1, 1), (0, 1)]), 1, 0))

    # Generate initial placement of connectors using greedy algorithm

    @Input
    def radius(self):
        if self.bracketshape == "circle":
            radius = 100
        else:
            radius = None
        return radius

    @Input
    def width(self):
        if self.bracketshape == "rectangle":
            width = 100
        else:
            width = None
        return width

    @Input
    def length(self):
        if self.bracketshape == "rectangle":
            length = 100
        else:
            length = None
        return length

    # @Attribute
    # def connectors(self):
    #     if len(self.connectors_list) > 0:
    #         return ManipulateAnything(to_manipulate=self.connectors_list)

    @Attribute
    def initial_placement_problem(self):
        problems, problem_names, manual_solutions = create_knapsack_packing_problem(self.initial_placement_container,
                                                                                    self.initial_placement_items[0])
        return problems, problem_names, manual_solutions

    @Attribute
    def initial_placement(self):
        for i, (problem, problem_name, solution) in enumerate(zip(self.initial_placement_problem[0],
                                                                  self.initial_placement_problem[1],
                                                                  self.initial_placement_problem[2])):
            population = generate_population(problem, self.population_size, self.item_specialization_iter_proportion)

        for i in range(self.population_size):
            max_value = 0
            if population[i].value > max_value:
                max_value = population[i].value
                max_index = i

        # print(population[max_index].placed_items.keys())
        # print(population[max_index].placed_items)
        # print(len(population[max_index].placed_items.keys()))
        cog = [[]]*self.n1
        for i in range(self.n1):
            if i in population[max_index].placed_items.keys():
                # print(population[max_index].placed_items[i])
                x, y = population[max_index].placed_items[i].position
                cog[i] = [x, y, 0]
            else:
                cog[i] = [0, 0, 0]
        return cog

    @Attribute
    def bracket_area(self):
        if self.bracketshape == "rectangle":
            bracket_area = self.width * self.length
        elif self.bracketshape == "circle":
            bracket_area = np.pi * self.radius**2
        elif self.bracketshape == "file":
            bracket_area = self.bracket_from_file.children[0].children[0].children[0].area
        else:
            bracket_area = 0
        return bracket_area

    @Attribute
    def initial_placement_items(self):
        items1, area1 = connector_input_converter(self.type1, self.n1, self.tol, self.df, self.df2)
        items2, area2 = connector_input_converter(self.type2, self.n2, self.tol, self.df, self.df2)
        items3, area3 = connector_input_converter(self.type3, self.n3, self.tol, self.df, self.df2)
        items4, area4 = connector_input_converter(self.type4, self.n4, self.tol, self.df, self.df2)
        if area1 + area2 + area3 + area4 > self.bracket_area:
            msg = "Combined connector area larger than bracket area, impossible " \
                  "to fit all connectors. Try using less or smaller connectors"
            warnings.warn(msg)
            if self.popup_gui:
                generate_warning("Warning: Value changed", msg)
        input = items1 + items2 + items3 + items4
        area = [area1, area2, area3, area4]
        return input, area

    @Attribute
    def optimize_items(self):
        items1, area1 = connector_input_converter(self.type1, self.n1_problem, self.tol, self.df, self.df2)
        items2, area2 = connector_input_converter(self.type2, self.n2_problem, self.tol, self.df, self.df2)
        items3, area3 = connector_input_converter(self.type3, self.n3_problem, self.tol, self.df, self.df2)
        items4, area4 = connector_input_converter(self.type4, self.n4_problem, self.tol, self.df, self.df2)
        if area1 + area2 + area3 + area4 > self.bracket_area:
            msg = "Combined connector area larger than bracket area, impossible " \
                  "to fit all connectors. Try using less or smaller connectors"
            warnings.warn(msg)
            if self.popup_gui:
                generate_warning("Warning: Value changed", msg)
        input = items1 + items2 + items3 + items4
        area = [area1, area2, area3, area4]
        return input, area

    @Attribute
    def initial_placement_container(self):
        if self.bracketshape == "rectangle":
            container = Polygon([(0.0, 0), (self.width, 0.0), (self.width, self.length), (0.0, self.length)])
        if self.bracketshape == "circle":
            container = Circle((0, 0), self.radius)
        if self.bracketshape == 'file':
            points = []
            for i in range(0, len(self.bracket_from_file.children[0].children[0].children[0].edges)):
                points.append((self.bracket_from_file.children[0].children[0].children[0].edges[i].start.x,
                               self.bracket_from_file.children[0].children[0].children[0].edges[i].start.y))
            container = Polygon(points)
        return container

    @Attribute
    def pts_container(self):
        if self.bracketshape == "rectangle":
            pts_container = [(0.0, 0), (self.width, 0.0), (self.width, self.length), (0.0, self.length)]
        if self.bracketshape == "circle":
            pts_container = self.radius
        if self.bracketshape == 'file':
            points = []
            for i in range(0, len(self.bracket_from_file.children[0].children[0].children[0].edges)):
                points.append((self.bracket_from_file.children[0].children[0].children[0].edges[i].start.x,
                               self.bracket_from_file.children[0].children[0].children[0].edges[i].start.y))
            pts_container = points
        return pts_container

    @Attribute
    def optimize_container(self):
        if self.bracketshape == "rectangle":
            container = Polygon([(0.0, 0), (self.width, 0.0), (self.width, self.length), (0.0, self.length)])
        if self.bracketshape == "circle":
            container = Circle((0, 0), self.radius)
        if self.bracketshape == 'file':
            points = []
            for i in range(0, len(self.bracket_from_file.children[0].children[0].children[0].edges)):
                points.append((self.bracket_from_file.children[0].children[0].children[0].edges[i].start.x,
                               self.bracket_from_file.children[0].children[0].children[0].edges[i].start.y))
            container = Polygon(points)
        return container

    @Part
    def connector_part(self):
        return Connector(c_type=self.type1,
                         df=self.df,
                         n=self.n1,
                         cog=self.initial_placement,
                         rotation=[0]*self.n1)

    @Part
    def bracket_box(self):
        return Box(width=self.width,
                   length=self.length,
                   height=self.height,
                   centered=False,
                   hidden=False if self.bracketshape == "rectangle" else True,
                   label="Bracket")

    @Part
    def bracket_cylinder(self):
        return Cylinder(radius=self.radius,
                        height=self.height,
                        centered=False,
                        hidden=False if self.bracketshape == "circle" else True,
                        label="Bracket")

    @Part
    def bracket_from_file(self):
        return STEPReader(filename=self.filename,
                          hidden=False if self.bracketshape == "file" else True,
                          label="Bracket")

    @Part
    def step(self):
        return STEPWriter(trees=self.bracket_test)

    @Part
    def labels(self):
        return TextLabel(text="Bracket",
                         position=self.bracket_box.cog,
                         overlay=True)





if __name__ == '__main__':
    from parapy.gui import display
    bracket_obj = Bracket()
    obj = ManipulateAnything(to_manipulate=bracket_obj,
                             pts_container=bracket_obj.pts_container)
    display([obj])
