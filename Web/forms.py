from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, EmailField, SubmitField, IntegerField, FileField, TextAreaField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from flask_wtf.file import FileAllowed
from flask import flash

from .models import User


class RegisterForm(FlaskForm):
    username = StringField(render_kw={"placeholder": "Felhasználónév"}, validators=[DataRequired(), Length(min=4, max=30)])
    email = EmailField(render_kw={"placeholder": "E-mail"}, validators=[DataRequired(), Length(max=30), Email(message="A megadott formátum nem helyes!")])
    password = PasswordField(render_kw={"placeholder": "Jelszó"}, validators=[DataRequired(), Length(min=8, max=100)])
    password_confirm = PasswordField(render_kw={"placeholder": "Jelszó újra"}, validators=[DataRequired(), EqualTo("password")])
    submit = SubmitField("Regisztráció")

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).all()
        
        if user:
            flash("Ez a felhasználónév már foglalt!", "danger")
            raise ValidationError("Unavaible username")

    def validate_email(self, email):
        email = User.query.filter_by(email=email.data).all()

        if email:
            flash("Ez az email cím már foglalt!", "danger")
            raise ValidationError("Unavaible email")

class LoginForm(FlaskForm):
    username = StringField(render_kw={"placeholder": "Felhasználónév"}, validators=[DataRequired()])
    password = PasswordField(render_kw={"placeholder": "Jelszó"}, validators=[DataRequired()])
    submit = SubmitField("Bejelentkezés")



class ShopUploadForm(FlaskForm):
    file = FileField("Fájl", validators=[DataRequired(), FileAllowed(["jpg", "png"], "Csak képeket tölthetsz fel!")])
    title = StringField(render_kw={"placeholder": "Megnevezés"}, validators=[DataRequired(), Length(max=50)])
    description = TextAreaField(render_kw={"placeholder": "Leírás"}, validators=[Length(max=200)])
    price = IntegerField(render_kw={"placeholder": "Ár"})
    submit = SubmitField("Feltöltés")