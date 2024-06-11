from flask import render_template, request, redirect, url_for, flash

from service.services.baseService import BaseService
from ..models import User
import flask_bcrypt
from flask_login import UserMixin, login_user, LoginManager, login_required, logout_user, current_user
from service import db

class AuthController:
    def __init__(self):
        self.service = BaseService(db.session)

    def login(self):
        if request.method=="POST":
            user = User.query.filter_by(email=request.form.email).first()
            print(user)
            if user:
                if flask_bcrypt.check_password_hash(user.password, request.form.password):
                    login_user(user)
                    return redirect(url_for('admin_dashboard'))
            else:
                flash("Email ou mot de passe invalide")
        return render_template('pages/admin/login.html')
    
    