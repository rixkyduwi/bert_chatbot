from application import app #ini untuk mengambil app dari file __init__.py dari folder application 


if __name__ == "__main__":
    app.run(port=5000,debug=True)