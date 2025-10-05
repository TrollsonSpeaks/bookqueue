import json
import os
from datetime import datetime

class BookManager:
    def __init__(self, data_file='books.json'):
        self.data_file = data_file
        self.books = self.load_books()

    def load_books(self):
        """Load books from JSON file, create empty structure if file doesn't exist"""
        if os.path.exists(self.data_file):
            try:
                with open(self.data_file, 'r') as f:
                    return json.load(f)
            except json.JSONDecodeError:
                print("Warning: Could not read books file. Starting fresh.")
                return self.create_empty_structure()
        else:
            return self.create_empty_structure()

    def create_empty_structure(self):
        """Create the basic data structure for our books"""
        return {
            'to_read': [],
            'currently_reading': [],
            'finished': []
        }

    def save_books(self):
        """Save books to JSON file"""
        with open(self.data_file, 'w') as f:
            json.dump(self.books, f, indent=2)

    def add_book(self, title, author, priority='medium'):
        """Add a book to the to_read list"""
        book = {
            'title': title,
            'author': author,
            'priority': priority,
            'added_date': datetime.now().strftime('%Y-%m-%d'),
            'notes': ''
        }
        self.books['to_read'].append(book)
        self.save_books()
        print(f"Added '{title}' by {author} to your reading queue!")

    def view_queue(self):
        """Display the current reading queue"""
        if not self.books['to_read']:
            print("Your reading queue is empty! Add some books.")
            return

        print("\n📚 YOUR READING QUEUE:")
        print("-" * 50)

        priority_order = {'high': 1, 'medium': 2, 'low': 3}
        sorted_books = sorted(self.books['to_read'],
                           key=lambda x: priority_order.get(x['priority'], 2))

        for i, book in enumerate(sorted_books, 1):
            priority_emoji = {'high': '🔥', 'medium': '📖', 'low': '💤'}
            emoji = priority_emoji.get(book['priority'], '📖')
            print(f"{i}. {emoji} {book['title']} by {book['author']} ({book['priority']} priority)")

    def move_to_currently_reading(self):
        """Move a book from queue to currently reading"""
        if not self.books['to_read']:
            print("No books in your queue to move!")
            return

        self.view_queue()
        try:
            choice = int(input("\nWhich book number to start reading? ")) - 1
            if 0 <= choice < len(self.books['to_read']):
                book = self.books['to_read'].pop(choice)
                book['started_date'] = datetime.now().strftime('%Y-%m-%d')
                self.books['currently_reading'].append(book)
                self.save_books()
                print(f"Started reading '{book['title']}'! Happy reading! 📖")
            else:
                print("Invalid book number.")
        except ValueError:
            print("Please enter a valid number.")

    def view_currently_reading(self):
        """"Display currently reading books"""
        if not self.books['currently_reading']:
            print("You're not currently reading anything. Time to start a book!")
            return

        print("\n📖 CURRENTLY READING:")
        print("-" * 50)
        for i, book in enumerate(self.books['currently_reading'], 1):
            print(f"{i}, {book['title']} by {book['author']}")
            print(f"   Started: {book['started_date']}")

    def finish_book(self):
        """"Move a book from currently reading to finished"""
        if not self.books['currently_reading']:
            print("No books currently being read!")
            return

        self.view_currently_reading()
        try:
            choice = int(input("\nWhich book did you finish? ")) - 1
            if 0 <= choice < len(self.books['currently_reading']):
                book = self.books['currently_reading'].pop(choice)
                book['finished_date'] = datetime.now().strftime('%Y-%m-%d')

                rating = input("Rate it 1-5 stars (option): ").strip()
                if rating and rating.isdigit() and 1 <= int(rating) <= 5:
                    book['rating'] = int(rating)

                notes = input("Any notes or thoughts? (optional): ").strip()
                if notes:
                    book['notes'] = notes

                self.books['finished'].append(book)
                self.save_books()
                print(f"Congratulations on finishing '{book['title']}'! 🎉")
            else:
                print("Invalid book number.")
        except ValueError:
            print("Please enter a valid number.")

    def view_finished_books(self):
        """Display finished books"""
        if not self.books['finished']:
            print("No finished books yet. Keep reading!")
            return

        print("\n✅ FINISHED BOOKS:")
        print("-" * 50)
        for i, book in enumerate(self.books['finished'], 1):
            rating_stars = "⭐" * book.get('rating', 0) if book.get('rating') else "No rating"
            print(f"{i}. {book['title']} by {book['author']}")
            print(f"   Finished: {book['finished_date']} | {rating_stars}")
            if book.get('notes'):
                print(f"    Notes: {book['notes']}")

    def get_stats(self):
        """Dispaly reading statistics"""
        total_to_read = len(self.books['to_read'])
        total_reading = len(self.books['currently_reading'])
        total_finished = len(self.books['finished'])

        print("\n📊 YOUR READING STATS:")
        print("-" * 50)
        print(f"📚 Books in queue: {total_to_read}")
        print(f"📖 Currently reading: {total_reading}")
        print(f"✅ Books finished: {total_finished}")
        print(f"🎯 Total books tracked: {total_to_read + total_reading + total_finished}")

        current_year = datetime.now().year
        books_this_year = [book for book in self.books['finished']
                          if book.get('finished_date', '').startswith(str(current_year))]
        print(f"📅Books finished in {current_year}: {len(books_this_year)}")

        rated_books = [book for book in self.books['finished'] if book.get('rating')]
        if rated_books:
            avg_rating = sum(book['rating'] for book in rated_books) / len(rated_books)
            print(f"⭐ Average rating: {avg_rating:.1f}/5 stars")

    def search_books(self):
        """Search through all books"""
        query = input("Search for (title or author): ").strip().lower()
        if not query:
            return

        found_books = []

        for category, books in self.books.items():
            for book in books:
                if (query in book['title'].lower() or
                    query in book['author'].lower()):
                    found_books.append((book, category))

        if not found_books:
            print(f"No books found matching '{query}'")
            return

        print(f"\n🔍 SEARCH RESULTS for '{query}':")
        print("-" * 50)
        for book, category in found_books:
            status_emoji = {'to_read': '📚', 'currently_reading': '📖', 'finished': '✅'}
            emoji = status_emoji.get(category, '📚')
            print(f"{emoji} {book['title']} by {book['author']} ({category.replace('_', ' ')})")

    def random_book_picker(self):
        """Pick a random book from the queue when you can't decide"""
        import random

        if not self.books['to_read']:
            print("No books in your queue! Add some books first.")
            return

        weighted_books = []
        for book in self.books['to_read']:
            weight = {'high': 3, 'medium': 2, 'low': 1}.get(book['priority'], 2)
            weighted_books.extend([book] * weight)

        chosen_book = random.choice(weighted_books)

        print(f"\n🎲 RANDOM BOOK PICKER SAYS:")
        print("-" * 50)
        print(f"📖 Read: '{chosen_book['title']}' by {chosen_book['author']}")
        print(f"Priority: {chosen_book['priority']}")

        start_now = input("\nStart reading this book now? (y/n): ").strip().lower()
        if start_now == 'y':
            self.books['to_read'].remove(chosen_book)
            chosen_book['started_date'] = datetime.now().strftime('%Y-%m-%d')
            self.books['currently_reading'].append(chosen_book)
            self.save_books()
            print(f"Started reading '{chosen_book['title']}'! 📖")
