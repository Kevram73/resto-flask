from datetime import datetime, timezone
from flask import abort, jsonify, render_template, request
from flask_login import current_user
from service.models import Category
from service.services.baseService import BaseService
from service import db

class CategoryController:
    def __init__(self):
        self.service = BaseService(db.session)
        
    def get_categories(self):
        categories = self.service.get_all(Category)
        return render_template("pages/admin/pages/categories/index.html", user=current_user.username, data=categories)

    def get_category(self, id):
        category = self.service.get(Category, id)
        if not category:
            abort(404)
        return jsonify(category)

    def create_category(self):
        if not request.json or not 'name' in request.json or not 'type_category_id' in request.json:
            abort(400)

        active = request.json['active']
        if active == 'true':
            active = True
        else:
            active = False
        
        data = {
            'name': request.json['name'],
            'type_category_id': request.json['type_category_id'],
            'active' : active,
            'created_at': datetime.now(timezone.utc),  # Optionally set defaults for fields not provided
            'updated_at': datetime.now(timezone.utc)
        }
        category = self.service.create(Category, data)
        return jsonify(category), 201

    def update_category(self, id):
        if not request.json:
            abort(400)
        category = self.service.get(Category, id)
        if not category:
            abort(404)
        data = {}

        if data:
            if 'name' in request.json:
                data['name'] = request.json['name']

            if 'active' in request.json and request.json['active'] == 'true':
                data['active'] = True
            elif 'active' in request.json and request.json['active'] == 'false':
                data['active'] = False

            if 'type_category_id' in request.json:
                data['type_category_id'] = request.json['type_category_id']

            data['updated_at'] = datetime.now(timezone.utc)
        result = self.service.update(Category, id, data)
        if not result:
            abort(404)
        return jsonify(result)

    def delete_category(self, id):
        result = self.service.delete(Category, id)
        if not result:
            abort(404)
        return jsonify({'result': True})