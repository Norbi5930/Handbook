from Web import app 

SECRET_KEY = "YOUR KEY"
SQLALCHEMY_DATABASE_URI = "YOUR DATABASE"
app.config["UPLOAD_FOLDER"] = "Web/static/images"

app.config["PROFILE_PICTURE_UPLOAD_FOLDER"] = "Web/static/profile_images"
app.config["POST_PICTURE_UPLOAD_FOLDER"] = "Web/static/posts_images"



app.config["MAIL_SERVER"] = "smtp.googlemail.com"
app.config["MAIL_PORT"] = 587
app.config["MAIL_USE_TLS"] = True
app.config["MAIL_USERNAME"] = "bnorbert0925@gmail.com"
app.config["MAIL_PASSWORD"] = "fqit wekr amjx muah"