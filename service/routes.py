from service import app, db, csrf
from flask import render_template, request, jsonify, make_response, url_for, flash, redirect
from flask_login import UserMixin, login_user, LoginManager, login_required, logout_user, current_user
from service.forms import LoginForm
from service.models import User, Document, Article, BoxItem, Comment, UsefulData
import flask_bcrypt

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

@app.route("/test", methods=['GET'])
def test():
    return jsonify({"message": "Hello World!"})

