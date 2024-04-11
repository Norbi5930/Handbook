from flask import render_template, url_for, redirect, flash, jsonify, request
from flask_login import logout_user, current_user, login_user, login_required
from werkzeug.utils import secure_filename
import os
import datetime
from random import randint
from sqlalchemy import func, or_, and_

from . import app, db, bcrypt
from .models import User, WebShopElements, Carts, Posts, FriendRequests, FriendList, NotificationMessage, Chat, Message, PostReport
from .forms import RegisterForm, LoginForm, ShopUploadForm, EditProfilePictureForm, UploadPostForm




with app.app_context():
    try:
        db.create_all()
    except:
        print("Nem sikerült csatlakozni az adatbázishoz!")



@app.route("/")
@app.route("/home")
def home():
    return render_template("index.html", title="Kezdőlap")



@app.route("/register", methods=["GET", "POST"])
def register():
    if current_user.is_authenticated:
        return redirect(url_for("my_profile"))
    form = RegisterForm()

    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode("utf-8")
        user = User(username=form.username.data, email=form.email.data, password=hashed_password, logged=True, admin=False)
        db.session.add(user)
        db.session.commit()
        login_user(user)
        flash("Sikeres regisztráció!", "success")
        return redirect(url_for("home"))

    return render_template("register.html", title="Regisztráció", form=form)


@app.route("/login", methods=["GET", "POST"])
def login():
    if current_user.is_authenticated:
        return redirect(url_for("my_profile"))
    form = LoginForm()

    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()

        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=True)
            user.logged = True
            db.session.commit()
            flash("Sikeres bejelentkezés!", "success")
        else:
            flash("Sikertelen bejelentkezés!", "danger")
            return redirect(url_for("login"))
        
        return redirect(url_for("home"))

    return render_template("login.html", title="Bejelentkezés", form=form)


@app.route("/shop", methods=["GET", "POST"])
def shop():
    
    items = db.session.query(WebShopElements).order_by(func.random()).all()
    return render_template("shop.html", title="WebShop", items=items)


@app.route("/posts", methods=["GET", "POST"])
def posts():

    posts = db.session.query(Posts).order_by(func.random()).all()

    return render_template("posts.html", title="Hírfolyam", posts=posts)


@app.route("/shop/upload", methods=["GET", "POST"])
@login_required
def shop_upload():
    form = ShopUploadForm()
    if form.validate_on_submit():
        time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        file = form.file.data
        filename = secure_filename(file.filename)
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(file_path)
        item = WebShopElements(uploader_id=current_user.id,uploader_photo=current_user.picture, uploader_name=current_user.username, title=form.title.data, description=form.description.data, price=form.price.data, image_file=filename, date=time)
        db.session.add(item)
        db.session.commit()
        flash("Sikeres feltöltés!", "success")
        return redirect(url_for('home'))
    return render_template('shop_upload.html', title="Feltöltés", form=form)

@app.route("/post/upload", methods=["GET", "POST"])
def post_upload():
    form = UploadPostForm()

    if form.validate_on_submit():
        file = form.picture.data
        time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        if file:
            filename = secure_filename(file.name)
            file_path = os.path.join(app.config["POST_PICTURE_UPLOAD_FOLDER"], filename)
            file.save(file_path)
            post = Posts(uploader_id=current_user.id, uploader_photo=current_user.picture, uploader_name=current_user.username, title=form.title.data, description=form.description.data, image_file=filename, date=time)
        else:
            post = Posts(uploader_id=current_user.id, uploader_photo=current_user.picture, uploader_name=current_user.username, title=form.title.data, description=form.description.data, date=time)
        db.session.add(post)
        db.session.commit()
        flash("Sikeresen közzétéve!", "success")
        return redirect(url_for("my_profile"))

    return render_template("post_upload.html", title="Feltöltés", form=form)


