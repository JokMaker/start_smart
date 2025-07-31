"""
Database Backup System for StartSmart
Automated backup functionality for production deployment
"""
import sqlite3
import shutil
import os
from datetime import datetime
import logging

def setup_backup_logging():
    """Setup logging for backup operations"""
    logging.basicConfig(
        filename='backup.log',
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(message)s'
    )

def create_backup():
    """Create a backup of the database"""
    try:
        setup_backup_logging()
        
        # Create backups directory if it doesn't exist
        backup_dir = 'backups'
        os.makedirs(backup_dir, exist_ok=True)
        
        # Generate backup filename with timestamp
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        backup_filename = f'startsmart_backup_{timestamp}.db'
        backup_path = os.path.join(backup_dir, backup_filename)
        
        # Copy database file
        if os.path.exists('startsmart.db'):
            shutil.copy2('startsmart.db', backup_path)
            
            # Log success
            logging.info(f"Database backup created: {backup_path}")
            print(f"✅ Database backup created: {backup_path}")
            
            # Clean old backups (keep last 7 days)
            clean_old_backups(backup_dir)
            
            return backup_path
        else:
            logging.error("Database file not found")
            print("❌ Database file not found")
            return None
            
    except Exception as e:
        logging.error(f"Backup failed: {str(e)}")
        print(f"❌ Backup failed: {str(e)}")
        return None

def clean_old_backups(backup_dir, keep_days=7):
    """Clean old backup files, keep only recent ones"""
    try:
        cutoff_time = datetime.now().timestamp() - (keep_days * 24 * 3600)
        
        for filename in os.listdir(backup_dir):
            if filename.startswith('startsmart_backup_') and filename.endswith('.db'):
                file_path = os.path.join(backup_dir, filename)
                if os.path.getctime(file_path) < cutoff_time:
                    os.remove(file_path)
                    logging.info(f"Removed old backup: {filename}")
                    
    except Exception as e:
        logging.error(f"Error cleaning old backups: {str(e)}")

def restore_backup(backup_path):
    """Restore database from backup"""
    try:
        if not os.path.exists(backup_path):
            print(f"❌ Backup file not found: {backup_path}")
            return False
            
        # Create a backup of current database before restore
        if os.path.exists('startsmart.db'):
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            pre_restore_backup = f'pre_restore_backup_{timestamp}.db'
            shutil.copy2('startsmart.db', pre_restore_backup)
            print(f"📋 Current database backed up as: {pre_restore_backup}")
        
        # Restore from backup
        shutil.copy2(backup_path, 'startsmart.db')
        
        logging.info(f"Database restored from: {backup_path}")
        print(f"✅ Database restored from: {backup_path}")
        return True
        
    except Exception as e:
        logging.error(f"Restore failed: {str(e)}")
        print(f"❌ Restore failed: {str(e)}")
        return False

def verify_database():
    """Verify database integrity"""
    try:
        conn = sqlite3.connect('startsmart.db')
        cursor = conn.cursor()
        
        # Check if all tables exist
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
        tables = cursor.fetchall()
        
        expected_tables = ['users', 'jobs', 'applications', 'startups', 'mentorship_requests', 'resources']
        existing_tables = [table[0] for table in tables]
        
        for table in expected_tables:
            if table in existing_tables:
                cursor.execute(f"SELECT COUNT(*) FROM {table}")
                count = cursor.fetchone()[0]
                print(f"✅ Table '{table}': {count} records")
            else:
                print(f"❌ Missing table: {table}")
        
        conn.close()
        return True
        
    except Exception as e:
        print(f"❌ Database verification failed: {str(e)}")
        return False

if __name__ == "__main__":
    print("🔄 Starting database backup...")
    backup_path = create_backup()
    
    if backup_path:
        print("🔍 Verifying database...")
        verify_database()
        print("✅ Backup process completed successfully!")
    else:
        print("❌ Backup process failed!")
