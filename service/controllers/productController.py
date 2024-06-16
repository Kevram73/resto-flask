from datetime import datetime, timezone
from flask import abort, jsonify, render_template, request
from flask_login import current_user
from service.models import Product
from service.services.baseService import BaseService
from service import db
from service.services.fileManager import FileManager

file_folder = FileManager('product')
class ProductController:
    def __init__(self):
        self.service = BaseService(db.session)
        
    def get_products(self):
        products = self.service.get_all(Product)
        return render_template("pages/admin/pages/products/index.html", user=current_user.username, data=products)

    def get_product(self, id):
        product = self.service.get(Product, id)
        if not product:
            abort(404)
        return jsonify(product)

    def create_product(self):
        if not request.json:
            abort(400)
        if 'price' not in request.json or not 'name' in request.json or 'category_id' not in request.json or 'group_id' not in request.json:
            abort(400)

        active = request.json['active']
        image_name = None
        if 'image' in request.json:
            image = request.files['image']
            if image.filename != '':
                image_name, message = file_folder.save_file(image)

        if active == 'true':
            active = True
        else:
            active = False
        
        data = {
            'name': request.json['name'],
            'category_id': request.json['category_id'],
            'group_id': request.json['group_id'],
            'price': request.json['price'],
            'description': request.json['description'],
            'image': image_name,
            'active' : active,
            'created_at': datetime.now(timezone.utc),  # Optionally set defaults for fields not provided
            'updated_at': datetime.now(timezone.utc)
        }
        product = self.service.create(Product, data)
        return jsonify(product), 201

    def update_product(self, id):
        if not request.json:
            abort(400)
        product = self.service.get(Product, id)
        if not product:
            abort(404)
        data = {}

        if data:
            if 'name' in request.json:
                data['name'] = request.json['name']
            if 'category_id' in request.json:
                data['category_id'] = request.json['category_id']
            if 'group_id' in request.json:
                data['group_id'] = request.json['group_id']
            if 'price' in request.json:
                data['price'] = request.json['price']
            if 'description' in request.json:
                data['description'] = request.json['description']
            image_name = None
            if 'image' in request.json:
                image = request.files['image']
                product = Product.query.filter_by(id=id).first()
                if image.filename != '' and product['image'] is not None:
                    del1, message_del = file_folder.delete_file(product['image'])
                    image_name, message = file_folder.save_file(image)
                if image_name:
                    data['image'] = image_name

            if 'active' in request.json and request.json['active'] == 'true':
                data['active'] = True
            elif 'active' in request.json and request.json['active'] == 'false':
                data['active'] = False

            data['updated_at'] = datetime.now(timezone.utc)
        result = self.service.update(Product, id, data)
        if not result:
            abort(404)
        return jsonify(result)

    def delete_product(self, id):
        product = Product.query.filter_by(id=id).first()
        result = None
        del1 = None
        if product['image'] is not None:
            del1, message_del = file_folder.delete_file(product['image'])
        if del1:
            result = self.service.delete(Product, id)
        if not result:
            abort(404)
        return jsonify({'result': True})