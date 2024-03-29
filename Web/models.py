from Web import db, login_manager
from flask_login import UserMixin
from sqlalchemy import and_, or_


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
    posts = db.relationship("Posts", backref="user_posts", lazy=True)
    cart = db.relationship("Carts", backref="user_cart", lazy=True)
    notification = db.relationship("NotificationMessage", backref="notification", lazy=True)
    friend_requests = db.relationship("FriendRequests", foreign_keys="FriendRequests.send_id", backref="sender", lazy=True) 

    @property
    def friends(self):
        friends = User.query.join(FriendList, or_(
            FriendList.owner_id == self.id,
            FriendList.friend_id == self.id
        )).filter(User.id != self.id).all()
        return friends




class WebShopElements(db.Model):
    __tablename__ = "shopelements"
    id = db.Column(db.Integer, primary_key=True)
    uploader_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    uploader_photo = db.Column(db.String(100))
    uploader_name = db.Column(db.String(30), nullable=False)
    title = db.Column(db.String(50), nullable=False)
    description = db.Column(db.String(200))
    price = db.Column(db.Integer, nullable=False)
    image_file = db.Column(db.String(100))
    date = db.Column(db.String(30), nullable=False)


class Posts(db.Model):
    __tablename__ = "posts"
    id = db.Column(db.Integer, primary_key=True)
    uploader_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    uploader_photo = db.Column(db.String(100))
    uploader_name = db.Column(db.String(30), nullable=False)
    title = db.Column(db.String(60), nullable=False)
    description = db.Column(db.String(200))
    image_file = db.Column(db.String(100))
    date = db.Column(db.String(30), nullable=False)

class Carts(db.Model):
   __tablename__ = "carts"
   id = db.Column(db.Integer, primary_key=True)
   itemID = db.Column(db.Integer, db.ForeignKey("shopelements.id"), nullable=False)
   cartOwnerID = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)



class NotificationMessage(db.Model):
    __tablename__ = "notification_Messages"
    id = db.Column(db.Integer, primary_key=True)
    owner_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    message = db.Column(db.String(100), nullable=False)
    read = db.Column(db.Boolean)
    category = db.Column(db.String(30), nullable=False)
    request_id = db.Column(db.Integer)
    date = db.Column(db.String(40), nullable=False)



class FriendRequests(db.Model):
    __tablename__ = "friendrequests"
    id = db.Column(db.Integer, primary_key=True)
    send_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    received_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    accepted = db.Column(db.Boolean)


class FriendList(db.Model):
    __tablename__ = "friendlist"
    id = db.Column(db.Integer, primary_key=True)
    owner_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    friend_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)

class Chat(db.Model):
    __tablename__ = "chat"
    id = db.Column(db.Integer, primary_key=True)
    user1_id = db.Column(db.Integer, nullable=False)
    user2_id = db.Column(db.Integer, nullable=False)
    messages = db.relationship("Message", backref="messages", lazy=True)
        

class Message(db.Model):
    __tablename__ = "message"
    id = db.Column(db.Integer, primary_key=True)
    chat_id = db.Column(db.Integer, db.ForeignKey("chat.id"))
    sender_username = db.Column(db.String(40), nullable=False)
    message = db.Column(db.String(200), nullable=False)
    date = db.Column(db.String(40), nullable=False)