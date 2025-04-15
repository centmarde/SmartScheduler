from flask_sqlalchemy import SQLAlchemy

# Initialize SQLAlchemy
db = SQLAlchemy()

# Import models after db is defined to avoid circular imports
from .teachers import Teacher
from .sections import Section
from .subjects import Subject
from .schedules import Schedule

# Export models
__all__ = ['db', 'Teacher', 'Subject', 'Section', 'Schedule']
