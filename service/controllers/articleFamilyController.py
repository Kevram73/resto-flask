from datetime import datetime, timezone
from flask import abort, jsonify, render_template, request, redirect, url_for
from flask_login import current_user
from service.models import ArticleFamily
from service.services.baseService import BaseService
from service import db

class ArticleFamilyController:
    def __init__(self):
        self.service = BaseService(db.session)
        
    def get_articleFamilies(self):
        articleFamilies = self.service.get_all(ArticleFamily)
        return render_template("pages/articles/articleFamily.html", user='current_user.username', data=articleFamilies)

    def get_articleFamily(self, id):
        articleFamily = self.service.get(ArticleFamily, id)
        if not articleFamily:
            abort(404)
        return jsonify(articleFamily)

    def create_articleFamily(self):
        if not request.form or not 'name' in request.form:
            abort(400)
        data = {
            'name': request.form['name'],
            'created_at': datetime.now(timezone.utc),  # Optionally set defaults for fields not provided
            'updated_at': datetime.now(timezone.utc)
        }
        articleFamily = self.service.create(ArticleFamily, data)
        return redirect(url_for('admin_articleFamilies'))

    def update_articleFamily(self, id):
        if not request.form:
            abort(400)
        articleFamily = self.service.get(ArticleFamily, id)
        if not articleFamily:
            abort(404)
        data = {}
        if 'name' in request.form:
            data['name'] = request.form['name']
        if data:
            data['updated_at'] = datetime.now(timezone.utc)
        result = self.service.update(ArticleFamily, id, data)
        if not result:
            abort(404)
        return redirect(url_for('admin_articleFamilies'))

    def delete_articleFamily(self, id):
        result = self.service.delete(ArticleFamily, id)
        if not result:
            abort(404)
        return redirect(url_for('admin_articleFamilies'))