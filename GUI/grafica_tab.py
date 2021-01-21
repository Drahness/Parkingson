import threading
from datetime import datetime, timedelta

import matplotlib
from PyQt5.QtWidgets import QSizePolicy, QWidget, QListView, QHBoxLayout, QLabel, QVBoxLayout, QRadioButton
from matplotlib import ticker as ticker, pyplot as pyplot
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg
from matplotlib.dates import AutoDateLocator, ConciseDateFormatter, date2num
from matplotlib.figure import Figure

from GUI import GUI_Resources
from GUI.GUI_Resources import get_error_dialog_msg

from GUI.pacient_oriented_tab_interface import PacientInterface
from database.Settings import UserSettings
from database.models import PruebasListModel

matplotlib.use('Qt5Agg')


class Grafica(FigureCanvasQTAgg):
    autox = AutoDateLocator()
    formatterx = ConciseDateFormatter(autox)
    formatterx.formats = ['año %y',  # ticks are mostly years
                          'mes %b',  # ticks are mostly months
                          'dia %d',  # ticks are mostly days
                          '%Hh %Mm',  # hrs
                          '%Hh %Mm',  # min
                          '%Mm %Ss', ]  # secs

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

    def __init__(self, parent=None, width=5, height=4, dpi=100):
        PacientInterface.__init__(self)
        # fig = Figure(figsize=(width, height), dpi=dpi)
        # self.axes = fig.add_subplot(111)
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
        self.resize(200, 200)
        FigureCanvasQTAgg.updateGeometry(self)
        self.setSizePolicy(QSizePolicy.Maximum, QSizePolicy.Maximum)


