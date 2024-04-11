from Web import app 

SECRET_KEY = "asdkognings15xb15436698bcvaf"
SQLALCHEMY_DATABASE_URI = "mysql+pymysql://root@localhost/handbook"
app.config["UPLOAD_FOLDER"] = "Web/static/images"
app.config["PROFILE_PICTURE_UPLOAD_FOLDER"] = "Web/static/profile_images"
app.config["POST_PICTURE_UPLOAD_FOLDER"] = "Web/static/posts_images"
