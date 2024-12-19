from PyQt5.QtWidgets import QDialog, QVBoxLayout, QLabel, QLineEdit, QPushButton, QFileDialog, QComboBox
from PyQt5.QtCore import pyqtSignal
from database.database import Database

class AddBookDialog(QDialog):
    book_added = pyqtSignal()

    def __init__(self, parent=None):
        super().__init__(parent)
        self.db = Database()
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()

        self.title_label = QLabel("Название:", self)
        self.title_edit = QLineEdit(self)
        layout.addWidget(self.title_label)
        layout.addWidget(self.title_edit)

        self.author_label = QLabel("Автор:", self)
        self.author_edit = QLineEdit(self)
        layout.addWidget(self.author_label)
        layout.addWidget(self.author_edit)

        self.genre_label = QLabel("Жанр:", self)
        self.genre_combo = QComboBox(self)
        self.genre_combo.addItems(["Фантастика", "Детектив", "Роман", "Научная литература", "Другое"])
        layout.addWidget(self.genre_label)
        layout.addWidget(self.genre_combo)

        self.book_path_label = QLabel("Ссылка на книгу:", self)
        self.book_path_edit = QLineEdit(self)
        self.book_path_button = QPushButton("Выбрать файл", self)
        self.book_path_button.clicked.connect(self.select_book_file)
        layout.addWidget(self.book_path_label)
        layout.addWidget(self.book_path_edit)
        layout.addWidget(self.book_path_button)

        self.cover_path_label = QLabel("Ссылка на обложку:", self)
        self.cover_path_edit = QLineEdit(self)
        self.cover_path_button = QPushButton("Выбрать файл", self)
        self.cover_path_button.clicked.connect(self.select_cover_file)
        layout.addWidget(self.cover_path_label)
        layout.addWidget(self.cover_path_edit)
        layout.addWidget(self.cover_path_button)

        self.add_button = QPushButton("Добавить книгу", self)
        self.add_button.clicked.connect(self.add_book)
        layout.addWidget(self.add_button)

        self.setLayout(layout)

    def select_book_file(self):
        file_path, _ = QFileDialog.getOpenFileName(self, "Выбрать файл книги", "", "All Files (*)")
        if file_path:
            self.book_path_edit.setText(file_path)

    def select_cover_file(self):
        file_path, _ = QFileDialog.getOpenFileName(self, "Выбрать файл обложки", "", "Image Files (*.png *.jpg *.bmp)")
        if file_path:
            self.cover_path_edit.setText(file_path)

    def add_book(self):
        title = self.title_edit.text()
        author = self.author_edit.text()
        genre = self.genre_combo.currentText()
        book_path = self.book_path_edit.text()
        cover_path = self.cover_path_edit.text()

        if title and author and book_path and cover_path:
            self.db.add_book(title, author, genre, book_path, cover_path)
            self.book_added.emit()
            self.close()
