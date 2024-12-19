import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QStackedWidget
from PyQt5.QtCore import QFile, QTextStream
from views.library_view import LibraryView
from views.notes_view import NotesView

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Моя библиотека")
        self.setGeometry(100, 100, 1000, 800)  # Увеличиваем размер окна

        self.stacked_widget = QStackedWidget()
        self.setCentralWidget(self.stacked_widget)

        self.library_view = LibraryView()
        self.notes_view = NotesView()

        self.stacked_widget.addWidget(self.library_view)
        self.stacked_widget.addWidget(self.notes_view)

        self.library_view.book_selected.connect(self.show_notes_view)
        self.notes_view.back_to_library.connect(self.show_library_view)

        self.load_styles()

    def show_notes_view(self, book_id):
        self.notes_view.load_book(book_id)
        self.stacked_widget.setCurrentWidget(self.notes_view)

    def show_library_view(self):
        self.stacked_widget.setCurrentWidget(self.library_view)

    def load_styles(self):
        file = QFile("styles/styles.css")
        file.open(QFile.ReadOnly | QFile.Text)
        stream = QTextStream(file)
        stylesheet = stream.readAll()
        self.setStyleSheet(stylesheet)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