@app.route("/my_profile", methods=["GET", "POST"])
def my_profile():
    return render_template("my_profile.html", title="Profilom", items=current_user.uploads, posts=current_user.posts)


@app.route("/notifications", methods=["GET", "POST"])
def notifications():
    
    for notification in current_user.notification:
        notification.read = True
    
    db.session.commit()
    return render_template("notification.html", title="Értesítések", notifications=current_user.notification, friend_request=FriendRequests)


@app.route("/friends", methods=["GET", "POST"])
def friends():
    return render_template("friends.html", title="Barátok", friends=current_user.friends)


@app.route("/friends/search", methods=["GET"])
def friends_search():
    return redirect(url_for("friends"))
    #search_data = request.args.get("search")
    #if search_data:
    #    print(search_data)
    #    friends = User.query.join(FriendList, or_(
    #        and_(FriendList.owner_id == current_user.id, FriendList.friend_id == current_user.id),
    #        and_(User.username == search_data)
    #    )).all()
    #    return render_template("friends.html", title=f'Barátok "{search_data}"', friends=friends)
    #else:
    #    return redirect(url_for("friends"))
    

@app.route("/my_profile/edit", methods=["GET", "POST"])
def edit_proife():
    form = EditProfilePictureForm()

    if form.validate_on_submit():
        file = form.file.data
        filename = secure_filename(file.filename)
        file_path = os.path.join(app.config["PROFILE_PICTURE_UPLOAD_FOLDER"], filename)
        file.save(file_path)
        current_user.picture = filename
        db.session.commit()
        return redirect(url_for('my_profile'))

    return render_template("edit_profile.html", title="Szerkesztés", form=form)

@app.route("/cart", methods=["GET", "POST"])
@login_required
def cart():
    cart_items = Carts.query.filter_by(cartOwnerID=current_user.id).all()
    items = []
    price = 0
    for cart_item in cart_items:
        webshop_element = WebShopElements.query.get(cart_item.itemID)
        if webshop_element:
            items.append(webshop_element)
            price += webshop_element.price

    return render_template("cart.html", title="Kosaram", items=items, items_id=cart_items, price=price)


@app.route("/<name>", methods=["GET", "POST"])
def profile(name):
    user = User.query.filter_by(username=name).first()

    return render_template("profile.html", title=f"{name}", user=user, items=user.uploads, posts=user.posts, friendlist=FriendList) if user else render_template("index.html", title="Kezdőlap")

@app.route("/search")
def search():
    search_data = request.args.get("search")
    if search_data:
        users = User.query.filter(or_(User.username.like(f"%{search_data}%")))
        return render_template("search.html", title=search_data, users=users)
    else:
        return redirect(request.referrer)
    

@app.route("/chats", methods=["GET"])
def chats():
    return render_template("chats.html", title="Chatek", User=User)

def chat_scan(user_id):
    chat = db.session.query(Chat).filter(
        or_(
            and_(Chat.user1_id == current_user.id, Chat.user2_id == user_id),
            and_(Chat.user1_id == user_id, Chat.user2_id == current_user.id)
        )
    ).first()
    return chat

@app.route("/chat/<user_id>", methods=["GET", "POST"])
def chat(user_id):
    result = chat_scan(user_id)
    if result:
        if request.method == "POST":
            data = request.get_json()
            if data:
                message = data.get("message")
                time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")
                user_message = Message(chat_id=result.id, sender_username=current_user.username, message=message, date=time)
                result.read_message = True
                db.session.add(user_message)
                db.session.commit()
                return jsonify({"success": True})
    else:
        username = User.query.get_or_404(user_id).username
        chat = Chat(user1_id = current_user.id, user2_id=user_id, user1_name=current_user.username, user2_name=username, read_message=False)
        db.session.add(chat)
        db.session.commit()
        result = chat
    return render_template("chat.html", title="Chat", chat=result)


