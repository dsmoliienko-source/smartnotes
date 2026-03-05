from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QLabel, QLineEdit, QTextEdit, QListWidget, QInputDialog, QHBoxLayout, QVBoxLayout, QFormLayout
import os

app = QApplication([])
notes = []

STYLE = """
    QWidget {
        background-color: #082925;
        color: #EAFBF9;
        font-family: 'Segoe UI', Arial, sans-serif;
        font-size: 13px;
    }

    QTextEdit {
        background-color: #007854;
        color: #F5FFFC;
        border: 2px solid #004933;
        border-radius: 10px;
        font-size: 14px;
        selection-background-color: #00D797;
    }
    
    QLineEdit {
        background-color: #007854;
        color: #F5FFFC;
        border: 2px solid #004933;
        border-radius: 6px;
        selection-background-color: #00D797;
    }
    
    QLineEdit:focus {
        border: 2px solid #004900;
    }

    QListWidget {
        background-color: #007854;
        color: #F5FFFC;
        border: 2px solid #004933;
        border-radius: 6px;
        selection-background-color: #00D797;
    }
   
    QListWidget:item {
        padding: 6px 8px;
        border-raidus: 4px;
    }
    
    QListWidget:item:selected {
        background-color: #FF2854;
        color: #F5FFFC;
    }
    
    QListWidget:item:hover:!selected {
        background-color: #FF5874;
    }

    QLabel {
        font-weight: bold;
        font-size: 15px;
        color: #ffffff;
        padding: 4px 0px 2px 2px;
    }

    QPushButton {
        background-color: #ffffff;
        color: #000000;
        border: 2px solid #004933;
        border-radius: 6px;
        padding: 7px 12px;
        font-weight: bold;
    }
    QPushButton:hover {
        background-color: #000000;
        color: #ffffff;
    }
    QPushButton:pressed {
        background-color: #082925;
        color: #EAFBF9
    }

"""

'''

| Вікно |
'''
notes_win = QWidget()
notes_win.setWindowTitle("Smart Notes") #Назва програми
notes_win.resize(900,600) #Розмір програми
notes_win.setStyleSheet(STYLE)

'''
| Віджети вікна |
'''
#0 - Нотатка
field_text = QTextEdit()

#1 - Список нотаток
list_notes = QListWidget()
list_notes_label = QLabel("Список нотаток")

#2 - Кнопки для списку нотаток
button_notes_create = QPushButton("Створити Нотатку") #Поява вікна - "Дайте назву нотатці"
button_notes_delete = QPushButton("Видалити Нотатку")
button_notes_save = QPushButton("Зберегти Нотатку")

#3 - Теги
list_tags_label = QLabel("Список тегів")
list_tags = QListWidget()
field_tag = QLineEdit('')
field_tag.setPlaceholderText("Введіть тег...") #правильно setPlaceholderText, а не placeholderText
button_tag_create = QPushButton("Додати Тег")
button_tag_delete = QPushButton("Видалити Тег")
button_tag_search = QPushButton("Шукати нотатку за Тегом")

#4 - Лейаути (загальний + сама нотатка)
layout_notes = QHBoxLayout()
col_1 = QVBoxLayout()
col_1.addWidget(field_text)

#Лейаут для списку нотаток
col_2 = QVBoxLayout()
col_2.addWidget(list_notes_label)
col_2.addWidget(list_notes)

#Кнопки для списку нотаток
row_1 = QHBoxLayout()
row_1.addWidget(button_notes_create)
row_1.addWidget(button_notes_delete)

col_2.addLayout(row_1) #не addWidget, а addLayout
col_2.addWidget(button_notes_save)

#Лейаут для тегів
col_2.addWidget(list_tags_label)
col_2.addWidget(list_tags)
col_2.addWidget(field_tag)

#Лейаут для кнопок тегів
row_2 = QHBoxLayout()
row_2.addWidget(button_tag_create)
row_2.addWidget(button_tag_delete)

