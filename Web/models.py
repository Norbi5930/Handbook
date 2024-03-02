from Web import db, login_manager
from flask_login import UserMixin


@login_manager.user_loader
def load_user(id):
    return User.query.get(str(id))



class User(db.Model, UserMixin):
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(30), nullable=False, unique=True)
    email = db.Column(db.String(30), nullable=False, unique=True)
    password = db.Column(db.String(100), nullable=False)
    logged = db.Column(db.Boolean)
    admin = db.Column(db.Boolean)
    about = db.Column(db.String(300))
    picture = db.Column(db.String(100))
    uploads = db.relationship("WebShopElements", backref="uploader", lazy=True)
    cart = db.relationship("Carts", backref="user_cart", lazy=True)
    notification = db.relationship("NotificationMessage", backref="notification", lazy=True)




class WebShopElements(db.Model):
    __tablename__ = "shopelements"
    id = db.Column(db.Integer, primary_key=True)
    uploader_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    title = db.Column(db.String(50), nullable=False)
    description = db.Column(db.String(200))
    price = db.Column(db.Integer, nullable=False)
    image_file = db.Column(db.String(100))
    date = db.Column(db.String(30), nullable=False)


class Carts(db.Model):
   __tablename__ = "Carts"
   id = db.Column(db.Integer, primary_key=True)
   itemID = db.Column(db.Integer, db.ForeignKey("shopelements.id"), nullable=False)
   cartOwnerID = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)



class NotificationMessage(db.Model):
    __tablename__ = "Notification_Messages"
    id = db.Column(db.Integer, primary_key=True)
    owner_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    message = db.Column(db.String(100), nullable=False)
    read = db.Column(db.Boolean)
