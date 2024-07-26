from datetime import datetime, timezone
from flask import abort, jsonify, render_template, request, redirect, url_for
from flask_login import current_user
from service.models import Stock, Fournisseur, Article
from service.services.baseService import BaseService
from service.controllers.articleController import ArticleController
from service import db

articleController = ArticleController()

class StockController:
    def __init__(self):
        self.service = BaseService(db.session)
    
    def update_article_stock(self,article, stock):
        message = None
        stock_quantity = int(stock['quantity'])
        if article:
            data = {}
            if stock['in_out'] == True:
                data['quantity'] = article['quantity'] + stock_quantity
                data['status'] = True
                message = 'Ajouter de {stock_quantity} avec success'
            elif stock['in_out'] == False:
                if stock_quantity < article['quantity']:
                    data['quantity'] = article['quantity'] - stock_quantity
                    data['status'] = True
                    message = 'Sortie de {stock_quantity} article'
                else:
                    message = None
                    data['status'] = False
            if data:
                resultat = self.service.update(Article, article['id'], data)
        return message, resultat['quantity']
        
    def get_stocks(self):
        articles = self.service.get_all(Article)
        fournisseurs = self.service.get_all(Fournisseur)
        stocks = self.service.get_all(Stock)
        return render_template("pages/articles/stock.html", user='current_user.username', data=stocks, articles=articles, fournisseurs=fournisseurs)

    def get_stock(self, id):
        stock = self.service.get(Stock, id)
        if not stock:
            abort(404)
        return jsonify(stock)

    def create_stock(self):
        if not request.form or 'quantity' not in request.form or 'in_out' not in request.form or 'article_id' not in request.form:
            abort(400)
        in_out = request.form['in_out']
        if in_out == 'True':
            in_out = True
        elif in_out == 'False':
            in_out = False
        
        data = {
            'quantity': request.form['quantity'],
            'article_id': request.form['article_id'],
            'fournisseur_id': request.form['fournisseur_id'],
            'in_out' : in_out,
            'created_at': datetime.now(timezone.utc),  # Optionally set defaults for fields not provided
            #'updated_at': datetime.now(timezone.utc)
        }
        article = articleController.get_article(request.form['article_id'])
        if article:
            message, article_quantity = self.update_article_stock(article,data)
        if message:
            stock = self.service.create(Stock, data)
            
        return redirect(url_for('admin_stocks'))

    def update_stock(self, id):
        if not request.json:
            abort(400)
        stock = self.service.get(Stock, id)
        if not stock:
            abort(404)
        data = {}

        if stock:
            if 'quantity' in request.form:
                data['quantity'] = request.form['quantity']
            if 'in_out' in request.form and request.form['in_out'] == 'true':
                data['in_out'] = True
            elif 'in_out' in request.form and request.form['in_out'] == 'false':
                data['in_out'] = False
            if 'article_id' in request.form:
                data['article_id'] = request.form['article_id']
            if 'fournisseur_id' in request.form:
                data['fournisseur_id'] = request.form['fournisseur_id']

            #data['updated_at'] = datetime.now(timezone.utc)
        result = self.service.update(Stock, id, data)
        if not result:
            abort(404)
        return redirect(url_for('admin_stocks'))

    def delete_stock(self, id):
        result = self.service.delete(Stock, id)
        if not result:
            abort(404)
        return redirect(url_for('admin_stocks'))
    
    
