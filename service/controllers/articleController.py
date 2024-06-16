from datetime import datetime, timezone
from flask import abort, jsonify, render_template, request
from flask_login import current_user
from service.models import Article
from service.services.baseService import BaseService
from service import db

class ArticleController:
    def __init__(self):
        self.service = BaseService(db.session)
        
    def get_articles(self):
        articles = self.service.get_all(Article)
        return render_template("pages/admin/pages/articles/index.html", user=current_user.username, data=articles)

    def get_article(self, id):
        article = self.service.get(Article, id)
        if not article:
            abort(404)
        return jsonify(article)

    def create_article(self):
        if not request.json or not 'libelle' in request.json or not 'fournisseur_id' in request.json:
            abort(400)
        status = request.json['status']
        if status == 'true':
            status = True
        else:
            status = False
        
        data = {
            'libelle': request.json['libelle'],
            'famille': request.json['famille'],
            'prix_achat_unit': request.json['prix_achat_unit'],
            'prix_vente_unit': request.json['prix_vente_unit'],
            'quantity': request.json['quantity'],
            'unite': request.json['unite'],
            'status': status,
            'user_id': current_user.id,
            'fournisseur_id': request.json['fournisseur_id'],
            'created_at': datetime.now(timezone.utc),  # Optionally set defaults for fields not provided
            'updated_at': datetime.now(timezone.utc)
        }
        article = self.service.create(Article, data)
        return jsonify(article), 201

    def update_article(self, id):
        if not request.json:
            abort(400)
        article = self.service.get(Article, id)
        if not article:
            abort(404)
        data = {}

        if data:
            if 'libelle' in request.json:
                data['libelle'] = request.json['libelle']
            if 'famille' in request.json:
                data['famille'] = request.json['famille']
            if 'prix_achat_unit' in request.json:
                data['prix_achat_unit'] = request.json['prix_achat_unit']
            if 'prix_vente_unit' in request.json:
                data['prix_vente_unit'] = request.json['prix_vente_unit']
            if 'quantity' in request.json:
                data['quantity'] = request.json['quantity']
            if 'unite' in request.json:
                data['unite'] = request.json['unite']
            if 'fournisseur_id' in request.json:
                data['fournisseur_id'] = request.json['fournisseur_id']

            if 'status' in request.json and request.json['status'] == 'true':
                data['status'] = True
            elif 'status' in request.json and request.json['status'] == 'false':
                data['status'] = False
            data['updated_at'] = datetime.now(timezone.utc)
        result = self.service.update(Article, id, data)
        if not result:
            abort(404)
        return jsonify(result)

    def delete_article(self, id):
        result = self.service.delete(Article, id)
        if not result:
            abort(404)
        return jsonify({'result': True})