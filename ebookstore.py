# import library
import sqlite3

# connect to the database
db = sqlite3.connect('ebookstore.db')

# create cursor
cursor = db.cursor()

# Create table if not exist
cursor.execute('''
               CREATE TABLE IF NOT EXISTS book 
               (id INTEGER PRIMARY KEY, title TEXT, authour TEXT,
               quantity INTEGER)''')
# commit changes
db.commit()

# populate book records
book_records = [
    (3001, 'A Tale of Two Cities', 'Charles Dickens', 30),
    (3002, 'Harry Potter and the Philosophers stone', 'J.K. Rowling', 40),
    (3003, 'The Lion, the Witch and the Wardrobe', 'C.S. Lewis', 25),
    (3004, 'The Lord of the Rings', ' J.R.R Tolkien', 37),
    (3005, 'Alice in wonderland', 'Lewis Carroll', 12)
                ]
# use executemany function
cursor.executemany(''' INSERT INTO book (id, title, authour, quantity)
                   VALUES (?, ?, ?, ?)''', book_records)
db.commit()

# Create book class
class Book():
    '''initialise'''
    def __init__(self, id, title, authour, quantity):
        self.id = id
        self.title = title
        self.authour = authour
        self.quantity = quantity

    # add methods for each option
    def display_details(self):
        print("Book ID:", self.id)
        print("Title:", self.title)
        print("Author:", self.authour)
        print("Quantity:", self.quantity)

    def update_info(self, title, authour, quantity):
        self.title = title
        self.authour = authour
        self.quantity = quantity

    def add_to_database(self, db, cursor):
        id = int(input("Please enter the book id: \n"))
        # use sql commands 
        cursor.execute('''SELECT id FROM book WHERE id = ?''', (id,))
        existing_id = cursor.fetchone()
        # check for existing id
        if existing_id:
            print("This id already exists. Please try again.")
            return

        title = input("Please enter the title of the book: \n")
        author = input("Please enter the author: \n")
        quantity = int(input("Please enter the quantity of books: \n"))

        cursor.execute('''INSERT INTO book (id, title, authour, quantity)
                           VALUES (?, ?, ?, ?)''', (id, title, author, quantity))
        print("Book added to inventory!")
        db.commit()

    def update_in_database(self, db, cursor):
        current_id = int(input("Please enter the current ID of the book to edit: \n"))
        cursor.execute('''SELECT id FROM book WHERE id = ?''', (current_id,))
        existing_id = cursor.fetchone()
        # check if id does not exist
        if not existing_id:
            print("This ID does not exist. Please try again.")
            return
        # option to change id added
        new_id = input("Please enter the new ID or press Enter to keep the same: \n")
        if not new_id:
            new_id = current_id
        else:
            new_id = int(new_id)

        title = input("Please update the title: \n")
        author = input("Please update the author: \n")
        quantity = int(input("Please update the quantity: \n"))

        cursor.execute('''UPDATE book
                          SET id = ?, title = ?, authour = ?, quantity = ?
                          WHERE id = ?''', (new_id, title, author, quantity, current_id))

        print("Book Info Updated!")
        db.commit()

    def delete_from_database(self, db, cursor):
        del_id = int(input("Please enter the ID of the book you would like to delete: \n"))
        cursor.execute('''SELECT id FROM book WHERE id = ?''', (del_id,))
        existing_id = cursor.fetchone()
        # check if does not exist
        if not existing_id:
            print("This ID does not exist. Please try again.")
            return

        cursor.execute('''DELETE FROM book WHERE id = ?''', (del_id,))
        print("Book deleted")

        db.commit()

    def search_database(self, db, cursor):
        search_id = int(input("Please enter the book ID you would like to view: \n"))

        cursor.execute('''SELECT * FROM book WHERE id = ?''', (search_id,))
        row = cursor.fetchone()

        if row:
            book = Book(*row)
            book.display_details()
        # handle error if book not found
        else:
            print("Book not found in the database. Please enter an existing ID")

        db.commit()

while True:
    try:
        # create menu options and get user user input
        clerk_choice = int(input('''\n Please choose an option:
                                 1. Enter book
                                 2. Update book
                                 3. Delete book
                                 4. Search books
                                 0. Exit
                                 Enter Now: ''')
                                 )
        if clerk_choice == 1:
            # create object with empty place holder
            # use none, which will be filled by user input
            book = Book(None, None, None, None)
            book.add_to_database(db, cursor)

        if clerk_choice == 2:
            book = Book(None, None, None, None)
            book.update_in_database(db, cursor)

        if clerk_choice == 3:
            book = Book(None, None, None, None)
            book.delete_from_database(db, cursor)

        if clerk_choice == 4:
            book = Book(None, None, None, None)
            book.search_database(db, cursor)

        if clerk_choice == 0:
            print("Goodbye!")
            break
        
    # Handle errors
    except ValueError:
        print("You have entered an incorrect option. Please try again")

    except Exception as e:
        db.rollback()
        print("An error has occurred. Please try again")

# close database
db.close()
print("Connection to database closed!")
