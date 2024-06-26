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
from service.controllers.articleController import ArticleController
from service.controllers.casheerController import CasheerController
from service.controllers.typeCategoryController import TypeCategoryController
from service.controllers.categoryController import CategoryController
from service.controllers.companyController import CompanyController

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
articleController = ArticleController()
casheerController = CasheerController()
typeCategoryController = TypeCategoryController()
categoryController = CategoryController()
companyController = CompanyController()

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

# Article routes
#@login_required
@app.route('/admin/articles', methods=['GET', 'POST'])
def admin_articles():
    return articleController.get_articles()

#@login_required
@app.route('/admin/articles/<int:id>', methods=['GET'])
def admin_articles_get(id):
    return articleController.get_article(id)

#@login_required
@app.route('/admin/articles/add', methods=['GET', 'POST'])
def admin_articles_add():
    return articleController.create_article()

#@login_required
@app.route('/admin/articles/edit/<int:id>', methods=['GET', 'POST'])
def admin_articles_update(id):
    return articleController.update_article(id)

#@login_required
@app.route('/admin/articles/delete/<int:id>', methods=['GET','POST'])
def admin_articles_delete(id):
    return articleController.delete_article(id)

# Casheer routes
#@login_required
@app.route('/admin/casheers', methods=['GET', 'POST'])
def admin_casheers():
    return casheerController.get_casheers()

#@login_required
@app.route('/admin/casheers/<int:id>', methods=['GET'])
def admin_casheers_get(id):
    return casheerController.get_casheer(id)

#@login_required
@app.route('/admin/casheers/add', methods=['GET', 'POST'])
def admin_casheers_add():
    return casheerController.create_casheer()

#@login_required
@app.route('/admin/casheers/edit/<int:id>', methods=['GET', 'POST'])
def admin_casheers_update(id):
    return casheerController.update_casheer(id)

#@login_required
@app.route('/admin/casheers/delete/<int:id>', methods=['GET','POST'])
def admin_casheers_delete(id):
    return casheerController.delete_casheer(id)

# TypeCategory routes
#@login_required
@app.route('/admin/typeCategories', methods=['GET', 'POST'])
def admin_typeCategories():
    return typeCategoryController.get_typeCategories()

#@login_required
@app.route('/admin/casheers/<int:id>', methods=['GET'])
def admin_typeCategories_get(id):
    return typeCategoryController.get_typeCategory(id)

#@login_required
@app.route('/admin/typeCategories/add', methods=['GET', 'POST'])
def admin_typeCategories_add():
    return typeCategoryController.create_typeCategory()

#@login_required
@app.route('/admin/typeCategories/edit/<int:id>', methods=['GET', 'POST'])
def admin_typeCategories_update(id):
    return typeCategoryController.update_typeCategory(id)

#@login_required
@app.route('/admin/typeCategories/delete/<int:id>', methods=['GET','POST'])
def admin_typeCategories_delete(id):
    return typeCategoryController.delete_typeCategory(id)

# Category routes
#@login_required
@app.route('/admin/categories', methods=['GET', 'POST'])
def admin_categories():
    return categoryController.get_categories()

#@login_required
@app.route('/admin/categories/<int:id>', methods=['GET'])
def admin_categories_get(id):
    return categoryController.get_category(id)

#@login_required
@app.route('/admin/categories/add', methods=['GET', 'POST'])
def admin_categories_add():
    return categoryController.create_category()

#@login_required
@app.route('/admin/categories/edit/<int:id>', methods=['GET', 'POST'])
def admin_categories_update(id):
    return categoryController.update_category(id)

#@login_required
@app.route('/admin/categories/delete/<int:id>', methods=['GET','POST'])
def admin_categories_delete(id):
    return categoryController.delete_category(id)

# Company routes
#@login_required
@app.route('/admin/companies', methods=['GET', 'POST'])
def admin_companies():
    return companyController.get_companies()

#@login_required
@app.route('/admin/companies/<int:id>', methods=['GET'])
def admin_companies_get(id):
    return companyController.get_company(id)

#@login_required
@app.route('/admin/companies/add', methods=['GET', 'POST'])
def admin_companies_add():
    return companyController.create_company()

#@login_required
@app.route('/admin/companies/edit/<int:id>', methods=['GET', 'POST'])
def admin_companies_update(id):
    return companyController.update_company(id)

#@login_required
@app.route('/admin/companies/delete/<int:id>', methods=['GET','POST'])
def admin_companies_delete(id):
    return companyController.delete_company(id)