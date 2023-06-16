import uuid
from typing import List

import couchdb
import openai
import os
from os.path import dirname, normpath

from PyQt6.QtCore import QDir

from PyQt6.QtGui import QAction, QImage, QPixmap, QIcon
from PyQt6.QtWidgets import QStyleFactory, QSizePolicy
from PyQt6.QtWidgets import QApplication, QMainWindow, QPushButton, QLabel, QTextEdit, QWidget, QVBoxLayout, QToolBar, \
    QTableWidget, QTableWidgetItem, QCheckBox
from PyQt6.QtCore import Qt, QThread, pyqtSignal, QUrl
import speech_recognition as sr
from word2number import w2n

from controller.impl import MouseController, TypingController, SearchController, HoldingController, PressingController, \
    HotKeyController

controllers = {
    'mouse': MouseController(), 'type': TypingController(),
    'search': SearchController(), 'hold': HoldingController(),
    'press': PressingController(), 'hotkey': HotKeyController()
}

QDir.addSearchPath("icons", r"C:\dev\VoiceAssistant2\resources\icons")


class CouchDBConnector:
    def __init__(self, server_url, database_name, username, password):
        self.server_url = server_url
        self.database_name = database_name
        self.username = username
        self.password = password
        self.couchdb_server = couchdb.Server(server_url)
        self.couchdb_server.resource.credentials = (username, password)

    def write_data(self, data):
        db = self.couchdb_server[self.database_name]
        document_id = str(uuid.uuid4())
        db[document_id] = data

    def find_by_key(self, key):
        db = self.couchdb_server[self.database_name]
        query = {
            'selector': {
                key: {
                    "$ne": None,
                }
            },
            'fields': [key]
        }
        try:
            for doc in db.find(query):
                return doc[key]
        except KeyError:
            print(f"document was not found by key {key}")

    def find_by_value(self, key, value, fields):
        db = self.couchdb_server[self.database_name]
        query = {
            'selector': {
                key: {
                    "$eq": value,
                    "$ne": None,
                }
            },

            'fields': fields
        }
        try:
            row = db.find(query)
            return list(row)[0]
        except IndexError:
            print(f"document was not found by value {value}")

    def get_query_size(self, key):
        db = self.couchdb_server[self.database_name]

        query = {
            "selector": {
                key: {
                    "$ne": None,
                }
            },
            "fields": [key],
        }
        print(len(list(db.find(query))))
        return len(list(db.find(query)))

    def get_query(self, *query_params):
        key_rules = []
        for k in query_params:
            key_rule = {
                k: {
                    "$ne": None
                }
            }
            key_rules.append(key_rule)
        db = self.couchdb_server[self.database_name]
        query = {
            "selector": {
                '$and': key_rules
            },
            "fields": [*query_params],
        }
        return list(db.find(query))


class AudioListener(QThread):
    recognized = pyqtSignal(str)

    def __init__(self):
        super().__init__()
        self.recognizer = sr.Recognizer()
        self.microphone = sr.Microphone()
        self.stop_listening = None

    def start_voice_assistant(self, callback):
        with self.microphone as source:
            self.recognizer.adjust_for_ambient_noise(source)

        self.stop_listening = self.recognizer.listen_in_background(self.microphone, callback)

    def stop(self):
        if self.stop_listening:
            self.stop_listening(wait_for_stop=False)


class ViewDataWindow(QWidget):
    def __init__(self, icon_path: str, title: str, connector: CouchDBConnector, header_labels: [], *query_params):
        super().__init__()
        icon = QIcon(icon_path)
        self.setWindowIcon(icon)
        self.setWindowTitle(title)
        self.table = QTableWidget()
        self.table.setSortingEnabled(True)
        self.connector = connector
        self.query_params = query_params
        self.setGeometry(100, 100, 400, 300)

        # Create a layout
        self.layout = QVBoxLayout(self)
        self.table_current_size = None
        # Refresh macros
        self.refresh_button = QPushButton("Refresh", self)
        data = self.connector.get_query(*query_params)

        self.construct_info_table(data)
        self.table.setHorizontalHeaderLabels(header_labels)

        # Add the table widget to the layout
        self.layout.addWidget(self.table)

        self.layout.addWidget(self.refresh_button)
        self.refresh_button.clicked.connect(self.on_refresh)

        # Set the layout on the QWidget
        self.setLayout(self.layout)

    def construct_info_table(self, data: []):
        pass

    def on_refresh(self):
        data = self.connector.get_query(*self.query_params)
        new_size = len(data)

        if self.table_current_size and new_size > self.table_current_size:
            print("updated")
            self.construct_info_table(data)
            self.table_current_size = new_size
            self.table.update()


class ViewMacrosWindow(ViewDataWindow):
    def __init__(self, icon_path: str, title: str, connector: CouchDBConnector, *query_params):
        super().__init__(icon_path, title, connector, *query_params)

    def construct_info_table(self, data: []):

        self.table.setColumnCount(2)

        macros_data = []

        for doc in data:
            macros_name, macros_action = doc.values()
            macros_data.append([macros_name, ','.join(macros_action)])

        self.table.setRowCount(len(macros_data))
        self.table_current_size = len(macros_data)

        for row, rowData in enumerate(macros_data):
            for col, value in enumerate(rowData):
                item = QTableWidgetItem(value)

                self.table.setItem(row, col, item)


