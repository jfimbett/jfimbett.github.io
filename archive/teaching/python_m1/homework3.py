#%%
class Book:
    def __init__(self, title, author):
        self.title = title
        self.author = author
        self.available = True
    
    def __str__(self):
        return f"{self.title} by {self.author}"

class Library:
    def __init__(self):
        self.books = []
    
    def add_book(self, book):
        self.books.append(book)
    
    def display_books(self):
        for book in self.books:
            availability = "Available" if book.available else "Not Available"
            print(f"{book} - {availability}")
    
    def borrow_book(self, title):
        for book in self.books:
            if book.title == title:
                if book.available:
                    book.available = False
                    print(f"You have borrowed '{title}'")
                else:
                    print(f"Sorry, '{title}' is not available.")
                return
        print(f"'{title}' not found in the library.")
    
    def return_book(self, title):
        for book in self.books:
            if book.title == title:
                if not book.available:
                    book.available = True
                    print(f"You have returned '{title}'")
                else:
                    print(f"'{title}' was not borrowed.")
                return
        print(f"'{title}' not found in the library.")

    def __add__(self, other):
        new_library = Library()
        new_library.books = self.books + other.books
        return new_library

# Example usage:
if __name__ == "__main__":
    my_library = Library()
    book1 = Book("The Great Gatsby", "F. Scott Fitzgerald")
    book2 = Book("1984", "George Orwell")
    book3 = Book("To Kill a Mockingbird", "Harper Lee")

    my_library.add_book(book1)
    my_library.add_book(book2)
    my_library.add_book(book3)

    print("Available books:")
    my_library.display_books()

    print("\nBorrowing '1984'...")
    my_library.borrow_book("1984")

    print("\nAttempting to borrow '1984' again...")
    my_library.borrow_book("1984")

    print("\nReturning '1984'...")
    my_library.return_book("1984")

    print("\nAvailable books after returning:")
    my_library.display_books()


    my_new_library = my_library + my_library 

    my_new_library.display_books()