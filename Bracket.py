from parapy.geom import GeomBase, Box, Cylinder, translate, rotate90, TextLabel
from parapy.gui.display import get_top_window
from parapy.core import Input, Attribute, Part, warnings, MutableSequence, List, action
from parapy.core.widgets import Dropdown, FilePicker
from parapy.core.validate import Positive
from parapy.exchange import STEPReader
from connector import Connector
from parapy.gui.actions import ViewerSelection
from connector_input_converter import connector_input_converter, read_connector_excel, connector_class_input_converter
from shapely.geometry import Polygon, Point
from source.circle import Circle
from Manipulation2 import ManipulateAnything
import numpy as np
import sys
from source.evolutionary import generate_population
from source.problem_solution import PlacedShape, Solution, Container, Item
from working_testing import create_knapsack_packing_problem
from warnings_and_functions import generate_warning, show, hide, initial_item_placement
sys.path.append('source')


class Bracket(GeomBase):
    # Shape input: rectangle, circle or file
    shapeoptions = ["rectangle", "circle", "file"]

    # Input block bracket generator
    bracketshape = Input("rectangle", label="Choose bracket shape:",
                         widget=Dropdown(shapeoptions, labels=["Rectangular", "Circular",
                                                               "Create from file"]))
    filename = Input(__file__, widget=FilePicker)

    # Height or thickness of the to be designed bracket
    height = Input(3, validator=Positive(incl_zero=True), label="Thickness of bracket")

    # Specify tolerance between connectors
    tol = Input(3, label="Tolerance", validator=Positive(incl_zero=True))

    # Connector input: various abbreviated connector types. See 'Connector details.xsl' for reference.
    connectorlabels, df, df2 = read_connector_excel('Connector details.xlsx', 'Connector details',
                                                    'Cavity specific area')
    connectorlabels = connectorlabels + ["No connector added yet"]

    # Widget section connector type selection
    type1 = Input("MIL/20-A", label="Type Connector (to be added)",
                  widget=Dropdown(connectorlabels))
    n1 = Input(1, label="Number of this type (to be added)", validator=Positive(incl_zero=True))
    n1_problem = Input(1, label="Total number of this type", validator=Positive(incl_zero=True))

    type2 = Input("No connector added yet", label="Type Connector",
                  widget=Dropdown(connectorlabels))
    n2 = Input(0, label="Placed number of this type", validator=Positive(incl_zero=True))
    n2_problem = Input(0, label="Total number of this type", validator=Positive(incl_zero=True))

    type3 = Input("No connector added yet", label="Type Connector",
                  widget=Dropdown(connectorlabels))
    n3 = Input(0, label="Placed number of this type", validator=Positive(incl_zero=True))
    n3_problem = Input(0, label="Total number of this type", validator=Positive(incl_zero=True))

    type4 = Input("No connector added yet", label="Type Connector",
                  widget=Dropdown(connectorlabels))
    n4 = Input(0, label="Placed number of this type", validator=Positive(incl_zero=True))
    n4_problem = Input(0, label="Total number of this type", validator=Positive(incl_zero=True))

    # Connector color
    connector_color = Input([98, 179, 196])

    # Bracket color
    bracket_color = Input([199, 192, 185])

    # Allow pop-up
    popup_gui = Input(True, label="Allow pop-up")

    # Toggle to generate initial placement of connectors
    generate_initial_placement = Input(False, widget=Dropdown([True, False], labels=['True', 'False']))

    # How many different initial placements should be generated and how
    population_size = Input(1)
    initial_solution_generations = Input(100000)
    container = Input(Container(np.inf, Polygon([(0, 0), (1, 0), (1, 1), (0, 1)])))
    items = Input(Item(Polygon([(0, 0), (1, 0), (1, 1), (0, 1)]), 1, 0))

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

    @Attribute
    def valid_file(self):
        valid_file = False
        if self.bracketshape == 'file':
            if self.filename[-3:] == 'stp':
                valid_file = True
            else:
                msg = "Warning: add a valid STEP file to proceed"
                warnings.warn(msg)
                if self.popup_gui:
                    generate_warning("Warning: Invalid file", msg)
        return valid_file

    @action(label="Click to show bracket", button_label="SHOW")
    def show_bracket(self):
        if self.bracketshape == 'file':
            hide(self.bracket_box)
            hide(self.bracket_cylinder)
            if self.valid_file is True:
                self.bracket_from_file.children[0].children[0].children[0].children[0].color = self.bracket_color
                show(self.bracket_from_file.children[0].children[0].children[0].children[0])

        elif self.bracketshape == 'rectangle':
            if self.valid_file is True:
                hide(self.bracket_from_file.children[0].children[0].children[0].children[0])
            hide(self.bracket_cylinder)
            show(self.bracket_box)
        else:
            hide(self.bracket_box)
            if self.valid_file is True:
                hide(self.bracket_from_file.children[0].children[0].children[0].children[0])
            show(self.bracket_cylinder)

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
            population = generate_population(problem, self.population_size,
                                             initial_solution_generations=self.initial_solution_generations)

        for i in range(self.population_size):
            max_value = 0
            if population[i].value > max_value:
                max_value = population[i].value
                max_index = i

        cog = [[]]*(self.n1+self.n2+self.n3+self.n4)
        for i in range(self.n1+self.n2+self.n3+self.n4):
            print(range(self.n1+self.n2+self.n3+self.n4))
            if i in population[max_index].placed_items.keys():
                print(population[max_index].placed_items.keys())
                x, y = population[max_index].placed_items[i].position
                print(x, y)
                cog[i] = [x, y, 0]
            else:
                cog[i] = [self.optimize_container.centroid.x, self.optimize_container.centroid.y, 0]

        print(cog)

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
        if self.n1_problem < self.n1:
            self.n1_problem = self.n1
        if self.n2_problem < self.n2:
            self.n2_problem = self.n2
        if self.n3_problem < self.n3:
            self.n3_problem = self.n3
        if self.n4_problem < self.n4:
            self.n4_problem = self.n4
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
            container = Polygon([(0.0 + 0.5 * self.tol, 0 + 0.5 * self.tol),
                                 (self.width - 0.5 * self.tol, 0.0 + 0.5 * self. tol),
                                 (self.width - 0.5 * self.tol, self.length - 0.5 * self.tol),
                                 (0.0 + 0.5 * self.tol, self.length - 0.5 * self.tol)])
        if self.bracketshape == "circle":
            container = Circle((0, 0), self.radius - self.tol)
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
            pts_container = [self.radius]
        if self.bracketshape == 'file':
            points = []
            for i in range(0, len(self.bracket_from_file.children[0].children[0].children[1].children)):
                points.append((self.bracket_from_file.children[0].children[0].children[1].children[i].start.x,
                               self.bracket_from_file.children[0].children[0].children[1].children[i].start.y))
            pts_container = points
        return pts_container

    @Attribute
    def optimize_container(self):
        if self.bracketshape == "rectangle":
            container = Polygon([(0.0 + 0.5 * self.tol, 0 + 0.5 * self.tol),
                                 (self.width - 0.5 * self.tol, 0.0 + 0.5 * self. tol),
                                 (self.width - 0.5 * self.tol, self.length - 0.5 * self.tol),
                                 (0.0 + 0.5 * self.tol, self.length - 0.5 * self.tol)])
        if self.bracketshape == "circle":
            container = Circle((self.radius, self.radius), self.radius - self.tol)
        if self.bracketshape == 'file':
            points = []
            for i in range(0, len(self.bracket_from_file.children[0].children[0].children[0].edges)):
                points.append((self.bracket_from_file.children[0].children[0].children[0].edges[i].start.x,
                               self.bracket_from_file.children[0].children[0].children[0].edges[i].start.y))
            container = Polygon(points)
        return container

    # Mutable Sequence of placed connectors
    @Part
    def connectors(self):
        return MutableSequence(type=Connector,
                               quantify=0)

    # List with placed types only
    @Attribute
    def type_list(self):
        return List()

    # List with placed types and corresponding numbers and total numbers
    @Attribute
    def conn_list(self):
        return List()

    # Shapely Polygon used for boundary condition check
    @Attribute
    def poly_container(self):
        if len(self.pts_container) > 1:
            pol_container = Polygon(self.pts_container)
        else:
            pol_container = Point(self.radius, self.radius).buffer(self.radius)
        return pol_container

    # Function to update placed types and corresponding numbers in GUI
    def update_type_list(self):
        if len(self.type_list) == 1:
            self.type2 = self.conn_list[0][0]
            self.n2 = self.conn_list[0][1]
            self.n2_problem = self.conn_list[0][2]
            self.type3 = "No connector added yet"
            self.n3 = 0
            self.n3_problem = 0
            self.type4 = "No connector added yet"
            self.n4 = 0
            self.n4_problem = 0
        else:
            self.type2 = self.conn_list[-1][0]
            self.n2 = self.conn_list[-1][1]
            self.n2_problem = self.conn_list[-1][2]
        if len(self.type_list) == 2:
            self.type3 = self.conn_list[0][0]
            self.n3 = self.conn_list[0][1]
            self.n3_problem = self.conn_list[0][2]
            self.type4 = "No connector added yet"
            self.n4 = 0
            self.n4_problem = 0
        if len(self.type_list) == 3:
            self.type3 = self.conn_list[-2][0]
            self.n3 = self.conn_list[-2][1]
            self.n3_problem = self.conn_list[-2][2]
            self.type4 = self.conn_list[0][0]
            self.n4 = self.conn_list[0][1]
            self.n4_problem = self.conn_list[0][2]

    # Button to append a connector of type 1
    @action(label='Click to add new connector', button_label='ADD')
    def append_connector(self):
        present = False
        if self.type1 in self.type_list:
            present = True
        if present is False and len(self.type_list) >= 4:
            msg = "Warning: You are adding a fifth connector type"
            warnings.warn(msg)
            if self.popup_gui:
                generate_warning("Warning: Invalid action", msg)
            raise Exception(msg)

        connector = Connector(c_type=self.type1,
                              df=self.df,
                              n=self.n1,
                              bracket_height=self.height,
                              bracket=self.find_child_by_label("Bracket"),
                              lastplaced_item=self.connectors[-1] if len(self.connectors) > 0 else "None",
                              poly_container=self.poly_container,
                              tol=self.tol,
                              label="Connectors: " + self.type1,
                              color=self.connector_color,
                              cog=initial_item_placement(self=self,
                                                         bracket=self.find_child_by_label("Bracket"),
                                                         lastplaced_item=self.connectors[-1] if len(self.connectors) > 0
                                                         else "None",
                                                         half_width=connector_class_input_converter(self.type1,
                                                                                                    self.df)[0][0]/2,
                                                         half_length=connector_class_input_converter(self.type1,
                                                                                                     self.df)[0][1]/2,
                                                         step=0.5, n=self.n1, tol=self.tol))
        self.connectors.append(connector)
        if self.type1 in self.type_list:
            indx = self.type_list.index(self.type1)
            self.conn_list[indx][1] = self.conn_list[indx][1] + self.n1
            self.conn_list[indx][2] = self.conn_list[indx][2] + self.n1_problem
        else:
            self.type_list.append(self.type1)
            self.conn_list.append([self.type1, self.n1, self.n1_problem])
        self.update_type_list()

        for i in range(0, self.n1):
            if connector.shape == "rectangle" or connector.shape == "square":
                show(connector.rectangle_connector[i])
            if connector.shape == "circle":
                show(connector.circular_connector[i])

    # Button to remove last addition
    @action(label='Click to remove last addition',button_label='DELETE LAST')
    def pop_last(self):
        pop_list = self.connectors[-1].find_children(
            fn=lambda conn: conn.__class__ == Box or conn.__class__ == Cylinder)
        hide(pop_list)
        index = self.type_list.index(pop_list[0].label)
        if self.conn_list[index][1] - len(pop_list) == 0:
            del self.type_list[index]
            del self.conn_list[index]
            print("entire type:", pop_list[0].label, "deleted")
        else:
            self.conn_list[index][1] = self.conn_list[index][1] - len(pop_list)
            self.conn_list[index][2] = self.conn_list[index][2] - len(pop_list)
            print("number of type:", pop_list[0].label, "reduced to", self.conn_list[index][1])
        self.update_type_list()
        self.connectors.pop()

    @action(label="Click to remove selection", button_label='DELETE SELECTION')
    def remove_connectors(self):
        # Enter selection mode for the user to select connectors in the viewer
        main_window = get_top_window()
        context = ViewerSelection(main_window, multiple=True)
        if context.start():
            for slctd_obj in context.selected:
                prnt = slctd_obj.parent.index
                if slctd_obj.__class__ == Box:
                    # Prevent user from removing bracket object
                    if slctd_obj == self.bracket_box \
                            or slctd_obj == self.bracket_cylinder \
                            or slctd_obj == self.bracket_from_file:
                        msg = "Warning: Bracket can not be deleted"
                        warnings.warn(msg)
                        if self.popup_gui:
                            generate_warning("Warning: Invalid action", msg)
                    else:
                        # Hide the removed box object from the GUI and from parent lists
                        removed_obj = self.connectors[prnt].rectangle_connector[slctd_obj.index]
                        hide(removed_obj)
                        index = self.type_list.index(removed_obj.label)
                        if self.conn_list[index][1] - 1 == 0:
                            del self.type_list[index]
                            del self.conn_list[index]
                            print("entire type:", removed_obj.label, "deleted")
                        else:
                            self.conn_list[index][1] = self.conn_list[index][1] - 1
                            self.conn_list[index][2] = self.conn_list[index][2] - 1
                            print("number of type:", removed_obj.label, "reduced to", self.conn_list[index][1])
                        self.update_type_list()
                        self.connectors[prnt].rectangle_connector.remove(slctd_obj)
                    if self.connectors[prnt].rectangle_connector.quantify == 0:
                        self.connectors.remove(self.connectors[prnt])
                elif slctd_obj.__class__ == Cylinder:
                    # Hide the removed cylinder object from the GUI and from parent lists
                    removed_obj = self.connectors[prnt].circular_connector[slctd_obj.index]
                    hide(removed_obj)
                    index = self.type_list.index(removed_obj.label)
                    if self.conn_list[index][1] - 1 == 0:
                        del self.type_list[index]
                        del self.conn_list[index]
                        print("entire type:", removed_obj.label, "removed")
                    else:
                        self.conn_list[index][1] = self.conn_list[index][1] - 1
                        self.conn_list[index][2] = self.conn_list[index][2] - 1
                        print("number of type:", removed_obj.label, "reduced to", self.conn_list[index][1])
                    self.update_type_list()
                    self.connectors[prnt].circular_connector.remove(slctd_obj)
                    if self.connectors[prnt].circular_connector.quantify == 0:
                        self.connectors.remove(self.connectors[prnt])

    # @Part
    # def connector_part1(self):
    #     return Connector(c_type=self.type1,
    #                      df=self.df,
    #                      n=self.n1,
    #                      bracket_height=self.height,
    #                      cog=self.initial_placement[0:self.n1],
    #                      rotation=[0]*self.n1,
    #                      color=self.connector_color,
    #                      label="Connector type 1")
    #
    # @Part
    # def connector_part2(self):
    #     return Connector(c_type=self.type2,
    #                      df=self.df,
    #                      n=self.n2,
    #                      bracket_height=self.height,
    #                      cog=self.initial_placement[self.n1:self.n1+self.n2],
    #                      rotation=[0] * self.n2,
    #                      color=self.connector_color,
    #                      label="Connector type 2")
    #
    # @Part
    # def connector_part3(self):
    #     return Connector(c_type=self.type3,
    #                      df=self.df,
    #                      n=self.n3,
    #                      bracket_height=self.height,
    #                      cog=self.initial_placement[self.n1+self.n2:self.n1+self.n2+self.n3],
    #                      rotation=[0] * self.n3,
    #                      color=self.connector_color,
    #                      label="Connector type 3")
    #
    # @Part
    # def connector_part4(self):
    #     return Connector(c_type=self.type4,
    #                      df=self.df,
    #                      n=self.n4,
    #                      bracket_height=self.height,
    #                      cog=self.initial_placement[self.n1+self.n2+self.n3:self.n1+self.n2+self.n3+self.n4],
    #                      rotation=[0] * self.n4,
    #                      color=self.connector_color,
    #                      label="Connector type 4")

    @Part
    def bracket_box(self):
        return Box(width=self.width,
                   length=self.length,
                   height=self.height,
                   centered=False,
                   hidden=False if self.bracketshape == "rectangle" else True,
                   label="Bracket",
                   color=[199, 192, 185])

    @Part
    def bracket_cylinder(self):
        return Cylinder(radius=self.radius,
                        height=self.height,
                        position=translate(self.position, 'x', self.radius, 'y', self.radius),
                        centered=False,
                        hidden=False if self.bracketshape == "circle" else True,
                        label="Bracket",
                        color=[199, 192, 185])

    @Part
    def bracket_from_file(self):
        return STEPReader(filename=self.filename,
                          hidden=False if self.bracketshape == "file" else True,
                          label="Bracket",
                          color=[199, 192, 185])

    @Part
    def bracket_label(self):
        return TextLabel(text="Bracket",
                         position=translate(rotate90(self.bracket_box.position, rotation_axis='z'),
                                            'x', 1,
                                            'y', 1,
                                            'z', self.height),
                         overlay=True)

    # @Attribute(in_tree=True)
    # def labels_connectors(self):
    #     labels = []
    #     for i in self.connectors:
    #         labels.append(TextLabel(text=self.type1,
    #                                 position=Position(Point(i[0], i[1], self.height)),
    #                                 overlay=True))
    #     return labels


if __name__ == '__main__':
    from parapy.gui import display
    bracket_obj = Bracket()
    obj = ManipulateAnything(to_manipulate=bracket_obj,
                             connector_color=bracket_obj.connector_color)
    display([obj])
