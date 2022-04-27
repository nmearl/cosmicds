from astropy.modeling import models, fitting
from glue.config import viewer_tool
from glue.core import HubListener
from glue.core.message import (DataCollectionAddMessage,
                               DataCollectionDeleteMessage, DataUpdateMessage,
                               LayerArtistVisibilityMessage, NumericalDataChangedMessage,
                               SubsetMessage, SubsetUpdateMessage)
from glue.core.exceptions import IncompatibleAttribute
from glue_jupyter.bqplot.common.tools import Tool
from numpy import isnan

from cosmicds.stories.hubbles_law.utils import line_mark

@viewer_tool
class LineFitTool(Tool, HubListener):

    tool_id = 'cds:linefit'
    action_text = 'Fit lines'
    tool_tip = 'Fit lines to data'
    mdi_icon = 'mdi-chart-timeline-variant'
    
    def __init__(self, viewer, **kwargs):
        super().__init__(viewer, **kwargs)
        self.lines = {}
        self.slopes = {}
        #self._data_filter = lambda message: message.data.label in self.layer_labels
        #self._subset_filter = lambda message: message.subset.label in self.layer_labels and message.data.label in self.layer_labels
        # self.hub.subscribe(self, DataCollectionAddMessage,
        #                    handler=self._on_data_collection_added, filter=self._data_filter)
        self.hub.subscribe(self, DataCollectionDeleteMessage,
                           handler=self._on_data_collection_deleted, filter=self._data_collection_filter)
        self.hub.subscribe(self, DataUpdateMessage,
                           handler=self._on_layer_updated, filter=self._update_filter)
        # self.hub.subscribe(self, NumericalDataChangedMessage,
        #                    handler=self._on_layer_updated, filter=self._data_filter)
        self.hub.subscribe(self, SubsetUpdateMessage,
                           handler=self._on_layer_updated, filter=self._update_filter)

    def _data_collection_filter(self, msg):
        return msg.data in self.lines.keys()

    def _update_filter(self, msg):
        data = msg.subset if isinstance(msg, SubsetMessage) else msg.data
        return data in self.lines.keys() \
            and msg.attribute in [self.viewer.state.x_att, self.viewer.state.y_att]

    def _on_data_collection_deleted(self, msg):
        remove = [layer for layer in self.lines.keys() if layer.state.layer == msg.data]
        lines = [self.lines[x] for x in remove]
        self.figure.marks = [mark for mark in self.figure.marks if mark not in lines]
        for layer in remove:
            self._remove_line(layer)

    def _on_layer_updated(self, msg):
        data = msg.subset if isinstance(msg, SubsetMessage) else msg.data
        for layer in self.viewer.layers:
            layer_data = layer.state.layer
            if layer.state.visible and layer_data == data:
                self._remove_line(layer)
                self._fit_to_layer(layer)
                return

    @property
    def figure(self):
        return self.viewer.figure

    @property
    def dc(self):
        return self.viewer.session.data_collection

    @property
    def layer_labels(self):
        return [x.state.layer.label for x in self.viewer.layers]

    @property
    def hub(self):
        return self.viewer.session.hub

    def _create_fit_line(self, layer):
        data = layer.state.layer
        x = data[self.viewer.state.x_att]
        y = data[self.viewer.state.y_att]
        fit = fitting.LinearLSQFitter()
        line_init = models.Linear1D(intercept=0, fixed={'intercept':True})
        fitted_line = fit(line_init, x, y)
        x = [0, 2 * self.viewer.state.x_max] # For now, the line spans from 0 to twice the edge of the viewer
        y = fitted_line(x)
    
        # Create the fit line object
        # Keep track of this line and its slope
        start_x, end_x = x
        start_y, end_y = y
        slope = fitted_line.slope.value
        label = 'Slope = %.0f ks / s / Mpc' % slope if not isnan(slope) else None
        color = layer.state.color if layer.state.color != '0.35' else 'black'
        line = line_mark(layer, start_x, start_y, end_x, end_y, color, label)
        return line, slope

    def activate(self):
        self._fit_to_layers()

    def deactivate(self):
        self._clear_lines()

    def _fit_to_layer(self, layer, add=True):
        try:
            line, slope = self._create_fit_line(layer)
            data = layer.state.layer
            self.lines[data] = line
            self.slopes[data] = slope
        except IncompatibleAttribute:
            pass

        if add:
            self.figure.marks = self.figure.marks + [line]

    def _fit_to_layers(self):

        marks_to_keep = [mark for mark in self.figure.marks if mark not in self.line_marks]

        self.lines = {}
        self.slopes = {}
        for layer in self.viewer.layers:
            if layer.state.visible:
                self._fit_to_layer(layer, add=False)

        self.figure.marks = marks_to_keep + list(self.line_marks)

    def _remove_line(self, layer):
        data = layer.state.layer
        line = self.lines.get(data, None)
        del self.lines[data]
        del self.slopes[data]
        self.figure.marks = [mark for mark in self.figure.marks if mark != line]

    def _clear_lines(self):
        self.figure.marks = [mark for mark in self.figure.marks if mark not in self.line_marks]
        self.lines = {}
        self.slopes = {}

    def refresh(self):
        self._clear_lines()
        self._fit_to_layers()
            
    
    @property
    def line_marks(self):
        return self.lines.values()


    