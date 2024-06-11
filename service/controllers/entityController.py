from datetime import datetime
from flask import abort, jsonify, render_template, request
from flask_login import current_user
from service.models import Entity
from service.services.baseService import BaseService
from service import db

class EntityController:
    def __init__(self):
        self.service = BaseService(db.session)
        
    def get_entities(self):
        entities = self.service.get_all(Entity)
        return render_template("pages/admin/pages/entities/index.html", user=current_user.username, data=entities)

    def get_entity(self, id):
        entity = self.service.get(Entity, id)
        if not entity:
            abort(404)
        return jsonify(entity)

    def create_entity(self):
        if not request.json or not 'name' in request.json:
            abort(400)
        data = {
            'name': request.json['name'],
            'created_at': datetime.utcnow(),  # Optionally set defaults for fields not provided
            'updated_at': datetime.utcnow()
        }
        entity = self.service.create(Entity, data)
        return jsonify(entity), 201

    def update_entity(self, id):
        if not request.json:
            abort(400)
        entity = self.service.get(Entity, id)
        if not entity:
            abort(404)
        data = {}
        if 'name' in request.json:
            data['name'] = request.json['name']
        if data:
            data['updated_at'] = datetime.utcnow()
        result = self.service.update(Entity, id, data)
        if not result:
            abort(404)
        return jsonify(result)

    def delete_entity(self, id):
        result = self.service.delete(Entity, id)
        if not result:
            abort(404)
        return jsonify({'result': True})