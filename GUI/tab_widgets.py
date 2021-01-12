import datetime
import sys

import re
import matplotlib
from PyQt5 import QtWidgets
from PyQt5.QtCore import pyqtSignal
from PyQt5.QtGui import QIntValidator
from PyQt5.QtWidgets import QWidget, QCalendarWidget, QDateEdit, QSizePolicy, QListView, QLabel
from matplotlib import dates, ticker as ticker, pyplot as pyplot
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg
from matplotlib.dates import AutoDateLocator, ConciseDateFormatter, date2num

from GUI import GUI_Resources
from GUI.GUI_Resources import get_pacient_widget_ui, get_error_dialog_msg, get_cronometro_widget_ui, \
    get_cronometro_bar_widget
from GUI.cronometro import Timer
from database.entities import Pacient, Prueba
from database.models import PruebasListModel
from main_window import UI

matplotlib.use('Qt5Agg')


class PacientInterface:
    """Los tabs heredan de esta. Ya que todos tienen casi la misma logica"""
    def __init__(self):
        self.last_pacient = None
        self.pacient = None
        self.index = None
        self.on_focus = False
        self.statusChangeSlot = None
        self.pacientSelectedSignal = None
        self.currentChangedSignal = None
        pass


    def getsignal_pacient_selected(self) -> pyqtSignal:
        return self.pacientSelectedSignal


    def set_signal_pacient_selected(self, signal: pyqtSignal):
        self.pacientSelectedSignal = signal


    def getsignal_current_changed(self) -> pyqtSignal:
        return self.currentChangedSignal


    def set_signal_current_changed(self, signal: pyqtSignal):
        self.currentChangedSignal = signal

    def pacientSelected(self, pacient, index):
        """The signal pacientSelected will get a Pacient and a row in the model."""
        self.pacient = pacient
        self.index = index

    def init(self):
        """Inicializas el widget. Concretamente las señales desde el mainWindow."""
        from main_window import UI
        #UI.get_instance().pacientSelected.connect(self.pacientSelected)
        self.pacientSelectedSignal.connect(self.pacientSelected)
        self.currentChangedSignal.connect(self.currentChanged)
        #UI.get_instance().central.parent_tab_widget.currentChanged.connect(self.currentChanged)
        #self.statusChangeSlot = UI.get_instance().changeStatusBar

    def set_change_status_bar(self,signal: pyqtSignal):
        self.statusChangeSlot = signal

    def get_change_status_bar(self):
        return self.statusChangeSlot

    def currentChanged(self, index):
        self.on_focus = False
        self.sender().currentWidget().on_focus = True


