from flask_app.config.mysqlconnection import connectToMySQL
from flask_app import app
import re
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
from flask import flash, session
from flask_bcrypt import Bcrypt
bcrypt = Bcrypt(app)


class User:
    db = "recipes"
    def __init__(self,data):
        self.id = data['id']
        self.first_name = data['first_name']
        self.last_name = data['last_name']
        self.email = data['email']
        self.password = data['password']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']

    def fullName(self):
    return f'{self.first_name} {self.last_name}'

    @classmethod
    def save(cls,data):
        query = "INSERT INTO users (first_name, last_name, email, password) VALUES (%(first_name)s, %(last_name)s,%(email)s, %(password)s);"
        return connectToMySQL(cls.db).query_db(query,data)

    @classmethod
    def get_all(cls):
        query = "SELECT * FROM users;"
        results = connectToMySQL(cls.db).query_db(query) #only query not data
        users = []
        for row in results:
            users.append( cls(row))
        return users

    @classmethod
    def get_by_id(cls,data):
        query = "SELECT * FROM users WHERE id = %(id)s;"
        results = connectToMySQL(cls.db).query_db(query,data)
        return cls(results[0])

    # @classmethod
    # def get_by_email(cls,data):
    #     query = "SELECT * FROM users WHERE email = %(email)s;"
    #     results = connectToMySQL(cls.db).query_db(query,data)
        # return cls(results[0])
    
    @staticmethod
    def validate_register(user):
        is_valid = True
        query = "SELECT * FROM users WHERE email = %(email)s;"
        results = connectToMySQL(User.db).query_db(query,user)
        print(user)
        if len(results) >= 1:
            flash("Email address is already been taken, Please Register")
            is_valid=False
        if not EMAIL_REGEX.match(user['email']):
            flash("Invalid Email!!")
            is_valid=False
        if len(user['first_name']) < 3:
            flash("First name must be at least 2 characters")
            is_valid=False
        if len(user['last_name']) < 3:
            flash("Last name must be at least 2 characters")
            is_valid=False
        if len(user['password']) < 8:
            flash("Password must be at least 8 characters")
            is_valid=False
        if user['password'] != user['confirm']:
            flash("Passwords do not match")
            is_valid =False
        return is_valid


    @staticmethod
    def validate_login(user):
        is_valid =True
        query = "SELECT * FROM users WHERE email = %(email)s;"
        results = connectToMySQL(User.db).query_db(query,user)
        if len(results) < 1:
            is_valid =False
            flash("Invalid Email")
            return is_valid
        else:
            person = results[0]
        print(person['id'])
        print(user['password'])
        if not bcrypt.check_password_hash(person['password'], user['password']):
            is_valid =False
            flash("Invalid Password")
            return is_valid
        session['user_id'] = person['id']
        return is_valid