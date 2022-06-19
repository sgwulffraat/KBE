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

def initial_item_placement(self, bracket, lastplaced_item, half_width, half_length, step, n, tol):
    position_list = []
    if bracket.__class__ == Cylinder:
        bracket_max_x = 2 * bracket.radius
        bracket_max_y = 2 * bracket.radius
    elif bracket.__class__ == Box:
        bracket_max_x = bracket.width
        bracket_max_y = bracket.length
    else:
        bracket_max_x = 2 * bracket.radius
        bracket_max_y = 2 * bracket.radius
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
            start_position_x = half_width + tol
            start_position_y = half_length + tol
            previous_half_length = 0
            previous_half_width = 0
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