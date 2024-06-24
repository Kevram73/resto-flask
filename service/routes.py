from service import app, db
from flask import render_template, request, jsonify, make_response, url_for, flash, redirect
from flask_login import UserMixin, login_user, LoginManager, login_required, logout_user, current_user
from service.controllers.authController import AuthController
from service.controllers.entityController import EntityController
from service.controllers.userController import UserController
from service.controllers.groupController import GroupController
from service.controllers.tableController import TableController
from service.controllers.fournisseurController import FournisseurController
from service.controllers.userEntityController import UserEntityController
from service.controllers.articleFamilyController import ArticleFamilyController

from service.models import User, Article
import flask_bcrypt

from service.services.baseService import BaseService

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'
service = BaseService(db.session)

entityController = EntityController()
groupController = GroupController()
userController = UserController()
tableController = TableController()
authController = AuthController()
fournisseurController = FournisseurController()
userEntityController = UserEntityController()
articleFamilyController = ArticleFamilyController()

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

# Groups routes
@login_required
@app.route('/admin/groups', methods=['GET', 'POST'])
def admin_groups():
    return groupController.get_groups()

@login_required
@app.route('/admin/groups/<int:id>', methods=['GET'])
def admin_groups_get(id):
    return groupController.get_group(id)

@login_required
@app.route('/admin/groups/add', methods=['GET', 'POST'])
def admin_groups_add():
    return groupController.create_group()
    
@login_required
@app.route('/admin/groups/edit/<int:id>', methods=['GET', 'POST'])
def admin_groups_update(id):
    return groupController.update_group(id)
    
@login_required
@app.route('/admin/groups/delete/<int:id>', methods=['GET','POST'])  # Changed to POST for better practice
def admin_groups_delete(id):
    return groupController.delete_group(id)

# Users routes
@login_required
@app.route('/admin/users', methods=['GET', 'POST'])
def admin_users():
    return userController.get_users()

@login_required
@app.route('/admin/users/<int:id>', methods=['GET'])
def admin_users_get(id):
    return userController.get_user(id)

@login_required
@app.route('/admin/users/add', methods=['GET', 'POST'])
def admin_users_add():
    return userController.create_user()
    
@login_required
@app.route('/admin/users/edit/<int:id>', methods=['GET', 'POST'])
def admin_users_update(id):
    return userController.update_user(id)
  
@login_required
@app.route('/admin/users/delete/<int:id>', methods=['GET','POST'])  # Changed to POST for better practice
def admin_users_delete(id):
    return userController.delete_user(id)

# Entities routes
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
@app.route('/admin/entities/edit/<int:id>', methods=['GET', 'POST'])
def admin_entities_update(id):
    return entityController.update_entity(id)

@login_required
@app.route('/admin/entities/delete/<int:id>', methods=['GET','POST'])
def admin_entities_delete(id):
    return entityController.delete_entity(id)

# Tables routes
#@login_required
@app.route('/admin/tables', methods=['GET', 'POST'])
def admin_tables():
    return tableController.get_tables()

#@login_required
@app.route('/admin/tables/<int:id>', methods=['GET'])
def admin_tables_get(id):
    return tableController.get_table(id)

#@login_required
@app.route('/admin/tables/add', methods=['GET', 'POST'])
def admin_tables_add():
    return tableController.create_table()

#@login_required
@app.route('/admin/tables/edit/<int:id>', methods=['GET', 'POST'])
def admin_tables_update(id):
    return tableController.update_table(id)

#@login_required
@app.route('/admin/tables/delete/<int:id>', methods=['GET','POST'])
def admin_tables_delete(id):
    return tableController.delete_table(id)

# Fournisseurs routes
#@login_required
@app.route('/admin/fournisseurs', methods=['GET', 'POST'])
def admin_fournisseurs():
    return fournisseurController.get_fournisseurs()

#@login_required
@app.route('/admin/fournisseurs/<int:id>', methods=['GET'])
def admin_fournisseurs_get(id):
    return fournisseurController.get_fournisseur(id)

#@login_required
@app.route('/admin/fournisseurs/add', methods=['GET', 'POST'])
def admin_fournisseurs_add():
    return fournisseurController.create_fournisseur()

#@login_required
@app.route('/admin/fournisseurs/edit/<int:id>', methods=['GET', 'POST'])
def admin_fournisseurs_update(id):
    return fournisseurController.update_fournisseur(id)

#@login_required
@app.route('/admin/fournisseurs/delete/<int:id>', methods=['GET','POST'])
def admin_fournisseurs_delete(id):
    return fournisseurController.delete_fournisseur(id)

# UserEntity routes
#@login_required
@app.route('/admin/userEntities', methods=['GET', 'POST'])
def admin_userEntities():
    return userEntityController.get_userEntities()

#@login_required
@app.route('/admin/userEntities/<int:id>', methods=['GET'])
def admin_userEntities_get(id):
    return userEntityController.get_userEntity(id)

#@login_required
@app.route('/admin/userEntities/add', methods=['GET', 'POST'])
def admin_userEntities_add():
    return userEntityController.create_userEntity()

#@login_required
@app.route('/admin/userEntities/edit/<int:id>', methods=['GET', 'POST'])
def admin_userEntities_update(id):
    return userEntityController.update_userEntity(id)

#@login_required
@app.route('/admin/userEntities/delete/<int:id>', methods=['GET','POST'])
def admin_userEntities_delete(id):
    return userEntityController.delete_userEntity(id)

# ArticleFamily routes
#@login_required
@app.route('/admin/articleFamilies', methods=['GET', 'POST'])
def admin_articleFamilies():
    return articleFamilyController.get_articleFamilies()

#@login_required
@app.route('/admin/articleFamilies/<int:id>', methods=['GET'])
def admin_articleFamilies_get(id):
    return articleFamilyController.get_articleFamily(id)

#@login_required
@app.route('/admin/articleFamilies/add', methods=['GET', 'POST'])
def admin_articleFamilies_add():
    return articleFamilyController.create_articleFamily()

#@login_required
@app.route('/admin/articleFamilies/edit/<int:id>', methods=['GET', 'POST'])
def admin_articleFamilies_update(id):
    return articleFamilyController.update_articleFamily(id)

#@login_required
@app.route('/admin/articleFamilies/delete/<int:id>', methods=['GET','POST'])
def admin_articleFamilies_delete(id):
    return articleFamilyController.delete_articleFamily(id)