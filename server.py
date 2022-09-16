#Flask Server

#Imports
from flask import Flask, render_template, request, redirect, url_for, make_response, jsonify, session




app = Flask(__name__)
app.secret_key = "super secret key"



@app.route('/')
def index():
    return render_template('index.html')


app.route('/get_login', methods=['GET'])
def get_login():
    return redirect('/')


@app.route('/register', methods=['POST'])
def register():
    user = {
        "username": request.form["name"],
        "password": request.form["password"]
    }
    db.users.insert_one(user)
    return render_template('index.html')


@app.route('/get_register', methods=['GET'])
def get_register():
    return render_template('register.html')
