import typing
from parapy.core import Base, ensure_iterable
from parapy.gui.display import get_top_window
from parapy.gui.viewer import Viewer
from parapy.geom import Box, Cylinder, translate
from shapely.geometry import Polygon

def generate_warning(warning_header, msg):
    from tkinter import Tk, messagebox

    # initialization
    window = Tk()
    window.withdraw()

    # generates message box
    messagebox.showwarning(warning_header, msg)

    # kills the gui
    window.deiconify()
    window.destroy()
    window.quit()

def hide(objects: typing.Union[Base, typing.Iterable[Base]]):
    return redraw(objects, show=False)


def show(objects: typing.Union[Base, typing.Iterable[Base]]):
    return redraw(objects, show=True)


def redraw(objects: typing.Union[Base, typing.Iterable[Base]], show: bool,
           viewer: Viewer = None, update: bool = True):
    """triggers a redraw of the main viewer. If show is True, draws the objects again,
    else hides them."""
    objects = ensure_iterable(objects)
    if viewer is None:
        window = get_top_window()
        viewer = window.viewer
    if viewer is None:
        return
    if show:
        viewer.display(objects, update=update)
    else:
        viewer.hide(objects, update=update)

    def pol_pts(self, stationary_connector, tol):
        """Function to get edge points of any rectangular connector"""
        pts = [(stationary_connector.cog[0] + ((stationary_connector.width/2 + tol)
                                               * (stationary_connector.orientation.x[0])
                                               - (stationary_connector.length/2 + tol)
                                               * (stationary_connector.orientation.x[1])),
                stationary_connector.cog[1] + ((stationary_connector.width/2 + tol)
                                               * -(stationary_connector.orientation.y[0])
                                               + (stationary_connector.length/2 + tol)
                                               * (stationary_connector.orientation.y[1]))),
               (stationary_connector.cog[0] + ((stationary_connector.width/2 + tol)
                                               * (stationary_connector.orientation.x[0])
                                               + (stationary_connector.length/2 + tol)
                                               * (stationary_connector.orientation.x[1])),
                stationary_connector.cog[1] - ((stationary_connector.length/2 + tol)
                                               * (stationary_connector.orientation.y[1])
                                               + (stationary_connector.width/2 + tol)
                                               * (stationary_connector.orientation.y[0]))),
               (stationary_connector.cog[0] - ((stationary_connector.width/2 + tol)
                                               * (stationary_connector.orientation.x[0])
                                               - (stationary_connector.length/2 + tol)
                                               * (stationary_connector.orientation.x[1])),
                stationary_connector.cog[1] - ((stationary_connector.width/2 + tol)
                                               * -(stationary_connector.orientation.y[0])
                                               + (stationary_connector.length/2 + tol)
                                               * (stationary_connector.orientation.y[1]))),
               (stationary_connector.cog[0] - ((stationary_connector.width/2 + tol)
                                               * (stationary_connector.orientation.x[0])
                                               + (stationary_connector.length/2 + tol)
                                               * (stationary_connector.orientation.x[1])),
                stationary_connector.cog[1] + ((stationary_connector.width/2 + tol)
                                               * (stationary_connector.orientation.y[0])
                                               + (stationary_connector.length/2 + tol)
                                               * (stationary_connector.orientation.y[1])))
               ]
        return pts
#
# def overlap_check()
#     pol_list = []
#     box_list = self.to_manipulate.connectors.find_children(fn=lambda conn: conn.__class__
#                                                                            == Box)
#     cylinder_list = self.to_manipulate.connectors.find_children(fn=lambda conn: conn.__class__
#                                                                                 == Cylinder)
#     if type(self.slctd_conn) is not str:
#         for cylinder in cylinder_list:
#             if cylinder.id != self.slctd_conn.id:
#                 stationary_cylinder = cylinder
#                 polygon = Point((stationary_cylinder.cog[0]),
#                                 (stationary_cylinder.cog[1])).buffer(stationary_cylinder.radius
#                                                                      + tol)
#                 pol_list.append(polygon)
#         for box in box_list:
#             if box.id != self.slctd_conn.id:
#                 stationary_connector = box
#                 polygon = Polygon(self.pol_pts(stationary_connector))
#                 pol_list.append(polygon)
#
#     if len(self.pol_list) != 0:
#         cond = []
#         for i in range(0, len(self.pol_list)):
#             cond.append(pol_connector_no_tol.overlaps(self.pol_list[i]))
#         if any(cond):

