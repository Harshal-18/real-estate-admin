import sys
import os

# Add the parent directory to Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app import create_app, db
from sqlalchemy import text

def test_database_connection():
    app = create_app()
    
    try:
        # Test the connection by executing a simple query
        with app.app_context():
            # Try to execute a simple SELECT query
            result = db.session.execute(text('SELECT 1'))
            result.scalar()
            print("\n✅ Successfully connected to the database!")
            
            # Get database information
            result = db.session.execute(text('SELECT DATABASE() as db_name'))
            db_name = result.scalar()
            print(f"Connected to database: {db_name}")
            
            # Get table information without modifying anything
            result = db.session.execute(text("""
                SELECT TABLE_NAME 
                FROM information_schema.tables 
                WHERE table_schema = :db_name 
                AND table_type = 'BASE TABLE'
            """), {'db_name': db_name})
            
            tables = result.fetchall()
            print("\nExisting tables in the database:")
            print("=" * 30)
            for table in tables:
                print(f"- {table[0]}")
            
    except Exception as e:
        print("\n❌ Failed to connect to the database!")
        print(f"Error: {str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    test_database_connection() 