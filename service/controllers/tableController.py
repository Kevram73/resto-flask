from datetime import datetime, timezone
from flask import abort, jsonify, render_template, redirect, request, url_for
from flask_login import current_user
from service.models import Table, Entity
from service.services.baseService import BaseService
from service import db

class TableController:
    def __init__(self):
        self.service = BaseService(db.session)
        
    def get_tables(self):
        entities = self.service.get_all(Entity)
        tables = self.service.get_all(Table)
        return render_template("pages/tables/index.html", user='current_user.username', data=tables, entities=entities)

    def get_table(self, id):
        table = self.service.get(Table, id)
        if not table:
            abort(404)
        return jsonify(table)

    def create_table(self):
        print(request.form)
        if not request.form or not 'table_name' in request.form or not 'entity_id' in request.form or not 'capacity' in request.form:
            abort(400)

        active = None
        available = None
        if 'available' in request.form and request.form['available'] == 'True':
            available = True
        elif 'available' in request.form and request.form['available'] == 'False':
            available = False

        if 'active' in request.form and request.form['active'] == 'True':
            active = True
        elif 'active' in request.form and request.form['active'] == 'False':
            active = False
        
        data = {
            'table_name': request.form['table_name'],
            'capacity': request.form['capacity'],
            'entity_id': request.form['entity_id'],
            'available' : available,
            'active' : active,
            'created_at': datetime.now(timezone.utc),  # Optionally set defaults for fields not provided
            'updated_at': datetime.now(timezone.utc)
        }
        table = self.service.create(Table, data)
        return redirect(url_for('admin_tables'))

    def update_table(self, id):
        print(request.form)
        if not request.form:
            abort(400)
        table = self.service.get(Table, id)
        if not table:
            abort(404)
        data = {}

        if table:
            if 'table_name' in request.form:
                data['table_name'] = request.form['table_name']

            if 'available' in request.form and request.form['available'] == 'True':
                data['available'] = True
            elif 'available' in request.form and request.form['available'] == 'False':
                data['available'] = False

            if 'active' in request.form and request.form['active'] == 'True':
                data['active'] = True
            elif 'active' in request.form and request.form['active'] == 'False':
                data['active'] = False

            if 'capacity' in request.form:
                data['capacity'] = request.form['capacity']
            if 'entity_id' in request.form:
                data['entity_id'] = request.form['entity_id']

            data['updated_at'] = datetime.now(timezone.utc)
        print(data)
        if data:
            result = self.service.update(Table, id, data)
            if not result:
                abort(404)
        return redirect(url_for('admin_tables'))

    def delete_table(self, id):
        result = self.service.delete(Table, id)
        if not result:
            abort(404)
        return redirect(url_for('admin_tables'))