from datetime import datetime, timezone
from flask import abort, jsonify, render_template, request
from flask_login import current_user
from service.models import Fournisseur
from service.services.baseService import BaseService
from service import db

class FournisseurController:
    def __init__(self):
        self.service = BaseService(db.session)
    
    def unique_validator(self,validation):
        if validation == 'name':
            return Fournisseur.query.filter_by(name=validation).first()
        if validation == 'email':
            return Fournisseur.query.filter_by(email=validation).first()
        if validation == 'contact':
            return Fournisseur.query.filter_by(contact=validation).first()
        
    def get_fournisseurs(self):
        fournisseurs = self.service.get_all(Fournisseur)
        return render_template("pages/admin/pages/fournisseurs/index.html", user=current_user.username, data=fournisseurs)

    def get_fournisseur(self, id):
        fournisseur = self.service.get(Fournisseur, id)
        if not fournisseur:
            abort(404)
        return jsonify(fournisseur)

    def create_fournisseur(self):
        if not request.json or not 'name' in request.json or not 'contact' in request.json or not 'address' in request.json:
            abort(400)
        name = request.json['name']
        email = request.json['email']
        contact = request.json['contact']
        if self.unique_validator(name) or self.unique_validator(email) or self.unique_validator(contact):
            abort(400)
        data = {
            'name': name,
            'email': email,
            'contact': contact,
            'address': request.json['address'],
            'balance': request.json['balance'],
            'created_at': datetime.now(timezone.utc),  # Optionally set defaults for fields not provided
            'updated_at': datetime.now(timezone.utc)
        }
        fournisseur = self.service.create(Fournisseur, data)
        return jsonify(fournisseur), 201

    def update_fournisseur(self, id):
        if not request.json:
            abort(400)
        fournisseur = self.service.get(Fournisseur, id)
        if not fournisseur:
            abort(404)
        name = request.json['name']
        email = request.json['email']
        contact = request.json['contact']
        data = {}

        if data:
            if 'name' in request.json and not self.unique_validator(name):
                data['name'] = name
            if 'email' in request.json and not self.unique_validator(email):
                data['email'] = email
            if 'contact' in request.json and not self.unique_validator(contact):
                data['contact'] = contact
            if 'address' in request.json:
                data['address'] = request.json['address']
            if 'balance' in request.json:
                data['balance'] = request.json['balance']

            data['updated_at'] = datetime.now(timezone.utc)
        result = self.service.update(Fournisseur, id, data)
        if not result:
            abort(404)
        return jsonify(result)

    def delete_fournisseur(self, id):
        result = self.service.delete(Fournisseur, id)
        if not result:
            abort(404)
        return jsonify({'result': True})