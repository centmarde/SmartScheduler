import os
from flask import Flask, jsonify
from flask_cors import CORS
from flask_migrate import Migrate
from dotenv import load_dotenv
# Import db and all models
from models import db, Teacher, Subject, Section, Schedule

# Load environment variables
load_dotenv()

# Initialize Flask app
app = Flask(__name__)
CORS(app)

# Get the absolute path of the directory containing this script
BASE_DIR = os.path.abspath(os.path.dirname(__file__))

# Ensure the db directory exists
db_path = os.getenv('DATABASE_URL').replace('sqlite:///', '')
db_dir = os.path.dirname(db_path)
os.makedirs(db_dir, exist_ok=True)

# Configure database
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Print database path for debugging
print(f"Database URL: {app.config['SQLALCHEMY_DATABASE_URI']}")
print(f"Database File Path: {db_path}")

# Initialize db with app
db.init_app(app)

# Initialize Flask-Migrate
migrate = Migrate(app, db)

# Create database tables
with app.app_context():
    db.create_all()
    
    # Optionally, seed the database with initial data
    Teacher.seed(db.session)
    Subject.seed(db.session)
    Section.seed(db.session)
    
    # Seed the many-to-many relationships after all individual models are seeded
    Subject.seed_section_subject(db.session)
    
    # Seed schedules using the MOGA algorithm
    # Schedule.seed(db.session)

# Register routes blueprint
from routes.sections import sections_bp
app.register_blueprint(sections_bp, url_prefix='/sections')

# Add this line to import the schedules blueprint
from routes.schedules import schedules_bp
app.register_blueprint(schedules_bp, url_prefix='/schedules')

# Global error handlers
@app.errorhandler(404)
def not_found(error):
    return jsonify({'error': 'Resource not found'}), 404

@app.errorhandler(400)
def bad_request(error):
    return jsonify({'error': 'Bad request'}), 400

# Run the application
if __name__ == '__main__':
    app.run(host='127.0.0.1', port=8080, debug=True)