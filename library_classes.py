class Book:
    def __init__(self, title, book_id, content, pdf_path):
        self.title = title
        self.book_id = book_id
        self.content = content
        self.pdf_path = pdf_path

    def __str__(self):
        return f"Book: {self.title}, ID: {self.book_id}, Summary: {self.content},PDF Path: {self.pdf_path}"




class Library:
    def __init__(self):
        self.books = []

    def add_book(self, book, member):
        if isinstance(member, AdministrativeMember):
            self.books.append(book)
        else:
            return "Error: Only administrative members can add books to the library."

    def remove_book(self, book_id, member):
        if isinstance(member, AdministrativeMember):
            self.books = [book for book in self.books if book.book_id != book_id]
        else:
            return "Error: Only administrative members can remove books from the library."

    def borrow_book(self, book_id, member):
        if member.active_book is None:
            for book in self.books:
                if book.book_id == book_id:
                    member.active_book = book
                    self.books.remove(book)
                    return f"{member.member_id} has borrowed '{book.title}'"
            return "Book not found"
        else:
            return "Member already has an active book"




    def return_book(self, member):
        if member.active_book:
            self.add_book(member.active_book, member)
            member.active_book = None
            return "Book returned"
        else:
            return "No active book to return"




class Member:
    def __init__(self, member_id, password, wallet_balance=0):
        self.member_id = member_id
        self.password = password
        self.active_book = None
        self.wallet_balance = wallet_balance

    def borrow_book(self, book_id, library):
        if self.wallet_balance >= 5:
            self.wallet_balance -= 5
            return library.borrow_book(book_id, self)
        else:
            return "Insufficient funds to borrow a book"

    def return_book(self, library):
        if self.active_book:
            self.wallet_balance += 2.5
        return library.return_book(self)




class StudentMember(Member):
    def __init__(self, member_id, password):
        super().__init__(member_id, password)

    def borrow_book(self, book_id, library):
        return library.borrow_book(book_id, self)  # Student members borrow for free




class AdministrativeMember(Member):
    def __init__(self, member_id, password):
        super().__init__(member_id, password)

    def add_book_to_library(self, library, book):
        library.add_book(book, self)

    def remove_book_from_library(self, library, book_id):
        library.remove_book(book_id, self)

    def borrow_book(self, book_id, library):
        return library.borrow_book(book_id, self)  # Administrative members borrow for free
