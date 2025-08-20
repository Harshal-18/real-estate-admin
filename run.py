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
                print("Database connection successful!")
                return True
        except Exception as e:
            attempt += 1
            print(f"Waiting for database... (attempt {attempt}/{max_attempts})")
            print(f"   Error: {str(e)}")
            time.sleep(2)
    
    print("Database connection failed after maximum attempts")
    return False

def init_db():
    """Initialize database tables"""
    with app.app_context():
        try:
            db.create_all()
            print("Database tables created successfully!")
        except Exception as e:
            print(f"Error creating tables: {e}")

def seed_db():
    """Seed database with initial data"""
    try:
        from Database.seed_data import seed_data
        with app.app_context():
            seed_data()
    except Exception as e:
        print(f"Error seeding database: {e}")

if __name__ == '__main__':
    # Wait for database to be ready
    if wait_for_db():
        init_db()
        seed_db()
        
        # Start the Flask app
        print("Starting Flask application...")
        app.run(host="0.0.0.0", debug=False, port=5000)
    else:
        print("Failed to connect to database. Exiting.")
        exit(1)

# For gunicorn
if __name__ != '__main__':
    # Initialize database when app starts
    init_db()
    seed_db()