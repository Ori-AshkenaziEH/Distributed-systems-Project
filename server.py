#Flask Server

#Imports
from flask import Flask, render_template, request, redirect, url_for, make_response, jsonify, session




app = Flask(__name__)
app.secret_key = "super secret key"



@app.route('/')
def index():
    return render_template('index.html')
