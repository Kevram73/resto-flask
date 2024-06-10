from flask import Flask, request, jsonify, g
from service import db
from service.models import Article, Casheer, Depense, Entity, ExploitAccount, Fournisseur, Group, Order, Product, Stock, Table, User
from datetime import datetime

app = Flask(__name__)

# Each class here handles CRUD operations for one model
class BaseService:
    def __init__(self):
        self.session = db.session

    def create(self, model, data):
        new_entry = model(**data)
        self.session.add(new_entry)
        self.session.commit()
        return jsonify({'data': new_entry.to_dict(), 'success': True}), 201

    def get(self, model, id):
        entry = model.query.get(id)
        if not entry:
            return jsonify({'message': f'{model.__name__} not found', 'success': False}), 404
        return jsonify({'data': entry.to_dict(), 'success': True})

    def update(self, model, id, data):
        entry = model.query.get(id)
        if not entry:
            return jsonify({'message': f'{model.__name__} not found', 'success': False}), 404
        for key, value in data.items():
            setattr(entry, key, value)
        entry.updated_at = datetime.utcnow()
        self.session.commit()
        return jsonify({'success': True, 'message': f'{model.__name__} updated successfully'})

    def delete(self, model, id):
        entry = model.query.get(id)
        if entry:
            self.session.delete(entry)
            self.session.commit()
            return jsonify({'success': True, 'message': f'{model.__name__} deleted successfully'}), 204
        return jsonify({'message': f'{model.__name__} not found', 'success': False}), 404

    def close_db_connection(self, exception=None):
        db = getattr(g, '_database', None)
        if db is not None:
            db.close()