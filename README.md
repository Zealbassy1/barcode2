# Inventory Management System

A comprehensive Flask-based inventory management system with barcode scanning functionality, designed for small to medium businesses.

## Features

- **Barcode Scanning**: Integrated barcode scanning for product identification
- **Product Management**: Add, update, and track product inventory
- **Sales Processing**: Complete checkout system with cart functionality
- **Real-time Reporting**: Inventory analytics and sales reports
- **Nigerian Naira Support**: Currency formatting for Nigerian businesses
- **PostgreSQL Database**: Persistent data storage with proper relationships
- **Responsive Design**: Bootstrap-based UI that works on all devices

## Tech Stack

- **Backend**: Flask (Python)
- **Database**: PostgreSQL
- **Frontend**: HTML5, CSS3, JavaScript (Vanilla)
- **UI Framework**: Bootstrap 5 with dark theme
- **Barcode Scanning**: QuaggaJS library
- **Icons**: Feather Icons
- **Charts**: Chart.js for analytics

## Installation

1. Clone the repository:
```bash
git clone https://github.com/YOUR_USERNAME/YOUR_REPO_NAME.git
cd YOUR_REPO_NAME
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Set up environment variables:
```bash
export DATABASE_URL="your_postgresql_connection_string"
export SESSION_SECRET="your_secret_key"
```

4. Run the application:
```bash
python main.py
```

5. Open your browser and navigate to `http://localhost:5000`

## Usage

### Dashboard
- View inventory overview and quick stats
- Monitor low stock alerts
- Access recent sales data

### Inventory Management
- Scan barcodes to add/receive products
- Manually add new products
- Update stock quantities
- Track stock movements

### Sales Processing
- Scan items for checkout
- Manage shopping cart
- Process payments
- Generate receipts

### Reports & Analytics
- Inventory reports with category breakdowns
- Sales analytics and trends
- Low stock monitoring
- Data visualization with charts

## Database Schema

The system uses three main tables:
- **Products**: Store product information and current stock
- **Sales**: Record all sales transactions
- **Stock Movements**: Track all inventory changes

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Submit a pull request

## License

This project is open source and available under the MIT License.