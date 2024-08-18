import matplotlib.colors
from matplotlib.figure import Figure
from matplotlib.backends.backend_qtagg import (
    FigureCanvasQTAgg,
    NavigationToolbar2QT as NavigationToolbar,
)
from PySide6 import QtGui
from PySide6.QtWidgets import (
    QMainWindow,
    QVBoxLayout,
    QWidget,
    QApplication,
    QLabel,
    QPushButton,
    QSpinBox,
    QColorDialog,
)
import sys
import matplotlib
import numpy as np
import random

matplotlib.use("Qt5Agg")


class MplCanvas(FigureCanvasQTAgg):

    def __init__(self, parent=None, width=4, height=4, dpi=100):
        fig = Figure(figsize=(width, height), dpi=dpi)
        fig.tight_layout()
        self.axes = fig.add_subplot(111)
        super(MplCanvas, self).__init__(fig)


class MainWindow(QMainWindow):

    def __init__(self, *args, **kwargs):
        super(MainWindow, self).__init__(*args, **kwargs)

        self.setWindowTitle("Github Style Profile Picture Generator")
        self.setMinimumSize(500, 300)

        # Initiate variable to hold image plot data for later use
        self.plot_data = None
        self.plot_color = QtGui.QColor(255, 255, 255)

        desc_label = QLabel(
            "Set how many squares your profile picture will be generated with.\nBy default, Guthub uses 5 squares."
        )

        # Create spinbox to set plot dimensions
        self.spinbox = QSpinBox()
        self.spinbox.setRange(3, 100)
        self.spinbox.setValue(5)  # Default Github image is 5x5 squares

        # Create button to generate image
        button = QPushButton("Generate Image!")
        button.clicked.connect(self.generate_plot)

        color_button = QPushButton("Change Image Color")
        color_button.clicked.connect(self.change_color)

        # Create the maptlotlib FigureCanvas object,
        # which defines a single set of axes as self.axes.
        self.canvas = MplCanvas(self, width=4, height=4, dpi=100)
        self.canvas.axes.axis("off")

        # Create toolbar, passing canvas as first parament, parent (self, the MainWindow) as second.
        toolbar = NavigationToolbar(self.canvas, self)

        layout = QVBoxLayout()
        layout.addWidget(desc_label)
        layout.addWidget(self.spinbox)
        layout.addWidget(button)
        layout.addWidget(color_button)
        layout.addWidget(toolbar)
        layout.addWidget(self.canvas)

        # Create a placeholder widget to hold our toolbar and canvas.
        widget = QWidget()
        widget.setLayout(layout)
        self.setCentralWidget(widget)

        self.show()

    def generate_plot(self):
        # Create grid of values, values are symmetrical along the middle of the row
        n = self.spinbox.value()
        data = np.zeros((n, n))
        for row in data:
            middle = int(len(row) / 2 + 1)
            counter = 0
            while counter != middle:
                row[counter] = row[len(row) - 1 - counter] = random.randint(0, 1)
                counter += 1

        # Save plot data for later use
        self.plot_data = data

        # Create Random color, RGB values are floats between 0 and 1
        color = (random.random(), random.random(), random.random())

        # Create color map
        cmap = matplotlib.colors.ListedColormap(["white", color])
        bounds = [0, 1]
        norm = matplotlib.colors.BoundaryNorm(bounds, cmap.N)

        # Save the color as QColor object for later use
        r, g, b = color
        color = QtGui.QColor.fromRgbF(r, g, b)
        self.plot_color = color

        # Draw the plot
        self.canvas.axes.imshow(data, cmap=cmap, norm=norm)
        self.canvas.draw()

    def change_color(self):
        new_color = QColorDialog.getColor(self.plot_color)
        # Check if an image plot data was generated, else do nothing
        if self.plot_data is not None:
            cmap = matplotlib.colors.ListedColormap(["white", new_color.name()])
            self.canvas.axes.imshow(self.plot_data, cmap=cmap)
            self.canvas.draw()

        self.plot_color = new_color

if __name__ == "__main__":
    app = QApplication(sys.argv)
    w = MainWindow()
    app.exec()
