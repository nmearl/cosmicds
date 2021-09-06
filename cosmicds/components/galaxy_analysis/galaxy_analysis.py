from ipyvuetify import VuetifyTemplate
from ipywidgets import widget_serialization
from glue.core.state_objects import State
from glue_jupyter.state_traitlets_helpers import GlueState
from echo import CallbackProperty

from ...utils import load_template


class ComponentState(State):
    adddata_disabled = CallbackProperty(1)
    prev1_disabled = CallbackProperty(1)
    next1_disabled = CallbackProperty(1)


class GalaxyAnalysis(VuetifyTemplate):
    template = load_template("galaxy_analysis.vue", __file__).tag(sync=True)
    state = GlueState().tag(sync=True)
    viewers = Dict().tag(sync=True, **widget_serialization)

    def __init__(self, session, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._session = session
        self.state = ComponentState()

        # Scatter viewer used for the display of the measured galaxy data
        hub_const_viewer = self._application_handler.new_data_viewer(
            BqplotScatterView, data=None, show=False)
        hub_fit_viewer = self._application_handler.new_data_viewer(
            BqplotScatterView, data=None, show=False)

    def add_viewer(self, viewer_class, data_label):
        viewer = viewer_class(self.session)
        viewer.register_to_hub(self.session.hub)
        
        data = self.data_collection[data_label]
        

    @property
    def data_collection(self):
        return self._session.data_collection