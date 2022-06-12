from parapy.core import Base, Input, on_event, Attribute
from parapy.geom import Compound, Position, Box, Vector
from parapy.geom import Polygon as para_Polygon
from parapy.gui.events import EVT_RIGHT_CLICK_OBJECT
from parapy.gui.manipulation import EndEvent, Gizmo, Manipulation, MotionEvent, Translation, Rotation
from shapely.geometry import Polygon, Point
import numpy as np


class ManipulateAnything(Base):
    label = Input('right-click the connector(s) to manipulate selected')
    to_manipulate = Input(in_tree=True)
    rotation_increment = Input(45)
    pts_container = Input()
    slctd_conn = Input('no connector selected yet')

    # @Attribute(in_tree=True)
    # def boundary(self):
    #     edges = Box(400, 400, 200, centered=True, color='blue', transparency=.5).edges
    #     for e in edges:
    #         e.color = 'red'
    #     return edges

    @Attribute
    def pol_container(self):
        if len(self.to_manipulate.pts_container) > 0:
            pol_container = Polygon(self.pts_container)
        else:
            pol_container = Point(0, 0).buffer(self.pts_container)
        return pol_container

    @on_event(EVT_RIGHT_CLICK_OBJECT)
    def on_click(self, evt):
        if evt.selected[0] == self.to_manipulate.bracket_box \
                or evt.selected[0] == self.to_manipulate.bracket_cylinder \
                or evt.selected[0] == self.to_manipulate.bracket_from_file:
            return print("Bracket is not manipulable")
        elif evt.multiple:
            self.start_manipulation_many(evt.selected, evt.source)
        else:
            self.start_manipulation_one(evt.selected[0], evt.source)
            self.slctd_conn = evt.selected[0]

    # Veto connector placement outside of bracket domain
    def _on_motion(self, evt: MotionEvent):
        current_position = evt.current_position
        print(evt.current_position.orientation.y, evt.current_position.orientation.x)
        if len(self.slctd_conn.faces) == 3:
            pol_connector = Point(current_position.x, current_position.y).buffer(self.slctd_conn.radius)
            if self.pol_container.contains(pol_connector) is False:
                evt.Veto()
        elif len(self.slctd_conn.faces) == 6:
            pol_connector = Polygon([(current_position.x + ((self.slctd_conn.width/2 + self.to_manipulate.tol)
                                                            * (current_position.orientation.x[0])
                                                            - (self.slctd_conn.length/2 + self.to_manipulate.tol)
                                                            * (current_position.orientation.x[1])),
                                      current_position.y + ((self.slctd_conn.width/2 + self.to_manipulate.tol)
                                                            * -(current_position.orientation.y[0])
                                                            + (self.slctd_conn.length/2 + self.to_manipulate.tol)
                                                            * (current_position.orientation.y[1]))),
                                     (current_position.x + ((self.slctd_conn.width/2 + self.to_manipulate.tol)
                                                            * (current_position.orientation.x[0])
                                                            + (self.slctd_conn.length/2 + self.to_manipulate.tol)
                                                            * (current_position.orientation.x[1])),
                                      current_position.y - ((self.slctd_conn.length/2 + self.to_manipulate.tol)
                                                            * (current_position.orientation.y[1])
                                                            + (self.slctd_conn.width/2 + self.to_manipulate.tol)
                                                            * (current_position.orientation.y[0]))),
                                     (current_position.x - ((self.slctd_conn.width/2 + self.to_manipulate.tol)
                                                            * (current_position.orientation.x[0])
                                                            - (self.slctd_conn.length/2 + self.to_manipulate.tol)
                                                            * (current_position.orientation.x[1])),
                                      current_position.y - ((self.slctd_conn.width/2 + self.to_manipulate.tol)
                                                            * -(current_position.orientation.y[0])
                                                            + (self.slctd_conn.length/2 + self.to_manipulate.tol)
                                                            * (current_position.orientation.y[1]))),
                                     (current_position.x - ((self.slctd_conn.width/2 + self.to_manipulate.tol)
                                                            * (current_position.orientation.x[0])
                                                            + (self.slctd_conn.length/2 + self.to_manipulate.tol)
                                                            * (current_position.orientation.x[1])),
                                      current_position.y + ((self.slctd_conn.width/2 + self.to_manipulate.tol)
                                                            * (current_position.orientation.y[0])
                                                            + (self.slctd_conn.length/2 + self.to_manipulate.tol)
                                                            * (current_position.orientation.y[1])))
                                     ])
            if self.pol_container.contains(pol_connector) is False:
                evt.Veto()

    def start_manipulation_one(self, obj, viewer):
        def on_submit(evt: EndEvent):
            self._on_submit(evt, obj)

        return self._start_manipulation(obj, on_submit, self._on_motion, viewer)

    def are_orientations_aligned(self, orientations):
        ori, *oris = orientations
        for _ori in oris:
            if not _ori.is_almost_equal(ori):
                return False
        return True

    def start_manipulation_many(self, objs, viewer):
        if self.are_orientations_aligned((o.orientation for o in objs)):
            basis_pos = objs[0].position
        else:
            basis_pos = Position()

        obj = Compound(
            objs,
            position=basis_pos.replace(
                location=objs[0].position.midpoint(
                    objs[-1].position)))

        def on_submit(evt: EndEvent):
            for obj in objs:
                self._on_submit(evt, obj)

        return self._start_manipulation(obj, on_submit, self._on_motion, viewer)

    def _start_manipulation(self, obj, on_submit, on_motion, viewer):
        gizmo = Gizmo(size=20, position=obj.position, modes=[Translation(axis=Vector(1, 0, 0)),
                                                             Translation(axis=Vector(0, 1, 0)),
                                                             Rotation(increment=self.rotation_increment*np.pi/180,
                                                                      normal=Vector(0, 0, 1))])
        obj = Manipulation(obj=obj,
                           viewer=viewer,
                           on_submit=on_submit,
                           on_motion=on_motion,
                           ghost=obj,
                           gizmo=gizmo, )
        obj.start()

    def _on_submit(self, evt: EndEvent, obj):
        obj.position = evt.transformation.apply(obj.position)
        self.position = evt.current_position

if __name__ == '__main__':
    from parapy.geom import Cube
    from parapy.gui import display
