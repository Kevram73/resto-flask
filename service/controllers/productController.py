from datetime import datetime, timezone
from flask import abort, jsonify, render_template, request, redirect, url_for
from flask_login import current_user
from service.models import Product, Category, Group
from service.services.baseService import BaseService
from service import db
from service.services.fileManager import FileManager

file_folder = FileManager('product')
class ProductController:
    def __init__(self):
        self.service = BaseService(db.session)
        
    def get_products(self):
        products = self.service.get_all(Product)
        categories = self.service.get_all(Category)
        groups = self.service.get_all(Group)
        return render_template("pages/products/index.html", user='current_user.username', data=products, groups=groups, categories=categories)

    def get_product(self, id):
        product = self.service.get(Product, id)
        if not product:
            abort(404)
        return jsonify(product)

    def create_product(self):
        categories = self.service.get_all(Category)
        groups = self.service.get_all(Group)
        if request.method == 'POST':
            if not request.form:
                abort(400)
            else:
                if 'price' not in request.form or not 'name' in request.form or 'category_id' not in request.form or 'group_id' not in request.form:
                    abort(400)

                active = request.form['active']
                image_name = None
                if request.files['image']:
                    image = request.files['image']
                    if image.filename != '':
                        image_name, message = file_folder.save_file(image)

                if active == 'True':
                    active = True
                else:
                    active = False
                
                data = {
                    'name': request.form['name'],
                    'category_id': request.form['category_id'],
                    'group_id': request.form['group_id'],
                    'price': request.form['price'],
                    'description': request.form.get('description'),
                    'image': image_name,
                    'active' : active,
                    #'created_at': datetime.now(timezone.utc),  # Optionally set defaults for fields not provided
                    #'updated_at': datetime.now(timezone.utc)
                }
                product = self.service.create(Product, data)
                if product:
                    return redirect(url_for('admin_products'))
        return render_template("pages/products/new.html", groups=groups, categories=categories)

    def update_product(self, id):
        categories = self.service.get_all(Category)
        groups = self.service.get_all(Group)
        product = self.service.get(Product, id)
        if not product:
            abort(404)
        if request.method == 'POST':
            if not request.form:
                abort(400)
            data = {}

            if product:
                if 'name' in request.form:
                    data['name'] = request.form['name']
                if 'category_id' in request.form:
                    data['category_id'] = request.form['category_id']
                if 'group_id' in request.form:
                    data['group_id'] = request.form['group_id']
                if 'price' in request.form:
                    data['price'] = request.form['price']
                if 'description' in request.form:
                    data['description'] = request.form['description']
                image_name = None
                if request.files != '':
                    image = request.files['image']
                    product = Product.query.filter_by(id=id).first()
                    if image.filename != '' and product.image != None:
                        del1, message_del = file_folder.delete_file(product.image)
                        image_name, message = file_folder.save_file(image)
                    elif image.filename != '':
                        image_name, message = file_folder.save_file(image)
                    if image_name:
                        data['image'] = image_name

                if 'active' in request.form and request.form['active'] == 'True':
                    data['active'] = True
                elif 'active' in request.form and request.form['active'] == 'False':
                    data['active'] = False

                #if data:
                #    data['updated_at'] = datetime.now(timezone.utc)
                result = self.service.update(Product, id, data)
                if result:
                    return redirect(url_for('admin_products'))
            
        return render_template("pages/products/edit.html", product=product, groups=groups, categories=categories)

    def delete_product(self, id):
        product = Product.query.filter_by(id=id).first()
        result = None
        del1 = None
        if product.image is not None:
            del1, message_del = file_folder.delete_file(product.image)

        result = self.service.delete(Product, id)
        if not result:
            abort(404)
        return redirect(url_for('admin_products'))