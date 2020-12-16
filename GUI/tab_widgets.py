import datetime
import sys

import matplotlib
from PyQt5 import QtWidgets
from PyQt5.QtCore import pyqtSignal
from PyQt5.QtGui import QIntValidator
from PyQt5.QtWidgets import QWidget, QCalendarWidget, QDateEdit, QSizePolicy
from matplotlib import dates, ticker as ticker, pyplot as pyplot
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg
from matplotlib.dates import AutoDateLocator, ConciseDateFormatter, date2num

from GUI import GUI_Resources
from GUI.GUI_Resources import get_pacient_widget_ui, get_error_dialog_msg, get_cronometro_widget_ui, \
    get_cronometro_bar_widget
from GUI.cronometro import Timer
from database.entities import Pacient, Prueba
from database.models import PruebasListModel
import matplotlib

from main_window import UI

matplotlib.use('Qt5Agg')


class PacientInterface:
    """Los tabs heredan de esta. Ya que todos tienen casi la misma logica"""

    def __init__(self):
        self.last_pacient = None
        self.pacient = None
        self.index = None
        self.on_focus = False
        pass

    def pacientSelected(self, pacient, index):
        """The signal pacientSelected will get a Pacient and a row in the model."""
        self.pacient = pacient
        self.index = index

    def init(self):
        from main_window import UI
        UI.get_instance().pacientSelected.connect(self.pacientSelected)
        UI.get_instance().central.parent_tab_widget.currentChanged.connect(self.currentChanged)

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

    def buttons(self, *args):
        name = self.sender().objectName()
        print(name)
        if name == "accept_button":
            self.save_pacient()
            self.resultSignal.emit(True, self.index)
        elif name == "cancel_button":
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


class MplCanvas(FigureCanvasQTAgg, PacientInterface):
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
        super(MplCanvas, self).__init__(self.fig)
        FigureCanvasQTAgg.setSizePolicy(self, QSizePolicy.Expanding, QSizePolicy.Expanding)
        FigureCanvasQTAgg.updateGeometry(self)

    def currentChanged(self, index):
        super().currentChanged(index)
        if self.pacient is not None:
            self.pacientSelected(self.pacient,None)

    def pacientSelected(self, pacient, index):
        super().pacientSelected(pacient,index)
        if self.on_focus:
            self.load_graph(pacient)
        else:
            self.setVisible(False)
            pass

    def load_graph(self,pacient):
        self.setVisible(False)
        test1 = []
        test2 = []
        test3 = []
        total = []
        dates = []  # X axis
        try:
            self.setVisible(True)
            pruebas = self.model.get_pruebas(pacient)
            if len(pruebas) > 0:
                self.ax.clear()
                for x in range(0, len(pruebas)):
                    prueba = pruebas[x]
                    dates.append(prueba.datetime)

                    test1.append(prueba.laps[0].total_seconds())
                    test2.append(prueba.laps[1].total_seconds())
                    test3.append(prueba.laps[2].total_seconds())
                    total.append(test1[x] + test2[x] + test3[x])

                self.ax.plot(date2num(dates), matplotlib.dates.num2date(test1), lw=0.75, label='lap1')
                self.ax.plot(date2num(dates), matplotlib.dates.num2date(test2), lw=0.75, label='lap2')
                self.ax.plot(date2num(dates), matplotlib.dates.num2date(test3), lw=0.75, label='lap3')
                self.ax.plot(date2num(dates), matplotlib.dates.num2date(test3), lw=0.75, label='Total')

                self.ax.xaxis.set_major_locator(MplCanvas.autox)
                self.ax.xaxis.set_major_formatter(MplCanvas.formatterx)
                self.ax.yaxis.set_major_formatter(MplCanvas.funcformatter)

                self.ax.grid(True)
                self.ax.legend(frameon=False)

                for tick in self.ax.get_xticklabels():
                    tick.set_rotation(55)
            else:
                self.ax.clear()
            self.draw()
        except Exception as e:
            string = f"Error en la matriz {type(e).__name__} paciente {pacient.dni}\n"
            string += "Valores:\n"
            string += f"{dates}\n"
            string += f"{test1}\n"
            string += f"{test2}\n"
            string += f"{test3}"
            get_error_dialog_msg(e, string, "Error de insertacion").exec_()

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
        self.sender().emit_again = True

    def init(self):
        super().init()



if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    widget = GUI_Resources.get_graph_widget(QWidget())

    widget.widget = MplCanvas()
    widget.show()
    app.exec_()