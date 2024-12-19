import sqlite3

class Database:
    def __init__(self, db_name='library.db'):
        self.conn = sqlite3.connect(db_name)
        self.create_tables()

    def create_tables(self):
        with self.conn:
            self.conn.execute('''
                CREATE TABLE IF NOT EXISTS books (
                    id INTEGER PRIMARY KEY,
                    title TEXT,
                    author TEXT,
                    genre TEXT,
                    book_path TEXT,
                    cover_path TEXT
                )
            ''')
            self.conn.execute('''
                CREATE TABLE IF NOT EXISTS notes (
                    id INTEGER PRIMARY KEY,
                    book_id INTEGER UNIQUE,
                    content TEXT,
                    FOREIGN KEY (book_id) REFERENCES books (id)
                )
            ''')

    def add_book(self, title, author, genre, book_path, cover_path):
        with self.conn:
            self.conn.execute('INSERT INTO books (title, author, genre, book_path, cover_path) VALUES (?, ?, ?, ?, ?)',
                              (title, author, genre, book_path, cover_path))

    def get_books(self):
        cursor = self.conn.execute('SELECT * FROM books')
        return cursor.fetchall()

    def get_unique_authors(self):
        cursor = self.conn.execute('SELECT DISTINCT author FROM books')
        return [row[0] for row in cursor.fetchall()]

    def get_unique_genres(self):
        cursor = self.conn.execute('SELECT DISTINCT genre FROM books')
        return [row[0] for row in cursor.fetchall()]

    def add_note(self, book_id, content):
        with self.conn:
            self.conn.execute('INSERT INTO notes (book_id, content) VALUES (?, ?)',
                              (book_id, content))

    def get_note(self, book_id):
        cursor = self.conn.execute('SELECT * FROM notes WHERE book_id = ?', (book_id,))
        return cursor.fetchone()

    def update_note(self, book_id, content):
        with self.conn:
            cursor = self.conn.execute('SELECT * FROM notes WHERE book_id = ?', (book_id,))
            note = cursor.fetchone()
            if note:
                self.conn.execute('UPDATE notes SET content = ? WHERE book_id = ?', (content, book_id))
            else:
                self.conn.execute('INSERT INTO notes (book_id, content) VALUES (?, ?)', (book_id, content))
