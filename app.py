import os
import logging
from datetime import datetime, timedelta
from flask import Flask, render_template, request, jsonify, redirect, url_for, flash
from flask_cors import CORS
from models import db, Product, Sale, StockMovement
from decimal import Decimal

# Configure logging
logging.basicConfig(level=logging.DEBUG)

app = Flask(__name__)
app.secret_key = os.environ.get("SESSION_SECRET", "dev-secret-key-change-in-production")
CORS(app)

# Database configuration
database_url = os.environ.get("DATABASE_URL")
if not database_url:
    raise RuntimeError("DATABASE_URL environment variable is not set")

app.config["SQLALCHEMY_DATABASE_URI"] = database_url
app.config["SQLALCHEMY_ENGINE_OPTIONS"] = {
    "pool_recycle": 300,
    "pool_pre_ping": True,
}
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

# Initialize database
db.init_app(app)

# Constants
low_stock_threshold = 10

# Create database tables
with app.app_context():
    db.create_all()

@app.route('/')
def index():
    """Main dashboard showing overview"""
    total_products = Product.query.count()
    low_stock_items = Product.query.filter(Product.quantity <= low_stock_threshold).all()
    
    today = datetime.now().date()
    total_sales_today = Sale.query.filter(
        db.func.date(Sale.timestamp) == today
    ).count()
    
    # Calculate total inventory value
    products = Product.query.all()
    total_inventory_value = sum(float(product.price) * product.quantity for product in products)
    
    stats = {
        'total_products': total_products,
        'low_stock_count': len(low_stock_items),
        'total_sales_today': total_sales_today,
        'total_inventory_value': total_inventory_value
    }
    
    return render_template('index.html', stats=stats, low_stock_items=low_stock_items[:5])

@app.route('/inventory')
def inventory_page():
    """Inventory management page"""
    return render_template('inventory.html')

@app.route('/sales')
def sales_page():
    """Sales/checkout page"""
    return render_template('sales.html')

@app.route('/reports')
def reports_page():
    """Reports and analytics page"""
    return render_template('reports.html')

@app.route('/product/<barcode>')
def product_details(barcode):
    """Product details page"""
    product = Product.query.get(barcode)
    if not product:
        flash('Product not found', 'error')
        return redirect(url_for('inventory_page'))
    
    return render_template('product_details.html', product=product)

# API Endpoints

@app.route('/api/scan', methods=['POST'])
def scan_barcode():
    """Handle barcode scan"""
    try:
        data = request.get_json()
        barcode = data.get('barcode', '').strip()
        scan_type = data.get('type', 'lookup')  # lookup, receive, sale
        
        if not barcode:
            return jsonify({'success': False, 'message': 'No barcode provided'}), 400
        
        if scan_type == 'lookup':
            product = Product.query.get(barcode)
            if product:
                return jsonify({
                    'success': True,
                    'product': product.to_dict()
                })
            else:
                return jsonify({'success': False, 'message': 'Product not found in inventory'}), 404
        
        elif scan_type == 'receive':
            quantity = data.get('quantity', 1)
            product = Product.query.get(barcode)
            if product:
                # Record stock movement
                stock_movement = StockMovement(
                    barcode=barcode,
                    movement_type='receive',
                    quantity=quantity,
                    previous_quantity=product.quantity,
                    new_quantity=product.quantity + quantity,
                    notes=f'Received {quantity} units'
                )
                
                product.quantity += quantity
                product.last_updated = datetime.utcnow()
                
                db.session.add(stock_movement)
                db.session.commit()
                
                return jsonify({
                    'success': True,
                    'message': f'Added {quantity} units. New quantity: {product.quantity}',
                    'new_quantity': product.quantity
                })
            else:
                return jsonify({'success': False, 'message': 'Product not found. Please register it first.'}), 404
        
        elif scan_type == 'sale':
            quantity = data.get('quantity', 1)
            product = Product.query.get(barcode)
            if not product:
                return jsonify({'success': False, 'message': 'Product not found in inventory'}), 404
            
            if product.quantity < quantity:
                return jsonify({'success': False, 'message': 'Insufficient stock'}), 400
            
            # Process sale
            previous_quantity = product.quantity
            product.quantity -= quantity
            product.last_updated = datetime.utcnow()
            
            # Record sale
            sale = Sale(
                barcode=barcode,
                product_name=product.name,
                quantity=quantity,
                price=product.price,
                total=product.price * quantity
            )
            
            # Record stock movement
            stock_movement = StockMovement(
                barcode=barcode,
                movement_type='sale',
                quantity=-quantity,
                previous_quantity=previous_quantity,
                new_quantity=product.quantity,
                notes=f'Sale of {quantity} units'
            )
            
            db.session.add(sale)
            db.session.add(stock_movement)
            db.session.commit()
            
            return jsonify({
                'success': True,
                'message': f'Sale processed. Remaining stock: {product.quantity}',
                'sale': {
                    'product_name': product.name,
                    'quantity': quantity,
                    'total': float(sale.total),
                    'remaining_stock': product.quantity
                }
            })
        
        return jsonify({'success': False, 'message': 'Invalid scan type'}), 400
        
    except Exception as e:
        logging.error(f"Error processing scan: {str(e)}")
        db.session.rollback()
        return jsonify({'success': False, 'message': 'Internal server error'}), 500

