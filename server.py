from flask import Flask, request, render_template, json, redirect, jsonify, make_response, send_file, send_from_directory, session
from flask_cors import CORS, cross_origin
import datetime, threading, csv, time, os, io
import pandas as pd
import uuid
from pymongo import  MongoClient

mongodb = MongoClient('mongodb://localhost:27017')
db = mongodb['website_bs']
db_accounts = db.accounts
db_devices = db.devices

app = Flask(__name__)
CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'

logged_accounts = []

@app.route('/',methods=["POST","GET","OPTIONS"])
def ret():
    if request.method == "GET":
        return render_template('login1.html'), 200
    elif request.method == "POST":
        file_name = request.files["file"]

        return 'Success sending your file.. Will be available at dashboard once its finished..',200
        #return str(all_results),200
        #file = request.files['file']
        #fixed_lines = file.read().split('\n')

@app.route('/index',methods=['POST','GET','OPTIONS'])
def index():
    if not session.get('logged_in'):
        return 'Log in first. <a href="/login">'
    else:
        if request.method == 'GET':
            return render_template('index.html'),200

@app.route('/register',methods=["POST","GET","OPTIONS"])
def register():
    if request.method == "GET":
        return render_template('signup3.html'), 200
    elif request.method == "POST":
        file_name = request.get_json()
        print(file_name)
        nam = file_name['name']
        em = file_name['email']
        pw = file_name['password']
        g1 = {'name':nam,
                      'email':em,
                      'password':pw}
        res = db_accounts.find_one({'email':g1['email']})
        if res:
            return jsonify(message="Its already registered."),409
        else:
            db_accounts.insert_one(g1)
            session['logged_in'] = True
            session['username'] = g1['email']
            return {'redirect_url':'/index'}#jsonify(message="Succesfully Registerd"),200
        #print(file_name['name'])
        #res = register_acc(file_name)
        #if res == False:
        #    return 'Already registered',200
        #elif res == True:
        #    return 'Success registered...', 200


        #return str(all_results),200
        #file = request.files['file']
        #fixed_lines = file.read().split('\n')

@app.route('/download/<path:filename>', methods=['GET', 'POST'])
def download(filename):
    return send_from_directory(directory=os.getcwd(), filename=filename)


@app.route('/logout', methods=['GET', 'POST'])
def logout():
    session['logged_in'] = False
    return ret()


@app.route('/sip', methods=['GET', 'POST'])
def sip():
    if not session.get('logged_in'):
        return render_template('login1.html')
    else:

        return 'Hello Boss!  <a href="/logout">Logout</a>'

def _build_cors_prelight_response():
    response = make_response()
    response.headers.add("Access-Control-Allow-Origin", "*")
    response.headers.add('Access-Control-Allow-Headers', "*")
    response.headers.add('Access-Control-Allow-Methods', "*")
    return response
app.secret_key = os.urandom(12)
app.run(host='0.0.0.0', port=5000, debug=True)