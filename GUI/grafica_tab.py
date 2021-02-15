from datetime import datetime, timedelta

import matplotlib
from PyQt5.QtWidgets import QSizePolicy, QWidget, QListView, QHBoxLayout, QLabel, QVBoxLayout, QRadioButton, QMenu
from matplotlib import ticker as ticker, pyplot as pyplot
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg
from matplotlib.backends.backend_template import FigureCanvas
from matplotlib.dates import AutoDateLocator, ConciseDateFormatter, date2num
from matplotlib.figure import Figure

import Utils
from GUI import GUI_Resources
from GUI.GUI_Resources import get_error_dialog_msg, get_selector_widget
from GUI.MenuBar import Menu
from GUI.static_actions import StaticActions

from GUI.pacient_oriented_tab_interface import PacientInterface
from GUI.prueba_form import PruebaDialog
from database.settings import UserSettings
from database.models import PruebasListModel
from database.prueba import Prueba

matplotlib.use('Qt5Agg')


class Grafica(FigureCanvasQTAgg, FigureCanvas):
    autox = AutoDateLocator()
    formatterx = ConciseDateFormatter(autox)
    formatterx.formats = ['%y',  # ticks are mostly years
                          '%b',  # ticks are mostly months
                          '%d',  # ticks are mostly days
                          '%H:%Mh',  # hrs
                          '%H:%Mh',  # min
                          '%M:%S', ]  # secs

    def formatter(x, pos):
        hours, remainder = divmod(x, 3600)
        minutes, seconds = divmod(remainder, 60)
        if x < 3600:
            format_string = "{:02}'{:02}\"".format(int(minutes),
                                                   int(seconds))
        else:
            format_string = "{:02}:{:02}'{:02}\"".format(int(hours), int(minutes), int(seconds))
        return format_string

    funcformatter = ticker.FuncFormatter(formatter)

    def __init__(self, parent=None, width=5, height=4, dpi=100):
        PacientInterface.__init__(self)
        fig = Figure(figsize=(width, height), dpi=dpi)
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
        FigureCanvas.__init__(self, self.fig)
        FigureCanvasQTAgg.updateGeometry(self)
        self.setSizePolicy(QSizePolicy.Maximum, QSizePolicy.Maximum)


