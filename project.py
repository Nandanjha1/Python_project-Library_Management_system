import tkinter as tk
from tkinter import messagebox
import mysql.connector

def setup_db():
    conn = mysql.connector.connect(
        host="localhost",    
        user="root",        
        password="Nandan@123", 
        database="library_db"  
    )
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS books (
                 id INT AUTO_INCREMENT PRIMARY KEY,
                 title VARCHAR(255) NOT NULL, 
                 author VARCHAR(255) NOT NULL, 
                 year INT, 
                 isbn INT)''')
    conn.commit()
    conn.close()

def add_book(title, author, year, isbn):
    conn = mysql.connector.connect(
        host="localhost",
        user="root",
        password="Nandan@123",
        database="library_db"
    )
    c = conn.cursor()
    c.execute("INSERT INTO books (title, author, year, isbn) VALUES (%s, %s, %s, %s)",
              (title, author, year, isbn))
    conn.commit()
    conn.close()
    messagebox.showinfo("Success", "Book added successfully")

def delete_book(book_id):
    conn = mysql.connector.connect(
        host="localhost",
        user="root",
        password="Nandan@123",
        database="library_db"
    )
    c = conn.cursor()
    c.execute("DELETE FROM books WHERE id=%s", (book_id,))
    conn.commit()
    conn.close()
    messagebox.showinfo("Success", "Book deleted successfully")

def view_books():
    conn = mysql.connector.connect(
        host="localhost",
        user="root",
        password="Nandan@123",
        database="library_db"
    )
    c = conn.cursor()
    c.execute("SELECT * FROM books")
    rows = c.fetchall()
    conn.close()
    return rows

def search_books(title="", author="", year="", isbn=""):
    conn = mysql.connector.connect(
        host="localhost",
        user="root",
        password="Nandan@123",
        database="library_db"
    )
    c = conn.cursor()
    query = "SELECT * FROM books WHERE title LIKE %s AND author LIKE %s AND year LIKE %s AND isbn LIKE %s"
    c.execute(query, (f"%{title}%", f"%{author}%", f"%{year}%", f"%{isbn}%"))
    rows = c.fetchall()
    conn.close()
    return rows

class LibraryApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Library Management System")

        tk.Label(root, text="Title").grid(row=0, column=0)
        tk.Label(root, text="Author").grid(row=0, column=2)
        tk.Label(root, text="Year").grid(row=1, column=0)
        tk.Label(root, text="ISBN").grid(row=1, column=2)

        self.title_text = tk.StringVar()
        self.author_text = tk.StringVar()
        self.year_text = tk.StringVar()
        self.isbn_text = tk.StringVar()

        self.title_entry = tk.Entry(root, textvariable=self.title_text)
        self.author_entry = tk.Entry(root, textvariable=self.author_text)
        self.year_entry = tk.Entry(root, textvariable=self.year_text)
        self.isbn_entry = tk.Entry(root, textvariable=self.isbn_text)

        self.title_entry.grid(row=0, column=1)
        self.author_entry.grid(row=0, column=3)
        self.year_entry.grid(row=1, column=1)
        self.isbn_entry.grid(row=1, column=3)

        tk.Button(root, text="Add Book", width=12, command=self.add_book).grid(row=2, column=3)
        tk.Button(root, text="Delete Book", width=12, command=self.delete_book).grid(row=3, column=3)
        tk.Button(root, text="View All", width=12, command=self.view_books).grid(row=4, column=3)
        tk.Button(root, text="Search", width=12, command=self.search_books).grid(row=5, column=3)

        self.book_list = tk.Listbox(root, height=10, width=40)
        self.book_list.grid(row=2, column=0, rowspan=6, columnspan=2)
        self.book_list.bind('<<ListboxSelect>>', self.get_selected_book)

        self.scrollbar = tk.Scrollbar(root)
        self.scrollbar.grid(row=2, column=2, rowspan=6)
        self.book_list.configure(yscrollcommand=self.scrollbar.set)
        self.scrollbar.configure(command=self.book_list.yview)

        self.selected_book = None

    def get_selected_book(self, event):
        try:
            index = self.book_list.curselection()[0]
            self.selected_book = self.book_list.get(index)
            self.title_entry.delete(0, tk.END)
            self.title_entry.insert(tk.END, self.selected_book[1])
            self.author_entry.delete(0, tk.END)
            self.author_entry.insert(tk.END, self.selected_book[2])
            self.year_entry.delete(0, tk.END)
            self.year_entry.insert(tk.END, self.selected_book[3])
            self.isbn_entry.delete(0, tk.END)
            self.isbn_entry.insert(tk.END, self.selected_book[4])
        except IndexError:
            self.selected_book = None

    def add_book(self):
        add_book(self.title_text.get(), self.author_text.get(), self.year_text.get(), self.isbn_text.get())
        self.view_books()

    def delete_book(self):
        if self.selected_book:
            delete_book(self.selected_book[0])
            self.view_books()

    def view_books(self):
        self.book_list.delete(0, tk.END)
        for row in view_books():
            self.book_list.insert(tk.END, row)

    def search_books(self):
        self.book_list.delete(0, tk.END)
        for row in search_books(self.title_text.get(), self.author_text.get(), self.year_text.get(), self.isbn_text.get()):
            self.book_list.insert(tk.END, row)

if __name__ == "__main__":
    setup_db()
    root = tk.Tk()
    app = LibraryApp(root)
    root.mainloop()
