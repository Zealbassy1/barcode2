# Setup Guide for Inventory Management System

## Quick Start

1. **Create New GitHub Repository**
   - Go to https://github.com/new
   - Name: `inventory-management-system`
   - Don't initialize with README (we have our own files)

2. **Upload Files to GitHub**
   You can upload these files using GitHub's web interface:
   - `app.py` - Main Flask application
   - `main.py` - Application entry point
   - `models.py` - Database models
   - `templates/` folder with all HTML files
   - `static/` folder with CSS and JavaScript
   - `README.md` - Project documentation
   - `.gitignore` - Git ignore rules

3. **Environment Setup**
   ```bash
   # Install Python dependencies
   pip install flask flask-cors flask-sqlalchemy psycopg2-binary email-validator gunicorn

   # Set environment variables
   export DATABASE_URL="postgresql://username:password@localhost/dbname"
   export SESSION_SECRET="your-secret-key-here"
   ```

4. **Database Setup**
   - Create a PostgreSQL database
   - Run the app once to create tables automatically
   - The app will create the necessary tables on first run

5. **Run Application**
   ```bash
   python main.py
   # or for production
   gunicorn --bind 0.0.0.0:5000 main:app
   ```

## Features Ready to Use

✅ Complete inventory management system
✅ Barcode scanning functionality  
✅ Sales processing with cart
✅ Reports and analytics
✅ Nigerian Naira currency support
✅ Responsive Bootstrap design
✅ PostgreSQL database integration

## Next Steps After Upload

1. Update the repository URL in README.md
2. Add any additional configuration needed
3. Test the deployment on your preferred hosting platform
4. Customize the styling or add new features as needed

Your inventory management system is ready to go!