from application import app #ini untuk mengambil app dari file __init__.py dari folder application 


if __name__ == "__main__":
    app.run(host='192.168.100.63',port=5000,debug=True)