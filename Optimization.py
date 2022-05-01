from parapy.geom import *
from parapy.core import *
from parapy.core.widgets import Dropdown
from Bracket import Bracket, generate_warning
from working_testing import perform_experiments

class Optimization(GeomBase):
    """By choosing optimization options the optimization problem is defined. When set to "still completing input",
    the user is working on finalizing input. When set to "Optimize for fully defined input", the input provided by the
    user is the complete set of connectors that should be placed on a given bracket. When set to "Optimize for partially
    defined input", the input provided by the user is a set of connectors that must be placed on the bracket, however if
    all of those have been fit, the extra space is filled with more connectors while maximizing contact per area. When
    set to "Optimize for contact per area", no connectors that must be placed are specified and the program solved for
    maximum contact per area using any connector type."""
    optimization_options = ["Still completing input", "KnapsackPacking"]
    optimization = Input("KnapsackPacking",label="Optimization Setting",widget=Dropdown(optimization_options,labels=["Working on Inputs","Optimize!"]))

    solution_directory = "../Output/Problems/CustomKnapsackPacking/Test/"
    number_of_different_solutions = Input(1)
    generations = Input(30)

    @Part
    def to_be_optimized(self):
        return Bracket()

    @Attribute
    def optimized(self):
            if self.optimization == "KnapsackPacking":
                placed_item_index, placed_items = perform_experiments(self.optimization,self.solution_directory,load_experiments=False,container=self.to_be_optimized.optimize_container,items=self.to_be_optimized.optimize_items[0],num_experiments = self.number_of_different_solutions)
                placed_items_faces = []
                number_n1 = number_n2 = number_n3 = number_n4 = area_connectors = 0

                for i in range(len(self.to_be_optimized.connectorlabels)):
                    setattr(self,self.to_be_optimized.connectorlabels[i],f"0 of {self.to_be_optimized.connectorlabels[i]} were placed")

                for i in placed_item_index:
                    placed_item_coor = []
                    for j in range(len(placed_items[i]["x_coor"])):
                        placed_coor = Point(placed_items[i]["x_coor"][j],placed_items[i]["y_coor"][j],0)
                        placed_item_coor.append(placed_coor)
                    placed_items_faces.append(Face(Polygon(placed_item_coor),color="red"))
                    #annotations.append(TextLabel(f"Connector type: {self.to_be_optimized.}")) #Use COG of faces for position of TextLabel

                    if i in range(self.to_be_optimized.n1):
                        number_n1 = number_n1 + 1
                        area_connectors = area_connectors + self.to_be_optimized.optimize_items[1][0]
                    elif i in range(self.to_be_optimized.n1,
                                    self.to_be_optimized.n1+self.to_be_optimized.n2):
                        number_n2 = number_n2 + 1
                        area_connectors = area_connectors + self.to_be_optimized.optimize_items[1][1]
                    elif i in range(self.to_be_optimized.n1+self.to_be_optimized.n2,
                                    self.to_be_optimized.n1 + self.to_be_optimized.n2+self.to_be_optimized.n3):
                        number_n3 = number_n3 + 1
                        area_connectors = area_connectors + self.to_be_optimized.optimize_items[1][2]
                    elif i in range(self.to_be_optimized.n1+self.to_be_optimized.n2+self.to_be_optimized.n3,
                                    self.to_be_optimized.n1 + self.to_be_optimized.n2+self.to_be_optimized.n3+self.to_be_optimized.n4):
                        number_n4 = number_n4 + 1
                        area_connectors = area_connectors + self.to_be_optimized.optimize_items[1][3]

                print(area_connectors)
                type1 = f"{number_n1} of {self.to_be_optimized.type1} were placed"
                type2 = f"{number_n2} of {self.to_be_optimized.type2} were placed"
                type3 = f"{number_n3} of {self.to_be_optimized.type3} were placed"
                type4 = f"{number_n4} of {self.to_be_optimized.type4} were placed"

                msg = f"""{number_n1} of {self.to_be_optimized.type1} were placed, 
{number_n2} of {self.to_be_optimized.type2} were placed,
{number_n3} of {self.to_be_optimized.type3} were placed, 
{number_n4} of {self.to_be_optimized.type4} were placed.
Total available area: {self.to_be_optimized.bracket_area} [mm^2],
Area of connectors: {area_connectors} [mm^2],
Area utilization: {area_connectors / self.to_be_optimized.bracket_area * 100} %"""
                warnings.warn(msg)
                generate_warning("Optimization complete:", msg)

                return placed_items_faces, type1, type2, type3, type4


if __name__ == "__main__":
    from parapy.gui import display
    obj = Optimization()

    display(obj)

