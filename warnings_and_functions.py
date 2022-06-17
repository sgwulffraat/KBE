import typing
from parapy.core import Base, ensure_iterable
from parapy.gui.display import get_top_window
from parapy.gui.viewer import Viewer

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