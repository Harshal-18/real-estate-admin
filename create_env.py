import os

def create_env_file():
    env_content = """# Database credentials
MYSQL_HOST=localhost
MYSQL_USER=root
MYSQL_PASSWORD=Harshal@18
MYSQL_DB=real_estate_db

# Flask configuration
FLASK_APP=app
FLASK_ENV=development
SECRET_KEY=848c941c28e047ff3e6a3c0c61343331af50f86a8f5c4fda"""

    try:
        with open('.env', 'w') as f:
            f.write(env_content)
        print("✅ Successfully created .env file!")
    except Exception as e:
        print(f"❌ Error creating .env file: {str(e)}")

if __name__ == "__main__":
    create_env_file() 