@app.route('/api/products', methods=['GET'])
def get_products():
    """Get all products"""
    products = Product.query.all()
    return jsonify({'products': [product.to_dict() for product in products]})

@app.route('/api/products', methods=['POST'])
def add_product():
    """Add new product"""
    try:
        data = request.get_json()
        barcode = data.get('barcode', '').strip()
        
        if not barcode:
            return jsonify({'success': False, 'message': 'Barcode is required'}), 400
        
        existing_product = Product.query.get(barcode)
        if existing_product:
            return jsonify({'success': False, 'message': 'Product already exists'}), 400
        
        # Create new product
        product = Product(
            barcode=barcode,
            name=data.get('name', ''),
            price=Decimal(str(data.get('price', 0))),
            quantity=int(data.get('quantity', 0)),
            category=data.get('category', ''),
            supplier=data.get('supplier', ''),
            description=data.get('description', '')
        )
        
        db.session.add(product)
        db.session.commit()
        
        return jsonify({'success': True, 'message': 'Product added successfully'})
        
    except ValueError as e:
        return jsonify({'success': False, 'message': 'Invalid price or quantity format'}), 400
    except Exception as e:
        logging.error(f"Error adding product: {str(e)}")
        db.session.rollback()
        return jsonify({'success': False, 'message': 'Internal server error'}), 500

@app.route('/api/products/<barcode>', methods=['PUT'])
def update_product(barcode):
    """Update existing product"""
    try:
        product = Product.query.get(barcode)
        if not product:
            return jsonify({'success': False, 'message': 'Product not found'}), 404
        
        data = request.get_json()
        
        # Update product fields
        if 'name' in data:
            product.name = data['name']
        if 'price' in data:
            product.price = Decimal(str(data['price']))
        if 'quantity' in data:
            product.quantity = int(data['quantity'])
        if 'category' in data:
            product.category = data['category']
        if 'supplier' in data:
            product.supplier = data['supplier']
        if 'description' in data:
            product.description = data['description']
        
        product.last_updated = datetime.utcnow()
        
        db.session.commit()
        
        return jsonify({'success': True, 'message': 'Product updated successfully'})
        
    except ValueError as e:
        return jsonify({'success': False, 'message': 'Invalid price or quantity format'}), 400
    except Exception as e:
        logging.error(f"Error updating product: {str(e)}")
        db.session.rollback()
        return jsonify({'success': False, 'message': 'Internal server error'}), 500

@app.route('/api/products/<barcode>', methods=['DELETE'])
def delete_product(barcode):
    """Delete product"""
    product = Product.query.get(barcode)
    if not product:
        return jsonify({'success': False, 'message': 'Product not found'}), 404
    
    try:
        db.session.delete(product)
        db.session.commit()
        return jsonify({'success': True, 'message': 'Product deleted successfully'})
    except Exception as e:
        logging.error(f"Error deleting product: {str(e)}")
        db.session.rollback()
        return jsonify({'success': False, 'message': 'Internal server error'}), 500

@app.route('/api/sales', methods=['GET'])
def get_sales():
    """Get sales history"""
    sales = Sale.query.order_by(Sale.timestamp.desc()).all()
    return jsonify({'sales': [sale.to_dict() for sale in sales]})

@app.route('/api/reports/inventory', methods=['GET'])
def inventory_report():
    """Get inventory report"""
    products = Product.query.all()
    total_value = sum(float(product.price) * product.quantity for product in products)
    
    low_stock_items = [
        {
            'barcode': product.barcode, 
            'name': product.name, 
            'quantity': product.quantity
        }
        for product in products
        if product.quantity <= low_stock_threshold
    ]
    
    # Group by category
    categories = {}
    for product in products:
        category = product.category or 'Uncategorized'
        if category not in categories:
            categories[category] = {'count': 0, 'value': 0}
        categories[category]['count'] += 1
        categories[category]['value'] += float(product.price) * product.quantity
    
    report = {
        'total_products': len(products),
        'total_value': total_value,
        'low_stock_items': low_stock_items,
        'categories': categories
    }
    
    return jsonify(report)

@app.route('/api/reports/sales', methods=['GET'])
def sales_report():
    """Get sales report"""
    today = datetime.now().date()
    week_ago = today - timedelta(days=7)
    
    # Get today's sales
    today_sales = Sale.query.filter(
        db.func.date(Sale.timestamp) == today
    ).all()
    
    # Get this week's sales
    week_sales = Sale.query.filter(
        db.func.date(Sale.timestamp) >= week_ago
    ).all()
    
    # Get recent sales (last 10)
    recent_sales = Sale.query.order_by(Sale.timestamp.desc()).limit(10).all()
    
    report = {
        'today': {
            'count': len(today_sales),
            'total': sum(float(sale.total) for sale in today_sales)
        },
        'week': {
            'count': len(week_sales),
            'total': sum(float(sale.total) for sale in week_sales)
        },
        'recent_sales': [sale.to_dict() for sale in recent_sales]
    }
    
    return jsonify(report)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 5000)), debug=True)
