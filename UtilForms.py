from PyQt5.QtWidgets import QVBoxLayout, QWidget, QLineEdit, QLabel, QHBoxLayout


class Form(QWidget):
    def __init__(self,departmentJSON: dict,editable :bool= True):
        super(Form, self).__init__()
        mainLay = QVBoxLayout()
        self.childss = []
        self.departmentJSON = departmentJSON
        self.setLayout(mainLay)
        for key, value in departmentJSON.items():
            widget = CustomWidget(key,value,departmentJSON,editable)
            mainLay.addWidget(widget)
            self.childss.append(widget)

    def turnEditable(self,editable):
        return Form(self.departmentJSON,editable)

    def save(self):
        for child in self.childss:
            child.changed()
        self.turnEditable(False)

class CustomWidget(QWidget):
    def __init__(self, key,value,departmentJSON,editable: bool= True):
        super(CustomWidget, self).__init__()
        self.departmentJSON = departmentJSON
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
            self.departmentJSON[self.key] = self.edit.text()
        except AttributeError:
            pass

    def turnEditable(self):
        return CustomWidget(self.key,self.value,self.departmentJSON)
