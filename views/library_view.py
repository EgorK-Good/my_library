from PyQt5.QtWidgets import QWidget, QVBoxLayout, QPushButton, QLineEdit, QGridLayout, QScrollArea, QComboBox, QLabel
from PyQt5.QtCore import pyqtSignal
from database.database import Database
from views.add_book_dialog import AddBookDialog
from views.book_card import BookCard

class LibraryView(QWidget):
    book_selected = pyqtSignal(int)

    def __init__(self):
        super().__init__()
        self.db = Database()
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()

        self.search_bar = QLineEdit(self)
        self.search_bar.setPlaceholderText("Поиск книг...")
        self.search_bar.textChanged.connect(self.search_books)
        layout.addWidget(self.search_bar)

        self.author_filter = QComboBox(self)
        self.author_filter.addItem("Все авторы")
        self.author_filter.currentIndexChanged.connect(self.filter_books)
        layout.addWidget(QLabel("Автор:"))
        layout.addWidget(self.author_filter)

        self.genre_filter = QComboBox(self)
        self.genre_filter.addItem("Все жанры")
        self.genre_filter.currentIndexChanged.connect(self.filter_books)
        layout.addWidget(QLabel("Жанр:"))
        layout.addWidget(self.genre_filter)

        self.scroll_area = QScrollArea()
        self.scroll_area.setWidgetResizable(True)
        self.scroll_content = QWidget()
        self.scroll_layout = QGridLayout(self.scroll_content)
        self.scroll_area.setWidget(self.scroll_content)
        layout.addWidget(self.scroll_area)

        self.add_book_button = QPushButton("Добавить книгу", self)
        self.add_book_button.clicked.connect(self.open_add_book_dialog)
        layout.addWidget(self.add_book_button)

        self.load_filters()
        self.load_books()

        self.setLayout(layout)

    def load_filters(self):
        authors = self.db.get_unique_authors()
        genres = self.db.get_unique_genres()

        self.author_filter.clear()
        self.author_filter.addItem("Все авторы")
        self.author_filter.addItems(authors)

        self.genre_filter.clear()
        self.genre_filter.addItem("Все жанры")
        self.genre_filter.addItems(genres)

    def load_books(self):
        # Clear the grid layout
        for i in reversed(range(self.scroll_layout.count())):
            widget = self.scroll_layout.itemAt(i).widget()
            if widget is not None:
                widget.setParent(None)

        books = self.db.get_books()
        row, col = 0, 0
        for book in books:
            book_card = BookCard(book[0], book[1], book[2], book[3], book[5], book[4])
            book_card.book_selected.connect(self.on_book_selected)
            self.scroll_layout.addWidget(book_card, row, col)
            col += 1
            if col == 4:
                col = 0
                row += 1

    def search_books(self, text):
        self.filter_books()

    def filter_books(self):
        author = self.author_filter.currentText()
        genre = self.genre_filter.currentText()
        search_text = self.search_bar.text()

        # Clear the grid layout
        for i in reversed(range(self.scroll_layout.count())):
            widget = self.scroll_layout.itemAt(i).widget()
            if widget is not None:
                widget.setParent(None)

        books = self.db.get_books()
        row, col = 0, 0
        for book in books:
            if (author == "Все авторы" or author == book[2]) and (genre == "Все жанры" or genre == book[3]) and (search_text.lower() in book[1].lower() or search_text.lower() in book[2].lower()):
                book_card = BookCard(book[0], book[1], book[2], book[3], book[5], book[4])
                book_card.book_selected.connect(self.on_book_selected)
                self.scroll_layout.addWidget(book_card, row, col)
                col += 1
                if col == 4:
                    col = 0
                    row += 1

    def on_book_selected(self, book_id):
        self.book_selected.emit(book_id)

    def open_add_book_dialog(self):
        dialog = AddBookDialog(self)
        dialog.book_added.connect(self.load_books)
        dialog.exec_()
