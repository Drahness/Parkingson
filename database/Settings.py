from datetime import timedelta

import typing
from PyQt5.QtCore import QSettings, QSize, pyqtSignal


class Settings(QSettings):
    change_signal = pyqtSignal(str)
    _keys = {}

    def __init__(self, scope: QSettings.Scope, organization, application_name):
        super(Settings, self).__init__(scope, organization, application_name)
        for key in self.allKeys():
            self._keys[key] = []

    def set_value_if_not_present(self, key: str, value: typing.Any) -> None:
        if key not in self.allKeys():
            self.setValue(key, value)

    def syncWorker(self):
        memo_values = self.__keys.copy()
        while True:
            for key in self.__keys:
                pass

    def attach_to(self, key, method_to_be_called):
        self._keys[key].append(method_to_be_called)


class SystemSettings(Settings):
    FULLSCREEN = "fullscreen"
    SIZE = "size"
    POSITION = "position"

    def __init__(self, scope: QSettings.Scope = QSettings.SystemScope):
        super(SystemSettings, self).__init__(scope, "Sofistically Fair Inheritance", "InRellity")
        self.set_value_if_not_present(self.FULLSCREEN, False)
        self.set_value_if_not_present(self.SIZE, 0)
        self.set_value_if_not_present(self.POSITION, 0)


class UserSettings(SystemSettings):
    LAP_NAME_FORMAT = "lap{}_name"
    LAP_LOWMEDIUM_FORMAT = "lap{}_lowmedium_start"
    LAP_MEDIUMHARD_FORMAT ="lap{}_mediumhard_start"
    LAP3_NAME = "Acabar"
    LAP0_NAME = "lap0_name"
    LAP1_NAME = "lap1_name"
    LAP2_NAME = "lap2_name"
    LAP_TOTAL_NAME = "lap_total_name"
    LAP_NUMBER = "lap_total_name"
    LAP0_LOWMEDIUM_START = "lap0_lowmedium_start"
    LAP1_LOWMEDIUM_START = "lap1_lowmedium_start"
    LAP2_LOWMEDIUM_START = "lap2_lowmedium_start"
    LAP0_MEDIUMHARD_START = "lap0_mediumhard_start"
    LAP1_MEDIUMHARD_START = "lap1_mediumhard_start"
    LAP2_MEDIUMHARD_START = "lap2_mediumhard_start"

    def get_lap_name(self, lap: int):
        return self.value(self.LAP_NAME_FORMAT.format(lap))

    def get_lap_time(self, lap:int, importance: int):
        if importance % 2 == 0:
            return self.value(self.LAP_LOWMEDIUM_FORMAT.format(lap))
        elif importance % 2 == 1:
            return self.value(self.LAP_MEDIUMHARD_FORMAT.format(lap))

    def __init__(self, username):
        super(UserSettings, self).__init__(QSettings.UserScope)
        self.beginGroup(username)
        self.set_value_if_not_present(self.LAP0_NAME, "Marcha")
        self.set_value_if_not_present(self.LAP1_NAME, "Equilibrio")
        self.set_value_if_not_present(self.LAP2_NAME, "Doble Tarea")
        self.set_value_if_not_present(self.LAP3_NAME, "Finalizar")
        self.set_value_if_not_present(self.LAP_TOTAL_NAME, "Circuit")
        self.set_value_if_not_present(self.LAP_NUMBER, 3)
        self.set_value_if_not_present(self.LAP0_LOWMEDIUM_START, timedelta(seconds=17, microseconds=160000))
        self.set_value_if_not_present(self.LAP1_LOWMEDIUM_START, timedelta(seconds=15, microseconds=140000))
        self.set_value_if_not_present(self.LAP2_LOWMEDIUM_START, timedelta(seconds=10, microseconds=430000))
        self.set_value_if_not_present(self.LAP0_MEDIUMHARD_START, timedelta(seconds=23, microseconds=560000))
        self.set_value_if_not_present(self.LAP1_MEDIUMHARD_START, timedelta(seconds=25, microseconds=900000))
        self.set_value_if_not_present(self.LAP2_MEDIUMHARD_START, timedelta(seconds=13, microseconds=340000))
