import datetime
import re

from PyQt5.QtCore import pyqtSignal
from PyQt5.QtGui import QIntValidator
from PyQt5.QtWidgets import QWidget, QCalendarWidget, QDateEdit, QLabel, QComboBox, QLineEdit, QDoubleSpinBox, \
    QPushButton
from VideoCapture import Device
from GUI.GUI_Resources import get_pacient_widget_ui
from GUI.tab_widgets import PacientInterface
from database.entities import Pacient


class PacientWidget(QWidget, PacientInterface):
    default_date = datetime.date(1990, 12, 12)
    finishedSignal: pyqtSignal = pyqtSignal(bool)  # maybe another name is better
    resultSignal: pyqtSignal = pyqtSignal(bool, int)
    """ bool if canceled or accepted. int, the row of the pacient or -1 if new pacient """

    def __init__(self, debug=False):
        PacientInterface.__init__(self)
        QWidget.__init__(self)
        get_pacient_widget_ui(self)
        #
        self.combo_items = ["", "0", "1", "1.5", "2", "2.5", "3", "4", "5"]
        self.gender_items = ["", "Hombre", "Mujer"]
        self.debug = debug
        self.on_focus = True
        # Declaramos los objetos
        self.calendarWidget: QCalendarWidget = self.calendarWidget
        self.nacimiento_field: QDateEdit = self.nacimiento_field
        self.estadio_combo_box: QComboBox = self.estadio_combo_box
        self.label_estadio: QLabel = self.label_estadio
        self.imc_result: QLabel = self.imc_result
        self.altura_edit: QDoubleSpinBox = self.altura_edit
        self.peso_edit: QDoubleSpinBox = self.peso_edit
        self.imc_label: QLabel = self.imc_label
        self.telefono_edit: QLineEdit = self.telefono_edit
        self.direccion_edit: QLineEdit = self.direccion_edit
        self.email_edit: QLineEdit = self.email_edit
        self.consejo_imc: QLabel = self.consejo_imc

        self.error_apellidos: QLabel = self.error_apellidos
        self.error_dni: QLabel = self.error_dni
        self.error_estadio: QLabel = self.error_estadio
        self.error_nombre: QLabel = self.error_nombre
        self.error_telefono: QLabel = self.error_telefono
        self.error_gender: QLabel = self.error_gender
        self.error_email: QLabel = self.error_email

        self.gender_combo_box: QComboBox = self.gender_combo_box
        self.diagnostico_date_edit: QDateEdit = self.diagnostico_date_edit
        self.peso_edit.editingFinished.connect(self.calculate_imc)
        self.altura_edit.editingFinished.connect(self.calculate_imc)
        self.peso_edit.valueChanged.connect(self.calculate_imc)
        self.altura_edit.valueChanged.connect(self.calculate_imc)
        self.gender_combo_box.addItems(self.gender_items)
        self.estadio_combo_box.addItems(self.combo_items)
        self.calendarWidget.clicked.connect(self.on_calendar_changed)
        self.nacimiento_field.dateChanged.connect(self.on_calendar_changed)

        self.altura_edit.setDecimals(2)
        self.peso_edit.setDecimals(2)
        self.altura_edit.setSingleStep(0.01)
        self.peso_edit.setRange(0, 500)

        self.altura_edit.setRange(0, 3.0)
        self.accept_button.clicked.connect(self.buttons)
        self.cancel_button.clicked.connect(self.buttons)
        self.accept_button: QPushButton = self.accept_button
        self.cancel_button: QPushButton = self.cancel_button

        self.consejo_imc.setVisible(False)  # TODO Cambiar cuando acabe con el objeto settings
        self.pacientSelected(None)
        self.set_enabled(False)

    def save_pacient(self):
        """Updates the instance."""
        combo_index = self.estadio_combo_box.currentIndex()
        gender_index = self.gender_combo_box.currentIndex()

        self.pacient.dni = self.dni_field.text()
        self.pacient.apellidos = self.apellidos_field.text()
        self.pacient.nombre = self.nombre_field.text()
        self.pacient.nacimiento = self.nacimiento_field.date()
        self.pacient.notas = self.notas_field.toPlainText()
        self.pacient.estadio = self.estadio_combo_box.itemText(combo_index)
        self.pacient.direccion = self.direccion_edit.text()
        self.pacient.fecha_diagnostico = self.nacimiento_field.date()
        self.pacient.altura = self.altura_edit.value()
        self.pacient.peso = self.peso_edit.value()
        self.pacient.genero = self.gender_combo_box.itemText(gender_index)
        self.pacient.mail = self.email_edit.text()
        self.pacient.telefono = self.telefono_edit.text()
        self.pacient.fotocara = 0x000000  # TODO
        self.pacient.fotocuerpo = 0x000000  # TODO
        return self.pacient

    def check_input(self):
        errored = False
        combo_index = self.estadio_combo_box.currentIndex()
        gender_index = self.gender_combo_box.currentIndex()
        if not re.fullmatch("((([X-Z])|([LM])){1}([-]?)((\d){7})([-]?)([A-Z]{1}))|((\d{8})([-]?)([A-Z]))",
                            self.dni_field.text()) and not re.fullmatch("/^[0-9]{8}[TRWAGMYFPDXBNJZSQVHLCKE]$/i",
                                                                        self.dni_field.text()) and not self.debug:
            errored = True
            self.error_dni.setText("No has introducido un documento de identidad valido.")
        if not len(self.apellidos_field.text()) > 0 and not self.debug:
            errored = True
            self.error_apellidos.setText("Este campo no debe estar vacio.")
        if not len(self.nombre_field.text()) > 0 and not self.debug:
            errored = True
            self.error_nombre.setText("Este campo no debe estar vacio.")
        if self.estadio_combo_box.itemText(combo_index) == "" and not self.debug:
            errored = True
            self.error_estadio.setText("No has introducido un estadio valido.")
        if re.match("[^@]+@[^@]+\.[^@]+", self.email_edit.text()) and not self.debug:  # TODO
            errored = True
            self.error_email.setText("No has introducido un email valido.")
        if self.gender_combo_box.itemText(gender_index) == "" and not self.debug:
            errored = True
            self.error_gender.setText("No has introducido un genero valido.")
        if self.altura_edit.value() == 0 and not self.debug:
            errored = True
            self.error_altura.setText("No has introducido la altura del paciente.")
        if self.peso_edit.value() == 0 and not self.debug:
            errored = True
            self.error_peso.setText("No has introducido el peso del paciente.")
        if self.telefono_edit.text() == "" and not self.debug:
            errored = True
            self.error_telefono.setText("No has introducido el telefono del paciente.")
        return not errored

    def buttons(self, *args):
        name = self.sender().objectName()
        print(name)
        self.error_dni.setText("")
        self.error_estadio.setText("")
        self.error_nombre.setText("")
        self.error_telefono.setText("")
        self.error_apellidos.setText("")
        self.error_gender.setText("")
        self.error_email.setText("")
        self.error_peso.setText("")
        if name == "accept_button":
            if self.save_pacient():
                if self.check_input():
                    self.resultSignal.emit(True, self.index)
                    self.set_enabled(False)
        elif name == "cancel_button":
            if self.save_pacient():
                self.pacient = None
                self.resultSignal.emit(False, -1)
                self.set_enabled(False)

    def pacientSelected(self, pacient: Pacient, row: int = None):
        """Overriden method from PacientInterface"""
        self.index = row
        if pacient is not None:
            if isinstance(pacient, dict):  # Por si acaso
                dni = pacient.get("dni")
                nombre = pacient.get("nombre")
                apellidos = pacient.get("apellidos")
                estadio = pacient.get("estadio", default=0)
                nacimiento = pacient.get("nacimiento", default=self.default_date)
                notas = pacient.get("notas")
                genero = pacient.get("genero")
                altura = pacient.get("altura")
                mail = pacient.get("mail")
                fotocuerpo = pacient.get("fotocuerpo")
                fotocara = pacient.get("fotocara")
                telefono = pacient.get("telefono")
                direccion = pacient.get("direccion")
                peso = pacient.get("peso")
                fecha_diagnostico = pacient.get("fecha_diagnostico", default=self.default_date)
            elif isinstance(pacient, Pacient):
                dni = pacient.dni
                nombre = pacient.nombre
                apellidos = pacient.apellidos
                estadio = pacient.estadio or 0
                nacimiento = pacient.nacimiento or self.default_date
                notas = pacient.notas
                genero = pacient.genero
                altura = pacient.altura
                mail = pacient.mail
                fotocuerpo = pacient.fotocuerpo  # TODO
                fotocara = pacient.fotocara  # TODO
                telefono = pacient.telefono
                direccion = pacient.direccion
                peso = pacient.peso
                fecha_diagnostico = pacient.fecha_diagnostico
            else:
                raise AssertionError()
        else:
            dni = None
            nombre = None
            apellidos = None
            estadio = None
            nacimiento = self.default_date
            notas = None
            genero = None
            altura = 0
            mail = None
            fotocuerpo = None  # TODO
            fotocara = None  # TODO
            telefono = None
            direccion = None
            peso = 0
            fecha_diagnostico = self.default_date
        if self.combo_items.count(estadio):
            estadio_index = self.combo_items.index(str(pacient.estadio))
        else:
            estadio_index = 0
        if self.combo_items.count(genero):
            gender_index = self.gender_items.index(pacient.genero)
        else:
            gender_index = 0
        self.pacient = pacient
        self.last_pacient = dni
        self.dni_field.setText(dni)
        self.apellidos_field.setText(apellidos)
        self.nombre_field.setText(nombre)
        self.estadio_combo_box.setCurrentIndex(estadio_index)
        self.gender_combo_box.setCurrentIndex(gender_index)
        self.nacimiento_field.setDate(nacimiento)
        self.notas_field.setText(notas)
        self.calendarWidget.setSelectedDate(nacimiento)
        self.telefono_edit.setValidator(QIntValidator())
        self.diagnostico_date_edit.setDate(fecha_diagnostico)
        self.direccion_edit.setText(direccion)
        self.altura_edit.setValue(altura)
        self.peso_edit.setValue(peso)
        self.gender_combo_box.itemText(gender_index)
        self.email_edit.setText(mail)
        self.telefono_edit.setText(str(telefono))
        self.calculate_imc()

    def set_enabled(self, enabled: bool):
        self.dni_field.setEnabled(enabled)
        self.apellidos_field.setEnabled(enabled)
        self.nombre_field.setEnabled(enabled)
        self.estadio_combo_box.setEnabled(enabled)
        self.nacimiento_field.setEnabled(enabled)
        self.notas_field.setEnabled(enabled)
        self.calendarWidget.setEnabled(enabled)
        self.cancel_button.setVisible(enabled)
        self.accept_button.setVisible(enabled)
        self.estadio_combo_box.setEnabled(enabled)
        self.altura_edit.setEnabled(enabled)
        self.peso_edit.setEnabled(enabled)
        self.telefono_edit.setEnabled(enabled)
        self.direccion_edit.setEnabled(enabled)
        self.email_edit.setEnabled(enabled)
        self.consejo_imc.setEnabled(enabled)
        self.gender_combo_box.setEnabled(enabled)
        self.diagnostico_date_edit.setEnabled(enabled)
        self.error_dni.setEnabled(enabled)
        self.error_estadio.setEnabled(enabled)
        self.error_nombre.setEnabled(enabled)
        self.imc_result.setEnabled(enabled)
        self.finishedSignal.emit(not enabled)

    def on_calendar_changed(self, *args):
        self.calendarWidget.setSelectedDate(args[0])
        self.nacimiento_field.setDate(args[0])

    def pacient_selected(self) -> bool:
        return self.pacient is not None

    def calculate_imc(self):
        peso = self.peso_edit.value()
        altura = self.altura_edit.value()
        if altura != 0:
            self.imc_result.setText(str(peso / (altura * altura)))
        else:
            self.imc_result.setText("NaN")
        # https://www.seedo.es/index.php/pacientes/calculo-imc

    def take_picture(self): # TODO
        cam = Device()
        cam.saveSnapshot('image.jpg');