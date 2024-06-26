import numpy as np
import pandas as pd
import random
import sys

from PyQt6.QtWidgets import (
    QMainWindow, QApplication,
    QLabel, QDialog, QToolBar, QStatusBar,
    QPushButton, QDialogButtonBox,
    QFormLayout, QDoubleSpinBox, QMessageBox,
    QCheckBox, QFileDialog, QComboBox, QVBoxLayout, QHBoxLayout
)
from PyQt6.QtGui import QAction, QIcon
from PyQt6.QtCore import Qt, QSize, QStringListModel, QTimer

from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg, NavigationToolbar2QT as NavigationToolbar
from matplotlib.figure import Figure
import matplotlib.pyplot as plt

#Plot Object
class MplCanvas(FigureCanvasQTAgg):
    def __init__(self, parent=None, width=2, height=4, dpi=0):
        fig = Figure(figsize=(width, height), dpi=dpi)
        self.ax = fig.add_subplot(111)
        super(MplCanvas, self).__init__(fig)

class MainWindow(QMainWindow):
    def __init__(self, *args, **kwargs):
        super(MainWindow, self).__init__(*args, **kwargs)

        #Window Attributes
        self.setWindowTitle("Main Window")
        self.setFixedSize(QSize(800, 500))

        #Window Plotting Canvas
        self.canvas = MplCanvas(self, width=5, height=4, dpi=10)
        self.initialize_canvas = True

        #Toolbar
        toolbar = QToolBar("Toolbar")
        toolbar.setIconSize(QSize(16, 16))
        self.addToolBar(toolbar)

        #Toolbar Buttons
        sample_button = QAction(QIcon("icons/ui-tooltip--arrow.png"), "Sample Button", self)
        sample_button.setStatusTip("Sample Button")
        sample_button.triggered.connect(self.toggle)
        toolbar.addAction(sample_button)

        #Menu
        menu = self.menuBar()
        file_menu = menu.addMenu("&File")
        edit_menu = menu.addMenu("&Edit")
        view_menu = menu.addMenu("&View")

        #Menu Options
        window_select = QAction("&Sample Window...", self)
        #Add Button Click Event
        window_select.triggered.connect(self.sample_window)

        #Add Submenu items
        file_menu.addAction(window_select)

        #Plotting Data
        n_data = 50
        self.xdata = list(range(n_data))
        self.ydata = [0 for i in range(n_data)]

        #Plotting
        self.toggle_plot = False
        self.setCentralWidget(self.canvas)
        self._plot_ref = None
        self.canvas.draw()

        #Update Plot Timer
        self.timer = QTimer()
        self.timer.setInterval(100)
        self.timer.timeout.connect(self.update_plot)



    #Window Functions

    def sample_window(self):
        menu = SampleWindowMenu()
        menu.exec()

    def toggle(self):
        self.toggle_plot = not self.toggle_plot
        self.update_plot()

    def update_plot(self):
        if self.toggle_plot == True:
            self.timer.start()
            self.ydata = self.ydata[1:] + [random.randint(0, 10)]
            if self._plot_ref is None:
                plot_refs = self.canvas.ax.plot(self.xdata, self.ydata)
                self._plot_ref = plot_refs[0]
            else:
                self._plot_ref.set_ydata(self.ydata)
            self.canvas.draw()
        else:
            self.timer.stop()

class SampleWindowMenu(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.setWindowTitle("Sample Menu")

        #Window Buttons
        QBtn = QDialogButtonBox.StandardButton.Ok | QDialogButtonBox.StandardButton.Cancel

        self.button_box = QDialogButtonBox(QBtn)
        self.button_box.accepted.connect(self.accept)
        self.button_box.rejected.connect(self.reject)

        #Menu Input
        self.menu_input = QComboBox()
        self.menu_input.addItems(["Choice 1", "Choice 2"])

        #Numeric Input
        self.numeric_input = QDoubleSpinBox()

        #Window Layout
        self.layout = QFormLayout()

        #Add Inputs
        self.layout.addRow("Menu Input", self.menu_input)
        self.layout.addRow("Numeric Input", self.numeric_input)
        self.layout.addWidget(self.button_box)
        self.setLayout(self.layout)



app = QApplication(sys.argv)
window=MainWindow()
window.show()
app.exec()