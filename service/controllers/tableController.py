from datetime import datetime, timezone
from flask import abort, jsonify, render_template, request
from flask_login import current_user
from service.models import Table
from service.services.baseService import BaseService
from service import db

class TableController:
    def __init__(self):
        self.service = BaseService(db.session)
        
    def get_tables(self):
        tables = self.service.get_all(Table)
        return render_template("pages/admin/pages/tables/index.html", user=current_user.username, data=tables)

    def get_table(self, id):
        table = self.service.get(Table, id)
        if not table:
            abort(404)
        return jsonify(table)

    def create_table(self):
        if not request.json or not 'table_name' in request.json or not 'entity_id' in request.json or not 'capacity' in request.json:
            abort(400)

        available = request.json['available']
        active = request.json['active']

        if available == 'true':
            available = True
        else:
            available = False

        if active == 'true':
            active = True
        else:
            active = False
        
        data = {
            'table_name': request.json['table_name'],
            'capacity': request.json['capacity'],
            'entity_id': request.json['entity_id'],
            'available' : available,
            'active' : active,
            'created_at': datetime.now(timezone.utc),  # Optionally set defaults for fields not provided
            'updated_at': datetime.now(timezone.utc)
        }
        table = self.service.create(Table, data)
        return jsonify(table), 201

    def update_table(self, id):
        if not request.json:
            abort(400)
        table = self.service.get(Table, id)
        if not table:
            abort(404)
        data = {}

        if data:
            if 'table_name' in request.json:
                data['table_name'] = request.json['table_name']

            if 'available' in request.json and request.json['available'] == 'true':
                data['available'] = True
            elif 'available' in request.json and request.json['available'] == 'false':
                data['available'] = False

            if 'active' in request.json and request.json['active'] == 'true':
                data['active'] = True
            elif 'active' in request.json and request.json['active'] == 'false':
                data['active'] = False

            if 'capacity' in request.json:
                data['capacity'] = request.json['capacity']
            if 'entity_id' in request.json:
                data['entity_id'] = request.json['entity_id']

            data['updated_at'] = datetime.now(timezone.utc)
        result = self.service.update(Table, id, data)
        if not result:
            abort(404)
        return jsonify(result)

    def delete_table(self, id):
        result = self.service.delete(Table, id)
        if not result:
            abort(404)
        return jsonify({'result': True})