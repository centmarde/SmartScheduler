from flask import Blueprint, jsonify, request
from models import db, Subject

subjects_bp = Blueprint('subjects', __name__)

@subjects_bp.route('/', methods=['GET'])
def get_all_subjects():
    """Get all subjects"""
    subjects = Subject.query.all()
    result = [{
        'id': subject.id,
        'name': subject.name,
        'code': subject.code,
        'description': subject.description,
        'teachers': [{'id': teacher.id, 'name': teacher.name} for teacher in subject.teachers]
    } for subject in subjects]
    
    return jsonify(result)

@subjects_bp.route('/<int:subject_id>', methods=['GET'])
def get_subject(subject_id):
    """Get a subject by ID"""
    subject = Subject.query.get(subject_id)
    
    if not subject:
        return jsonify({'error': 'Subject not found'}), 404
    
    result = {
        'id': subject.id,
        'name': subject.name,
        'code': subject.code,
        'description': subject.description,
        'teachers': [{'id': teacher.id, 'name': teacher.name} for teacher in subject.teachers],
        'sections': [{'id': section.id, 'name': section.name} for section in subject.sections]
    }
    
    return jsonify(result)

@subjects_bp.route('/section/<int:section_id>', methods=['GET'])
def get_subjects_by_section(section_id):
    """Get all subjects for a specific section"""
    # Assuming there's a relationship between subjects and sections through a join table or direct relationship
    # This needs to be adjusted based on your actual model structure
    from models import Section
    section = Section.query.get(section_id)
    if not section:
        return jsonify({'error': 'Section not found'}), 404
        
    subjects = section.subjects
    
    result = [{
        'id': subject.id,
        'name': subject.name,
        'code': subject.code,
        'description': subject.description
    } for subject in subjects]
    
    return jsonify(result)
