from Web import app 

SECRET_KEY = "asqwe1546asdwqeqwe1542"
SQLALCHEMY_DATABASE_URI = "mysql+pymysql://root@localhost/handbook"
app.config["UPLOAD_FOLDER"] = "Web/static/images"
app.config["PROFILE_PICTURE_UPLOAD_FOLDER"] = "Web/static/profile_images"
