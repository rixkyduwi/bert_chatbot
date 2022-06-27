from tokenize import Token
from turtle import pos
from flask import Blueprint, render_template,request,redirect,url_for,jsonify,make_response,flash
from application import app,db,ADMIN,SISWA,GURU
from .models import HISTORY
from .bert import bert_prediction
from flask_login import login_required, current_user
from application import models 
from werkzeug.utils import secure_filename
import os,glob,urllib.request
from functools import wraps
main = Blueprint('main', __name__)

def roles_required(*role_names):
    def decorator(original_route):
        @wraps(original_route)
        def decorated_route(*args, **kwargs):
            if not current_user.is_authenticated:
                print('The user is not authenticated.')
                return redirect(url_for('login'))
            
            print(current_user.role)
            print(role_names)
            if not current_user.role in role_names:
                print('The user does not have this role.')
                return redirect(url_for('login'))
            else:
                print('The user is in this role.')
                return original_route(*args, **kwargs)
        return decorated_route
    return decorator
@app.route('/') 
def index():
    return render_template('index.html')
@app.route('/login')
def login():
      if current_user.is_authenticated:
          return redirect(url_for('dashboard'))
      return render_template('login.html')
@app.route('/signup')
def signup():
      if current_user.is_authenticated:
          return redirect(url_for('dashboard'))
      return render_template('signup.html')
@app.route('/dashboard')
@roles_required('admin','guru')
def dashboard():
    return render_template("dashboard/index.html", name=current_user.name)
@app.route('/admin')
@roles_required('admin')
def admin():
    admin= ADMIN.query.all()
    return render_template("dashboard/index.html",admin=admin, name=current_user.name)
@app.route('/guru')
@roles_required('admin')
def guru():
    guru= GURU.query.all()
    return render_template("dashboard/index.html", guru=guru,name=current_user.name)
@app.route('/siswa')
@roles_required('admin','guru')
def siswa():
    siswa= SISWA.query.all()
    return render_template("dashboard/index.html", siswa=siswa, name=current_user.name)
@app.route('/history')
@roles_required('admin','guru')
def history():
    history= HISTORY.query.all()
    return render_template("dashboard/index.html", history=history, name=current_user.name)
@app.route("/apipredict", methods=['POST'])
@roles_required('admin','guru','siswa')
def apipredict():
    user=current_user.name
    context = request.form['context']
    print(context)
    question = request.form['question']
    print(question)
    return bert_prediction(user,str(context),str(question))
@app.route("/chatbot")
@roles_required('admin','guru','siswa')
def chatbot():
    return render_template("dashboard/chatbot copy.html")
    