from app import create_app, db
from sqlalchemy import text
import time
import os

app = create_app()

def wait_for_db():
    """Wait for database to be ready"""
    max_attempts = 30
    attempt = 0
    
    while attempt < max_attempts:
        try:
            with app.app_context():
                # Try a simple connection test
                result = db.session.execute(text('SELECT 1'))
                result.fetchone()
                print("✅ Database connection successful!")
                return True
        except Exception as e:
            attempt += 1
            print(f"⏳ Waiting for database... (attempt {attempt}/{max_attempts})")
            print(f"   Error: {str(e)}")
            time.sleep(2)
    
    print("❌ Database connection failed after maximum attempts")
    return False

if __name__ == '__main__':
    # Wait for database to be ready
    if wait_for_db():
        with app.app_context():
            # Create all database tables
            db.create_all()
            print("✅ Database tables created successfully!")
        
        # Start the Flask app
        print("🚀 Starting Flask application...")
        app.run(host="0.0.0.0", debug=True, port=5000)
    else:
        print("❌ Failed to connect to database. Exiting.")
        exit(1) 