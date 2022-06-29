from flask_login import UserMixin
import datetime
from application import db
from sqlalchemy import DATETIME, TIMESTAMP
class ADMIN(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True) # primary keys are required by SQLAlchemy
    email = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(100))
    role = db.Column(db.String(100))
    name = db.Column(db.String(1000))
    token = db.Column(db.String(1000))

class HISTORY(db.Model):
    id = db.Column(db.Integer, primary_key=True) # kudu ana primary key
    nama = db.Column(db.String(100))
    tanggal = db.Column(TIMESTAMP,default=datetime.datetime.now)
    konteks = db.Column(db.String(3000))
    pertanyaan = db.Column(db.String(1000))
    rank = db.Column(db.String(100))
    jawaban = db.Column(db.String(1000))
    score = db.Column(db.String(100))
    waktu_proses = db.Column(db.String(100))

class GURU(UserMixin, db.Model):
    NIP = db.Column(db.String(100), primary_key=True) # primary keys are required by SQLAlchemy
    Nama = db.Column(db.String(100))
    Password = db.Column(db.String(100))
    role = db.Column(db.String(100))
    Alamat = db.Column(db.String(1000))
    Token = db.Column(db.String(1000))

class SISWA(UserMixin, db.Model):
    NIS = db.Column(db.String(100), primary_key=True) # primary keys are required by SQLAlchemy
    Nama = db.Column(db.String(100))
    Password = db.Column(db.String(100))
    role = db.Column(db.String(100))
    Alamat = db.Column(db.String(1000))
    NamaOrtu = db.Column(db.String(1000))
    Token = db.Column(db.String(1000))
    