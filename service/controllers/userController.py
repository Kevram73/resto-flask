from datetime import datetime
from flask import abort, flash, jsonify, redirect, render_template, request, url_for
from flask_login import current_user
from service.models import User
from service.services.baseService import BaseService
from service import db
import flask_bcrypt

class UserController:
    def __init__(self):
        self.service = BaseService(db.session)
        
    def get_users(self):
        users = self.service.get_all(User)
        return render_template("pages/admin/pages/users/index.html", user=current_user.username, data=users)

    def get_user(self, id):
        user = self.service.get(User, id)
        if not user:
            abort(404)
        return jsonify(user)

    def create_user(self):
        if request.method == "POST":
            data = {
                'username': request.form['username'],
                'email': request.form['email'],
                'password': flask_bcrypt.generate_password_hash("password")
            }
            self.service.create(User, data)
            return redirect(url_for('admin_users'))
        return render_template("pages/admin/pages/users/new.html", user=current_user.username)

    def update_user(self, id):
        user = self.service.get(User, id)
        if request.method == "POST":
            data = {
                'username': request.form['username'],
                'email': request.form['email']
            }
            self.service.update(User, id, data)
            return redirect(url_for('admin_users'))
        return render_template("pages/admin/pages/users/edit.html", user=current_user.username, data=user)


    def delete_user(self, id):
        if self.service.delete(User, id):
            flash('User deleted successfully.')
        else:
            flash('User deletion failed.')
        return redirect(url_for('admin_users'))