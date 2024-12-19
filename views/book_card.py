from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QPushButton
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import pyqtSignal, Qt
import os

class BookCard(QWidget):
    book_selected = pyqtSignal(int)

    def __init__(self, book_id, title, author, genre, cover_path, book_path):
        super().__init__()
        self.book_id = book_id
        self.book_path = book_path
        self.init_ui(title, author, genre, cover_path)

    def init_ui(self, title, author, genre, cover_path):
        layout = QVBoxLayout()
        layout.setAlignment(Qt.AlignCenter)

        self.cover_label = QLabel(self)
        pixmap = QPixmap(cover_path)
        self.cover_label.setPixmap(pixmap.scaled(200, 300))  # Wider cover
        layout.addWidget(self.cover_label)

        self.title_label = QLabel(title, self)
        self.title_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(self.title_label)

        self.author_label = QLabel(author, self)
        self.author_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(self.author_label)

        self.genre_label = QLabel(genre, self)
        self.genre_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(self.genre_label)

        self.open_button = QPushButton("Открыть книгу", self)
        self.open_button.clicked.connect(self.open_book)
        layout.addWidget(self.open_button)

        self.setLayout(layout)

    def open_book(self):
        if os.path.exists(self.book_path):
            os.startfile(self.book_path)  # For Windows
            # For macOS, use: os.system(f"open {self.book_path}")
            # For Linux, use: os.system(f"xdg-open {self.book_path}")

    def mouseDoubleClickEvent(self, event):
        self.book_selected.emit(self.book_id)
