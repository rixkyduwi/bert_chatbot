from application import app,db,ADMIN,SISWA,GURU
from flask import Blueprint, render_template,request,redirect,url_for,jsonify,make_response,flash
from flask_login import login_user, logout_user, login_required,current_user
from werkzeug.security import check_password_hash,generate_password_hash
from flask import request,jsonify
import random, string,jwt

from flask_restful import Resource, Api
auth = Blueprint('auth', __name__)
api = Api(auth)


class apiregisterADMIN(Resource):
    def post(self):
        email = request.form.get('email')
        name = request.form.get('name')
        password = request.form.get('password')

        admin = ADMIN.query.filter_by(email=email).first() # if this returns a user, then the email already exists in database
        if admin: # if a user is found, we want to redirect back to signup page so user can try again
            flash('Email sudah ada')
            return redirect(url_for('signup'))
            # create a new user with the form data. Hash the password so the plaintext version isn't saved.
        admin_baru = ADMIN(email=email, name=name, password=generate_password_hash(password, method='sha256'),token='')
            # add the new user to the database
        db.session.add(admin_baru)
        db.session.commit()
        return redirect(url_for('login'))
class apiloginADMIN(Resource):
    def post(self):
        email = request.form['email']
        password = request.form['password']
        j=15
        admin= ADMIN.query.filter_by(email=email).first()
        if not admin:
            flash('email berbeda')
            return redirect(url_for('login'))
        elif not check_password_hash(admin.password, password):
            flash("password salah")
            return redirect(url_for('login'))
        token = ''.join(random.choices(string.ascii_uppercase + string.digits, k = j))
        admin.token= token
        login_user(admin)
        db.session.commit()
        return redirect(url_for('dashboard'))
@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))
class apiGURU(Resource):
    #login
    def get(self):
        NIP = request.form['nip']
        Password = request.form['password']
        guru= GURU.query.filter_by(NIP=NIP).first()
        j=15
        if not guru:
            flash('email berbeda')
            return redirect(url_for('login'))
        elif not check_password_hash(guru.password, Password):
            flash("password salah")
            return redirect(url_for('login'))
        token = ''.join(random.choices(string.ascii_uppercase + string.digits, k = j))
        guru.token= token
        login_user(guru)
        db.session.commit()
        return redirect(url_for('auth.apilogin'))  
    #register
    def post(self):
        NIP = request.form['nip']
        Nama = request.form['nama']
        Password = request.form['password']
        Alamat = request.form['alamat']
        guru = GURU.query.filter_by(NIP=NIP).first() # if this returns a user, then the email already exists in database
        if guru: # if a user is found, we want to redirect back to signup page so user can try again
            flash('NIP Sudah Ada')
            return redirect(url_for('signup'))
        admin = GURU(NIP=NIP,Nama=Nama,Password=generate_password_hash(Password),token= '',Alamat=Alamat)
        db.session.add(admin)
        db.session.commit()
        return redirect(url_for('dashboard'))
class apiSISWA(Resource):
    #login
    def get(self):
        NIS = request.form['nis']
        Password = request.form['password']
        j=15
        siswa= SISWA.query.filter_by(NIS=NIS).first()
        if not siswa:
            return "email berbeda"
        elif not check_password_hash(siswa.password, Password):
            return "password salah"
        token = ''.join(random.choices(string.ascii_uppercase + string.digits, k = j))
        siswa.token= token
        login_user(siswa)
        db.session.commit()
        return "halo"+str(siswa.Nama)
    #register
    def post(self):
        NIS = request.form['nis']
        Nama = request.form['nama']
        Password = request.form['password']
        Alamat = request.form['alamat']
        NamaOrtu =  request.form['namaortu']
        siswa =SISWA.query.filter_by(NIS=NIS).first() # if this returns a user, then the email already exists in database
        if siswa: # if a user is found
            return "NIS sudah ada"
        siswa = SISWA(NIS=NIS,Nama=Nama,Password=generate_password_hash(Password),Alamat=Alamat,NamaOrtu=NamaOrtu,token= '')
        db.session.add(siswa)
        db.session.commit()
        return "halo"+str(Nama)
api.add_resource(apiregisterADMIN, '/api/v1/admin/create', methods=['POST'])
api.add_resource(apiloginADMIN, '/api/v1/admin/login', methods=['POST'])
api.add_resource(apiSISWA, '/api/v1/siswa', methods=['GET','POST'])
api.add_resource(apiGURU, '/api/v1/guru', methods=['GET','POST'])