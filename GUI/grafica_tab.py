import matplotlib
from PyQt5.QtWidgets import QSizePolicy, QWidget, QListView
from matplotlib import ticker as ticker, pyplot as pyplot
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg
from matplotlib.dates import AutoDateLocator, ConciseDateFormatter, date2num

from GUI import GUI_Resources
from GUI.GUI_Resources import get_error_dialog_msg

from GUI.tab_widgets import PacientInterface
from database.models import PruebasListModel

matplotlib.use('Qt5Agg')


class Grafica(FigureCanvasQTAgg):
    autox = AutoDateLocator()
    formatterx = ConciseDateFormatter(autox)
    formatterx.formats = ['%y',  # ticks are mostly years
                          '%b',  # ticks are mostly months
                          '%d',  # ticks are mostly days
                          '%H:%M',  # hrs
                          '%H:%M',  # min
                          '%S.%f', ]  # secs

    def formatter(x, pos):
        hours, remainder = divmod(x, 3600)
        minutes, seconds = divmod(remainder, 60)
        if x < 3600:
            format_string = "{:02}:{:02}".format(int(minutes),
                                                 int(seconds))
        else:
            format_string = "{:02}:{:02}:{:02}".format(int(hours), int(minutes), int(seconds))
        return format_string

    funcformatter = ticker.FuncFormatter(formatter)

    def __init__(self, user:str ,parent=None, width=5, height=4, dpi=100):
        PacientInterface.__init__(self)
        # fig = Figure(figsize=(width, height), dpi=dpi)
        # self.axes = fig.add_subplot(111)
        self.model = PruebasListModel.get_instance(user)
        self.fig, self.ax = pyplot.subplots()
        self.line_lap0 = None
        self.line_lap1 = None
        self.line_lap2 = None
        self.line_total = None
        self.markers0 = None
        self.markers1 = None
        self.markers2 = None
        self.markers_total = None
        self.text0 = None
        self.text1 = None
        self.text2 = None
        super(Grafica, self).__init__(self.fig)
        FigureCanvasQTAgg.setSizePolicy(self, QSizePolicy.Expanding, QSizePolicy.Expanding)
        FigureCanvasQTAgg.updateGeometry(self)


class PerformanceTab(QWidget, PacientInterface):

    def __init__(self,user):
        super(PerformanceTab, self).__init__()
        PacientInterface.__init__(self)
        GUI_Resources.get_performance_widget(self)
        self.graph = Grafica(user)
        self.model: PruebasListModel = PruebasListModel.get_instance(user)
        self.listView: QListView = self.listView
        self.listView.setModel(self.model)
        self.model.change_model_list([])
        self.listView.clicked.connect(self.onPruebaClicked)
        self.horizontalLayout.addWidget(self.graph)


    def currentChanged(self, index):  # Tab changed
        super().currentChanged(index)
        if self.pacient is not None:
            self.pacientSelected(self.pacient, None)

    def pacientSelected(self, pacient, index):
        super().pacientSelected(pacient, index)
        if self.on_focus:
            self.load_graph(pacient)
        else:
            self.setVisible(False)
            pass

    def onPruebaClicked(self, *args):
        if self.graph.markers1 is not None:
            self.graph.markers0[0].set_marker(None)
            self.graph.markers1[0].set_marker(None)
            self.graph.markers2[0].set_marker(None)
            self.graph.markers_total[0].set_marker(None)
            """self.text0 # TODO
            self.text1
            self.text2"""
        row = args[0].row()
        prueba = self.model.get(row)
        total = prueba.laps[2].total_seconds() + prueba.laps[0].total_seconds() + prueba.laps[1].total_seconds()
        self.graph.markers0 = self.graph.ax.plot(prueba.datetime, prueba.laps[0].total_seconds(), marker="+",
                                                 markersize=20, color="blue")
        self.graph.markers1 = self.graph.ax.plot(prueba.datetime, prueba.laps[1].total_seconds(), marker="+",
                                                 markersize=20, color="green")
        self.graph.markers2 = self.graph.ax.plot(prueba.datetime, prueba.laps[2].total_seconds(), marker="+",
                                                 markersize=20, color="brown")
# todo

        self.graph.markers_total = self.graph.ax.plot(prueba.datetime, total, marker="+", markersize=20, color="red")
        self.graph.draw()
        pass

    def load_graph(self, pacient):
        test1 = []
        test2 = []
        test3 = []
        total = []
        dates = []  # X axis
        try:
            pruebas = self.model.get_pruebas(pacient)
            if len(pruebas) > 0:
                self.graph.ax.clear()
                for x in range(0, len(pruebas)):
                    prueba = pruebas[x]
                    dates.append(prueba.datetime)

                    test1.append(prueba.laps[0].total_seconds())
                    test2.append(prueba.laps[1].total_seconds())
                    test3.append(prueba.laps[2].total_seconds())
                    total.append(test1[x] + test2[x] + test3[x])

                self.graph.line_lap0 = self.graph.ax.plot(date2num(dates), matplotlib.dates.num2date(test1), lw=0.75,
                                                          label='lap1', color="blue", marker="o", markersize=2)
                self.graph.line_lap1 = self.graph.ax.plot(date2num(dates), matplotlib.dates.num2date(test2), lw=0.75,
                                                          label='lap2', color="green", marker="o", markersize=2)
                self.graph.line_lap2 = self.graph.ax.plot(date2num(dates), matplotlib.dates.num2date(test3), lw=0.75,
                                                          label='lap3', color="brown", marker="o", markersize=2)
                self.graph.line_total = self.graph.ax.plot(date2num(dates), matplotlib.dates.num2date(total), lw=0.75,
                                                           label='Total', color="red", marker="o", markersize=2)

                self.graph.ax.xaxis.set_major_locator(Grafica.autox)
                self.graph.ax.xaxis.set_major_formatter(Grafica.formatterx)
                self.graph.ax.yaxis.set_major_formatter(Grafica.funcformatter)
                self.graph.ax.yaxis.set_label("Tiempo de prueba")
                self.graph.ax.xaxis.set_label("Fecha")
                self.graph.ax.grid(True)
                self.graph.ax.legend(frameon=False)
                self.statusChangeSlot.emit(
                    f"Mostrando {len(test2)} pruebas, entre {dates[0]} y {dates[len(dates) - 1]}", 10)
                for tick in self.graph.ax.get_xticklabels():
                    tick.set_rotation(55)
            else:
                self.graph.ax.clear()
            self.graph.draw()

        except Exception as e:
            string = f"Error en la matriz {type(e).__name__} paciente {pacient.dni}\n"
            string += "Valores:\n"
            string += f"{dates}\n"
            string += f"{test1}\n"
            string += f"{test2}\n"
            string += f"{test3}"
            get_error_dialog_msg(e, string, "Error de insertacion").exec_()