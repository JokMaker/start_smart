import os
import sys
import sqlite3
from datetime import datetime

# Import our database scripts
from db_setup import setup_database
from db_sample_data import populate_sample_data
from db_update import update_database_schema

def backup_database():
    """Create a backup of the current database if it exists"""
    if os.path.exists('startsmart.db'):
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        backup_filename = f"startsmart_backup_{timestamp}.db"
        
        try:
            # Read the content of the original database
            with open('startsmart.db', 'rb') as src_file:
                content = src_file.read()
            
            # Write the content to the backup file
            with open(backup_filename, 'wb') as dst_file:
                dst_file.write(content)
            
            print(f"Database backup created: {backup_filename}")
            return True
        except Exception as e:
            print(f"Backup failed: {e}")
            return False
    else:
        print("No existing database to backup.")
        return True  # No backup needed

def reset_database():
    """Delete the existing database and create a new one"""
    if os.path.exists('startsmart.db'):
        try:
            os.remove('startsmart.db')
            print("Existing database removed.")
        except Exception as e:
            print(f"Failed to remove existing database: {e}")
            return False
    
    # Create new database
    setup_database()
    return True

def show_database_info():
    """Display information about the current database"""
    if not os.path.exists('startsmart.db'):
        print("Database does not exist.")
        return
    
    conn = sqlite3.connect('startsmart.db')
    c = conn.cursor()
    
    # Get list of tables
    c.execute("SELECT name FROM sqlite_master WHERE type='table'")
    tables = c.fetchall()
    
    print("\n=== DATABASE INFORMATION ===")
    print(f"Database file: startsmart.db")
    print(f"File size: {os.path.getsize('startsmart.db') / 1024:.2f} KB")
    print(f"Number of tables: {len(tables)}")
    print("\nTables:")
    
    for table in tables:
        table_name = table[0]
        c.execute(f"SELECT COUNT(*) FROM {table_name}")
        row_count = c.fetchone()[0]
        print(f"  - {table_name}: {row_count} rows")
    
    # Get user counts by type
    c.execute("SELECT user_type, COUNT(*) FROM users GROUP BY user_type")
    user_types = c.fetchall()
    
    print("\nUser distribution:")
    for user_type in user_types:
        print(f"  - {user_type[0]}: {user_type[1]} users")
    
    conn.close()

def main():
    """Main function to manage the database"""
    print("StartSmart Database Management")
    print("==============================")
    print("1. Initialize/Update Database Schema")
    print("2. Populate with Sample Data")
    print("3. Reset Database (WARNING: This will delete all data)")
    print("4. Show Database Information")
    print("5. Exit")
    
    choice = input("\nEnter your choice (1-5): ")
    
    if choice == '1':
        update_database_schema()
        print("Database schema updated successfully.")
    
    elif choice == '2':
        populate_sample_data()
        print("Sample data added to the database.")
    
    elif choice == '3':
        confirm = input("WARNING: This will delete all existing data. Type 'CONFIRM' to proceed: ")
        if confirm == 'CONFIRM':
            if backup_database():
                if reset_database():
                    print("Database reset successfully.")
                    populate = input("Would you like to populate with sample data? (y/n): ")
                    if populate.lower() == 'y':
                        populate_sample_data()
        else:
            print("Database reset cancelled.")
    
    elif choice == '4':
        show_database_info()
    
    elif choice == '5':
        print("Exiting...")
        sys.exit(0)
    
    else:
        print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main()