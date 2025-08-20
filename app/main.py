from flask import render_template, request, redirect, url_for, flash
from app.models.user import User
from app import db, create_app
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

# Create the Flask app using the factory function
app = create_app()

@app.route('/users', methods=['GET'])
def list_users():
    try:
        users = User.query.all()
        return render_template('users.html', users=users)
    except Exception as e:
        print("Error fetching users:", e)
        return "An error occurred while fetching users."

@app.route('/users/new', methods=['GET', 'POST'])
def create_user():
    if request.method == 'POST':
        # Logic to create a new user
        first_name = request.form['first_name']
        last_name = request.form['last_name']
        email = request.form['email']
        phone = request.form.get('phone', '')
        
        # Check if user already exists
        existing_user = User.query.filter_by(email=email).first()
        if existing_user:
            flash('User with this email already exists!', 'error')
            return render_template('create_user.html')
        
        # Create new user with password (you might want to add password field to form)
        new_user = User()
        new_user.first_name = first_name
        new_user.last_name = last_name
        new_user.email = email
        new_user.phone = phone
        new_user.set_password('default_password')  # You should add password field to form
        
        db.session.add(new_user)
        db.session.commit()
        flash('User created successfully!', 'success')
        return redirect(url_for('list_users'))
    return render_template('create_user.html')

if __name__ == '__main__':
    app.run(debug=True)