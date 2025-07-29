#!/usr/bin/env python3
"""
Database initialization script for Render deployment
"""
import os
import subprocess
import time
from app import create_app, db
from sqlalchemy import text

def init_database():
    """Initialize database with backup data"""
    app = create_app()
    
    with app.app_context():
        try:
            # Check if database is empty
            result = db.session.execute(text("SELECT COUNT(*) FROM information_schema.tables WHERE table_schema = 'real_estate_db'"))
            table_count = result.scalar()
            
            if table_count == 0:
                print("🔄 Database is empty, importing backup data...")
                
                # Import backup data
                backup_file = "Database/backup.sql"
                if os.path.exists(backup_file):
                    # Get database connection details from environment
                    db_url = os.getenv('DATABASE_URL')
                    if db_url:
                        # Extract MySQL connection details
                        # DATABASE_URL format: mysql+pymysql://user:pass@host:port/db
                        parts = db_url.replace('mysql+pymysql://', '').split('@')
                        user_pass = parts[0].split(':')
                        host_db = parts[1].split('/')
                        
                        mysql_host = host_db[0].split(':')[0]
                        mysql_user = user_pass[0]
                        mysql_password = user_pass[1]
                        mysql_db = host_db[1]
                        
                        # Import backup using mysql command
                        cmd = [
                            'mysql',
                            '-h', mysql_host,
                            '-u', mysql_user,
                            f'-p{mysql_password}',
                            mysql_db,
                            '<', backup_file
                        ]
                        
                        try:
                            subprocess.run(cmd, shell=True, check=True)
                            print("✅ Backup data imported successfully!")
                        except subprocess.CalledProcessError as e:
                            print(f"⚠️ Could not import backup: {e}")
                            print("🔄 Creating tables from models...")
                            db.create_all()
                    else:
                        print("🔄 Creating tables from models...")
                        db.create_all()
                else:
                    print("🔄 No backup file found, creating tables from models...")
                    db.create_all()
            else:
                print("✅ Database already has data")
                
        except Exception as e:
            print(f"❌ Error initializing database: {e}")

if __name__ == "__main__":
    init_database() 