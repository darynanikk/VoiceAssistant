from PyQt6.QtWidgets import *
import sys


class ComboBoxLanguages(QWidget):
    languageStrings = ["English", "French", "German", "Quenya"]
    label1Strings = ["Hello", "Bonjour", "Hallo", "Namárië"]
    label2Strings = ["Farewell", "Bon Voyage", "Auf Wiedersehen", "Navaer"]

    def __init__(self):
        super().__init__()
        self.lang = self.languageStrings[0]

        self.combobox1 = QComboBox(self)
        self.combobox1.setGeometry(130, 70, 60, 40)
        [self.combobox1.addItem(lang) for lang in self.languageStrings]
        self.combobox1.currentTextChanged.connect(self.on_combobox_changed)

        self.msgLabel = QLabel(self.label1Strings[0], self)
        self.msgLabel.setGeometry(130, 120, 300, 80)

        self.msg2Label = QLabel(self.label2Strings[0], self)
        self.msg2Label.setGeometry(230, 120, 300, 80)

        self.setWindowTitle('Combobox Language Example')
        self.setGeometry(10, 10, 400, 200)

        self.move(850, 300)
        self.show()

    def on_combobox_changed(self, value):
        self.lang = value
        languageIndex = self.languageStrings.index(value)
        self.msgLabel.setText(self.label1Strings[languageIndex])
        self.msg2Label.setText(self.label2Strings[languageIndex])


app = QApplication(sys.argv)
button = ComboBoxLanguages()
app.exec()