class PacientWidget(QWidget, PacientInterface):
    default_date = datetime.date(1990, 12, 12)
    finishedSignal: pyqtSignal = pyqtSignal(bool)  # maybe another name is better
    resultSignal: pyqtSignal = pyqtSignal(bool, int)
    """ bool if canceled or accepted. int, the row of the pacient or -1 if new pacient """

    def __init__(self):
        super().__init__()
        get_pacient_widget_ui(self)
        self.on_focus = True  # Este sale por defecto
        self.calendarWidget.clicked.connect(self.on_calendar_changed)
        self.nacimiento_field.dateChanged.connect(self.on_calendar_changed)
        self.calendarWidget: QCalendarWidget = self.calendarWidget
        self.nacimiento_field: QDateEdit = self.nacimiento_field
        self.accept_button.clicked.connect(self.buttons)
        self.error_apellidos: QLabel
        self.error_dni: QLabel
        self.error_estadio: QLabel
        self.error_nombre: QLabel

        self.cancel_button.clicked.connect(self.buttons)
        self.pacientSelected(None)
        self.set_enabled(False)

    def save_pacient(self):
        """Updates the instance."""
        self.pacient.dni = self.dni_field.text()
        self.pacient.apellidos = self.apellidos_field.text()
        self.pacient.nombre = self.nombre_field.text()
        self.pacient.estadio = self.estadio_field.text()
        self.pacient.nacimiento = self.nacimiento_field.date()
        self.pacient.notas = self.notas_field.toPlainText()
        return self.pacient

    def check_input(self):
        errored = False
        if not re.fullmatch("((([X-Z])|([LM])){1}([-]?)((\d){7})([-]?)([A-Z]{1}))|((\d{8})([-]?)([A-Z]))",self.dni_field.text()) and not re.fullmatch("/^[0-9]{8}[TRWAGMYFPDXBNJZSQVHLCKE]$/i",self.dni_field.text()):
            errored = True
            self.error_dni.setText("No has introducido un documento de identidad valido.")
        if not len(self.apellidos_field.text()) > 0:
            errored = True
            self.error_apellidos.setText("Este campo no debe estar vacio.")
        if not len(self.nombre_field.text()) > 0:
            errored = True
            self.error_nombre.setText("Este campo no debe estar vacio.")
        if int(self.estadio_field.text()) > 3:
            errored = True
            self.error_estadio.setText("No has introducido un estadio valido.")
        return not errored

    def buttons(self, *args):
        name = self.sender().objectName()
        print(name)
        if name == "accept_button":
            if self.save_pacient():
                if self.check_input():
                    self.error_dni.setText("")
                    self.error_estadio.setText("")
                    self.error_nombre.setText("")
                    self.error_apellidos.setText("")
                    self.resultSignal.emit(True, self.index)
                    self.set_enabled(False)
        elif name == "cancel_button":
            if self.save_pacient():
                self.resultSignal.emit(False, -1)
                self.set_enabled(False)


    def pacientSelected(self, pacient, row: int = None):
        """Overriden method from PacientInterface"""
        self.index = row
        if pacient is not None:
            if isinstance(pacient, dict):
                dni = pacient.get("dni")
                nombre = pacient.get("nombre")
                apellidos = pacient.get("apellidos")
                estadio = pacient.get("estadio", default=0)
                nacimiento = pacient.get("nacimiento", default=self.default_date)
                notas = pacient.get("notas")
            elif isinstance(pacient, Pacient):
                dni = pacient.dni
                nombre = pacient.nombre
                apellidos = pacient.apellidos
                estadio = pacient.estadio or 0
                nacimiento = pacient.nacimiento or self.default_date
                notas = pacient.notas
            else:
                raise AssertionError()
        else:
            dni = None
            nombre = None
            apellidos = None
            estadio = ""
            nacimiento = self.default_date
            notas = None
        self.pacient = pacient
        self.last_pacient = dni
        self.dni_field.setText(dni)
        self.apellidos_field.setText(apellidos)
        self.nombre_field.setText(nombre)
        self.estadio_field.setText(str(estadio))
        self.nacimiento_field.setDate(nacimiento)
        self.notas_field.setText(notas)
        self.calendarWidget.setSelectedDate(nacimiento)
        self.estadio_field.setValidator(QIntValidator())

    def set_enabled(self, enabled: bool):
        self.dni_field.setEnabled(enabled)
        self.apellidos_field.setEnabled(enabled)
        self.nombre_field.setEnabled(enabled)
        self.estadio_field.setEnabled(enabled)
        self.nacimiento_field.setEnabled(enabled)
        self.notas_field.setEnabled(enabled)
        self.calendarWidget.setEnabled(enabled)
        self.cancel_button.setVisible(enabled)
        self.accept_button.setVisible(enabled)
        self.finishedSignal.emit(not enabled)

    def on_calendar_changed(self, *args):
        self.calendarWidget.setSelectedDate(args[0])
        self.nacimiento_field.setDate(args[0])

    def pacient_selected(self) -> bool:
        return self.pacient is not None


class Cronometro(QWidget, PacientInterface):
    STOPPED = 3
    STARTED = 0
    END = 2
    # La parte int, la voy a dejar, pero no la usare.
    finishedSignal: pyqtSignal = pyqtSignal(Prueba, int)

    def pacientSelected(self, pacient, index):
        super().pacientSelected(pacient, index)
        self.start_and_lap.setEnabled(True)

    def __init__(self, parent=None):
        super(Cronometro, self).__init__(parent)
        PacientInterface.__init__(self)
        get_cronometro_widget_ui(self)
        self.setObjectName("cronometro_paciente")
        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.progress_bar = get_cronometro_bar_widget()
        self.progress_bar.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.horizontalLayout.addWidget(self.progress_bar)
        self.stop_button.setEnabled(False)
        self.cancel_button.setEnabled(False)

        # self.horizontalLayout.setAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
        # self.setSizePolicy(QSizePolicy.Expanding,QSizePolicy.Expanding)
        # self.setStyleSheet("background:red")

        # Conexiones de los botones
        self.start_and_lap.clicked.connect(self.start_and_lap_slot)
        self.cancel_button.clicked.connect(self.cancel_slot)
        self.stop_button.clicked.connect(self.stop_slot)

        ###################################################################
        # Configuracion progress bar
        # self.start_and_lap.setEnabled(True)
        self.timer = None
        self.laps = []
        self.status = self.STOPPED
        self.start_and_lap.setText("Start")

    def start_and_lap_slot(self):
        if self.status == self.STOPPED:
            self.sender().emit_again = True
            self.status = self.STARTED

            self.timer = Timer()
            self.prueba_actual = Prueba(pacient_id=self.pacient.dni,
                                        datetime_of_test=datetime.datetime.now(),
                                        laps=self.timer.laps)
            self.timer.signaler.on_progress.connect(self.on_progress)
            UI.threadpool.start(self.timer)
            button_string = "Lap " + str(self.status + 1)
            self.start_and_lap.setText(button_string)

            self.stop_button.setEnabled(True)
            self.cancel_button.setEnabled(True)
        elif self.status == self.END:  # A acabado el ciclo.
            self.stop_slot()
            self.timer.lap()
            self.status = self.STOPPED
            self.cancel_button.setEnabled(False)
            self.stop_button.setEnabled(False)
            self.start_and_lap.setText("Start")
            self.finishedSignal.emit(self.prueba_actual, self.index)
            # self.laps.clear()  # Tengo que llevarlo a algun sitio
        else:  # Esta en ciclo.
            lap = self.timer.lap()
            self.progress_bar.setMaximun(lap)
            self.status += 1
            if self.status != self.END:
                button_string = "Lap " + str(self.status + 1)
            else:
                button_string = "End"
            self.start_and_lap.setText(button_string)

    def stop_slot(self):  # Paras el timer
        if self.status != self.STOPPED and self.timer is not None:
            self.cancel_button.setEnabled(False)
            self.stop_button.setEnabled(False)

            self.timer.stop()
            self.status = self.STOPPED
            self.start_and_lap.setText("Start")

    def cancel_slot(self):  # Reseteas el timer
        self.stop_slot()
        self.timer = None
        self.progress_bar.setValue(datetime.timedelta(seconds=0))

    def on_progress(self, timdelta: datetime.timedelta):
        self.sender().emit_again = False
        self.progress_bar.setValue(timdelta)
        self.statusChangeSlot.emit(f"{self.prueba_actual}", 1)
        self.sender().emit_again = True

    def init(self):
        super().init()


