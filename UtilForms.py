from PyQt5.QtWidgets import QVBoxLayout, QWidget, QLineEdit, QLabel, QHBoxLayout


class Form(QWidget):
    def __init__(self,json: dict,editable :bool= True):
        super(Form, self).__init__()
        mainLay = QVBoxLayout()
        self.childss = []
        self.json = json
        self.setLayout(mainLay)
        for key, value in json.items():
            widget = CustomWidget(key,value,json,editable)
            mainLay.addWidget(widget)
            self.childss.append(widget)

    def turnEditable(self,editable):
        return Form(self.json, editable)

    def save(self):
        for child in self.childss:
            child.changed()
        self.turnEditable(False)


class CustomWidget(QWidget):
    def __init__(self, key, value, json, editable: bool= True):
        super(CustomWidget, self).__init__()
        self.json = json
        self.key = key
        self.value = value
        secondaryLay = QHBoxLayout()
        secondaryLay.addWidget(QLabel(key))
        if editable:
            self.edit = QLineEdit(str(value))
            self.edit.returnPressed.connect(self.changed)
            secondaryLay.addWidget(self.edit)
        else:
            self.text = QLabel(str(value))
            secondaryLay.addWidget(self.text)

        self.setLayout(secondaryLay)

    def changed(self):
        try:
            self.json[self.key] = self.edit.text()
        except AttributeError:
            pass

    def turnEditable(self):
        return CustomWidget(self.key, self.value, self.json)