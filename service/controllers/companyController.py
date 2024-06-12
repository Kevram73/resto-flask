from datetime import datetime, timezone
from flask import abort, jsonify, render_template, request
from flask_login import current_user
from service.models import Company
from service.services.baseService import BaseService
from service import db

class CompanyController:
    def __init__(self):
        self.service = BaseService(db.session)
        
    def get_companies(self):
        companies = self.service.get_all(Company)
        return render_template("pages/admin/pages/companies/index.html", user=current_user.username, data=companies)

    def get_company(self, id):
        company = self.service.get(Company, id)
        if not company:
            abort(404)
        return jsonify(company)

    def create_company(self):
        if not request.json or not 'name' in request.json or not 'phone' in request.json:
            abort(400)
        name = request.json['name']
        email = request.json['email']
        contact = request.json['contact']
        if Company.query.filter_by(name=name).first():
            abort(400)
        data = {
            'name': name,
            'service_charge_value': request.json['service_charge_value'],
            'vat_charge_value': request.json['vat_charge_value'],
            'address': request.json['address'],
            'phone': request.json['phone'],
            'country': request.json['country'],
            'currency': request.json['currency'],
            'created_at': datetime.now(timezone.utc),  # Optionally set defaults for fields not provided
            'updated_at': datetime.now(timezone.utc)
        }
        company = self.service.create(Company, data)
        return jsonify(company), 201

    def update_company(self, id):
        if not request.json:
            abort(400)
        company = self.service.get(Company, id)
        if not company:
            abort(404)
        name = request.json['name']
        data = {}

        if data:
            if 'name' in request.json and not Company.query.filter_by(name=name).first():
                data['name'] = name
            if 'service_charge_value' in request.json:
                data['service_charge_value'] = request.json['service_charge_value']
            if 'vat_charge_value' in request.json:
                data['vat_charge_value'] = request.json['vat_charge_value']
            if 'address' in request.json:
                data['address'] = request.json['address']
            if 'phone' in request.json:
                data['phone'] = request.json['phone']
            if 'country' in request.json:
                data['country'] = request.json['country']
            if 'currency' in request.json:
                data['currency'] = request.json['currency']

            data['updated_at'] = datetime.now(timezone.utc)
        result = self.service.update(Company, id, data)
        if not result:
            abort(404)
        return jsonify(result)

    def delete_company(self, id):
        result = self.service.delete(Company, id)
        if not result:
            abort(404)
        return jsonify({'result': True})