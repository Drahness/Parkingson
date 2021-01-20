import datetime
import re
import threading

import cv2
import numpy
from PyQt5 import QtGui, QtCore
from PyQt5.QtCore import pyqtSignal, QPoint
from PyQt5.QtGui import QIntValidator, QPixmap, QImage
from PyQt5.QtWidgets import QWidget, QCalendarWidget, QDateEdit, QLabel, QComboBox, QLineEdit, QDoubleSpinBox, \
    QPushButton, QTabWidget, QToolButton, QFileDialog
from GUI.GUI_Resources import get_pacient_widget_ui, get_no_image_pixmap
from GUI.MenuBar import Menu
from GUI.actions import StaticActions
from GUI.tab_widgets import PacientInterface
from database.pacient import Pacient


class PacientWidget(QWidget, PacientInterface):
    no_image = get_no_image_pixmap()
    default_date = datetime.date(1990, 12, 12)
    finishedSignal: pyqtSignal = pyqtSignal(bool)  # maybe another name is better
    resultSignal: pyqtSignal = pyqtSignal(bool, int)
    """ bool if canceled or accepted. int, the row of the pacient or -1 if new pacient """

    def __init__(self, debug=False):
        PacientInterface.__init__(self)
        QWidget.__init__(self)
        get_pacient_widget_ui(self)
        # Variables.
        self.combo_items = ["", "0", "1", "1.5", "2", "2.5", "3", "4", "5"]
        self.gender_items = ["", "Hombre", "Mujer"]
        self.debug = debug
        self.on_focus = True
        # Declaramos los objetos
        self.nacimiento_calendar: QCalendarWidget = self.nacimiento_calendar
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
        self.diagnostico_tool: QToolButton = self.diagnostico_tool
        self.nacimiento_tool: QToolButton = self.nacimiento_tool
        self.error_apellidos: QLabel = self.error_apellidos
        self.error_dni: QLabel = self.error_dni
        self.error_estadio: QLabel = self.error_estadio
        self.error_nombre: QLabel = self.error_nombre
        self.error_telefono: QLabel = self.error_telefono
        self.error_gender: QLabel = self.error_gender
        self.error_email: QLabel = self.error_email
        self.gender_combo_box: QComboBox = self.gender_combo_box
        self.diagnostico_date_edit: QDateEdit = self.diagnostico_date_edit
        self.cara_image: QLabel = self.cara_image
        self.cuerpo_image: QLabel = self.cuerpo_image
        self.current_calendar: QLabel = self.current_calendar
        self.diagnostico_calendar: QCalendarWidget = self.diagnostico_calendar
        self.accept_button: QPushButton = self.accept_button
        self.cancel_button: QPushButton = self.cancel_button
        self.foto_tab: QTabWidget = self.foto_tab
        self.context_button: QToolButton = self.context_button
        # Fin declaracion
        # Conexiones
        self.peso_edit.editingFinished.connect(self.calculate_imc)
        self.altura_edit.editingFinished.connect(self.calculate_imc)
        self.peso_edit.valueChanged.connect(self.calculate_imc)
        self.altura_edit.valueChanged.connect(self.calculate_imc)
        self.accept_button.clicked.connect(self.buttons)
        self.cancel_button.clicked.connect(self.buttons)
        # Fin conexion
        # Conexion Calendarios.
        self.nacimiento_calendar.clicked.connect(self.on_calendar_changed)
        self.nacimiento_field.dateChanged.connect(self.on_calendar_changed)
        self.diagnostico_date_edit.dateChanged.connect(self.on_calendar_changed)
        self.diagnostico_calendar.clicked.connect(self.on_calendar_changed)
        self.diagnostico_tool.clicked.connect(self.activate_calendar)
        self.nacimiento_tool.clicked.connect(self.activate_calendar)
        # Fin conexion calendarios
        # Formateamos ciertas cosas.
        self.gender_combo_box.addItems(self.gender_items)
        self.estadio_combo_box.addItems(self.combo_items)
        self.diagnostico_calendar.setVisible(False)
        self.nacimiento_calendar.setVisible(False)
        self.altura_edit.setDecimals(2)
        self.peso_edit.setDecimals(2)
        self.altura_edit.setSingleStep(0.01)
        self.peso_edit.setRange(0, 500)
        self.altura_edit.setRange(0, 3.0)

        self.menu = Menu()
        self.action_select_pic = self.menu.addAction(StaticActions.seleccionar_foto)
        self.action_select_pic.triggered.connect(self.take_picture)
        self.action_take_pic = self.menu.addAction(StaticActions.tomar_foto)
        self.action_take_pic.triggered.connect(self.take_picture)

        self.context_button.clicked.connect(self.popup_context_menu)
        self.consejo_imc.setVisible(False)  # TODO Cambiar cuando acabe con el objeto settings
        self.pacientSelected(None)
        self.set_enabled(False)

    def popup_context_menu(self, *args):
        widget = self.sender()
        x = 0
        y = 0
        while widget.parent() is not None:
            x += widget.pos().x()
            y += widget.pos().y()
            widget = widget.parent()
        x += widget.pos().x() + 15
        y += widget.pos().y() - 10
        point = QPoint(x, y)
        self.menu.popup(point)

    def save_pacient(self):
        """Updates the instance."""
        combo_index = self.estadio_combo_box.currentIndex()
        gender_index = self.gender_combo_box.currentIndex()
        if self.pacient is not None:
            self.pacient.dni = self.dni_field.text()
            self.pacient.apellidos = self.apellidos_field.text()
            self.pacient.nombre = self.nombre_field.text()
            self.pacient.nacimiento = self.nacimiento_field.date()
            self.pacient.notas = self.notas_field.toPlainText()
            self.pacient.estadio = self.estadio_combo_box.itemText(combo_index)
            self.pacient.direccion = self.direccion_edit.text()
            self.pacient.fecha_diagnostico = self.diagnostico_date_edit.date()
            self.pacient.altura = self.altura_edit.value()
            self.pacient.peso = self.peso_edit.value()
            self.pacient.genero = self.gender_combo_box.itemText(gender_index)
            self.pacient.mail = self.email_edit.text()
            self.pacient.telefono = self.telefono_edit.text()
            barray_body = QtCore.QByteArray()
            barray_face = QtCore.QByteArray()
            buff_body = QtCore.QBuffer(barray_body)
            buff_face = QtCore.QBuffer(barray_face)
            buff_face.open(QtCore.QIODevice.WriteOnly)
            buff_body.open(QtCore.QIODevice.WriteOnly)
            if self.cara_image.pixmap() != self.no_image:
                pass
                ok = self.cara_image.pixmap().save(buff_face, "PNG")
                assert ok
                self.pacient.fotocara = barray_face.data()
            else:
                self.pacient.fotocara = None  # TODO

            if self.cuerpo_image.pixmap() != self.no_image:

                ok = self.cuerpo_image.pixmap().save(buff_body, "PNG")
                assert ok
                self.pacient.fotocuerpo = barray_body.data()
            else:
                self.pacient.fotocuerpo = None  # TODO
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
            # self.pacient = None
            threading.Thread(target=self.set_pics_worker,
                             args=(self.pacient.fotocara, self.pacient.fotocuerpo,)).start()
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
                altura = pacient.get("altura", default=0)
                mail = pacient.get("mail")
                fotocuerpo = pacient.get("fotocuerpo")
                fotocara = pacient.get("fotocara")
                telefono = pacient.get("telefono")
                direccion = pacient.get("direccion")
                peso = pacient.get("peso", default=0)
                fecha_diagnostico = pacient.get("fecha_diagnostico", default=self.default_date)
            elif isinstance(pacient, Pacient):
                dni = pacient.dni
                nombre = pacient.nombre
                apellidos = pacient.apellidos
                estadio = pacient.estadio or 0
                nacimiento = pacient.nacimiento or self.default_date
                notas = pacient.notas
                genero = pacient.genero
                altura = pacient.altura or 0
                mail = pacient.mail
                fotocuerpo = pacient.fotocuerpo  # TODO
                fotocara = pacient.fotocara  # TODO
                telefono = pacient.telefono
                direccion = pacient.direccion
                peso = pacient.peso or 0
                fecha_diagnostico = pacient.fecha_diagnostico or self.default_date
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
            telefono = ""
            direccion = None
            peso = 0
            fecha_diagnostico = self.default_date

        if estadio is not None and self.combo_items.count(str(estadio)):
            estadio_index = self.combo_items.index(str(estadio))
        else:
            if isinstance(estadio, float) and estadio.is_integer():
                estadio_index = self.combo_items.index(str(estadio.as_integer_ratio()[0]))
            else:
                estadio_index = 0
        if self.gender_items.count(genero):
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
        self.nacimiento_calendar.setSelectedDate(nacimiento)
        self.telefono_edit.setValidator(QIntValidator())
        self.diagnostico_date_edit.setDate(fecha_diagnostico)
        self.direccion_edit.setText(direccion)
        self.altura_edit.setValue(altura)
        self.peso_edit.setValue(peso)
        self.gender_combo_box.itemText(gender_index)
        self.email_edit.setText(mail)
        self.telefono_edit.setText(str(telefono))
        threading.Thread(target=self.set_pics_worker, args=(fotocara, fotocuerpo,)).start()
        self.calculate_imc()

    def set_enabled(self, enabled: bool):
        self.dni_field.setEnabled(enabled)
        self.apellidos_field.setEnabled(enabled)
        self.nombre_field.setEnabled(enabled)
        self.estadio_combo_box.setEnabled(enabled)
        self.nacimiento_field.setEnabled(enabled)
        self.notas_field.setEnabled(enabled)
        self.nacimiento_calendar.setEnabled(enabled)
        self.diagnostico_calendar.setEnabled(enabled)
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
        self.context_button.setEnabled(enabled)
        self.imc_result.setEnabled(enabled)
        self.finishedSignal.emit(not enabled)

    def pacient_selected(self) -> bool:
        return self.pacient is not None

    def calculate_imc(self):
        peso = self.peso_edit.value()
        altura = self.altura_edit.value()
        if altura != 0:
            self.imc_result.setText(str(round(peso / (altura * altura), 3)))
        else:
            self.imc_result.setText("NaN")
        # https://www.seedo.es/index.php/pacientes/calculo-imc

    def take_picture(self):
        if self.sender() == self.action_take_pic:
            cam = cv2.VideoCapture(0)
            window_name = "Pulsa ESC para salir. Espacio para tomar la foto"
            ret, frame = cam.read()
            cv2.imshow(window_name, frame)
            while cv2.getWindowProperty(window_name, cv2.WND_PROP_VISIBLE) >= 1:
                ret, frame = cam.read()
                if not ret:
                    break
                cv2.imshow(window_name, frame)
                k = cv2.waitKey(1)
                if k % 256 == 27:
                    cv2.destroyWindow(window_name)
                    break
                elif k % 256 == 32:
                    buffer = cv2.imencode("test.jpg", frame)[1]
                    image: numpy.ndarray = cv2.imdecode(buffer, cv2.IMREAD_UNCHANGED)
                    cam.release()
                    cv2.destroyWindow(window_name)
                    qformat = QImage.Format_Indexed8
                    size = image.shape
                    step = image.size / size[0]
                    if len(size) == 3:
                        if size[2] == 4:
                            qformat = QImage.Format_RGBA8888
                        else:
                            qformat = QImage.Format_RGB888
                    img = QImage(image, size[1], size[0], step, qformat)
                    img = img.rgbSwapped()
                    pixmap = QPixmap(QPixmap.fromImage(img))
                    if self.foto_tab.currentWidget() == self.cara_tab:
                        self.cara_image.setPixmap(pixmap)
                        pass
                    elif self.foto_tab.currentWidget() == self.cuerpo_tab:
                        self.cuerpo_image.setPixmap(pixmap)
                    break

        elif self.sender() == self.action_select_pic:
            file_dialog = QFileDialog()
            # file_dialog.setAcceptMode()
            chosen_file = file_dialog.getOpenFileName(filter="Image Files (*.png *.jpg *.jpeg *.bmp)")
            if chosen_file != '':
                bites = open(chosen_file[0], "br").read()
                if self.foto_tab.currentWidget() == self.cara_tab:
                    self.pacient.fotocara = bites
                    pixmap = QPixmap()
                    pixmap.loadFromData(bites)
                    self.cara_image.setPixmap(pixmap)
                    pass
                elif self.foto_tab.currentWidget() == self.cuerpo_tab:
                    self.pacient.fotocuerpo = bites
                    pixmap = QPixmap()
                    pixmap.loadFromData(bites)
                    self.cuerpo_image.setPixmap(pixmap)
        else:
            pass

    def activate_calendar(self):
        name = self.sender().objectName()
        if name == "nacimiento_tool":
            if self.nacimiento_calendar.isVisible():
                self.nacimiento_calendar.setVisible(False)
                self.current_calendar.setVisible(False)
            else:
                self.current_calendar.setVisible(True)
                self.current_calendar.setText("Fecha de nacimiento:")
                self.diagnostico_calendar.setVisible(False)
                self.nacimiento_calendar.setVisible(True)
        if name == "diagnostico_tool":
            if self.diagnostico_calendar.isVisible():
                self.diagnostico_calendar.setVisible(False)
                self.current_calendar.setVisible(False)
            else:
                self.current_calendar.setVisible(True)
                self.nacimiento_calendar.setVisible(False)
                self.current_calendar.setText("Fecha de diagnostico:")
                self.diagnostico_calendar.setVisible(True)

    def on_calendar_changed(self, *args):
        name = self.sender().objectName()
        if name == self.nacimiento_calendar.objectName() or name == self.nacimiento_field.objectName():
            self.nacimiento_calendar.setSelectedDate(args[0])
            self.nacimiento_field.setDate(args[0])
        elif name == self.diagnostico_calendar.objectName() or name == self.diagnostico_date_edit.objectName():
            self.diagnostico_calendar.setSelectedDate(args[0])
            self.diagnostico_date_edit.setDate(args[0])

    def set_pic_from_raw_worker(self, frame):
        buffer = cv2.imencode("test.jpg", frame)[1]
        image: numpy.ndarray = cv2.imdecode(buffer, cv2.IMREAD_UNCHANGED)
        qformat = QImage.Format_Indexed8
        size = image.shape
        step = image.size / size[0]
        if len(size) == 3:
            if size[2] == 4:
                qformat = QImage.Format_RGBA8888
            else:
                qformat = QImage.Format_RGB888
        img = QImage(image, size[1], size[0], step, qformat)
        # img = img.rgbSwapped()
        pixmap = QPixmap(QPixmap.fromImage(img))
        if self.foto_tab.currentWidget() == self.cara_tab:
            self.cara_image.setPixmap(pixmap)
            pass
        elif self.foto_tab.currentWidget() == self.cuerpo_tab:
            self.cuerpo_image.setPixmap(pixmap)

    def set_pics_worker(self, fotocara, fotocuerpo):
        """its planned to be a thread worker."""
        if fotocara is not None and isinstance(fotocara, bytes):
            pix = QPixmap()
            pix.loadFromData(fotocara)
            self.cara_image.setPixmap(pix)
        else:
            self.cara_image.setPixmap(self.no_image)
        if fotocuerpo is not None and isinstance(fotocuerpo, bytes):
            pix = QPixmap()
            pix.loadFromData(fotocuerpo)
            self.cuerpo_image.setPixmap(pix)
        else:
            self.cuerpo_image.setPixmap(self.no_image)