@app.route("/api/get_notifications", methods=["GET"])
def get_notifications():
    if current_user.is_authenticated:
        notifications = NotificationMessage.query.filter_by(owner_id=current_user.id).all()
        notifications_data = [{"id": notification.id, "message": notification.message, "read": notification.read} for notification in notifications]
        return jsonify({"success": True, "notifications": notifications_data})
    else:
        return jsonify({"success": False})

@app.route("/api/friend_request", methods=["GET", "POST"])
def friend_request():
    data = request.get_json()
    if data:
        user_id = data.get("userID")
        if FriendRequests.query.filter_by(send_id=current_user.id, received_id=user_id).first() or FriendList.query.filter_by(owner_id=current_user.id, friend_id=user_id).first():
            return jsonify({"success": False, "errorMessage": "Ez a személy már a barátod, vagy a baráti kérelmek között szerepel!"})
        else:
            time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")
            friend_request = FriendRequests(send_id=current_user.id, received_id=user_id, accepted=False)
            db.session.add(friend_request)
            db.session.commit()
            notification = NotificationMessage(owner_id=user_id, message=f"{current_user.username} barátkérelmet küldött neked!", read=False, category="Barátkérelem", request_id=friend_request.id, date=time)
            db.session.add(notification)
            db.session.commit()
            return jsonify({"success": True})
    else:
        return jsonify({"success": False})


@app.route("/api/friend_request/accept", methods=["GET", "POST"])
def accept_friend_request():
    data = request.get_json()
    if data:
        request_id = data.get("requestID")
        notification = NotificationMessage.query.get_or_404(request_id)
        friend_request = FriendRequests.query.get_or_404(notification.request_id)
        time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")
        if friend_request.received_id == current_user.id:
            accepted_message = NotificationMessage(owner_id=friend_request.send_id, message=f"{current_user.username} elfogadta a barátkérelmedet!", read=False, category="Üzenet", date=time)
        else:
            accepted_message = NotificationMessage(owner_id=friend_request.received_id, message=f"{current_user.username} elfogadta a barátkérelmedet!", read=False, category="Üzenet", date=time)
        db.session.add(accepted_message)
        friend_request.accepted = True
        friend = FriendList(owner_id=current_user.id, friend_id=friend_request.send_id)
        db.session.add(friend)
        db.session.commit()
        return jsonify({"success": True})
    else:
        return jsonify({"success": False})
    
@app.route("/api/friend_request/reject", methods=["GET", "POST"])
def reject_friend_request():
    data = request.get_json()
    if data:
        request_id = data.get("requestID")
        notification = NotificationMessage.query.get_or_404(request_id)
        friend_request = FriendRequests.query.get_or_404(notification.request_id)
        db.session.delete(notification)
        db.session.delete(friend_request)
        db.session.commit()
        return jsonify({"success": True})
    else:
        return jsonify({"success": False})
    

@app.route("/api/friend/remove", methods=["POST"])
def remove_friend():
    data = request.get_json()

    if data:
        friend_id = data.get("friendID")

        object = db.session.query(FriendList).filter(
            or_(
                and_(FriendList.owner_id == current_user.id, FriendList.friend_id == friend_id),
                and_(FriendList.owner_id == friend_id, FriendList.friend_id == current_user.id)
            )
        ).first()
        db.session.delete(object)
        db.session.commit()
        return jsonify({"success": True})
    else:
        return jsonify({"success": False})

@app.route("/api/add_cart", methods=["GET", "POST"])
def add_cart():
    data = request.get_json()
    item_id = data.get("itemID")
    if item_id:
        try:
            add_cart = Carts(itemID=item_id, cartOwnerID=current_user.id)
            db.session.add(add_cart)
            db.session.commit()
            return jsonify({"success": True})
        except:
            flash("Bejelentkezés szükséges!", "danger")
            return jsonify({"success": False, "errorcode": 315})
    else:
        return jsonify({"success": False, "message": "Nincs ilyen objektum!"})
    

