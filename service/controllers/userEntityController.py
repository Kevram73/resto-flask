from datetime import datetime, timezone
from flask import abort, jsonify, render_template, request
from flask_login import current_user
from service.models import UserEntity
from service.services.baseService import BaseService
from service import db

class UserEntityController:
    def __init__(self):
        self.service = BaseService(db.session)
        
    def get_userEntities(self):
        userEntities = self.service.get_all(UserEntity)
        return render_template("pages/admin/pages/userEntities/index.html", user=current_user.username, data=userEntities)

    def get_userEntity(self, id):
        userEntity = self.service.get(UserEntity, id)
        if not userEntity:
            abort(404)
        return jsonify(userEntity)

    def create_userEntity(self):
        if not request.json and not 'user_id' in request.json and 'entity_id' not in request.json:
            abort(400)
        data = {
            'user_id': request.json['user_id'],
            'entity_id': request.json['entity_id'],
            'created_at': datetime.now(timezone.utc),  # Optionally set defaults for fields not provided
            'updated_at': datetime.now(timezone.utc)
        }
        userEntity = self.service.create(UserEntity, data)
        return jsonify(userEntity), 201

    def update_userEntity(self, id):
        if not request.json:
            abort(400)
        userEntity = self.service.get(UserEntity, id)
        if not userEntity:
            abort(404)
        data = {}
        if data:
            if 'user_id' in request.json:
                data['user_id'] = request.json['user_id']
            if 'entity_id' in request.json:
                data['entity_id'] = request.json['entity_id']
            data['updated_at'] = datetime.now(timezone.utc)
        result = self.service.update(UserEntity, id, data)
        if not result:
            abort(404)
        return jsonify(result)

    def delete_userEntity(self, id):
        result = self.service.delete(UserEntity, id)
        if not result:
            abort(404)
        return jsonify({'result': True})