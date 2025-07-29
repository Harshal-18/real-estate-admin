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
            result = db.session.execute(text("SELECT COUNT(*) FROM information_schema.tables WHERE table_schema = 'public'"))
            table_count = result.scalar()
            
            if table_count == 0:
                print("🔄 Database is empty, importing backup data...")
                
                # Import backup data
                backup_file = "Database/backup_postgresql.sql"
                if os.path.exists(backup_file):
                    # Get database connection details from environment
                    db_url = os.getenv('DATABASE_URL')
                    if db_url:
                        # Extract PostgreSQL connection details
                        # DATABASE_URL format: postgresql://user:pass@host:port/db
                        parts = db_url.replace('postgresql://', '').split('@')
                        user_pass = parts[0].split(':')
                        host_db = parts[1].split('/')
                        
                        pg_host = host_db[0].split(':')[0]
                        pg_user = user_pass[0]
                        pg_password = user_pass[1]
                        pg_db = host_db[1]
                        
                        # Import backup using psql command
                        cmd = [
                            'psql',
                            '-h', pg_host,
                            '-U', pg_user,
                            '-d', pg_db,
                            '-f', backup_file
                        ]
                        
                        # Set password environment variable
                        env = os.environ.copy()
                        env['PGPASSWORD'] = pg_password
                        
                        try:
                            subprocess.run(cmd, env=env, check=True)
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