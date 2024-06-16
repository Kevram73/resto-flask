from datetime import datetime, timezone
from flask import abort, jsonify, render_template, request
from flask_login import current_user
from service.models import Stock
from service.services.baseService import BaseService
from service import db

class StockController:
    def __init__(self):
        self.service = BaseService(db.session)
        
    def get_stocks(self):
        stocks = self.service.get_all(Stock)
        return render_template("pages/admin/pages/stocks/index.html", user=current_user.username, data=stocks)

    def get_stock(self, id):
        stock = self.service.get(Stock, id)
        if not stock:
            abort(404)
        return jsonify(stock)

    def create_stock(self):
        if not request.json or 'quantity' not in request.json or 'in_out' not in request.json or 'article_id' not in request.json:
            abort(400)
        in_out = request.json['in_out']
        if in_out == 'true':
            in_out = True
        else:
            in_out = False
        
        data = {
            'quantity': request.json['quantity'],
            'article_id': request.json['article_id'],
            'foutnisseur_id': request.json['foutnisseur_id'],
            'in_out' : in_out,
            'created_at': datetime.now(timezone.utc),  # Optionally set defaults for fields not provided
            'updated_at': datetime.now(timezone.utc)
        }
        stock = self.service.create(Stock, data)
        return jsonify(stock), 201

    def update_stock(self, id):
        if not request.json:
            abort(400)
        stock = self.service.get(Stock, id)
        if not stock:
            abort(404)
        data = {}

        if data:
            if 'quantity' in request.json:
                data['quantity'] = request.json['quantity']
            if 'in_out' in request.json and request.json['in_out'] == 'true':
                data['in_out'] = True
            elif 'in_out' in request.json and request.json['in_out'] == 'false':
                data['in_out'] = False
            if 'article_id' in request.json:
                data['article_id'] = request.json['article_id']
            if 'fournisseur_id' in request.json:
                data['fournisseur_id'] = request.json['fournisseur_id']

            data['updated_at'] = datetime.now(timezone.utc)
        result = self.service.update(Stock, id, data)
        if not result:
            abort(404)
        return jsonify(result)

    def delete_stock(self, id):
        result = self.service.delete(Stock, id)
        if not result:
            abort(404)
        return jsonify({'result': True})