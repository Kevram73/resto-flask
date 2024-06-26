from datetime import datetime, timezone
from flask import abort, jsonify, render_template, request, redirect, url_for
from flask_login import current_user
from service.models import Company
from service.services.baseService import BaseService
from service import db

class CompanyController:
    def __init__(self):
        self.service = BaseService(db.session)
        
    def get_companies(self):
        companies = self.service.get_all(Company)
        return render_template("pages/companies/index.html", user='current_user.username', data=companies)

    def get_company(self, id):
        company = self.service.get(Company, id)
        if not company:
            abort(404)
        return jsonify(company)

    def create_company(self):
        if request.method == 'POST':
            if not request.form or not 'name' in request.form or not 'phone' in request.form:
                abort(400)
            name = request.form['name']
            if Company.query.filter_by(name=name).first():
                abort(400)
            data = {
                'name': name,
                'service_charge_value': request.form['service_charge_value'],
                'vat_charge_value': request.form['vat_charge_value'],
                'address': request.form['address'],
                'phone': request.form['phone'],
                'country': request.form['country'],
                'currency': request.form['currency'],
                'created_at': datetime.now(timezone.utc),  # Optionally set defaults for fields not provided
                'updated_at': datetime.now(timezone.utc)
            }
            company = self.service.create(Company, data)
            if company:
                return redirect(url_for('admin_companies'))

        return render_template("pages/companies/new.html")

    def update_company(self, id):
        company = self.service.get(Company, id)
        if not company:
            abort(404)
        if request.method == 'POST':
            if not request.form:
                abort(400)
            name = request.form['name']
            data = {}

            if company:
                if 'name' in request.form and not Company.query.filter_by(name=name).first():
                    data['name'] = name
                if 'service_charge_value' in request.form:
                    data['service_charge_value'] = request.form['service_charge_value']
                if 'vat_charge_value' in request.form:
                    data['vat_charge_value'] = request.form['vat_charge_value']
                if 'address' in request.form:
                    data['address'] = request.form['address']
                if 'phone' in request.form:
                    data['phone'] = request.form['phone']
                if 'country' in request.form:
                    data['country'] = request.form['country']
                if 'currency' in request.form:
                    data['currency'] = request.form['currency']

                data['updated_at'] = datetime.now(timezone.utc)
            result = self.service.update(Company, id, data)
            if not result:
                abort(404)
            elif result:
                return redirect(url_for('admin_companies'))
        return render_template("pages/companies/edit.html", company=company)

    def delete_company(self, id):
        result = self.service.delete(Company, id)
        if not result:
            abort(404)
        return redirect(url_for('admin_companies'))