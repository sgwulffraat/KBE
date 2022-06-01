from parapy.core import Attribute
from parapy.geom import Box
from parapy.gui import Manipulable
from parapy.gui.manipulation import EndEvent, MotionEvent
from connector import Connector
from connector_input_converter import read_connector_excel

connectorlabels, df, df2 = read_connector_excel('Connector details.xlsx', 'Connector details',
                                                'Cavity specific area')

class PlaneBoundCube(Connector, Manipulable):
    label = 'right-click me in the viewer to start manipulating'
    centered = True

    @Attribute(in_tree=True)
    def boundary(self):
        edges = Box(400, 400, 20, centered=True, color='blue', transparency=.6).edges
        for e in edges:
            e.color = 'red'
        return edges

    def on_motion(self, evt: MotionEvent):
        current_position = evt.current_position
        if -200 > current_position.y or current_position.y > 200:
            evt.Veto()
        if -200 > current_position.x or current_position.x > 200:
            evt.Veto()
        if -10 > current_position.z or current_position.z > 10:
            evt.Veto()

    def on_submit(self, evt: EndEvent):
        self.position = evt.current_position


if __name__ == '__main__':
    from parapy.gui import display

    obj2 = PlaneBoundCube(c_type="MIL/20-A", tol=3, df=df)
    display(obj2)