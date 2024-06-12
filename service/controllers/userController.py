from datetime import datetime, timezone
from flask import abort, flash, jsonify, redirect, render_template, request, url_for
from flask_login import current_user
from service.models import User
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
        return render_template("pages/admin/pages/users/index.html", user=current_user.username, data=users)

    def get_user(self, id):
        user = self.service.get(User, id)
        if not user:
            abort(404)
        return jsonify(user)

    def create_user(self):
        if request.method == "POST":
            if 'username' not in request.json or 'phone' not in request.json or 'group_id' not in request.json or 'password' not in request.json:
                abort(400)
            username = request.json['username']
            email = request.json['email']
            phone = request.json['phone']
            if self.unique_validator(username) or self.unique_validator(email) or self.unique_validator(phone):
                abort(400)
            data = {
                'username': username,
                'email': email,
                'phone': phone,
                'gender': request.json['gender'],
                'group_id': request.json['group_id'],
                'password': flask_bcrypt.generate_password_hash("password")
            }
            self.service.create(User, data)
            return redirect(url_for('admin_users'))
        return render_template("pages/admin/pages/users/new.html", user=current_user.username)

    def update_user(self, id):
        user = self.service.get(User, id)
        if request.method == "POST":
            data = {}
            if data:
                if 'username' in request.json:
                    data['username'] = request.json['username']
                if 'email' in request.json:
                    data['email'] = request.json['email']
                if 'phone' in request.json:
                    data['phone'] = request.json['phone']
                if 'gender' in request.json:
                    data['gender'] = request.json['gender']
                if 'group_id' in request.json:
                    data['group_id'] = request.json['group_id']
                if 'password' in request.json:
                    data['password'] = flask_bcrypt.generate_password_hash(request.json['password'])
                data['updated_at'] = datetime.now(timezone.utc)

            self.service.update(User, id, data)
            return redirect(url_for('admin_users'))
        return render_template("pages/admin/pages/users/edit.html", user=current_user.username, data=user)


    def delete_user(self, id):
        if self.service.delete(User, id):
            flash('User deleted successfully.')
        else:
            flash('User deletion failed.')
        return redirect(url_for('admin_users'))