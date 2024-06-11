from service import app, db, csrf
from flask import render_template, request, jsonify, make_response, url_for, flash, redirect
from flask_login import UserMixin, login_user, LoginManager, login_required, logout_user, current_user
from service.controllers.authController import AuthController
from service.controllers.entityController import EntityController
from service.controllers.userController import UserController

from service.models import User, Article
import flask_bcrypt

from service.services.baseService import BaseService

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'
service = BaseService(db.session)

entityController = EntityController()
userController = UserController()
authController = AuthController()

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


# Admin Login
@app.route('/admin/login', methods=['GET'])
def admin_login():
    return authController.login()    


@app.route('/admin/dashboard', methods=['GET', 'POST'])
def admin_dashboard():
    return render_template("pages/admin/dashboard.html")


@login_required
@app.route('/admin/users', methods=['GET', 'POST'])
def admin_users():
    return userController.get_users()

@login_required
@app.route('/admin/users/add', methods=['GET', 'POST'])
def admin_users_add():
    return userController.create_user()
    
@login_required
@app.route('/admin/users/edit/<int:id>', methods=['GET', 'POST'])
def admin_users_edit(id):
    return userController.update_user(id)
    
@login_required
@app.route('/admin/users/delete/<int:id>', methods=['POST'])  # Changed to POST for better practice
def admin_users_delete(id):
    return userController.delete_user(id)

@login_required
@app.route('/admin/entities', methods=['GET', 'POST'])
def admin_entities():
    return entityController.get_entities()

@login_required
@app.route('/admin/entities/<int:id>', methods=['GET'])
def admin_entities_get(id):
    return entityController.get_entity(id)

@login_required
@app.route('/admin/entities/add', methods=['GET', 'POST'])
def admin_entities_add():
    return entityController.create_entity()

@login_required
@app.route('/admin/users/edit/<int:id>', methods=['GET', 'POST'])
def admin_entities_update(id):
    return entityController.update_entity(id)

@login_required
@app.route('/admin/users/delete/<int:id>', methods=['POST'])
def admin_entities_delete(id):
    return entityController.delete_entity(id)
