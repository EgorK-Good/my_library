from PyQt5.QtWidgets import QWidget, QVBoxLayout, QPushButton, QTextEdit, QLabel
from PyQt5.QtCore import pyqtSignal
from database.database import Database

class NotesView(QWidget):
    back_to_library = pyqtSignal()

    def __init__(self):
        super().__init__()
        self.db = Database()
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()

        self.back_button = QPushButton("Назад к библиотеке", self)
        self.back_button.clicked.connect(self.back_to_library.emit)
        layout.addWidget(self.back_button)

        self.book_label = QLabel(self)
        layout.addWidget(self.book_label)

        self.notes_edit = QTextEdit(self)
        layout.addWidget(self.notes_edit)

        self.save_button = QPushButton("Сохранить заметку", self)
        self.save_button.clicked.connect(self.save_note)
        layout.addWidget(self.save_button)

        self.setLayout(layout)

    def load_book(self, book_id):
        self.current_book_id = book_id
        book = self.db.get_books()[book_id - 1]  # Assuming book_id is 1-based
        self.book_label.setText(f"{book[1]} by {book[2]}")
        note = self.db.get_note(book_id)
        if note:
            self.notes_edit.setText(note[2])
        else:
            self.notes_edit.clear()

    def save_note(self):
        content = self.notes_edit.toPlainText()
        self.db.update_note(self.current_book_id, content)
