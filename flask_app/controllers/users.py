from flask import render_template, redirect, session, request, flash
from flask_app import app
from flask_app.models.user import User
from flask_app.models.recipe import Recipe
from flask_bcrypt import Bcrypt
bcrypt = Bcrypt(app)


@app.route('/')
def index():
    return render_template('index.html')

@app.route('/register', methods=['POST'])
def register():

    if not User.validate_register(request.form):
        print("before redirect")
        return redirect('/')
    print("ive passed redirect")
    data ={
        "first_name": request.form['first_name'],
        "last_name": request.form['last_name'],
        "email": request.form['email'],
        "password": bcrypt.generate_password_hash(request.form['password'])
    }
    id=User.save(data)
    session['user_id'] = id
    
    return redirect('/dashboard')

@app.route('/login', methods=['POST'])
def login():
    # user = User.get_by_email(request.form)
    if not User.validate_login(request.form):
        return redirect('/')
    return redirect('/dashboard')

@app.route('/dashboard')
def dashbaord():
    if 'user_id' not in session:
        return redirect('/logout')
    data ={
        'id': session['user_id']
    }
    return render_template("dashboard.html", user=User.get_by_id(data), recipes=Recipe.get_all())

@app.route('/logout')
def logout():
    session.clear()
    return redirect('/')