@app.route("/api/remove_cart", methods=["GET", "POST"])
def remove_cart():
    data = request.get_json()
    item_id = data.get("itemID")
    if item_id:
        try:
            item = Carts.query.get_or_404(item_id)
            db.session.delete(item)
            db.session.commit()
            flash("Sikeresen eltávolítva a kosárból!", "success")
            return jsonify({"success": True})
        except Exception as error:
            flash("Nem tudtuk eltávolítani az elemet a kosarából, kérjük próbálja újra később!", "danger")
            return jsonify({"success": False})
    else:
        return jsonify({"success": False})
    
@app.route("/api/remove_shop", methods=["GET", "POST"])
def remove_shop():
    data = request.get_json()

    if data:
        item_id = data.get("itemID")
        item = WebShopElements.query.get_or_404(int(item_id))
        if item.uploader_id != current_user.id:
            if (current_user.admin):
                db.session.delete(item)
                db.session.commit()
                flash("Az objektum sikeresen törölve!", "success")
                return jsonify({"success": True})
            else:
                return jsonify({"success": False, "code": "403"})
        else:
            db.session.delete(item)
            db.session.commit()
            flash("Az objektum sikeresen törölve!", "success")
            return jsonify({"success": True})
        
@app.route("/api/delete_post", methods=["GET", "POST"])
def delete_post():
    data = request.get_json()

    post_id = data.get("postID")
    if post_id:
        post = Posts.query.get_or_404(int(post_id))
        if post:
            if post.uploader_id == current_user.id:
                db.session.delete(post)
                db.session.commit()
                flash("A post sikeresen törölve!", "success")
                return jsonify({"success": True})
            else:
                return jsonify({"success": False, "errorMessage": "Nincs jogodban ezt a postot törölni!"})
        else:
            return jsonify({"success": False})
    else:
        return jsonify({"success": False})
        
@app.route("/api/edit_about", methods=["GET", "POST"])
def edit_about():
    data = request.get_json()
    content = data.get("content")

    if content:
        try:
            current_user.about = str(content)
            db.session.commit()
            return jsonify({"success": True})
        except:
            flash("Sikertelen szerkesztés! Kérlek próbáld újra később!", "danger")
            return jsonify({"success": False})

    return jsonify({"success": False})

@app.route("/api/delete_image", methods=["GET", "POST"])
def delete_profile_image():
    data = request.get_json()


    if current_user.picture:
        current_user.picture = None
        db.session.commit()
        return jsonify({"success": True})
    return jsonify({"success": False})


@app.route("/api/change_email", methods=["GET", "POST"])
def change_email():
    data = request.get_json()
    email = data.get("email")
    if email:
        if not email == current_user.email:
            valide = User.query.filter_by(email=email).all()
           
            if not valide:
                current_user.email = str(email)
                db.session.commit()
                return jsonify({"success": True})
            else:
                return jsonify({"success": False, "errorMessage": "Az e-mail cím már foglalt!"})
        else:
            return jsonify({"success": False, "errorMessage": "Jelenleg ez az e-mail címe!"})
    else:
        jsonify({"success": False})


@app.route("/api/report_post", methods=["POST"])
def report_post():
    data = request.get_json()
    post_id = data.get("postID")

    if post_id:
        post = Posts.query.get_or_404(post_id)
        time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        print(time)
        report = PostReport(post_id=post_id, post_owner_id=post.uploader_id, reporter_id=current_user.id, date=time)
        db.session.add(report)
        db.session.commit()
        return jsonify({"success": True})
    else:
        flash("A művelet nem sikerült, kérlek próbáld újra később!", "danger")
        return jsonify({"success": False})

@app.route("/logout", methods=["GET", "POST"])
def logout():
    try:
        user = User.query.get_or_404(current_user.id)
        user.logged = False
        db.session.commit()
        logout_user()
        flash("Sikeres kijelentkezés!", "success")
    except:
        flash("Sikertelen kijelentkezés!", "danger")
    return redirect(url_for("home"))