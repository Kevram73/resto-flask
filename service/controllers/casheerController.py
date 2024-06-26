from datetime import datetime, timezone
from flask import abort, jsonify, render_template, request, redirect, url_for
from flask_login import current_user
from service.models import Casheer
from service.services.baseService import BaseService
from service import db

class CasheerController:
    def __init__(self):
        self.service = BaseService(db.session)
        
    def get_casheers(self):
        casheers = self.service.get_all(Casheer)
        return render_template("pages/casheers/index.html", user='current_user.username', data=casheers)

    def get_casheer(self, id):
        casheer = self.service.get(Casheer, id)
        if not casheer:
            abort(404)
        return jsonify(casheer)

    def create_casheer(self):
        if not request.form or not 'name' in request.form:
            abort(400)
        data = {
            'name': request.form['name'],
            'balance': request.form['balance'],
            'created_at': datetime.now(timezone.utc),  # Optionally set defaults for fields not provided
        }
        casheer = self.service.create(Casheer, data)
        return redirect(url_for('admin_casheers'))

    def update_casheer(self, id):
        if not request.form:
            abort(400)
        casheer = self.service.get(Casheer, id)
        if not casheer:
            abort(404)
        data = {}
        if 'name' in request.form:
            data['name'] = request.form['name']
        if 'balance' in request.form:
            data['balance'] = request.form['balance']
        result = self.service.update(Casheer, id, data)
        if not result:
            abort(404)
        return redirect(url_for('admin_casheers'))

    def delete_casheer(self, id):
        result = self.service.delete(Casheer, id)
        if not result:
            abort(404)
        return redirect(url_for('admin_casheers'))