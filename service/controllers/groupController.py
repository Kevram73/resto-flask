from datetime import datetime, timezone
from flask import abort, jsonify, render_template, request, redirect, url_for
from flask_login import current_user
from service.models import Group
from service.services.baseService import BaseService
from service import db

class GroupController:
    def __init__(self):
        self.service = BaseService(db.session)
        
    def get_groups(self):
        groups = self.service.get_all(Group)
        return render_template("pages/users/group.html", user='current_user.username', data=groups)

    def get_group(self, id):
        group = self.service.get(Group, id)
        if not group:
            abort(404)
        return jsonify(group)
    
    def create_group(self):
        if not request.form or not 'name' in request.form:
            abort(400)
        data = {
            'name': request.form['name'],
            'created_at': datetime.now(timezone.utc),  # Optionally set defaults for fields not provided
            'updated_at': datetime.now(timezone.utc)
        }
        group = self.service.create(Group, data)
        return redirect(url_for('admin_groups'))

    def update_group(self, id):
        if not request.form:
            abort(400)
        group = self.service.get(Group, id)
        if not group:
            abort(404)
        data = {}
        if 'name' in request.form:
            data['name'] = request.form['name']
        if data:
            data['updated_at'] = datetime.now(timezone.utc)
        result = self.service.update(Group, id, data)
        if not result:
            abort(404)
        return redirect(url_for('admin_groups'))

    def delete_group(self, id):
        result = self.service.delete(Group, id)
        if not result:
            abort(404)
        return redirect(url_for('admin_groups'))