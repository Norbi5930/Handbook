from flask import render_template, url_for, redirect, flash, jsonify, request
from flask_login import logout_user, current_user, login_user, login_required
from werkzeug.utils import secure_filename
import os
import datetime
from random import randint

from Web import app, db, bcrypt
from .models import User, WebShopElements, Carts
from .forms import RegisterForm, LoginForm, ShopUploadForm


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
    form = LoginForm()

    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()

        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=False)
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
    
    items = db.session.execute(db.select(WebShopElements)).scalars()

    return render_template("shop.html", title="WebShop", items=items)


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
        item = WebShopElements(uploader_id=current_user.id, title=form.title.data, description=form.description.data, price=form.price.data, image_file=filename, date=time)
        db.session.add(item)
        db.session.commit()
        flash("Sikeres feltöltés!")
        return redirect(url_for('home'))
    return render_template('shop_upload.html', title="Feltöltés", form=form)



@app.route("/cart", methods=["GET", "POST"])
@login_required
def cart():
    cart_items = Carts.query.filter_by(cartOwnerID=current_user.id).all()
    items = []
    for cart_item in cart_items:
        webshop_element = WebShopElements.query.get(cart_item.itemID)
        if webshop_element:
            items.append(webshop_element)

    return render_template("cart.html", title="Kosaram", items=items, items_id=cart_items)



@app.route("/api/add_cart", methods=["GET", "POST"])
def add_cart():
    data = request.get_json()
    item_id = data.get("itemID")
    print(item_id)
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