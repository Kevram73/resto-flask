from datetime import datetime, timezone
from flask import abort, jsonify, render_template, request
from flask_login import current_user
from service.models import Depense
from service.services.baseService import BaseService
from service import db

class DepenseController:
    def __init__(self):
        self.service = BaseService(db.session)
        
    def get_depenses(self):
        depenses = self.service.get_all(Depense)
        return render_template("pages/admin/pages/depenses/index.html", user=current_user.username, data=depenses)

    def get_depense(self, id):
        depense = self.service.get(Depense, id)
        if not depense:
            abort(404)
        return jsonify(depense)

    def create_depense(self):
        if not request.json or not 'libelle' in request.json:
            abort(400)
        
        data = {
            'libelle': request.json['libelle'],
            'amount': request.json['amount'],
            'amount_modif': request.json['amount_modif'],
            'user_id': current_user.id,
            'created_at': datetime.now(timezone.utc),  # Optionally set defaults for fields not provided
            'updated_at': datetime.now(timezone.utc)
        }
        depense = self.service.create(Depense, data)
        return jsonify(depense), 201

    def update_depense(self, id):
        if not request.json:
            abort(400)
        depense = self.service.get(Depense, id)
        if not depense:
            abort(404)
        data = {}

        if data:
            if 'libelle' in request.json:
                data['libelle'] = request.json['libelle']
            if 'amount' in request.json:
                data['amount'] = request.json['amount']
            if 'amount_modif' in request.json:
                data['amount_modif'] = request.json['amount_modif']
            
            data['updated_at'] = datetime.now(timezone.utc)
        result = self.service.update(Depense, id, data)
        if not result:
            abort(404)
        return jsonify(result)

    def delete_depense(self, id):
        result = self.service.delete(Depense, id)
        if not result:
            abort(404)
        return jsonify({'result': True})