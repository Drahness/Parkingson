import sys
import matplotlib
from PyQt5.QtWidgets import QSizePolicy

from GUI.GUI_Resources import get_error_dialog_msg
from GUI.form import PacientInterface
from database.models import PruebasListModel
from main_window import UI

matplotlib.use('Qt5Agg')

from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg
from matplotlib.figure import Figure
import matplotlib.pyplot as pyplot
from matplotlib import dates
from matplotlib.dates import date2num, AutoDateLocator, ConciseDateFormatter


class MplCanvas(FigureCanvasQTAgg, PacientInterface):
    years = dates.YearLocator()
    month = dates.MonthLocator()
    day = dates.DayLocator()
    hour = dates.HourLocator()
    minute = dates.MinuteLocator()
    seconds = dates.SecondLocator()

    day_fmt = dates.DateFormatter("%d")
    years_fmt = dates.DateFormatter("%Y")
    minutes_fmt = dates.DateFormatter("%M")
    hour_fmt = dates.DateFormatter("%H")

    auto = AutoDateLocator()

    formatter = ConciseDateFormatter(auto)
    formatter.formats = ['%y',  # ticks are mostly years
                         '%b',       # ticks are mostly months
                         '%d',       # ticks are mostly days
                         '%H:%M',    # hrs
                         '%H:%M',    # min
                         '%S.%f', ]  # secs


    def __init__(self, parent=None, width=5, height=4, dpi=100):
        #fig = Figure(figsize=(width, height), dpi=dpi)
        #self.axes = fig.add_subplot(111)
        self.model = PruebasListModel.get_instance()
        self.fig, self.ax = pyplot.subplots()
        #self.ax.au
        super(MplCanvas, self).__init__(self.fig)
        FigureCanvasQTAgg.setSizePolicy(self, QSizePolicy.Expanding, QSizePolicy.Expanding)
        FigureCanvasQTAgg.updateGeometry(self)

# TODO error cuando le das al cronometro, y se añáde un nuevo valor, lo hace con timedeltas.
# TODO mientras que en la BBDD se guarda en float
    def on_pacient_selected(self, pacient, index):
        try:
            pruebas = self.model.get_pruebas(pacient)
            if len(pruebas) > 0:
                test1 = []
                test2 = []
                test3 = []
                dates = []  # X axis
                indexes = []
                for x in range(0, len(pruebas)):
                    prueba = pruebas[x]
                    indexes.append(x)
                    dates.append(prueba.datetime)
                    test1.append(prueba.laps[0])
                    test2.append(prueba.laps[1])
                    test3.append(prueba.laps[2])
                self.ax.clear()
                print(dates)
                self.ax.plot(date2num(dates), date2num(test1))
                self.ax.xaxis.set_major_locator(MplCanvas.auto)
                self.ax.xaxis.set_major_formatter(MplCanvas.formatter)
                self.ax.xaxis.set_minor_locator(MplCanvas.minute)
                self.ax.xaxis.set_major_locator(MplCanvas.auto)
                self.ax.yaxis.set_major_formatter(MplCanvas.formatter)

            #for nn, ax in enumerate(self.ax):
             #   ax.plot(dates, y)
              #  # rotate_labels...
               # for label in ax.get_xticklabels():
                #    label.set_rotation(40)
                 #   label.set_horizontalalignment('right')
            self.draw()
        except Exception as e:
            string = f"Error en la matriz {type(e).__name__} paciente {pacient.dni}\n"
            string += "Valores:\n"
            string += f"{dates}\n"
            string += f"{test1}\n"
            string += f"{test2}\n"
            string += f"{test3}"
            get_error_dialog_msg(e, string, "Error de insertacion").exec_()

