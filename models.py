from datetime import datetime
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase

class Base(DeclarativeBase):
    pass

db = SQLAlchemy(model_class=Base)

class Product(db.Model):
    __tablename__ = 'products'
    
    barcode = db.Column(db.String(100), primary_key=True)
    name = db.Column(db.String(200), nullable=False)
    price = db.Column(db.Numeric(10, 2), nullable=False)
    quantity = db.Column(db.Integer, nullable=False, default=0)
    category = db.Column(db.String(100))
    supplier = db.Column(db.String(200))
    description = db.Column(db.Text)
    last_updated = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def to_dict(self):
        return {
            'barcode': self.barcode,
            'name': self.name,
            'price': float(self.price),
            'quantity': self.quantity,
            'category': self.category,
            'supplier': self.supplier,
            'description': self.description,
            'last_updated': self.last_updated,
            'created_at': self.created_at
        }

class Sale(db.Model):
    __tablename__ = 'sales'
    
    id = db.Column(db.Integer, primary_key=True)
    barcode = db.Column(db.String(100), db.ForeignKey('products.barcode'), nullable=False)
    product_name = db.Column(db.String(200), nullable=False)
    quantity = db.Column(db.Integer, nullable=False)
    price = db.Column(db.Numeric(10, 2), nullable=False)
    total = db.Column(db.Numeric(10, 2), nullable=False)
    payment_method = db.Column(db.String(50), default='cash')
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relationship
    product = db.relationship('Product', backref=db.backref('sales', lazy=True))
    
    def to_dict(self):
        return {
            'id': self.id,
            'barcode': self.barcode,
            'product_name': self.product_name,
            'quantity': self.quantity,
            'price': float(self.price),
            'total': float(self.total),
            'payment_method': self.payment_method,
            'timestamp': self.timestamp
        }

class StockMovement(db.Model):
    __tablename__ = 'stock_movements'
    
    id = db.Column(db.Integer, primary_key=True)
    barcode = db.Column(db.String(100), db.ForeignKey('products.barcode'), nullable=False)
    movement_type = db.Column(db.String(20), nullable=False)  # 'receive', 'sale', 'adjustment'
    quantity = db.Column(db.Integer, nullable=False)
    previous_quantity = db.Column(db.Integer, nullable=False)
    new_quantity = db.Column(db.Integer, nullable=False)
    notes = db.Column(db.Text)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relationship
    product = db.relationship('Product', backref=db.backref('stock_movements', lazy=True))
    
    def to_dict(self):
        return {
            'id': self.id,
            'barcode': self.barcode,
            'movement_type': self.movement_type,
            'quantity': self.quantity,
            'previous_quantity': self.previous_quantity,
            'new_quantity': self.new_quantity,
            'notes': self.notes,
            'timestamp': self.timestamp
        }