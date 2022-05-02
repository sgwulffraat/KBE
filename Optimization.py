import xlsxwriter
from parapy.geom import *
from parapy.core import *
from parapy.core.widgets import Dropdown
from Bracket import Bracket, generate_warning
from working_testing import perform_experiments
from parapy.exchange import *
import sys
sys.path.append('source')

class Optimization(GeomBase):
    """By choosing optimization options the optimization problem is defined. When set to "Inputs",
    the user is working on finalizing input. When set to "KnapsackPacking", the input provided by the
    user is the complete set of connectors that should be placed on a given bracket. """
    optimization_options = ["Inputs", "KnapsackPacking"]
    optimization = Input("Inputs",label="Optimization Setting",widget=Dropdown(optimization_options,labels=["Working on Inputs","Optimize!"]))

    solution_directory = ""
    number_of_different_solutions = Input(1)
    generations = Input(30)
    connector_height = Input(10)

    @Part
    def bracket(self):
        return Bracket()

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
                placed_item_index, placed_items = perform_experiments(self.optimization,self.solution_directory,load_experiments=False,container=self.bracket.optimize_container,items=self.bracket.optimize_items[0],num_experiments = self.number_of_different_solutions)
                placed_items_faces = []
                number_n1 = number_n2 = number_n3 = number_n4 = area_connectors1 = area_connectors2 = area_connectors3 = area_connectors4 = 0


                for i in placed_item_index:
                    placed_item_coor = []
                    for j in range(len(placed_items[i]["x_coor"])):
                        placed_coor = Point(placed_items[i]["x_coor"][j],placed_items[i]["y_coor"][j],0)
                        placed_item_coor.append(placed_coor)
                    placed_items_faces.append(Face(Polygon(placed_item_coor),color="red"))

                    if i in range(self.bracket.n1):
                        number_n1 = number_n1 + 1
                        if number_n1 == 1:
                            row = 0
                        area_connectors1 = area_connectors1 + self.bracket.optimize_items[1][0]/self.bracket.n1
                        worksheet.write(1,0,self.bracket.type1)
                        worksheet.write(1,1,number_n1)
                        worksheet.write(1,2,area_connectors1)
                        connector1.write(row,0,str(placed_item_coor))
                        row = row + 1

                    elif i in range(self.bracket.n1,
                                    self.bracket.n1+self.bracket.n2):
                        number_n2 = number_n2 + 1
                        if number_n2 == 1:
                            row = 0
                        area_connectors2 = area_connectors2 + self.bracket.optimize_items[1][1]/self.bracket.n2
                        worksheet.write(2, 0, self.bracket.type2)
                        worksheet.write(2, 1, number_n2)
                        worksheet.write(2, 2, area_connectors2)
                        connector2.write(row, 0, str(placed_item_coor))
                        row = row + 1

                    elif i in range(self.bracket.n1+self.bracket.n2,
                                    self.bracket.n1 + self.bracket.n2+self.bracket.n3):
                        number_n3 = number_n3 + 1
                        if number_n3 == 1:
                            row = 0
                        area_connectors3 = area_connectors3 + self.bracket.optimize_items[1][2]/self.bracket.n3
                        worksheet.write(3, 0, self.bracket.type3)
                        worksheet.write(3, 1, number_n3)
                        worksheet.write(3, 2, area_connectors3)
                        connector3.write(row, 0, str(placed_item_coor))
                        row = row + 1

                    elif i in range(self.bracket.n1+self.bracket.n2+self.bracket.n3,
                                    self.bracket.n1 + self.bracket.n2+self.bracket.n3+self.bracket.n4):
                        number_n4 = number_n4 + 1
                        if number_n4 == 1:
                            row = 0
                        area_connectors4 = area_connectors4 + self.bracket.optimize_items[1][3]/self.bracket.n4
                        worksheet.write(4, 0, self.bracket.type4)
                        worksheet.write(4, 1, number_n4)
                        worksheet.write(4, 2, area_connectors4)
                        connector4.write(row, 0, str(placed_item_coor))
                        row = row + 1

                area_connectors = area_connectors1 + area_connectors2 + area_connectors3 + area_connectors4
                type1 = f"{number_n1} of {self.bracket.type1} were placed"
                type2 = f"{number_n2} of {self.bracket.type2} were placed"
                type3 = f"{number_n3} of {self.bracket.type3} were placed"
                type4 = f"{number_n4} of {self.bracket.type4} were placed"

                worksheet.write(5, 0, 'Total:')
                worksheet.write(5, 1, number_n1+number_n2+number_n3+number_n4)
                worksheet.write(6, 0, 'Utilized area:')
                worksheet.write(6,1,area_connectors/self.bracket.bracket_area)

                msg = f"""{number_n1} of {self.bracket.type1} were placed, 
{number_n2} of {self.bracket.type2} were placed,
{number_n3} of {self.bracket.type3} were placed, 
{number_n4} of {self.bracket.type4} were placed.
Total available area: {self.bracket.bracket_area} [mm^2],
Area of connectors: {area_connectors} [mm^2],
Area utilization: {area_connectors / self.bracket.bracket_area * 100} %"""
                warnings.warn(msg)
                generate_warning("Optimization complete:", msg)
                workbook.close()
                return placed_items_faces, type1, type2, type3, type4

    @Part
    def connectors(self):
        return ExtrudedSolid(quantify = len(self.optimized[0]),face_in=self.optimized[0][child.index],distance = self.connector_height,direction=(0, 0, 1),color='red')

    @Part
    def step_writer(self):
        return STEPWriter(trees = [self.bracket,self.connectors])






if __name__ == "__main__":
    from parapy.gui import display
    obj = Optimization()

    display(obj)