class MplCanvasTest(FigureCanvasQTAgg):
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

    def __init__(self, parent=None, width=5, height=4, dpi=100):
        PacientInterface.__init__(self)
        # fig = Figure(figsize=(width, height), dpi=dpi)
        # self.axes = fig.add_subplot(111)
        self.model = PruebasListModel.get_instance()
        self.fig, self.ax = pyplot.subplots()
        self.line_lap0 = None
        self.line_lap1 = None
        self.line_lap2 = None
        self.line_total = None
        self.markers0 = None
        self.markers1 = None
        self.markers2 = None
        self.markers_total = None

        super(MplCanvasTest, self).__init__(self.fig)
        FigureCanvasQTAgg.setSizePolicy(self, QSizePolicy.Expanding, QSizePolicy.Expanding)
        FigureCanvasQTAgg.updateGeometry(self)

class PerformanceTab(QWidget, PacientInterface):

    def __init__(self):
        super(PerformanceTab, self).__init__()
        PacientInterface.__init__(self)
        GUI_Resources.get_performance_widget(self)
        self.graph = MplCanvasTest()
        self.model: PruebasListModel = PruebasListModel.get_instance()
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

    def onPruebaClicked(self,*args):
        if self.graph.markers1 is not None:
            self.graph.markers0[0].set_marker(None)
            self.graph.markers1[0].set_marker(None)
            self.graph.markers2[0].set_marker(None)
            self.graph.markers_total[0].set_marker(None)
        row = args[0].row()
        prueba = self.model.get(row)
        total = prueba.laps[2].total_seconds() + prueba.laps[0].total_seconds() + prueba.laps[1].total_seconds()
        self.graph.markers0 = self.graph.ax.plot(prueba.datetime,prueba.laps[0].total_seconds(),marker="+", markersize=20, color="blue")
        self.graph.markers1 = self.graph.ax.plot(prueba.datetime, prueba.laps[1].total_seconds(), marker="+", markersize=20, color="green")
        self.graph.markers2 = self.graph.ax.plot(prueba.datetime, prueba.laps[2].total_seconds(), marker="+", markersize=20, color="brown")
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

                self.graph.line_lap0 = self.graph.ax.plot(date2num(dates), matplotlib.dates.num2date(test1), lw=0.75, label='lap1', color="blue",marker="o", markersize=2)
                self.graph.line_lap1 = self.graph.ax.plot(date2num(dates), matplotlib.dates.num2date(test2), lw=0.75, label='lap2', color="green",marker="o", markersize=2)
                self.graph.line_lap2 = self.graph.ax.plot(date2num(dates), matplotlib.dates.num2date(test3), lw=0.75, label='lap3', color="brown",marker="o", markersize=2)
                self.graph.line_total = self.graph.ax.plot(date2num(dates), matplotlib.dates.num2date(total), lw=0.75, label='Total', color="red",marker="o", markersize=2)

                self.graph.ax.xaxis.set_major_locator(MplCanvasTest.autox)
                self.graph.ax.xaxis.set_major_formatter(MplCanvasTest.formatterx)
                self.graph.ax.yaxis.set_major_formatter(MplCanvasTest.funcformatter)
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

if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    widget = GUI_Resources.get_graph_widget(QWidget())

    widget.widget = PerformanceTab()
    widget.show()
    app.exec_()
