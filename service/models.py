from service import db
from datetime import datetime, timezone
from flask_login import UserMixin
from sqlalchemy_serializer import SerializerMixin


class Entity(db.Model, SerializerMixin):
    __tablename__ = "entities"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(256))
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.now(timezone.utc))
    updated_at = db.Column(db.DateTime, nullable=False, default=datetime.now(timezone.utc))

    def __repr__(self):
        return f"entity('{self.name}')"

class Group(db.Model, SerializerMixin):
    __tablename__ = "groups"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(256))
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.now(timezone.utc))
    updated_at = db.Column(db.DateTime, nullable=False, default=datetime.now(timezone.utc))

    def __repr__(self):
        return f"group('{self.name}')"
    
    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'created_at': self.created_at,
            'updated_at': self.updated_at,
        }

class User(db.Model, UserMixin):
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True)
    password = db.Column(db.String(128))
    email = db.Column(db.String(120), unique=True)
    phone = db.Column(db.String(120), unique=True)
    gender = db.Column(db.String(20))
    group_id = db.Column(db.Integer, db.ForeignKey(
        'groups.id'), nullable=False)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.now(timezone.utc))
    updated_at = db.Column(db.DateTime, nullable=False, default=datetime.now(timezone.utc))

    def __repr__(self):
        return f"user('{self.username}', '{self.email}')"

class Table(db.Model, SerializerMixin):
    __tablename__ = "tables"

    id = db.Column(db.Integer, primary_key=True)
    table_name = db.Column(db.String(100), nullable=False)
    capacity = db.Column(db.Integer, nullable=False)
    available = db.Column(db.Boolean, default=True, nullable=False)
    active = db.Column(db.Boolean, default=True, nullable=False)
    entity_id = db.Column(db.Integer, db.ForeignKey('entities.id'), nullable=False)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.now(timezone.utc))
    updated_at = db.Column(db.DateTime, nullable=False, default=datetime.now(timezone.utc))

    def __repr__(self):
        return f"<Table {self.table_name}>"
    
class Fournisseur(db.Model, SerializerMixin):
    __tablename__ = "fournisseurs"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(256), unique=True)
    email = db.Column(db.String(120), unique=True)
    contact = db.Column(db.String(120), unique=True)
    address = db.Column(db.String(120))
    balance = db.Column(db.Float)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.now(timezone.utc))
    updated_at = db.Column(db.DateTime, nullable=False, default=datetime.now(timezone.utc))

    def __repr__(self):
        return f"user('{self.name}', '{self.email}')"

class UserEntity(db.Model, SerializerMixin):
    __tablename__ = "user_entities"
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey(
        'users.id'), nullable=False)
    entity_id = db.Column(db.Integer, db.ForeignKey(
        'entities.id'), nullable=False)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.now(timezone.utc))
    updated_at = db.Column(db.DateTime, nullable=False, default=datetime.now(timezone.utc))

    def __repr__(self):
        return f"user_group('{self.user_id}', '{self.group_id}')"

class ArticleFamily(db.Model, SerializerMixin):
    __tablename__ = "article_families"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(256))
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.now(timezone.utc))
    updated_at = db.Column(db.DateTime, nullable=False, default=datetime.now(timezone.utc))

    def __repr__(self):
        return f"article_family('{self.name}')"

class Article(db.Model, SerializerMixin):
    __tablename__ = "articles"
    id = db.Column(db.Integer, primary_key=True)
    libelle = db.Column(db.String(256))
    famille = db.Column(db.Integer)
    prix_achat_unit = db.Column(db.Float, default=0.0)
    prix_vente_unit = db.Column(db.Float, default=0.0)
    quantity = db.Column(db.Integer)
    unite = db.Column(db.Integer)
    status = db.Column(db.Boolean)
    user_id = db.Column(db.Integer, db.ForeignKey(
        'users.id'), nullable=False)
    fournisseur_id = db.Column(db.Integer, db.ForeignKey(
        'fournisseurs.id'), nullable=False)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.now(timezone.utc))
    updated_at = db.Column(db.DateTime, nullable=False, default=datetime.now(timezone.utc))

    def user(self):
        return User.query.get(self.user_id)

    def __repr__(self):
        return f"article('{self.libelle}')"
    
class Casheer(db.Model, SerializerMixin):
    __tablename__ = "casheers"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(256))
    balance = db.Column(db.Float, default=0.0)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.now(timezone.utc))
    
    def __repr__(self):
        return f"casheer('{self.name}')"
    
class TypeCategory(db.Model, SerializerMixin):
    __tablename__ = "type_categories"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(256))
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.now(timezone.utc))
    
    def __repr__(self):
        return f"type_category('{self.name}')"

class Category(db.Model, SerializerMixin):
    __tablename__ = "categories"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(256))
    type_category_id = db.Column(db.Integer, db.ForeignKey(
        'type_categories.id'), nullable=False)
    active = db.Column(db.Boolean)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.now(timezone.utc))
    updated_at = db.Column(db.DateTime, nullable=False, default=datetime.now(timezone.utc))
    
    def __repr__(self):
        return f"category('{self.name}')"


