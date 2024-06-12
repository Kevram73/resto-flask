from datetime import datetime, timezone
from flask import abort, jsonify, render_template, request
from flask_login import current_user
from service.models import TypeCategory
from service.services.baseService import BaseService
from service import db

class TypeCategoryController:
    def __init__(self):
        self.service = BaseService(db.session)

    def get_typeCategories(self):
        typeCategories = self.service.get_all(TypeCategory)
        return render_template("pages/admin/pages/typeCategories/index.html", user=current_user.username, data=typeCategories)

    def get_typeCategory(self, id):
        typeCategory = self.service.get(TypeCategory, id)
        if not typeCategory:
            abort(404)
        return jsonify(typeCategory)

    def create_typeCategory(self):
        if not request.json or not 'name' in request.json:
            abort(400)
        data = {
            'name': request.json['name'],
            'created_at': datetime.now(timezone.utc),  # Optionally set defaults for fields not provided
        }
        typeCategory = self.service.create(TypeCategory, data)
        return jsonify(typeCategory), 201

    def update_typeCategory(self, id):
        if not request.json:
            abort(400)
        typeCategory = self.service.get(TypeCategory, id)
        if not typeCategory:
            abort(404)
        data = {}
        if 'name' in request.json:
            data['name'] = request.json['name']
        if data:
            data['updated_at'] = datetime.now(timezone.utc)
        result = self.service.update(TypeCategory, id, data)
        if not result:
            abort(404)
        return jsonify(result)

    def delete_typeCategory(self, id):
        result = self.service.delete(TypeCategory, id)
        if not result:
            abort(404)
        return jsonify({'result': True})