col_2.addLayout(row_2) #не addWidget, а addLayout
col_2.addWidget(button_tag_search)

#Зміна розмірів лейауту
layout_notes.addLayout(col_1, stretch = 2)
layout_notes.addLayout(col_2, stretch = 1)
notes_win.setLayout(layout_notes)

'''
Робота з нотатками
'''
#Завантаження нотаток
def load_notes():
    index = 0
    while True:
        filename = f"{index}.txt"
        if not os.path.exists(filename):
            break
        with open(filename, "r", encoding = "utf-8") as file:
            lines = file.read().split('\n')
            name = lines[0]
            text = lines[1]
            tags = lines[2].split() if len(lines) > 2 else []
            notes.append([name, text ,tags])
            list_notes.addItem(name)
        index += 1

#Збереження всіх нотаток
def save_all_notes():
    for i, note in enumerate(notes):
        with open(f"{i}.txt", "w", encoding="utf-8") as file:
            file.write(note[0] + '\n')
            file.write(note[1] + '\n')
            file.write(' '.join(note[2]) + '\n')

#Показ замітки
def show_note():
    key = list_notes.selectedItems()[0].text()
    for note in notes:
        if note[0] == key:
            field_text.setText(note[1])
            list_tags.clear()
            list_tags.addItems(note[2])

list_notes.itemClicked.connect(show_note)

#Створення замітки
def add_note():
    note_name, ok = QInputDialog.getText(notes_win, "Додати замітку", "Назва замітки:  ")
    if ok and note_name != "":
        note = [note_name, '', []]
        notes.append(note)
        list_notes.addItem(note_name)
        save_all_notes()
       
button_notes_create.clicked.connect(add_note)

#Збереження замітки
def save_note():
    if list_notes.selectedItems():
        key = list_notes.selectedItems()[0].text()
        for note in notes:
            if note[0] == key:
                note[1] = field_text.toPlainText()
                break
        save_all_notes()

button_notes_save.clicked.connect(save_note)

#Видалення замітки
def del_note():
    if list_notes.selectedItems():
        key = list_notes.selectedItems()[0].text()
        for i, note in enumerate(notes):
            if note[0] == key:
                notes.pop(i)
                break
        list_notes.clear()
        list_tags.clear()
        field_text.clear()
        for i in range(1000):
            try:
                os.remove(f"{i}.txt")
            except:
                break
        for note in notes:
            list_notes.addItem(note[0])
        save_all_notes()

button_notes_delete.clicked.connect(del_note)

'''
Робота з тегами
'''
#Додати тег
def add_tag():
    if list_notes.selectedItems():
        key = list_notes.selectedItems()[0].text()
        tag = field_tag.text()
        for note in notes:
            if note[0] == key and tag not in note[2]:
                note[2].append(tag)
                list_tags.addItem(tag)
                field_tag.clear()
        save_all_notes()
         
button_tag_create.clicked.connect(add_tag)

#Видалити тег
def del_tag():
    if list_tags.selectedItems():
        key = list_notes.selectedItems()[0].text()
        tag = list_tags.selectedItems()[0].text()
        for note in notes:
            if note[0] == key and tag in note[2]:
                note[2].remove(tag)
        list_tags.clear()
        for note in notes:
            if note[0] == key:
                list_tags.addItems(note[2])
        save_all_notes()

button_tag_delete.clicked.connect(del_tag)

#Знайти за тегом
def search_tag():
    tag = field_tag.text()
    if button_tag_search.text() == "Шукати нотатку за Тегом" and tag:
        list_notes.clear()
        for note in notes:
            if tag in note[2]:
                list_notes.addItem(note[0])
        button_tag_search.setText("Скинути пошук")
    else:
        list_notes.clear()
        for note in notes:
            list_notes.addItem(note[0])
        button_tag_search.setText("Шукати нотатку за Тегом")
        field_tag.clear()

button_tag_search.clicked.connect(search_tag)

'''
Запуск програми
'''
load_notes()
notes_win.show()
app.exec_()