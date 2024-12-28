import sqlite3
from datetime import datetime
import openai
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def init_db():
    """Initialize SQLite database and create table if it doesn't exist."""
    conn = sqlite3.connect('journal.db')
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS entries (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            entry TEXT NOT NULL,
            reflection TEXT NOT NULL,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    conn.commit()
    conn.close()

def generate_reflection(journal_entry):
    """Generate AI reflection using OpenAI API."""
    try:
        client = openai.OpenAI(api_key=os.getenv('OPENAI_API_KEY'))
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a compassionate journal reflection assistant. Generate positive insights and reflections based on journal entries."},
                {"role": "user", "content": f"Generate a positive reflection or insight based on this journal entry: {journal_entry}"}
            ],
            max_tokens=150
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"Error generating reflection: {str(e)}"

def save_entry(entry, reflection):
    """Save journal entry and reflection to database."""
    conn = sqlite3.connect('journal.db')
    c = conn.cursor()
    c.execute('INSERT INTO entries (entry, reflection) VALUES (?, ?)',
              (entry, reflection))
    conn.commit()
    conn.close()

def display_reflection(reflection):
    """Display the generated reflection."""
    print("\nAI Reflection:")
    print("-" * 50)
    print(reflection)
    print("-" * 50)

def main():
    """Main function to run the journal application."""
    init_db()
    
    while True:
        print("\nDaily Journal with AI Reflection")
        print("1. Write journal entry")
        print("2. Exit")
        
        choice = input("Choose an option (1-2): ")
        
        if choice == '1':
            journal_entry = input("\nWrite your journal entry (press Enter twice to finish):\n")
            reflection = generate_reflection(journal_entry)
            save_entry(journal_entry, reflection)
            display_reflection(reflection)
        elif choice == '2':
            print("Goodbye!")
            break
        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main()