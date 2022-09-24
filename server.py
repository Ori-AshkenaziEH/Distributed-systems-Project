# Server On FLask
from flask import Flask, render_template, request, redirect, url_for, make_response, jsonify, session
from MongoDB import db
import signal
from leader_election import LeaderElection
from multiprocessing import Process
import time

def handler(signum, frame):
    print("\nThe Server: " + le.znode_name + " is Offline.")
    print("Ctrl-c was pressed.\nEXIT\n", end="", flush=True)
    le.zk.stop()
    le.zk.close()
    exit(1)







app = Flask(__name__)
app.secret_key = "super secret key"
le = LeaderElection('localhost:2181', 'AppChat', '/election')
le.register()
signal.signal(signal.SIGINT, handler)










@app.route('/')
def index():
    return render_template('index.html')


@app.route('/login', methods=['POST'])
def login():
    username: str = request.form["name"]
    password: str = request.form["password"]
    Uresult = db.users.find_one({'username': username})
    Presult = db.users.find_one({'password': password})
    if Uresult is not None and Presult is not None:
        session['username'] = username
        session['password'] = password
        return redirect('/getallposts')
    else:
        return redirect('/get_register')


@app.route('/get_login', methods=['GET'])
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



@app.route('/getallposts', methods=['GET'])
def getallposts():
    collection = db.posts.find()
    return render_template("chat.html", collection= collection,username=session['username'])

@app.route('/post', methods=['POST'])
def post():
    post = {
        "username": session['username'],
        "post": request.form["post"]
    }
    db.posts.insert_one(post)
    return redirect('/getallposts')
