from parapy.core import Base, Input, on_event, Attribute
from parapy.geom import Compound, Position, Vector, RectangularSurface
from parapy.core.validate import warnings
from parapy.geom import Polygon as para_Polygon
from parapy.geom import Point as para_Point
from parapy.gui.events import EVT_RIGHT_CLICK_OBJECT
from parapy.gui.manipulation import EndEvent, Gizmo, Manipulation, MotionEvent, Translation, Rotation
from shapely.geometry import Polygon, Point
import numpy as np
from warning_pop_up import generate_warning
from parapy.gui.display import refresh_top_window



class ManipulateAnything(Base):
    label = Input('right-click the connector(s) to manipulate selected')
    to_manipulate = Input(in_tree=True, label='Design bracket here')
    rotation_increment = Input(45)
    pts_container = Input()

    slctd_conn = Input('No connector selected yet')
    # Allow pop up
    popup_gui = Input(True, label="Allow pop-up")

    @Attribute(in_tree=True)
    def tol_boundaries(self):
        bounds = []
        if len(self.bound_list) != 0:
            for i in self.bound_list:
                bounds.append(para_Polygon(i, color='red', transparency=.5))
        return bounds

    @Attribute
    def pol_container(self):
        if len(self.to_manipulate.pts_container) > 0:
            pol_container = Polygon(self.pts_container)
        else:
            pol_container = Point(0, 0).buffer(self.pts_container)
        return pol_container

    @Attribute
    def bound_list(self):
        bound_list = []
        for i in range(0, len(self.to_manipulate.connector_part1.cog)):
            if type(self.slctd_conn) is not str:
                if self.to_manipulate.connector_part1.shape == 'square':
                    if self.to_manipulate.connector_part1.square_connector[i].id != self.slctd_conn.id:
                        stationary_connector = self.to_manipulate.connector_part1.square_connector[i]
                        bound_pts = self.pol_pts(stationary_connector)
                        bound_para_points = []
                        for j in range(0, 4):
                            bound_para_points.append(para_Point(bound_pts[j][0],
                                                                bound_pts[j][1],
                                                                self.to_manipulate.height))
                        bound_list.append(bound_para_points)
            # if self.to_manipulate.connector_part1.shape == 'circle':
            #     ids.append(self.to_manipulate.connector_part1.circular_connector[i].id)
            # if self.to_manipulate.connector_part1.shape == 'rectangle':
            #     ids.append(self.to_manipulate.connector_part1.rectangle_connector[i].id)
        return bound_list

    @Attribute
    def pol_list(self):
        pol_list = []
        for i in range(0, len(self.to_manipulate.connector_part1.cog)):
            if type(self.slctd_conn) is not str:
                if self.to_manipulate.connector_part1.shape == 'square':
                    if self.to_manipulate.connector_part1.square_connector[i].id != self.slctd_conn.id:
                        stationary_connector = self.to_manipulate.connector_part1.square_connector[i]
                        polygon = Polygon(self.pol_pts(stationary_connector))
                        pol_list.append(polygon)
                # if self.to_manipulate.connector_part1.shape == 'circle':
                #     ids.append(self.to_manipulate.connector_part1.circular_connector[i].id)
                # if self.to_manipulate.connector_part1.shape == 'rectangle':
                #     ids.append(self.to_manipulate.connector_part1.rectangle_connector[i].id)
        return pol_list

    def pol_pts(self, stationary_connector):
        pts = [(stationary_connector.cog[0] + ((self.slctd_conn.width/2 + self.to_manipulate.tol)
                                               * (stationary_connector.orientation.x[0])
                                               - (self.slctd_conn.length/2 + self.to_manipulate.tol)
                                               * (stationary_connector.orientation.x[1])),
                stationary_connector.cog[1] + ((self.slctd_conn.width/2 + self.to_manipulate.tol)
                                               * -(stationary_connector.orientation.y[0])
                                               + (self.slctd_conn.length/2 + self.to_manipulate.tol)
                                               * (stationary_connector.orientation.y[1]))),
               (stationary_connector.cog[0] + ((self.slctd_conn.width/2 + self.to_manipulate.tol)
                                               * (stationary_connector.orientation.x[0])
                                               + (self.slctd_conn.length/2 + self.to_manipulate.tol)
                                               * (stationary_connector.orientation.x[1])),
                stationary_connector.cog[1] - ((self.slctd_conn.length/2 + self.to_manipulate.tol)
                                               * (stationary_connector.orientation.y[1])
                                               + (self.slctd_conn.width/2 + self.to_manipulate.tol)
                                               * (stationary_connector.orientation.y[0]))),
               (stationary_connector.cog[0] - ((self.slctd_conn.width/2 + self.to_manipulate.tol)
                                               * (stationary_connector.orientation.x[0])
                                               - (self.slctd_conn.length/2 + self.to_manipulate.tol)
                                               * (stationary_connector.orientation.x[1])),
                stationary_connector.cog[1] - ((self.slctd_conn.width/2 + self.to_manipulate.tol)
                                               * -(stationary_connector.orientation.y[0])
                                               + (self.slctd_conn.length/2 + self.to_manipulate.tol)
                                               * (stationary_connector.orientation.y[1]))),
               (stationary_connector.cog[0] - ((self.slctd_conn.width/2 + self.to_manipulate.tol)
                                               * (stationary_connector.orientation.x[0])
                                               + (self.slctd_conn.length/2 + self.to_manipulate.tol)
                                               * (stationary_connector.orientation.x[1])),
                stationary_connector.cog[1] + ((self.slctd_conn.width/2 + self.to_manipulate.tol)
                                               * (stationary_connector.orientation.y[0])
                                               + (self.slctd_conn.length/2 + self.to_manipulate.tol)
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

    # Veto connector placement outside of bracket domain
    def _on_motion(self, evt: MotionEvent):
        current_position = evt.current_position
        pol_connector = self._pol_connector_with_tol(current_position)
        pol_connector_no_tol = self._pol_connector_no_tol(current_position)
        self.slctd_conn.color = 'orange'
        refresh_top_window()
        if self.pol_container.contains(pol_connector) is False:
            evt.Veto()
        if len(self.pol_list) != 0:
            cond = []
            for i in range(0, len(self.pol_list)):
                cond.append(pol_connector_no_tol.overlaps(self.pol_list[i]))
            if any(cond):
                self.slctd_conn.color = 'red'

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
            else:
                obj.position = evt.transformation.apply(obj.position)
                self.position = evt.current_position
        else:
            self.slctd_conn.color = 'green'
            obj.position = evt.transformation.apply(obj.position)
            self.position = evt.current_position

