from library_classes import Book, Library, Member, StudentMember, AdministrativeMember
import os
import subprocess

def login(members):
    member_id = input("Enter your member ID: ")
    password = input("Enter your password: ")

    for member in members:
        if member.member_id == member_id and member.password == password:
            return member
    return None

def print_in_box(text):
    lines = text.split('\n')
    max_length = max(len(line) for line in lines)
    print(" " + "-" * (max_length + 2))
    for line in lines:
        print("| " + line.ljust(max_length) + " |")
    print(" " + "-" * (max_length + 2))

def open_active_book(member):
    if member.active_book:
        pdf_path = member.active_book.pdf_path
        if os.path.exists(pdf_path):
            print(f"Opening PDF for {member.active_book.title}")
            if os.name == 'posix':  # This options is used for MAC OS
                subprocess.run(['open', pdf_path])
            else:  # This option is for WİNDOWS
                os.startfile(pdf_path)
        else:
            print(f"File not found: {pdf_path}")
    else:
        print("User doesn't have an active book")

def main_menu():
    menu_text = """1 - List of books in library
2 - Borrow a book
3 - Return a book
4 - View active book
5 - Add book to library (Admin only)
6 - Remove book from library (Admin only)
7 - View balance
8 - Open Active Book
9 - Exit"""
    print_in_box(menu_text)


def main():
    my_library = Library()
    members = [
        Member("member1", "member1", 10),
        StudentMember("student1", "student1"),
        AdministrativeMember("admin1", "admin1")
    ]

    my_library.add_book(Book("Kürk Mantolu Madonna - Sabahattin Ali", 101, "Summary of KMM", r"C:\Users\ertun\Desktop\adres\adres\mektup.pdf"), members[2])
    my_library.add_book(Book("Hayvan Çiftliği - George Orwell", 102, "Summary of Hayvan Çiftliği", r"C:\Users\ertun\Desktop\adres\adres\mektup.pdf"), members[2])

    current_member = None
    while current_member is None:
        current_member = login(members)
        if current_member is None:
            print("Invalid login. Please try again.")

    while True:
        main_menu()
        choice = input("Choose an option: ")

        if choice == "1":
            for book in my_library.books:
                print(book)
        elif choice == "2":
            book_id = int(input("Enter book ID to borrow: "))
            print(current_member.borrow_book(book_id, my_library))
        elif choice == "3":
            print(current_member.return_book(my_library))
        elif choice == "4":
            if current_member.active_book:
                print(f"Active Book: {current_member.active_book}")
            else:
                print("No active book")
        elif choice == "5":
            if isinstance(current_member, AdministrativeMember):
                title = input("Enter book title: ")
                book_id = int(input("Enter book ID: "))
                content = input("Enter book summary: ")
                pdf_path = input("Enter path to book's PDF: ")  # New line to get the PDF path
                new_book = Book(title, book_id, content, pdf_path)
                print(current_member.add_book_to_library(my_library, new_book))
            else:
                print("Error: Only administrative members can add books.")
        elif choice == "6":
            if isinstance(current_member, AdministrativeMember):
                book_id = int(input("Enter book ID to remove: "))
                print(current_member.remove_book_from_library(my_library, book_id))
            else:
                print("Error: Only administrative members can remove books.")
        elif choice == "7":
            if isinstance(current_member, AdministrativeMember):
                print("You have full access to the systems.")
            elif isinstance(current_member, StudentMember):
                print("You don't have to pay for books.")
            else:
                print(f"Your balance is: ${current_member.wallet_balance}")
        elif choice == "8":
            open_active_book(current_member)
        elif choice == "9":
            break
        else:
            print("Invalid choice. Please try again.")


if __name__ == "__main__":
    main()
