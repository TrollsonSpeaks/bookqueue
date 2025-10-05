from book_manager import BookManager

def display_menu():
    print("\n" + "="*50)
    print("📚 BOOKQUEUE - Your Personal Reading Manager")
    print("="*50)
    print("1. Add a book to queue")
    print("2. View reading queue")
    print("3. Start reading a book")
    print("4. View currently reading")
    print("5. View finished books")
    print("6. View stats")
    print("7. Search books")
    print("8. Random book picker")
    print("9. Exit")
    print("-"*50)

def main():
    bm = BookManager()

    while True:
        display_menu()
        choice = input("Choose an option (1-5): ").strip()

        if choice == '1':
            title = input("Book title: ").strip()
            author = input("Author: ").strip()
            print("Priority level:")
            print("  h - High (read ASAP)")
            print("  m - Medium (normal)")
            print("  l - Low (someday)")
            priority_input = input("Priority (h/m/l, default=m): ").strip().lower()

            priority_map = {'h': 'high', 'm': 'medium', 'l': 'low', '': 'medium'}
            priority = priority_map.get(priority_input, 'median')
            bm.add_book(title, author, priority)

        elif choice == '2':
            bm.view_queue()

        elif choice == '3':
            bm.move_to_currently_reading()

        elif choice == '4':
            bm.view_currently_reading()
            if bm.books['currently_reading']:
                action = input("\nFinish a book? (y/n): ").strip().lower()
                if action == 'y':
                    bm.finish_book()

        elif choice == '5':
            bm.view_finished_books()

        elif choice == '6':
            bm.get_stats()

        elif choice == '7':
            bm.search_books()

        elif choice == '8':
            bm.random_book_picker()

        elif choice == '9':
            print("Happy reading! 📖")
            break

        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main()