class EvolutionTab(QWidget, PacientInterface):
    def __init__(self, user: str):
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
        self.custom: QRadioButton = self.custom
        self.anual.clicked.connect(self.radio_handler)
        self.mensual.clicked.connect(self.radio_handler)
        self.semanal.clicked.connect(self.radio_handler)
        self.todos.clicked.connect(self.radio_handler)
        self.graph = Grafica()
        self.prueba: Prueba = ...
        self.pruebas: list = ...
        self.graph_test_1 = Grafica()
        self.graph_test_2 = Grafica()
        self.graph_test_3 = Grafica()
        self.graph_test_total = Grafica()
        self.user = user
        self.graph_lay_1: QVBoxLayout = self.graph_lay_1
        self.graph_lay_2: QVBoxLayout = self.graph_lay_2
        self.graph_lay_3: QVBoxLayout = self.graph_lay_3
        self.graph_lay_1.addWidget(self.graph_test_1)
        self.graph_lay_2.addWidget(self.graph_test_2)
        self.graph_lay_3.addWidget(self.graph_test_3)
        self.graph_lay_total.addWidget(self.graph_test_total)
        self.target_layout.addWidget(self.graph)
        self.notas_lap3.setVisible(False)
        self.notas_lap2.setVisible(False)
        self.notas_lap1.setVisible(False)
        self.notas_total.setVisible(False)
        self.tiempo_total: QLabel = self.tiempo_total
        self.tiempo_1: QLabel = self.tiempo_1
        self.tiempo_2: QLabel = self.tiempo_2
        self.tiempo_3: QLabel = self.tiempo_3
        #self.notas_lap_total.setVisible(False)
        self.model: PruebasListModel = PruebasListModel.get_instance(user)
        self.evolution_listview.setModel(self.model)
        self.model.change_model_list([])
        self.evolution_listview.clicked.connect(self.onPruebaClicked)
        self.title_test1: QLabel = self.title_test1
        self.title_test2: QLabel = self.title_test2
        self.title_test3: QLabel = self.title_test3
        self.title_test_total: QLabel = self.title_test_total
        self.title_test1.setText(self.settings.value(self.settings.LAP0_NAME))
        self.title_test2.setText(self.settings.value(self.settings.LAP1_NAME))
        self.title_test3.setText(self.settings.value(self.settings.LAP2_NAME))
        self.title_test_total.setText("Total")
        self.filter = get_selector_widget()
        self.buscar.clicked.connect(self.handle_filter)
        self.filter.buscar.clicked.connect(self.handle_filter)
        self.evolution_listview.customContextMenuRequested.connect(self.custom_context_menu)
        self.menu = Menu()
        self.edit_prueba = self.menu.addAction(StaticActions.edit_prueba_action)
        self.del_prueba = self.menu.addAction(StaticActions.del_prueba_action)
        self.add_prueba = self.menu.addAction(StaticActions.add_prueba_action)
        self.add_prueba.setEnabled(False)
        self.edit_prueba.setEnabled(False)
        self.del_prueba.setEnabled(False)
        self.add_prueba.triggered.connect(self.handle_actions)
        self.edit_prueba.triggered.connect(self.handle_actions)
        self.del_prueba.triggered.connect(self.handle_actions)

    def handle_filter(self):
        if self.sender() == self.filter.buscar:
            desde = self.filter.desde.date().toPyDate()
            hasta = self.filter.hasta.date().toPyDate()
            self.custom.setChecked(True)
            self.filter.close()
            self.radio_handler((desde, hasta,))
        if self.sender() == self.buscar:
            self.filter.show()
            self.filter.desde.setDate(datetime.now())
            self.filter.hasta.setDate(datetime.now())

    def currentChanged(self, index):  # Tab changed
        super().currentChanged(index)
        if self.pacient is not None:
            self.pacientSelected(self.pacient, None)

    def pacientSelected(self, pacient, index):  # Pacient changed
        super().pacientSelected(pacient, index)
        StaticActions.add_prueba_action.setEnabled(True)
        StaticActions.del_prueba_action.setEnabled(False)
        StaticActions.edit_prueba_action.setEnabled(False)
        self.pruebas = self.model.get_pruebas(pacient)
        self.pruebas.sort()
        if self.on_focus:
            # threading.Thread(target=self.load_graph, args=pacient)
            #self.pruebas = self.model.get_pruebas(pacient)
            self.pacient_name.setText(self.pacient.get_fomatted_name())
            if self.semanal.isChecked():
                self.semanal.clicked.emit()
            elif self.mensual.isChecked():
                self.mensual.clicked.emit()
            elif self.anual.isChecked():
                self.anual.clicked.emit()
            else:  # self.sender() == self.todos
                self.todos.clicked.emit()
        else:
            self.setVisible(False)
            pass

    def onPruebaClicked(self, *args):
        self.edit_prueba.setEnabled(True)
        self.del_prueba.setEnabled(True)
        if self.graph.markers1 is not None:
            self.graph.markers0[0].set_marker(None)
            self.graph.markers1[0].set_marker(None)
            self.graph.markers2[0].set_marker(None)
            self.graph.markers_total[0].set_marker(None)
            self.graph_test_1.marker[0].set_marker(None)
            self.graph_test_2.marker[0].set_marker(None)
            self.graph_test_3.marker[0].set_marker(None)
            self.graph_test_total.marker[0].set_marker(None)
        row = args[0].row()
        self.prueba: Prueba = self.model.get(row)
        self.notas_lap3.setVisible(True)
        self.notas_lap2.setVisible(True)
        self.notas_lap1.setVisible(True)
        self.notas_total.setVisible(True)
        self.notas_lap3.setText(self.prueba.notas[2])
        self.notas_lap2.setText(self.prueba.notas[1])
        self.notas_lap1.setText(self.prueba.notas[0])
        total = self.prueba.laps[2].total_seconds() + self.prueba.laps[0].total_seconds() + self.prueba.laps[
            1].total_seconds()
        self.graph.markers0 = self.graph.ax.plot(self.prueba.datetime, self.prueba.laps[0].total_seconds(), marker="+",
                                                 markersize=20, color="blue")
        self.graph.markers1 = self.graph.ax.plot(self.prueba.datetime, self.prueba.laps[1].total_seconds(), marker="+",
                                                 markersize=20, color="green")
        self.graph.markers2 = self.graph.ax.plot(self.prueba.datetime, self.prueba.laps[2].total_seconds(), marker="+",
                                                 markersize=20, color="brown")
        self.graph.markers_total = self.graph.ax.plot(self.prueba.datetime, total, marker="+", markersize=20,
                                                      color="red")
        prueba = self.model.get(row % len(self.pruebas))
        self.graph_test_1.marker = self.graph_test_1.ax.plot(row % len(self.pruebas),
                                                             prueba.laps[0].total_seconds(),
                                                             marker="+",
                                                             markersize=10,
                                                             color="black")
        self.graph_test_2.marker = self.graph_test_2.ax.plot(row % len(self.pruebas),
                                                             prueba.laps[1].total_seconds(),
                                                             marker="+",
                                                             markersize=10,
                                                             color="black")
        self.graph_test_3.marker = self.graph_test_3.ax.plot(row % len(self.pruebas),
                                                             prueba.laps[2].total_seconds(),
                                                             marker="+",
                                                             markersize=10,
                                                             color="black")
        self.graph_test_total.marker = self.graph_test_total.ax.plot(row % len(self.pruebas),
                                                                     (prueba.laps[2] + prueba.laps[1] + prueba.laps[0]).total_seconds(),
                                                             marker="+",
                                                             markersize=10,
                                                             color="black")
        self.tiempo_total.setText(str(prueba.laps[2] + prueba.laps[1] + prueba.laps[0]))
        self.tiempo_1.setText(str(prueba.laps[0]))
        self.tiempo_2.setText(str(prueba.laps[1]))
        self.tiempo_3.setText(str(prueba.laps[2]))
        self.graph.draw()
        self.graph_test_1.draw()
        self.graph_test_2.draw()
        self.graph_test_3.draw()
        self.graph_test_total.draw()

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
                self.graph_test_1.ax.clear()
                self.graph_test_2.ax.clear()
                self.tiempo_total.setText("")
                self.tiempo_1.setText("")
                self.tiempo_2.setText("")
                self.tiempo_3.setText("")
                self.graph_test_3.ax.clear()
                self.graph_test_total.ax.clear()
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
                    tick.set_rotation(30)
            else:
                self.graph.ax.clear()
                self.graph_test_1.ax.clear()
                self.graph_test_2.ax.clear()
                self.graph_test_3.ax.clear()
                self.graph_test_total.ax.clear()
            self.graph.draw()
            try:
                test1_lowmid_limit = self.settings.value(self.settings.LAP0_LOWMEDIUM_START).total_seconds()
                test2_lowmid_limit = self.settings.value(self.settings.LAP1_LOWMEDIUM_START).total_seconds()
                test3_lowmid_limit = self.settings.value(self.settings.LAP2_LOWMEDIUM_START).total_seconds()

                test1_midhigh_limit = self.settings.value(self.settings.LAP0_MEDIUMHARD_START).total_seconds()
                test2_midhigh_limit = self.settings.value(self.settings.LAP1_MEDIUMHARD_START).total_seconds()
                test3_midhigh_limit = self.settings.value(self.settings.LAP2_MEDIUMHARD_START).total_seconds()

                test_total_lowmid_limit = test1_lowmid_limit + test2_lowmid_limit + test3_lowmid_limit
                test_total_midhigh_limit = test3_midhigh_limit + test2_midhigh_limit + test1_midhigh_limit

                self.graph_test_1.ax.plot((0,
                                           len(test1)),
                                          (test1_lowmid_limit, test1_lowmid_limit),
                                          color="orange",
                                          markersize=1)
                self.graph_test_1.ax.plot((0, len(test1)), (test1_midhigh_limit, test1_midhigh_limit),
                                          color="red",
                                          markersize=1)

                self.graph_test_2.ax.plot((0, len(test2)), (test2_lowmid_limit, test2_lowmid_limit),
                                          color="orange",
                                          markersize=1)
                self.graph_test_2.ax.plot((0, len(test2)), (test2_midhigh_limit, test2_midhigh_limit),
                                          color="red",
                                          markersize=1)

                self.graph_test_3.ax.plot((0, len(test3)), (test3_lowmid_limit, test3_lowmid_limit),
                                          color="orange",
                                          markersize=1)
                self.graph_test_3.ax.plot((0, len(test3)), (test3_midhigh_limit, test3_midhigh_limit),
                                          color="red",
                                          markersize=1)

                self.graph_test_total.ax.plot((0, len(test3)), (test_total_lowmid_limit, test_total_lowmid_limit),
                                          color="orange",
                                          markersize=1)
                self.graph_test_total.ax.plot((0, len(test3)), (test_total_midhigh_limit, test_total_midhigh_limit),
                                          color="red",
                                          markersize=1)

                for x in range(0, len(dates)):
                    test_total = test1[x] + test2[x] + test3[x]
                    if test1[x] < test1_lowmid_limit:
                        self.graph_test_1.ax.plot(x, test1[x], color="green", marker="o", markersize=2)
                    elif test1[x] < test1_midhigh_limit:
                        self.graph_test_1.ax.plot(x, test1[x], color="orange", marker="o", markersize=2)
                    else:
                        self.graph_test_1.ax.plot(x, test1[x], color="red", marker="o", markersize=2)
                    if test2[x] < test2_lowmid_limit:
                        self.graph_test_2.ax.plot(x, test2[x], color="green", marker="o", markersize=2)
                    elif test2[x] < test2_midhigh_limit:
                        self.graph_test_2.ax.plot(x, test2[x], color="orange", marker="o", markersize=2)
                    else:
                        self.graph_test_2.ax.plot(x, test2[x], color="red", marker="o", markersize=2)
                    if test3[x] < test3_lowmid_limit:
                        self.graph_test_3.ax.plot(x, test3[x], color="green", marker="o", markersize=2)
                    elif test3[x] < test3_midhigh_limit:
                        self.graph_test_3.ax.plot(x, test3[x], color="orange", marker="o", markersize=2)
                    else:
                        self.graph_test_3.ax.plot(x, test3[x], color="red", marker="o", markersize=2)
                    if test_total < test_total_lowmid_limit:
                        self.graph_test_total.ax.plot(x, test3[x], color="green", marker="o", markersize=2)
                    elif test_total < test_total_midhigh_limit:
                        self.graph_test_total.ax.plot(x, test_total, color="orange", marker="o", markersize=2)
                    else:
                        self.graph_test_total.ax.plot(x, test_total, color="red", marker="o", markersize=2)

                self.graph_test_1.ax.yaxis.set_major_formatter(Grafica.funcformatter)
                self.graph_test_1.ax.yaxis.set_label("Tiempo de prueba")
                self.graph_test_1.ax.grid(True)
                #self.graph_test_1.ax.legend(frameon=False)

                self.graph_test_2.ax.yaxis.set_major_formatter(Grafica.funcformatter)
                self.graph_test_2.ax.yaxis.set_label("Tiempo de prueba")
                self.graph_test_2.ax.grid(True)
                #self.graph_test_2.ax.legend(frameon=False)

                self.graph_test_3.ax.yaxis.set_major_formatter(Grafica.funcformatter)
                self.graph_test_3.ax.yaxis.set_label("Tiempo de prueba")
                self.graph_test_3.ax.grid(True)
                #self.graph_test_3.ax.legend(frameon=False)
                self.graph_test_total.ax.yaxis.set_major_formatter(Grafica.funcformatter)
                self.graph_test_total.ax.yaxis.set_label("Tiempo de prueba")
                self.graph_test_total.ax.grid(True)

                self.graph_test_1.draw()
                self.graph_test_2.draw()
                self.graph_test_3.draw()
                self.graph_test_total.draw()
            except Exception as e:
                string = f"Error en la matrices secundarias. {type(e).__name__} paciente {self.pacient.dni}\n"
                string += "Valores:\n"
                string += f"{dates}\n"
                string += f"{test1}\n"
                string += f"{test2}\n"
                string += f"{test3}"
                get_error_dialog_msg(e, string, "Error de insertacion").exec_()

        except Exception as e:
            string = f"Error en la matriz {type(e).__name__} paciente {self.pacient.id}\n"
            string += "Valores:\n"
            string += f"{dates}\n"
            string += f"{test1}\n"
            string += f"{test2}\n"
            string += f"{test3}"
            get_error_dialog_msg(e, string, "Error de insertacion").exec_()

    def radio_handler(self, condiciones: tuple):
        new_pruebas = []
        if isinstance(condiciones, bool):
            now = datetime.now()
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
        else:
            desde = condiciones[0]
            hasta = condiciones[1]
            for prueba in self.pruebas:
                es_mayor_que_el_principio = prueba >= desde
                es_menor_que_el_final = prueba <= hasta

                if es_mayor_que_el_principio and es_menor_que_el_final:
                    new_pruebas.append(prueba)
        self.load_graph(new_pruebas)

    def on_reload(self):
        super().get_on_reload_signal()
        self.todos.setChecked(True)
        self.tiempo_1.setText("")
        self.tiempo_2.setText("")
        self.tiempo_3.setText("")
        self.tiempo_total.setText("")
        self.notas_lap3.setText("")
        self.notas_lap2.setText("")
        self.notas_lap1.setText("")
        self.notas_lap3.setVisible(False)
        self.notas_lap2.setVisible(False)
        self.notas_lap1.setVisible(False)
        self.notas_total.setVisible(False)

    def custom_context_menu(self, *args) -> None:
        if self.sender() == self.evolution_listview:
            index = self.evolution_listview.indexAt(args[0]).row()
            self.prueba = self.model.get(index)
            StaticActions.del_prueba_action.setEnabled(True)
            StaticActions.edit_prueba_action.setEnabled(True)
            Utils.popup_context_menu(self.sender(), self.menu, args[0])

    def handle_actions(self):
        if self.sender() == self.edit_prueba and self.prueba:
            dialog = PruebaDialog(self.user)
            dialog.set_prueba(self.pacient, self.prueba)
            if dialog.exec_() == 1:
                self.model.update(dialog.get_prueba(), self.prueba)
            StaticActions.del_prueba_action.setEnabled(False)
            StaticActions.edit_prueba_action.setEnabled(False)
        elif self.sender() == self.add_prueba:
            dialog = PruebaDialog(self.user)
            dialog.set_prueba(self.pacient)
            if dialog.exec_() == 1:
                prueba = dialog.get_prueba()
                self.model.append(prueba)
                self.pruebas.append(prueba)
        elif self.sender() == self.del_prueba and self.prueba:
            dialog = GUI_Resources.get_confirmation_dialog_ui(f"Quieres eliminar la prueba seleccionada? \nPaciente: {self.pacient.get_fomatted_name()}")
            if dialog.exec_() == 1:
                StaticActions.del_prueba_action.setEnabled(False)
                StaticActions.edit_prueba_action.setEnabled(False)
                self.pruebas.remove(self.prueba)
                self.model.delete(self.prueba)
                self.prueba = None
                self.on_reload()
        self.pruebas.sort()
        self.load_graph(self.pruebas)
