# Replit.md - Inventory Management System

## Overview

This is a Flask-based inventory management system designed for small to medium businesses. The application provides comprehensive inventory tracking, sales processing, and reporting capabilities with barcode scanning functionality. It uses an in-memory storage approach for MVP development, with plans for database integration.

## User Preferences

Preferred communication style: Simple, everyday language.

## System Architecture

### Frontend Architecture
- **Technology**: HTML5, CSS3, JavaScript (vanilla)
- **UI Framework**: Bootstrap 5 with dark theme variant
- **Icons**: Feather Icons for consistent iconography
- **Responsive Design**: Mobile-first approach using Bootstrap's grid system
- **Client-side Libraries**: QuaggaJS for barcode scanning functionality

### Backend Architecture
- **Framework**: Flask (Python web framework)
- **Structure**: Single-module Flask application with template-based rendering
- **API Design**: RESTful endpoints with JSON responses for AJAX operations
- **Session Management**: Flask's built-in session handling with configurable secret key
- **CORS**: Enabled for cross-origin requests

### Data Storage Solutions
- **Current Implementation**: In-memory Python dictionaries for MVP
  - `inventory`: Dictionary storing product data by barcode
  - `sales_history`: List of sales transactions
- **Future Migration Path**: Prepared for PostgreSQL integration with psycopg2-binary dependency

### Authentication and Authorization
- **Current State**: Basic session management without user authentication
- **Security**: Environment-based secret key configuration
- **Future Enhancement**: Ready for user authentication system implementation

## Key Components

### Core Modules
1. **main.py**: Entry point and WSGI application setup
2. **app.py**: Main Flask application with routes and business logic
3. **Static Assets**: 
   - CSS styling with Bootstrap dark theme
   - JavaScript modules for scanner, inventory, and sales functionality
4. **Templates**: Jinja2 templates for all major pages (dashboard, inventory, sales, reports)

### Barcode Scanning System
- **Library**: QuaggaJS for client-side barcode recognition
- **Supported Formats**: Multiple barcode types (Code 128, EAN, UPC, Code 39, etc.)
- **Integration**: Seamless integration with inventory and sales workflows

### Business Logic Components
- **Inventory Management**: Add, update, and track product quantities
- **Sales Processing**: Cart-based checkout system with tax calculation
- **Low Stock Alerts**: Automated threshold-based notifications
- **Reporting**: Analytics for inventory levels and sales performance

## Data Flow

### Inventory Management Flow
1. **Product Addition**: Manual entry or barcode scan → Form validation → In-memory storage
2. **Stock Updates**: Barcode scan → Product lookup → Quantity adjustment → History tracking
3. **Low Stock Detection**: Real-time calculation based on configurable thresholds

### Sales Processing Flow
1. **Item Scanning**: Barcode detection → Product lookup → Cart addition
2. **Checkout Process**: Cart review → Tax calculation → Payment processing → Inventory deduction
3. **Transaction Recording**: Sale completion → History logging → Receipt generation

### Reporting Flow
1. **Data Aggregation**: Real-time calculation from in-memory data
2. **Dashboard Updates**: Live statistics display
3. **Report Generation**: On-demand analytics compilation

## External Dependencies

### Python Packages
- **Flask**: Web framework and routing
- **Flask-CORS**: Cross-origin resource sharing
- **Flask-SQLAlchemy**: ORM for future database integration
- **psycopg2-binary**: PostgreSQL adapter for database connectivity
- **email-validator**: Input validation for email fields
- **gunicorn**: Production WSGI server

### Frontend Libraries
- **Bootstrap 5**: UI framework with dark theme
- **Feather Icons**: Icon library
- **QuaggaJS**: Barcode scanning (CDN-based)

### System Dependencies
- **PostgreSQL**: Database server (configured but not yet implemented)
- **OpenSSL**: Security and encryption support

## Deployment Strategy

### Development Environment
- **Platform**: Replit with Python 3.11 runtime
- **Live Reload**: Gunicorn with reload flag for development
- **Port Configuration**: Configured for port 5000 with automatic port detection

### Production Deployment
- **Server**: Gunicorn WSGI server with autoscale deployment target
- **Process Management**: Multi-worker configuration with port reuse
- **Environment Variables**: Secure configuration through environment variables

### Database Migration Path
- **Current**: In-memory storage for rapid prototyping
- **Future**: PostgreSQL with SQLAlchemy ORM
- **Migration Strategy**: Structured data models ready for database schema creation

### Security Considerations
- **Secret Management**: Environment-based configuration
- **CORS Policy**: Controlled cross-origin access
- **Input Validation**: Server-side validation for all user inputs
- **Future Enhancements**: Authentication, authorization, and data encryption planned