class EvolutionTab(QWidget, PacientInterface):
    def __init__(self, user):
        super(EvolutionTab, self).__init__()
        PacientInterface.__init__(self)
        GUI_Resources.get_evolution_tab(self)
        self.settings: UserSettings = UserSettings(user)
        self.evolution_listview: QListView = self.evolution_listview
        self.target_layout: QHBoxLayout = self.target_layout
        self.pacient_name: QLabel = self.pacient_name
        self.todos: QRadioButton = self.todos
        self.semanal: QRadioButton = self.semanal
        self.mensual: QRadioButton = self.mensual
        self.anual: QRadioButton = self.anual

        self.anual.clicked.connect(self.radio_handler)
        self.mensual.clicked.connect(self.radio_handler)
        self.semanal.clicked.connect(self.radio_handler)
        self.todos.clicked.connect(self.radio_handler)

        self.graph = Grafica()
        self.pruebas = ...
        self.graph_test_1 = Grafica()
        self.graph_test_2 = Grafica()
        self.graph_test_3 = Grafica()

        self.graph_lay_1: QVBoxLayout = self.graph_lay_1
        self.graph_lay_2: QVBoxLayout = self.graph_lay_2
        self.graph_lay_3: QVBoxLayout = self.graph_lay_3

        self.graph_lay_1.addWidget(self.graph_test_1)
        self.graph_lay_2.addWidget(self.graph_test_2)
        self.graph_lay_3.addWidget(self.graph_test_3)
        self.target_layout.addWidget(self.graph)

        self.model: PruebasListModel = PruebasListModel.get_instance(user)
        self.evolution_listview.setModel(self.model)
        self.model.change_model_list([])
        self.evolution_listview.clicked.connect(self.onPruebaClicked)
        self.title_test1: QLabel = self.title_test1
        self.title_test2: QLabel = self.title_test2
        self.title_test3: QLabel = self.title_test3
        self.title_test1.setText(self.settings.value(self.settings.LAP0_NAME))
        self.title_test2.setText(self.settings.value(self.settings.LAP1_NAME))
        self.title_test3.setText(self.settings.value(self.settings.LAP2_NAME))



    def currentChanged(self, index):  # Tab changed
        super().currentChanged(index)
        if self.pacient is not None:
            self.pacientSelected(self.pacient, None)

    def pacientSelected(self, pacient, index):
        super().pacientSelected(pacient, index)
        if self.on_focus:
            # threading.Thread(target=self.load_graph, args=pacient)
            self.pruebas = self.model.get_pruebas(pacient)

            self.load_graph(self.pruebas.copy())
            string = ""
            if self.pacient.apellidos:
                string += self.pacient.apellidos
            if self.pacient.nombre and string == "":
                string += self.pacient.nombre
            elif self.pacient.nombre:
                string += ", " + self.pacient.nombre

            self.pacient_name.setText(string)
        else:
            self.setVisible(False)
            pass

    def onPruebaClicked(self, *args):
        if self.graph.markers1 is not None:
            self.graph.markers0[0].set_marker(None)
            self.graph.markers1[0].set_marker(None)
            self.graph.markers2[0].set_marker(None)
            self.graph.markers_total[0].set_marker(None)
            self.graph_test_1.marker[0].set_marker(None)
            self.graph_test_2.marker[0].set_marker(None)
            self.graph_test_3.marker[0].set_marker(None)

        row = args[0].row()
        prueba = self.model.get(row)
        total = prueba.laps[2].total_seconds() + prueba.laps[0].total_seconds() + prueba.laps[1].total_seconds()
        self.graph.markers0 = self.graph.ax.plot(prueba.datetime, prueba.laps[0].total_seconds(), marker="+",
                                                 markersize=20, color="blue")
        self.graph.markers1 = self.graph.ax.plot(prueba.datetime, prueba.laps[1].total_seconds(), marker="+",
                                                 markersize=20, color="green")
        self.graph.markers2 = self.graph.ax.plot(prueba.datetime, prueba.laps[2].total_seconds(), marker="+",
                                                 markersize=20, color="brown")
        self.graph.markers_total = self.graph.ax.plot(prueba.datetime, total, marker="+", markersize=20, color="red")
        prueba = self.model.get(row%len(self.pruebas))
        self.graph_test_1.marker = self.graph_test_1.ax.plot(row%len(self.pruebas),
                                                             prueba.laps[0].total_seconds(),
                                                             marker="+",
                                                             markersize=10,
                                                             color="black")
        self.graph_test_2.marker = self.graph_test_2.ax.plot(row%len(self.pruebas),
                                                             prueba.laps[1].total_seconds(),
                                                             marker="+",
                                                             markersize=10,
                                                             color="black")
        self.graph_test_3.marker = self.graph_test_3.ax.plot(row%len(self.pruebas),
                                                             prueba.laps[2].total_seconds(),
                                                             marker="+",
                                                             markersize=10,
                                                             color="black")
        #self.graph.ax.invert_xaxis()
        self.graph.draw()
        #self.graph_test_1.ax.invert_xaxis()
        #self.graph_test_1.ax.invert_xaxis()
        #self.graph_test_1.ax.invert_xaxis()
        self.graph_test_1.draw()
        self.graph_test_2.draw()
        self.graph_test_3.draw()

    def load_graph(self, pruebas):
        test1 = []
        test2 = []
        test3 = []
        total = []
        dates = []  # X axis
        try:

            self.model.change_model_list(pruebas)
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
                                                          label=self.settings.get_lap_name(0),
                                                          color="blue",
                                                          marker="o",
                                                          markersize=2)
                self.graph.line_lap1 = self.graph.ax.plot(date2num(dates), matplotlib.dates.num2date(test2), lw=0.75,
                                                          label=self.settings.get_lap_name(1),
                                                          color="green",
                                                          marker="o",
                                                          markersize=2)
                self.graph.line_lap2 = self.graph.ax.plot(date2num(dates), matplotlib.dates.num2date(test3),
                                                          lw=0.75,
                                                          label=self.settings.get_lap_name(2),
                                                          color="brown",
                                                          marker="o",
                                                          markersize=2)
                self.graph.line_total = self.graph.ax.plot(date2num(dates), matplotlib.dates.num2date(total), lw=0.75,
                                                           label=self.settings.value(self.settings.LAP_TOTAL_NAME),
                                                           color="red",
                                                           marker="o",
                                                           markersize=2)

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
                self.graph_test_1.ax.clear()
                self.graph_test_2.ax.clear()
                self.graph_test_3.ax.clear()
            self.graph.ax.invert_xaxis()
            self.graph.draw()
            try:  # No va.
                test1_lowmid_limit = self.settings.value(self.settings.LAP0_LOWMEDIUM_START).total_seconds()
                test2_lowmid_limit = self.settings.value(self.settings.LAP1_LOWMEDIUM_START).total_seconds()
                test3_lowmid_limit = self.settings.value(self.settings.LAP2_LOWMEDIUM_START).total_seconds()

                test1_midhigh_limit = self.settings.value(self.settings.LAP0_MEDIUMHARD_START).total_seconds()
                test2_midhigh_limit = self.settings.value(self.settings.LAP1_MEDIUMHARD_START).total_seconds()
                test3_midhigh_limit = self.settings.value(self.settings.LAP2_MEDIUMHARD_START).total_seconds()

                self.graph_test_1.ax.plot((0,
                                           len(test1)),
                                          (test1_lowmid_limit, test1_lowmid_limit),
                                          color="yellow",
                                          markersize=1)
                self.graph_test_1.ax.plot((0, len(test1)), (test1_midhigh_limit, test1_midhigh_limit),
                                          color="red",
                                          markersize=1)

                self.graph_test_2.ax.plot((0, len(test2)), (test2_lowmid_limit, test2_lowmid_limit),
                                          color="yellow",
                                          markersize=1)
                self.graph_test_2.ax.plot((0, len(test2)), (test2_midhigh_limit, test2_midhigh_limit),
                                          color="red",
                                          markersize=1)

                self.graph_test_3.ax.plot((0, len(test3)), (test3_lowmid_limit, test3_lowmid_limit),
                                          color="yellow",
                                          markersize=1)
                self.graph_test_3.ax.plot((0, len(test3)), (test3_midhigh_limit, test3_midhigh_limit),
                                          color="red",
                                          markersize=1)

                for x in range(0, len(dates)):
                    if test1[x] < test1_lowmid_limit:
                        self.graph_test_1.ax.plot(x, test1[x], color="green", marker="o", markersize=2)
                        pass  # green
                    elif test1[x] < test1_midhigh_limit:
                        self.graph_test_1.ax.plot(x, test1[x], color="yellow", marker="o", markersize=2)
                        pass  # yellow
                    else:
                        self.graph_test_1.ax.plot(x, test1[x], color="red", marker="o", markersize=2)
                        pass  # red

                    if test2[x] < test2_lowmid_limit:
                        self.graph_test_2.ax.plot(x, test2[x], color="green", marker="o", markersize=2)
                        pass  # green
                    elif test2[x] < test2_midhigh_limit:
                        self.graph_test_2.ax.plot(x, test2[x], color="yellow", marker="o", markersize=2)
                        pass  # yellow
                    else:
                        self.graph_test_2.ax.plot(x, test2[x], color="red", marker="o", markersize=2)
                        pass  # red

                    if test3[x] < test3_lowmid_limit:
                        self.graph_test_3.ax.plot(x, test3[x], color="green", marker="o", markersize=2)
                        pass  # green
                    elif test3[x] < test3_midhigh_limit:
                        self.graph_test_3.ax.plot(x, test3[x], color="yellow", marker="o", markersize=2)
                        pass  # yellow
                    else:
                        self.graph_test_3.ax.plot(x, test3[x], color="red", marker="o", markersize=2)
                        pass  # red

                self.graph_test_1.draw()
                self.graph_test_2.draw()
                self.graph_test_3.draw()
            except Exception as e:
                string = f"Error en la matrices secundarias. {type(e).__name__} paciente {self.pacient.dni}\n"
                string += "Valores:\n"
                string += f"{dates}\n"
                string += f"{test1}\n"
                string += f"{test2}\n"
                string += f"{test3}"
                get_error_dialog_msg(e, string, "Error de insertacion").exec_()

        except Exception as e:
            string = f"Error en la matriz {type(e).__name__} paciente {self.pacient.dni}\n"
            string += "Valores:\n"
            string += f"{dates}\n"
            string += f"{test1}\n"
            string += f"{test2}\n"
            string += f"{test3}"
            get_error_dialog_msg(e, string, "Error de insertacion").exec_()

    def radio_handler(self):
        now = datetime.now()
        new_pruebas = []
        if self.sender() == self.semanal:
            condition = now - timedelta(weeks=1)
        elif self.sender() == self.mensual:
            condition = now - timedelta(days=30)
        elif self.sender() == self.anual:
            condition = now - timedelta(days=365)
        else:  # self.sender() == self.todos
            condition = datetime.utcfromtimestamp(0)
        for prueba in self.pruebas:
            if prueba > condition:
                new_pruebas.append(prueba)
        self.load_graph(new_pruebas)