def initial_item_placement(self, bracket, lastplaced_item, half_width, half_length, step, n, tol):
    """Function that uses the bracket, last placed item, connector-to-be-placed dimensions and
    number of connectors-to-be-placed, tolerance between connectors and x step size to generate
    an automatic initial placement of the newly added connectors. The start position of the
    iteration depends on the last placed item before it. This functions first checks all positive
    x-coordinates at y-coordinate of previous placed item. If no position is found at that range,
     y is changed with the half-length of the connector + the tolerance and the iteration continues
     again with looping the x-coordinates"""
    position_list = []
    if bracket.__class__ == Cylinder:
        bracket_max_x = 2 * bracket.radius
        bracket_max_y = 2 * bracket.radius
    elif bracket.__class__ == Box:
        bracket_max_x = bracket.width
        bracket_max_y = bracket.length
    else:
        x = []
        y = []
        for i in self.pts_container:
            x.append(i[0])
            y.append(i[1])
        bracket_max_x = max(x)
        bracket_max_y = max(y)
    for child in range(0, n):
        iteration = True
        solution = False
        if child != 0:
            last_item = position_list[-1]
            start_position_x = last_item[0]
            start_position_y = last_item[1]
            previous_half_width = half_width
            previous_half_length = half_length
        elif lastplaced_item != "None" and child == 0:
            last_items = lastplaced_item.find_children(fn=lambda conn: conn.__class__ == Box
                                                                       or conn.__class__ == Cylinder)
            start_position_x = last_items[-1].cog[0]
            start_position_y = last_items[-1].cog[1]
            if last_items[-1].__class__ == Cylinder:
                previous_half_width = last_items[-1].radius
                previous_half_length = last_items[-1].radius
            else:
                previous_half_width = last_items[-1].width / 2
                previous_half_length = last_items[-1].length / 2
        else:
            previous_half_length = 0
            previous_half_width = 0
            if bracket.__class__ != Box and bracket.__class__ != Cylinder:
                start_position_x = half_width + tol - min(x)
                start_position_y = half_length + tol - min(y)
            else:
                start_position_x = half_width + tol
                start_position_y = half_length + tol
        for j in range(0, round((bracket_max_y
                                 - (start_position_y + previous_half_length + tol)) / half_length) + 1):
            if iteration is True:
                if j == 0:
                    if previous_half_length == 0:
                        position = [start_position_x, start_position_y]
                    else:
                        if start_position_y < half_length + tol:
                            position = [start_position_x + half_width + previous_half_width + tol, half_length + tol]
                        else:
                            position = [start_position_x + half_width + previous_half_width + tol, start_position_y]
                else:
                    if previous_half_length == 0:
                        position = [start_position_x, start_position_y + j * half_length]
                    else:
                        position = [half_width + tol, start_position_y + previous_half_length + tol + j * half_length]
                while position[0] < bracket_max_x:
                    position[0] = position[0] + step
                    pol_connector = Polygon([(position[0] + (half_width + tol),
                                              position[1] + (half_length + tol)),
                                             (position[0] + (half_width + tol),
                                              position[1] - (half_length + tol)),
                                             (position[0] - (half_width + tol),
                                              position[1] - (half_length + tol)),
                                             (position[0] - (half_width + tol),
                                              position[1] + (half_length + tol))
                                             ])
                    if self.poly_container.contains(pol_connector) is True:
                        position_list.append(position)
                        iteration = False
                        solution = True
                        break
        else:
            if solution is False:
                position_list.append([bracket.cog[0], bracket.cog[1]])
    return position_list
