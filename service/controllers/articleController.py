from datetime import datetime, timezone
from flask import abort, jsonify, render_template, request, redirect, url_for
from flask_login import current_user
from service.models import Article, Fournisseur, ArticleFamily
from service.services.baseService import BaseService
from service import db

class ArticleController:
    def __init__(self):
        self.service = BaseService(db.session)
        
    def get_articles(self):
        fournisseurs = self.service.get_all(Fournisseur)
        articles = self.service.get_all(Article)
        return render_template("pages/articles/index.html", user='current_user.username', data=articles, fournisseurs=fournisseurs)

    def get_article(self, id):
        article = self.service.get(Article, id)
        if not article:
            abort(404)
        return jsonify(article)

    def create_article(self):
        fournisseurs = self.service.get_all(Fournisseur)
        articleFamilies = self.service.get_all(ArticleFamily)
        if request.method == "POST":
            print(request.form)
            if not request.form or not 'libelle' in request.form or not 'fournisseur_id' in request.form:
                abort(400)
            status = None
            quantity = request.form['quantity']
            if 'quantity' in request.form and int(quantity) > 0:
                status = True
            else:
                status = False
            
            data = {
                'libelle': request.form['libelle'],
                'famille': request.form['famille'],
                'prix_achat_unit': request.form['prix_achat_unit'],
                'prix_vente_unit': request.form['prix_vente_unit'],
                'quantity': quantity,
                'unite': request.form['unite'],
                'status': status,
                'user_id': 1, #current_user.id,
                'fournisseur_id': request.form['fournisseur_id'],
                'created_at': datetime.now(timezone.utc),  # Optionally set defaults for fields not provided
                'updated_at': datetime.now(timezone.utc)
            }
            article = self.service.create(Article, data)
            if article:
                return redirect(url_for('admin_articles'))
        return render_template("pages/articles/new.html", user='current_user.username', families=articleFamilies, fournisseurs=fournisseurs)

    def update_article(self, id):
        fournisseurs = self.service.get_all(Fournisseur)
        articleFamilies = self.service.get_all(ArticleFamily)
        article = self.service.get(Article, id)
        print(article)
        if not article:
            abort(404)
        data = {}
        if request.method == "POST":
            if article:
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

                if 'quantity' in request.form and int(request.form['quantity']) > 0:
                    data['status'] = True
                else:
                    data['status'] = False

                if data:
                    data['updated_at'] = datetime.now(timezone.utc)
                result = self.service.update(Article, id, data)
                if result:
                    return redirect(url_for('admin_articles'))
        return render_template("pages/articles/edit.html", user='current_user.username', article=article, families=articleFamilies, fournisseurs=fournisseurs)

    def delete_article(self, id):
        result = self.service.delete(Article, id)
        if not result:
            abort(404)
        return redirect(url_for('admin_articles'))