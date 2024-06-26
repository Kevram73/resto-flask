from datetime import datetime, timezone
from flask import abort, jsonify, render_template, request, redirect, url_for
from flask_login import current_user
from service.models import TypeCategory
from service.services.baseService import BaseService
from service import db

class TypeCategoryController:
    def __init__(self):
        self.service = BaseService(db.session)

    def get_typeCategories(self):
        typeCategories = self.service.get_all(TypeCategory)
        return render_template("pages/categories/typeCategory.html", user='current_user.username', data=typeCategories)

    def get_typeCategory(self, id):
        typeCategory = self.service.get(TypeCategory, id)
        if not typeCategory:
            abort(404)
        return jsonify(typeCategory)

    def create_typeCategory(self):
        if not request.form or not 'name' in request.form:
            abort(400)
        data = {
            'name': request.form['name'],
            'created_at': datetime.now(timezone.utc),  # Optionally set defaults for fields not provided
        }
        typeCategory = self.service.create(TypeCategory, data)
        return redirect(url_for('admin_typeCategories'))

    def update_typeCategory(self, id):
        if not request.form:
            abort(400)
        typeCategory = self.service.get(TypeCategory, id)
        if not typeCategory:
            abort(404)
        data = {}
        if 'name' in request.form:
            data['name'] = request.form['name']
        if data:
            data['updated_at'] = datetime.now(timezone.utc)
        result = self.service.update(TypeCategory, id, data)
        if not result:
            abort(404)
        return redirect(url_for('admin_typeCategories'))

    def delete_typeCategory(self, id):
        result = self.service.delete(TypeCategory, id)
        if not result:
            abort(404)
        return redirect(url_for('admin_typeCategories'))