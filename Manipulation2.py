from parapy.core import Base, Input, on_event, Attribute
from parapy.geom import Compound, Position, Vector, Circle, Box, Cylinder
from parapy.core.validate import warnings
from parapy.geom import Polygon as para_Polygon
from parapy.geom import Point as para_Point
from parapy.gui.events import EVT_RIGHT_CLICK_OBJECT
from parapy.gui.manipulation import EndEvent, Gizmo, Manipulation, MotionEvent, Translation, Rotation
from shapely.geometry import Polygon, Point
import numpy as np
from warnings_and_functions import generate_warning, show, hide
from parapy.gui.display import refresh_top_window


class ManipulateAnything(Base):
    label = Input('right-click the connector(s) to manipulate selected')
    to_manipulate = Input(in_tree=True, label='Design bracket here')
    rotation_increment = Input(45)
    pts_container = Input()
    slctd_conn = Input('No connector selected yet')
    connector_color = Input([83, 120, 128])
    # Allow pop up
    popup_gui = Input(True, label="Allow pop-up")

    # Shapely polygon of container
    @Attribute
    def pol_container(self):
        if len(self.to_manipulate.pts_container) > 1:
            pol_container = Polygon(self.pts_container)
        else:
            pol_container = Point(self.to_manipulate.radius, self.to_manipulate.radius).buffer(self.to_manipulate.radius)
        return pol_container

    # Parapy GUI boundary polygon or circle
    @Attribute
    def tol_bounds(self):
        bounds = []
        box_list = self.to_manipulate.connectors.find_children(fn=lambda conn: conn.__class__ == Box)
        cylinder_list = self.to_manipulate.connectors.find_children(fn=lambda conn: conn.__class__ == Cylinder)
        if type(self.slctd_conn) is not str:
            for cylinder in cylinder_list:
                if cylinder.id != self.slctd_conn.id:
                    stationary_cylinder = cylinder
                    bounds.append(Circle(radius=stationary_cylinder.radius+self.to_manipulate.tol,
                                         position=stationary_cylinder.position,
                                         color='red', transparency=.5))
            for box in box_list:
                if box.id != self.slctd_conn.id:
                    stationary_connector = box
                    bound_pts = self.pol_pts(stationary_connector)
                    bound_para_points = []
                    for j in range(0, 4):
                        bound_para_points.append(para_Point(bound_pts[j][0],
                                                            bound_pts[j][1],
                                                            self.to_manipulate.height))
                    bounds.append(para_Polygon(bound_para_points, color='red', transparency=.5))
        return bounds

    # List of stationary shapely polygons
    @Attribute
    def pol_list(self):
        pol_list = []
        box_list = self.to_manipulate.connectors.find_children(fn=lambda conn: conn.__class__ == Box)
        cylinder_list = self.to_manipulate.connectors.find_children(fn=lambda conn: conn.__class__ == Cylinder)
        if type(self.slctd_conn) is not str:
            for cylinder in cylinder_list:
                if cylinder.id != self.slctd_conn.id:
                    stationary_cylinder = cylinder
                    polygon = Point((stationary_cylinder.cog[0]),
                                    (stationary_cylinder.cog[1])).buffer(stationary_cylinder.radius + self.to_manipulate.tol)
                    pol_list.append(polygon)
            for box in box_list:
                if box.id != self.slctd_conn.id:
                    stationary_connector = box
                    polygon = Polygon(self.pol_pts(stationary_connector))
                    pol_list.append(polygon)
        return pol_list

    # Function to get edge points of any rectangular connector
    def pol_pts(self, stationary_connector):
        pts = [(stationary_connector.cog[0] + ((stationary_connector.width/2 + self.to_manipulate.tol)
                                               * (stationary_connector.orientation.x[0])
                                               - (stationary_connector.length/2 + self.to_manipulate.tol)
                                               * (stationary_connector.orientation.x[1])),
                stationary_connector.cog[1] + ((stationary_connector.width/2 + self.to_manipulate.tol)
                                               * -(stationary_connector.orientation.y[0])
                                               + (stationary_connector.length/2 + self.to_manipulate.tol)
                                               * (stationary_connector.orientation.y[1]))),
               (stationary_connector.cog[0] + ((stationary_connector.width/2 + self.to_manipulate.tol)
                                               * (stationary_connector.orientation.x[0])
                                               + (stationary_connector.length/2 + self.to_manipulate.tol)
                                               * (stationary_connector.orientation.x[1])),
                stationary_connector.cog[1] - ((stationary_connector.length/2 + self.to_manipulate.tol)
                                               * (stationary_connector.orientation.y[1])
                                               + (stationary_connector.width/2 + self.to_manipulate.tol)
                                               * (stationary_connector.orientation.y[0]))),
               (stationary_connector.cog[0] - ((stationary_connector.width/2 + self.to_manipulate.tol)
                                               * (stationary_connector.orientation.x[0])
                                               - (stationary_connector.length/2 + self.to_manipulate.tol)
                                               * (stationary_connector.orientation.x[1])),
                stationary_connector.cog[1] - ((stationary_connector.width/2 + self.to_manipulate.tol)
                                               * -(stationary_connector.orientation.y[0])
                                               + (stationary_connector.length/2 + self.to_manipulate.tol)
                                               * (stationary_connector.orientation.y[1]))),
               (stationary_connector.cog[0] - ((stationary_connector.width/2 + self.to_manipulate.tol)
                                               * (stationary_connector.orientation.x[0])
                                               + (stationary_connector.length/2 + self.to_manipulate.tol)
                                               * (stationary_connector.orientation.x[1])),
                stationary_connector.cog[1] + ((stationary_connector.width/2 + self.to_manipulate.tol)
                                               * (stationary_connector.orientation.y[0])
                                               + (stationary_connector.length/2 + self.to_manipulate.tol)
                                               * (stationary_connector.orientation.y[1])))
               ]
        return pts

    @on_event(EVT_RIGHT_CLICK_OBJECT)
    def on_click(self, evt):
        if evt.selected[0] == self.to_manipulate.bracket_box \
                or evt.selected[0] == self.to_manipulate.bracket_cylinder \
                or evt.selected[0] == self.to_manipulate.bracket_from_file:
            return print("Bracket is not manipulable")
        elif evt.multiple:
            return print("Simultaneously moving multiple connectors is not yet allowed. "
                         "Please select one connector to manipulate.")
        else:
            self.start_manipulation_one(evt.selected[0], evt.source)
            self.slctd_conn = evt.selected[0]
            show(self.tol_bounds)

    # Veto connector placement outside of bracket domain and change color depending on overlap conditions
    def _on_motion(self, evt: MotionEvent):
        current_position = evt.current_position
        pol_connector = self._pol_connector_with_tol(current_position)
        pol_connector_no_tol = self._pol_connector_no_tol(current_position)
        if self.pol_container.contains(pol_connector) is False:
            evt.Veto()
        if len(self.pol_list) != 0:
            cond = []
            for i in range(0, len(self.pol_list)):
                cond.append(pol_connector_no_tol.overlaps(self.pol_list[i]))
            if any(cond):
                self.slctd_conn.color = 'red'
            else:
                self.slctd_conn.color = 'green'
            refresh_top_window()
        else:
            self.slctd_conn.color = 'green'

    # Function to get shapely polygon of selected connector with tolerances applied (used for container boundary check)
    def _pol_connector_with_tol(self, position):
        if len(self.slctd_conn.faces) == 3:
            pol_connector = Point(position.x, position.y).buffer(self.slctd_conn.radius + self.to_manipulate.tol)
        elif len(self.slctd_conn.faces) == 6:
            pol_connector = Polygon([(position.x + ((self.slctd_conn.width/2 + self.to_manipulate.tol)
                                                    * (position.orientation.x[0])
                                                    - (self.slctd_conn.length/2 + self.to_manipulate.tol)
                                                    * (position.orientation.x[1])),
                                      position.y + ((self.slctd_conn.width/2 + self.to_manipulate.tol)
                                                    * -(position.orientation.y[0])
                                                    + (self.slctd_conn.length/2 + self.to_manipulate.tol)
                                                    * (position.orientation.y[1]))),
                                     (position.x + ((self.slctd_conn.width/2 + self.to_manipulate.tol)
                                                    * (position.orientation.x[0])
                                                    + (self.slctd_conn.length/2 + self.to_manipulate.tol)
                                                    * (position.orientation.x[1])),
                                      position.y - ((self.slctd_conn.length/2 + self.to_manipulate.tol)
                                                    * (position.orientation.y[1])
                                                    + (self.slctd_conn.width/2 + self.to_manipulate.tol)
                                                    * (position.orientation.y[0]))),
                                     (position.x - ((self.slctd_conn.width/2 + self.to_manipulate.tol)
                                                    * (position.orientation.x[0])
                                                    - (self.slctd_conn.length/2 + self.to_manipulate.tol)
                                                    * (position.orientation.x[1])),
                                      position.y - ((self.slctd_conn.width/2 + self.to_manipulate.tol)
                                                    * -(position.orientation.y[0])
                                                    + (self.slctd_conn.length/2 + self.to_manipulate.tol)
                                                    * (position.orientation.y[1]))),
                                     (position.x - ((self.slctd_conn.width/2 + self.to_manipulate.tol)
                                                    * (position.orientation.x[0])
                                                    + (self.slctd_conn.length/2 + self.to_manipulate.tol)
                                                    * (position.orientation.x[1])),
                                      position.y + ((self.slctd_conn.width/2 + self.to_manipulate.tol)
                                                    * (position.orientation.y[0])
                                                    + (self.slctd_conn.length/2 + self.to_manipulate.tol)
                                                    * (position.orientation.y[1])))
                                     ])
        else:
            print("No valid connector found")
        return pol_connector

    # Function to get shapely polygon without tolerances applied (used for overlap with stationary connectors)
    def _pol_connector_no_tol(self, position):
        if len(self.slctd_conn.faces) == 3:
            pol_connector = Point(position.x, position.y).buffer(self.slctd_conn.radius)
        elif len(self.slctd_conn.faces) == 6:
            pol_connector = Polygon([(position.x + ((self.slctd_conn.width/2)
                                                    * (position.orientation.x[0])
                                                    - (self.slctd_conn.length/2)
                                                    * (position.orientation.x[1])),
                                      position.y + ((self.slctd_conn.width/2)
                                                    * -(position.orientation.y[0])
                                                    + (self.slctd_conn.length/2)
                                                    * (position.orientation.y[1]))),
                                     (position.x + ((self.slctd_conn.width/2)
                                                    * (position.orientation.x[0])
                                                    + (self.slctd_conn.length/2)
                                                    * (position.orientation.x[1])),
                                      position.y - ((self.slctd_conn.length/2)
                                                    * (position.orientation.y[1])
                                                    + (self.slctd_conn.width/2)
                                                    * (position.orientation.y[0]))),
                                     (position.x - ((self.slctd_conn.width/2)
                                                    * (position.orientation.x[0])
                                                    - (self.slctd_conn.length/2)
                                                    * (position.orientation.x[1])),
                                      position.y - ((self.slctd_conn.width/2)
                                                    * -(position.orientation.y[0])
                                                    + (self.slctd_conn.length/2)
                                                    * (position.orientation.y[1]))),
                                     (position.x - ((self.slctd_conn.width/2)
                                                    * (position.orientation.x[0])
                                                    + (self.slctd_conn.length/2)
                                                    * (position.orientation.x[1])),
                                      position.y + ((self.slctd_conn.width/2)
                                                    * (position.orientation.y[0])
                                                    + (self.slctd_conn.length/2)
                                                    * (position.orientation.y[1])))
                                     ])
        else:
            print("No valid connector found")
        return pol_connector

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
        current_position = evt.current_position
        pol_connector = self._pol_connector_no_tol(current_position)
        if len(self.pol_list) != 0:
            cond = []
            for i in range(0, len(self.pol_list)):
                cond.append(pol_connector.overlaps(self.pol_list[i]))
            if any(cond):
                msg = "The given position does not satisfy overlap or tolerance conditions. " \
                      "Try moving it further from other connectors"
                warnings.warn(msg)
                if self.popup_gui:
                    generate_warning("Warning: Position not valid", msg)
                raise Exception(msg)
            else:
                self.slctd_conn.color = self.connector_color
                obj.position = evt.transformation.apply(obj.position)
                self.position = evt.current_position
                hide(self.tol_bounds)
        else:
            self.slctd_conn.color = self.connector_color
            obj.position = evt.transformation.apply(obj.position)
            self.position = evt.current_position
            hide(self.tol_bounds)