class ViewHotkeysWindow(ViewDataWindow):

    def __init__(self, icon_path: str, title: str, connector: CouchDBConnector, *query_params):
        super().__init__(icon_path, title, connector, *query_params)

    def construct_info_table(self, data: []):
        self.table.setColumnCount(2)

        objs = []

        for doc in data:
            for val in doc.values():

                for obj in val:
                    objs.append(obj)

        hotkeys = []
        for data in objs:

            for friendly_name, desc in data.items():
                hotkeys.append([friendly_name, ','.join(desc)])

        self.table.setRowCount(len(hotkeys))
        for row, rowData in enumerate(hotkeys):
            for col, value in enumerate(rowData):
                item = QTableWidgetItem(value)

                self.table.setItem(row, col, item)


class HelpWindow(QWidget):

    def __init__(self):
        super().__init__()
        icon_path = QDir.searchPaths("icons")[0] + '/help.png'
        icon = QIcon(icon_path)

        self.setWindowIcon(icon)
        self.setWindowTitle("Help")
        self.setMinimumSize(300, 150)
        layout = QVBoxLayout()

        self.setLayout(layout)
        self.label = QLabel(self)

        self.label.setText(
            "<html>"
            "<body style='line-height: 100%'>"
            "1. Для активації асистента натисніть кнопку \"Start\"."
            "<br>"
            "<br>2. Розпізнаний текст виводиться в основному вікні додатку."
            "<br>"
            "<br>3. Скажіть \"Help\" me для отримання інформації про можливі голосові команди."
            "<br>"
            "<br>4. Для перегляду збережених макросів натисніть кнопку \"View macros\"."
            "<br>"
            "<br>5. Для перегляду збережених макросів натисніть кнопку \"View macros\"."
            "<br>"
            "<br>5. Для надання дозволу застосування спеціальних символів поставте прапорець у полі Enable hotkey."
            "</body>"
            "</html>"
        )

        self.label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        layout.addWidget(self.label)


class VoiceAssistantWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.connector = CouchDBConnector("http://localhost:5984", "voice_assistant_db", "daryna", "password")
        self.audio_listener = AudioListener()
        self.help_window = HelpWindow()
        icons_path = QDir.searchPaths("icons")[0]
        self.macros_view_window = ViewMacrosWindow(icons_path + '/macros.png', "View Macros",
                                                   self.connector, ["Name", "Actions"], "macros_name", "macros_actions")
        self.hotkeys_view_window = ViewHotkeysWindow(icons_path + '/hotkey.png', "View Hotkeys",
                                                     self.connector, ["Hotkey", "Description"], "hotkeys")

        icon_path = QDir.searchPaths("icons")[0] + '/voice-input.png'
        icon = QIcon(icon_path)
        self.setWindowIcon(icon)
        self.setWindowTitle("Voice Assistant")
        # self.setGeometry(100, 100, 400, 300)  # Adjust the window size and position as needed
        self.setFixedSize(760, 400)

        self.setCentralWidget(QWidget())  # Set the central widget
        self.layout = QVBoxLayout(self.centralWidget())  # Set the layout

        self.label = QLabel("", self)
        self.layout.addWidget(self.label)

        self.text_edit = QTextEdit(self)
        self.text_edit.setFixedSize(300, 200)

        self.layout.addWidget(self.text_edit)
        self.layout.setAlignment(self.text_edit, Qt.AlignmentFlag.AlignCenter)

        self.start_button = QPushButton("Start", self)
        self.start_button.setSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)
        self.layout.addWidget(self.start_button, alignment=Qt.AlignmentFlag.AlignCenter)

        self.stop_button = QPushButton("Stop")
        self.stop_button.setSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)
        self.layout.addWidget(self.stop_button, alignment=Qt.AlignmentFlag.AlignCenter)
        self.stop_button.setEnabled(False)

        # toolbar
        self.toolbar = QToolBar("Home")
        self.addToolBar(self.toolbar)

        # Help
        self.help_button = QAction("Help", self)
        self.help_button.setStatusTip("Help")
        self.help_button.triggered.connect(self.on_help_button_click)
        self.toolbar.addAction(self.help_button)

        # Glossary
        self.hotkeys_button = QAction("View Hotkeys", self)
        self.hotkeys_button.setStatusTip("View Hotkeys")
        self.hotkeys_button.triggered.connect(self.on_hotkeys_view_button_click)
        self.toolbar.addAction(self.hotkeys_button)

        # Macros
        self.macros_button = QAction("View macros", self)
        self.macros_button.setStatusTip("View macros")
        self.macros_button.triggered.connect(self.on_macros_view_button_click)
        self.toolbar.addAction(self.macros_button)

        # Create a checkbox
        self.hotkey_checkbox = QCheckBox("Enable Hotkeys")
        self.hotkey_checkbox.setStyleSheet("QCheckBox { color: #CFE2DE; }")
        self.hotkey_checkbox.setChecked(False)
        self.layout.addWidget(self.hotkey_checkbox)

        self.start_button.clicked.connect(self.start_listening)
        self.stop_button.clicked.connect(self.stop_listening)
        self.hotkey_checkbox.stateChanged.connect(self.on_hotkey_checkbox_state_changed)
        self.hotkey_checkbox.stateChanged.connect(self.on_hotkey_checkbox_state_changed)
        self.add_macros = False
        self.hotkey_option_enabled = False
        self.macros_num = 0
        self.macros = []

    def on_help_button_click(self, checked):
        if self.help_window.isVisible():
            self.help_window.hide()

        else:
            self.help_window.show()

    def on_hotkey_checkbox_state_changed(self, state):
        if state == 2:
            print("Checkbox is checked")
            self.hotkey_option_enabled = True
        else:
            print("Checkbox is unchecked")
            self.hotkey_option_enabled = False

    def on_hotkeys_view_button_click(self):
        if self.hotkeys_view_window.isVisible():
            self.hotkeys_view_window.hide()

        else:
            self.hotkeys_view_window.show()

    def on_macros_view_button_click(self):
        if self.macros_view_window.isVisible():
            self.macros_view_window.hide()

        else:
            self.macros_view_window.show()

    def stop_listening(self):
        self.audio_listener.stop()
        self.start_button.setEnabled(True)
        self.stop_button.setEnabled(False)

    def start_listening(self):

        def callback(recognizer, audio):
            try:
                speech = recognizer.recognize_vosk(audio)

                text = speech[14:-3]

                if "macros" in text:
                    number = None
                    try:
                        number = w2n.word_to_num(text.split()[1])
                    except ValueError:
                        print(f"Cannot convert {number} to integer value")

                    if self.connector.find_by_value("macros_name", f'macros-{number}',
                                                    ["macros_name", "macros_actions"]):
                        _, macros_actions = self.connector.find_by_value("macros_name", f'macros-{number}',
                                                                         ["macros_name", "macros_actions"]).values()
                        print(macros_actions)
                        for action in macros_actions:
                            controller_type = action.split()[0]
                            controller = controllers.get(controller_type)
                            controller.process(action.split()[1:])

                if "create" in text:
                    self.add_macros = True
                    size = self.connector.get_query_size("macros_name")
                    size += 1
                    self.macros_num = size
                    self.text_edit.append("Creating macros...")

                if "stop" in text:
                    self.add_macros = False
                    print(self.macros_num)
                    print(self.macros)
                    data = {
                        "macros_name": f"macros-{self.macros_num}",
                        "macros_actions": self.macros
                    }
                    self.connector.write_data(data)
                    self.macros = []
                    self.text_edit.append("Macros created.")

                if not self.add_macros:

                    if self.hotkey_option_enabled:
                        hotkey_controller = controllers.get('hotkey')
                        hot_keys_list = self.connector.find_by_key("hotkeys")
                        try:
                            hotkey = list(filter(lambda map: map.get(text), hot_keys_list))[0]
                            hotkey_controller.process(*hotkey[text])
                        except IndexError:
                            print(f"Hotkey {text} does not exist.")

                    if "mouse" in text:
                        mouse_controller = controllers.get("mouse")
                        mouse_controller.process(text.split()[1:])

                    if "hold" in text:
                        hold_controller = controllers.get("hold")
                        hold_controller.process(text.split()[1:])

                    if "press" in text:
                        press_controller = controllers.get("press")
                        press_controller.process(text.split()[1:])

                    if "type" in text:
                        type_controller = controllers.get("type")
                        print(' '.join(text.split()[1:]))
                        type_controller.process(' '.join(text.split()[1:]))

                    if "search" in text:
                        search_controller = controllers.get("search")
                        question = ' '.join(text.split()[1:])
                        if self.connector.find_by_key(question):
                            print("data exists")
                            print(self.connector.find_by_key(question))
                            self.text_edit.append(self.connector.find_by_key(question))
                        else:
                            answer = search_controller.process(question)
                            data = {question: answer}
                            self.connector.write_data(data)
                            self.text_edit.append(self.connector.find_by_key(question))

                if text != "":
                    self.text_edit.append(speech)
                    if self.add_macros and "create" not in text:
                        self.macros.append(text)

            except sr.UnknownValueError:
                self.text_edit.append("Sorry, I couldn't understand that.")
            except sr.RequestError:
                self.text_edit.append("Sorry, I couldn't access the speech recognition service.")

        self.audio_listener.start_voice_assistant(callback)
        self.start_button.setEnabled(False)
        self.stop_button.setEnabled(True)


if __name__ == "__main__":
    app = QApplication([])
    app.setStyle(QStyleFactory.create('Fusion'))
    window = VoiceAssistantWindow()

    window.setStyleSheet("""
            QMainWindow {
                background-image: url('Voice.jpeg');
                background-repeat: no-repeat;
        }
       """)

    window.show()
    app.exec()

# TODO Voice assistant design

# TODO add window model is loading

# TODO come up with more hot key words