class Company(db.Model, SerializerMixin):
    __tablename__ = "companies"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(256), unique=True)
    service_charge_value = db.Column(db.Float, default=0.0)
    vat_charge_value = db.Column(db.Float, default=0.0)
    address = db.Column(db.String(256))
    phone = db.Column(db.String(16))
    country = db.Column(db.String(32), default="Togo")
    currency = db.Column(db.String(10))
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.now(timezone.utc))
    updated_at = db.Column(db.DateTime, nullable=False, default=datetime.now(timezone.utc))

    def __repr__(self):
        return f"article('{self.title}')"


class Depense(db.Model, SerializerMixin):
    __tablename__ = "depenses"
    id = db.Column(db.Integer, primary_key=True)
    libelle = db.Column(db.String(256))
    amount = db.Column(db.Float)
    amount_modif = db.Column(db.Float, default=0.0)
    user_id = db.Column(db.Integer, db.ForeignKey(
        'users.id'), nullable=False)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.now(timezone.utc))
    updated_at = db.Column(db.DateTime, nullable=False, default=datetime.now(timezone.utc))

    def __repr__(self):
        return f"{self.libelle}"

class ExploitAccount(db.Model, SerializerMixin):
    __tablename__ = "exploit_account"
    id = db.Column(db.Integer, primary_key=True)
    type_category = db.Column(db.Integer, db.ForeignKey(
        'type_categories.id'), nullable=False)
    libelle = db.Column(db.String(256))
    description = db.Column(db.String(256))
    amount = db.Column(db.Float)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.now(timezone.utc))
    updated_at = db.Column(db.DateTime, nullable=False, default=datetime.now(timezone.utc))
    casheer_id = db.Column(db.Integer, db.ForeignKey(
        'casheers.id'), nullable=False)

class Product(db.Model, SerializerMixin):
    __tablename__ = "products"

    id = db.Column(db.Integer, primary_key=True)
    category_id = db.Column(db.Integer, db.ForeignKey('categories.id'), nullable=False)
    group_id = db.Column(db.Integer, db.ForeignKey('groups.id'), nullable=False)
    name = db.Column(db.String(100), nullable=False)
    price = db.Column(db.Float, nullable=False)
    description = db.Column(db.Text, nullable=True)
    image = db.Column(db.String(255), nullable=True)  # URL or path to image file
    active = db.Column(db.Boolean, default=True, nullable=False)

    def __repr__(self):
        return f"<Product {self.name}>"
    
class Order(db.Model, SerializerMixin):
    __tablename__ = "orders"

    id = db.Column(db.Integer, primary_key=True)
    bill_no = db.Column(db.String(50), nullable=False)
    date_time = db.Column(db.DateTime, default=datetime.now(timezone.utc), nullable=False)
    gross_amount = db.Column(db.Float, nullable=False)
    service_charge_rate = db.Column(db.Float, nullable=False)
    service_charge_amount = db.Column(db.Float, nullable=False)
    vat_charge_rate = db.Column(db.Float, nullable=False)
    vat_charge_amount = db.Column(db.Float, nullable=False)
    discount = db.Column(db.Float, nullable=False)
    net_amount = db.Column(db.Float, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    table_id = db.Column(db.Integer, db.ForeignKey('tables.id'), nullable=True)
    paid_status = db.Column(db.Boolean, default=False, nullable=False)
    made_status = db.Column(db.Boolean, default=False, nullable=False)
    entity_id = db.Column(db.Integer, db.ForeignKey('entities.id'), nullable=False)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.now(timezone.utc))
    updated_at = db.Column(db.DateTime, nullable=False, default=datetime.now(timezone.utc))
    
    def __repr__(self):
        return f"<Order {self.bill_no}>"
    

class OrderItem(db.Model, SerializerMixin):
    __tablename__ = "order_items"

    id = db.Column(db.Integer, primary_key=True)
    order_id = db.Column(db.Integer, db.ForeignKey('orders.id'), nullable=False)
    product_id = db.Column(db.Integer, db.ForeignKey('products.id'), nullable=False)
    qty = db.Column(db.Integer, nullable=False)
    rate = db.Column(db.Float, nullable=False)
    amount = db.Column(db.Float, nullable=False)
    made_at = db.Column(db.DateTime, nullable=True)
    status = db.Column(db.String(50), nullable=False)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.now(timezone.utc))
    updated_at = db.Column(db.DateTime, nullable=False, default=datetime.now(timezone.utc))
    
    def __repr__(self):
        return f"<OrderItem {self.id} for Order {self.order_id}>"

class Stock(db.Model, SerializerMixin):
    __tablename__ = "stocks"

    id = db.Column(db.Integer, primary_key=True)
    quantity = db.Column(db.Integer, nullable=False)
    in_out = db.Column(db.Boolean, nullable=False)  # True for in, False for out
    article_id = db.Column(db.Integer, db.ForeignKey('articles.id'), nullable=False)
    fournisseur_id = db.Column(db.Integer, db.ForeignKey('fournisseurs.id'), nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.now(timezone.utc), nullable=False)

    def __repr__(self):
        return f"<Stock {'in' if self.in_out else 'out'} {self.quantity} units>"
