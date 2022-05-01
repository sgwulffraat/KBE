from parapy.lib.webgui.components import (
    Config, Group, Inspector, Intfield, Slider, Tab, Tree, Viewer,
    Wizard, WorkArea, Step, MultiCheckbox)
from parapy.lib.webgui import *
from flask import Flask
from Bracket import Bracket
from parapy.geom import Box

uid = 'Bracket'
obj = Bracket()

config = Config(
    title="Hello World!",
    default_visibility=["."],  # show all
    tools=[Tree(position="left"),
           Viewer(position="middle"),
           Inspector(position="right")
           ]
)
app = Flask(__name__)
api = ParaPyWebGUI(host_frontend=True, url_prefix='/api')
api.add_instance(uid, obj)
api.default_config = config
api.init_app(app)

if __name__ == '__main__':
    from parapy.lib.webgui.ui import open_webbrowser_when_served
    url_api = f"http://127.0.0.1:5000/"
    url_frontend = f"http://127.0.0.1:5000/?modelId={uid}"
    open_webbrowser_when_served(url_api)
    open_webbrowser_when_served(url_frontend)
    app.run(threaded=False)
