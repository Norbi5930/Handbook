from Web import app 

SECRET_KEY = "adsas154a564a218ghh8fth4f"
SQLALCHEMY_DATABASE_URI = "mysql+pymysql://root@localhost/handbook"
app.config["UPLOAD_FOLDER"] = "Web/static/images/"