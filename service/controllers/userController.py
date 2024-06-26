from datetime import datetime, timezone
from flask import abort, flash, jsonify, redirect, render_template, request, url_for
from flask_login import current_user
from service.models import User, Group
from service.services.baseService import BaseService
from service import db
import flask_bcrypt

class UserController:
    def __init__(self):
        self.service = BaseService(db.session)

    def unique_validator(self,validation):
        if validation == 'name':
            return User.query.filter_by(username=validation).first()
        if validation == 'email':
            return User.query.filter_by(email=validation).first()
        if validation == 'contact':
            return User.query.filter_by(phone=validation).first()
        
    def get_users(self):
        users = self.service.get_all(User)
        groups = self.service.get_all(Group)
        return render_template("pages/users/index.html", user='current_user.username', data=users, groups=groups)

    def get_user(self, id):
        user = self.service.get(User, id)
        if not user:
            abort(404)
        return jsonify(user)

    def create_user(self):
        groups = self.service.get_all(Group)
        if request.method == "POST":
            if 'username' not in request.form or 'phone' not in request.form or 'group_id' not in request.form or 'password' not in request.form:
                abort(400)
            username = request.form['username']
            email = request.form['email']
            phone = request.form['phone']
            if self.unique_validator(username) or self.unique_validator(email) or self.unique_validator(phone):
                abort(400)
            data = {
                'username': username,
                'email': email,
                'phone': phone,
                'gender': request.form['gender'],
                'group_id': request.form['group_id'],
                'password': flask_bcrypt.generate_password_hash("password")
            }
            user = self.service.create(User, data)
            if user:
                return redirect(url_for('admin_users'))
        return render_template("pages/users/new.html", user='current_user.username', groups=groups)

    def update_user(self, id):
        groups = self.service.get_all(Group)
        user = self.service.get(User, id)
        if request.method == "POST":
            data = {}
            if 'username' in request.form:
                data['username'] = request.form['username']
            if 'email' in request.form:
                data['email'] = request.form['email']
            if 'phone' in request.form:
                data['phone'] = request.form['phone']
            if 'gender' in request.form:
                data['gender'] = request.form['gender']
            if 'group_id' in request.form:
                data['group_id'] = request.form['group_id']
            if 'password' in request.form:
                data['password'] = flask_bcrypt.generate_password_hash(request.form['password'])
            data['updated_at'] = datetime.now(timezone.utc)
            
            if data:
                result = self.service.update(User, id, data)
                if result:
                    return redirect(url_for('admin_users'))
        return render_template("pages/users/edit.html", user='current_user.username', data=user, groups=groups)


    def delete_user(self, id):
        if self.service.delete(User, id):
            flash('User deleted successfully.')
        else:
            flash('User deletion failed.')
        return redirect(url_for('admin_users'))