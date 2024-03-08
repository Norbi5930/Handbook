from Web import app 

SECRET_KEY = "KEY"
SQLALCHEMY_DATABASE_URI = "DATABASE"
app.config["UPLOAD_FOLDER"] = "Web/static/images"
app.config["PROFILE_PICTURE_UPLOAD_FOLDER"] = "Web/static/profile_images"
app.config["POST_PICTURE_UPLOAD_FOLDER"] = "Web/static/posts_images"
