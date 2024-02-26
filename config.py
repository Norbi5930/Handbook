from Web import app 

SECRET_KEY = "154sadasdztdfgbvcnb456"
SQLALCHEMY_DATABASE_URI = "mysql+pymysql://root@localhost/handbook"
app.config["UPLOAD_FOLDER"] = "Web/static/images"
