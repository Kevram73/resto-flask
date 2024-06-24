from datetime import datetime, timezone
from flask import abort, jsonify, render_template, request, redirect, url_for
from flask_login import current_user
from service.models import Entity
from service.services.baseService import BaseService
from service import db

class EntityController:
    def __init__(self):
        self.service = BaseService(db.session)
        
    def get_entities(self):
        entities = self.service.get_all(Entity)
        return render_template("pages/entities/index.html", user='current_user.username', data=entities)

    def get_entity(self, id):
        entity = self.service.get(Entity, id)
        if not entity:
            abort(404)
        return jsonify(entity)

    def create_entity(self):
        if not request.form or not 'name' in request.form:
            abort(400)
        data = {
            'name': request.form['name'],
            'created_at': datetime.now(timezone.utc),  # Optionally set defaults for fields not provided
            'updated_at': datetime.now(timezone.utc)
        }
        entity = self.service.create(Entity, data)
        return redirect(url_for('admin_entities'))

    def update_entity(self, id):
        if not request.form:
            abort(400)
        entity = self.service.get(Entity, id)
        if not entity:
            abort(404)
        data = {}
        if 'name' in request.form:
            data['name'] = request.form['name']
        if data:
            data['updated_at'] = datetime.now(timezone.utc)
        result = self.service.update(Entity, id, data)
        if not result:
            abort(404)
        return redirect(url_for('admin_entities'))

    def delete_entity(self, id):
        result = self.service.delete(Entity, id)
        if not result:
            abort(404)
        return redirect(url_for('admin_entities'))