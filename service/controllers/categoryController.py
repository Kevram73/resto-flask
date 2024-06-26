from datetime import datetime, timezone
from flask import abort, jsonify, render_template, request, redirect, url_for
from flask_login import current_user
from service.models import Category, TypeCategory
from service.services.baseService import BaseService
from service import db

class CategoryController:
    def __init__(self):
        self.service = BaseService(db.session)
        
    def get_categories(self):
        categories = self.service.get_all(Category)
        typeCategories = self.service.get_all(TypeCategory)
        return render_template("pages/categories/index.html", user='current_user.username', data=categories, typeCategories=typeCategories)

    def get_category(self, id):
        category = self.service.get(Category, id)
        if not category:
            abort(404)
        return jsonify(category)

    def create_category(self):
        if not request.form or not 'name' in request.form or not 'type_category_id' in request.form:
            abort(400)

        active = request.form['active']
        if active == 'True':
            active = True
        else:
            active = False
        
        data = {
            'name': request.form['name'],
            'type_category_id': request.form['type_category_id'],
            'active' : active,
            'created_at': datetime.now(timezone.utc),  # Optionally set defaults for fields not provided
            'updated_at': datetime.now(timezone.utc)
        }
        category = self.service.create(Category, data)
        return redirect(url_for('admin_categories'))

    def update_category(self, id):
        if not request.form:
            abort(400)
        category = self.service.get(Category, id)
        if not category:
            abort(404)
        data = {}
        result = None

        if category:
            if 'name' in request.form:
                data['name'] = request.form['name']

            if 'active' in request.form and request.form['active'] == 'True':
                data['active'] = True
            elif 'active' in request.form and request.form['active'] == 'False':
                data['active'] = False

            if 'type_category_id' in request.form:
                data['type_category_id'] = request.form['type_category_id']

            data['updated_at'] = datetime.now(timezone.utc)
        if data:
            result = self.service.update(Category, id, data)
        if not result:
            abort(404)
        return redirect(url_for('admin_categories'))

    def delete_category(self, id):
        result = self.service.delete(Category, id)
        if not result:
            abort(404)
        return redirect(url_for('admin_categories'))