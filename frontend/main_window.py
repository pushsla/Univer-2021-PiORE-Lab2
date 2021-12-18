import random

from PyQt5.QtWidgets import QMainWindow, QLabel, QSpinBox, QDoubleSpinBox, QScrollArea, QFormLayout, QGroupBox
from PyQt5 import uic

from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
import matplotlib.pyplot as plt

from lib.models import Models, Model
from lib.calc import MinSquared, Method
import lib.opti

import random as rnd


class MainWindow(QMainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)
        uic.loadUi('frontend/main_window.ui', self)

        self.xvec = tuple(i for i in range(self.spinBoxSamples.value()))
        self.yvec = tuple()
        self.model: Model = Model()
        self.method: Method = MinSquared(self.model, self.xvec, self.yvec)
        self.result = tuple()

        self.__data_fig: plt.figure = None
        self.__data_canvas: FigureCanvas = None

        self._connect_data_slots()
        self._connect_event_slots()
        self._connect_matplotlib()

    def _connect_matplotlib(self):
        self.__data_fig = plt.figure()
        self.__data_canvas = FigureCanvas(self.__data_fig)
        self.verticalLayoutPlot.addWidget(self.__data_canvas)

    def _connect_data_slots(self):
        self._connect_models()

    def _connect_event_slots(self):
        self.comboBoxModel.currentIndexChanged.connect(self._model_selected)
        self.spinBoxSamples.valueChanged.connect(self._update_xvec)
        self.pushButtonStart.clicked.connect(self._calculate)

    def _connect_models(self):
        self.comboBoxModel.addItem("", Model)
        for model in Models:
            self.comboBoxModel.addItem(model.name(), model)

    def _model_selected(self):
        self.model = self.comboBoxModel.currentData()()
        self._connect_model_params()
        self._set_model_repr()

    def _set_model_repr(self):
        self.labelModel.setText(str(self.model))

    def _connect_model_params(self):
        def lambda_hack(name, edit, is_coef: bool):
            def func():
                if is_coef:
                    self.model.set_coef(name, edit.value())
                    self._set_model_repr()
                else:
                    self.model.set_prop(name, edit.value())
                    self._connect_model_params()
                    self._set_model_repr()
            return func

        layout = self.formLayoutModelSetup

        for i in reversed(range(layout.count())):
            layout.itemAt(i).widget().setParent(None)

        props, coefs = self.model.params
        for name, value in props.items():
            label = QLabel(name)
            edit = QSpinBox()
            edit.setValue(value)

            layout.addRow(label, edit)

            edit.valueChanged.connect(lambda_hack(name, edit, False))

        area = QScrollArea()
        form = QFormLayout()
        box = QGroupBox()
        for name, value in coefs.items():
            label = QLabel(name)
            edit = QDoubleSpinBox()
            edit.setValue(value)

            form.addRow(label, edit)

            edit.valueChanged.connect(lambda_hack(name, edit, True))

        box.setLayout(form)
        area.setWidget(box)
        area.setWidgetResizable(True)

        layout.addWidget(area)

    def _update_xvec(self):
        self.xvec = tuple((i+rnd.randint(-2, 2)/10)/10 for i in range(self.spinBoxSamples.value()))
        pass

    def _calculate(self):
        self._update_xvec()
        self.yvec = tuple(self.model.y(x)+random.random()/10 for x in self.xvec)
        self.method = MinSquared(self.model, self.xvec, self.yvec)

        self.result = lib.opti.make_system(self.method)

        form = QFormLayout()
        box = QGroupBox()
        for name, value in self.result.items():
            label = QLabel(name)
            label2 = QLabel(str(value))

            form.addRow(label, label2)


        box.setLayout(form)
        self.scrollAreaResults.setWidget(box)
        self.scrollAreaResults.setWidgetResizable(True)

        self._draw_plots()

    def _draw_plots(self):
        xmodel = self.xvec
        ymodel = self.yvec

        yresult = tuple(self.model.y_with_custom_coefs(x, tuple(self.result.values())) for x in xmodel)

        self.__data_fig.clear()
        ax = self.__data_fig.add_subplot()
        ax.plot(xmodel, ymodel)
        ax.scatter(xmodel, yresult, c='red')
        self.__data_canvas.draw()

