from datetime import datetime, timezone
from flask import abort, jsonify, render_template, request, redirect, url_for
from flask_login import current_user
from service.models import UserEntity, Entity, User
from service.services.baseService import BaseService
from service import db

class UserEntityController:
    def __init__(self):
        self.service = BaseService(db.session)
        
    def get_userEntities(self):
        entities = self.service.get_all(Entity)
        users = self.service.get_all(User)
        userEntities = self.service.get_all(UserEntity)
        return render_template("pages/entities/userEntity.html", user='current_user.username', data=userEntities, users=users, entities=entities)

    def get_userEntity(self, id):
        userEntity = self.service.get(UserEntity, id)
        if not userEntity:
            abort(404)
        return jsonify(userEntity)

    def create_userEntity(self):
        print(request.form)
        if not request.form and not 'user_id' in request.form and 'entity_id' not in request.form:
            abort(400)
        data = {
            'user_id': request.form['user_id'],
            'entity_id': request.form['entity_id'],
            'created_at': datetime.now(timezone.utc),  # Optionally set defaults for fields not provided
            'updated_at': datetime.now(timezone.utc)
        }
        userEntity = self.service.create(UserEntity, data)
        return redirect(url_for('admin_userEntities'))

    def update_userEntity(self, id):
        if not request.form:
            abort(400)
        userEntity = self.service.get(UserEntity, id)
        if not userEntity:
            abort(404)
        data = {}
        if userEntity:
            if 'user_id' in request.form:
                data['user_id'] = request.form['user_id']
            if 'entity_id' in request.form:
                data['entity_id'] = request.form['entity_id']
            data['updated_at'] = datetime.now(timezone.utc)
        result = self.service.update(UserEntity, id, data)
        if not result:
            abort(404)
        return redirect(url_for('admin_userEntities'))

    def delete_userEntity(self, id):
        result = self.service.delete(UserEntity, id)
        if not result:
            abort(404)
        return redirect(url_for('admin_userEntities'))