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
    return render_template("dashboard/index.html", name=current_user.nama)
@app.route('/admin') 
@roles_required('admin') 
def admin(): 
    admin= ADMIN.query.all()
    return render_template("dashboard/data_admin.html",admin=admin,name=current_user.nama)
@main.route('/deleteadmin/<id>')
@roles_required('admin') 
def deleteadmin(id):
    try:
        if request.method == 'GET':
            admin = ADMIN.query.filter_by(id=id).first()
            db.session.delete(admin)
            db.session.commit()
            flash('Data Admin Sudah Dihapus')
    except Exception as e:
        return make_response(e)
    return redirect(url_for('admin'))
@app.route('/guru') 
@roles_required('admin') 
def guru(): 
    guru= GURU.query.all() 
    return render_template("dashboard/data_guru.html", guru=guru,name=current_user.nama)
@main.route('/deleteguru/<id>')
@roles_required('admin') 
def deleteguru(id):
    try:
        if request.method == 'GET':
            guru = GURU.query.filter_by(NIP=id).first()
            db.session.delete(guru)
            db.session.commit()
            flash('Data Guru Sudah Dihapus')
    except Exception as e:
        return make_response(e)
    return redirect(url_for('guru'))
@app.route('/siswa') 
@roles_required('admin','guru') 
def siswa(): 
    siswa= SISWA.query.all() 
    return render_template("dashboard/data_siswa.html", siswa=siswa, name=current_user.nama)
@main.route('/deletesiswa/<id>')
@roles_required('admin','guru') 
def deletesiswa(id):
    try:
        if request.method == 'GET':
            siswa= SISWA.query.filter_by(NIS=id).first()
            db.session.delete(siswa)
            db.session.commit()
            flash('Data Siswa Sudah Dihapus')
    except Exception as e:
        return make_response(e)
    return redirect(url_for('siswa'))
@app.route('/history')
@roles_required('admin','guru') 
def history(): 
    history= HISTORY.query.all() 
    return render_template("dashboard/data_history.html", history=history, name=current_user.nama)
@app.route('/history_siswa')
@roles_required('admin','siswa') 
def history_siswa(): 
    history= HISTORY.query.filter_by(nama=current_user.nama).first()
    return render_template("dashboard/index.html",tanggal=history['tanggal'], history=history, name=current_user.nama)
@app.route("/apipredict", methods=['POST']) 
def apipredict():  
    user=current_user.nama
    context = request.form['context'] 
    print(context) 
    question = request.form['question'] 
    print(question) 
    return bert_prediction(user,str(context),str(question)) 
@app.route("/apipredictandroid", methods=['POST']) 
def apipredictandroid():  
    user='user android'
    context = request.form['context'] 
    print(context) 
    question = request.form['question'] 
    print(question) 
    return bert_prediction(user,str(context),str(question)) 
@app.route("/chatbot") 
def chatbot(): 
    return render_template("dashboard/chatbot.html") 
@app.route("/chatbotandroid") 
def chatbotandroid(): 
    return render_template("dashboard/chatbotandroid.html") 
    