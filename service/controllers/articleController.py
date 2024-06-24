from datetime import datetime, timezone
from flask import abort, jsonify, render_template, request, redirect, url_for
from flask_login import current_user
from service.models import Article
from service.services.baseService import BaseService
from service import db

class ArticleController:
    def __init__(self):
        self.service = BaseService(db.session)
        
    def get_articles(self):
        articles = self.service.get_all(Article)
        return render_template("pages/articles/index.html", user='current_user.username', data=articles)

    def get_article(self, id):
        article = self.service.get(Article, id)
        if not article:
            abort(404)
        return jsonify(article)

    def create_article(self):
        if not request.form or not 'libelle' in request.form or not 'fournisseur_id' in request.form:
            abort(400)
        status = request.form['status']
        if status == 'True':
            status = True
        else:
            status = False
        
        data = {
            'libelle': request.form['libelle'],
            'famille': request.form['famille'],
            'prix_achat_unit': request.form['prix_achat_unit'],
            'prix_vente_unit': request.form['prix_vente_unit'],
            'quantity': request.form['quantity'],
            'unite': request.form['unite'],
            'status': status,
            'user_id': 1, #current_user.id,
            'fournisseur_id': request.form['fournisseur_id'],
            'created_at': datetime.now(timezone.utc),  # Optionally set defaults for fields not provided
            'updated_at': datetime.now(timezone.utc)
        }
        article = self.service.create(Article, data)
        return redirect(url_for('admin_articles'))

    def update_article(self, id):
        if not request.form:
            abort(400)
        article = self.service.get(Article, id)
        if not article:
            abort(404)
        data = {}

        if data:
            if 'libelle' in request.form:
                data['libelle'] = request.form['libelle']
            if 'famille' in request.form:
                data['famille'] = request.form['famille']
            if 'prix_achat_unit' in request.form:
                data['prix_achat_unit'] = request.form['prix_achat_unit']
            if 'prix_vente_unit' in request.form:
                data['prix_vente_unit'] = request.form['prix_vente_unit']
            if 'quantity' in request.form:
                data['quantity'] = request.form['quantity']
            if 'unite' in request.form:
                data['unite'] = request.form['unite']
            if 'fournisseur_id' in request.form:
                data['fournisseur_id'] = request.form['fournisseur_id']

            if 'status' in request.form and request.form['status'] == 'True':
                data['status'] = True
            elif 'status' in request.form and request.form['status'] == 'False':
                data['status'] = False
            if data:
                data['updated_at'] = datetime.now(timezone.utc)
        result = self.service.update(Article, id, data)
        if not result:
            abort(404)
        return redirect(url_for('admin_articles'))

    def delete_article(self, id):
        result = self.service.delete(Article, id)
        if not result:
            abort(404)
        return redirect(url_for('admin_articles'))