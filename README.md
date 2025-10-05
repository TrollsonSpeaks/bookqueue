# BookQueue 📚

A command-line tool to manage your personal reading list, track progress, and never forget what to read next!

## What it does

- **Queue Management**: Add books with priority levels (high/medium/low)
- **Reading Tracking**: Move books through to-read → currently reading → finished
- **Notes & Ratings**: Rate finished books and add personal notes
- **Smart Features**: Search your library, view reading stats, random book picker
- **Data Persistence**: All data saved locally in JSON format

## Features

### Core Functionality
- Add books to your reading queue with priority levels
- View your queue sorted by priority (high priority books first)
- Start reading books (moves them to "currently reading")
- Mark books as finished with ratings (1-5 stars) and notes

### Advanced Features
- **Reading Stats**: Track books read this year, average ratings, total books
- **Search**: Find books by title or author across all categories
- **Random Picker**: Can't decide what to read? Let the app pick for you!
- **Priority System**: High priority books are weighted more in random selection

## How to run

```bash
# Clone the repository
git clone https://github.com/YOUR_USERNAME/bookqueue.git
cd bookqueue

# Run the application
python3 main.py
