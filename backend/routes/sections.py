from flask import Blueprint, request, jsonify
from models.sections import Section
from models import db

sections_bp = Blueprint('sections', __name__)

@sections_bp.route('/', methods=['GET'])
def get_all_sections():
    """Get all sections"""
    sections = Section.query.all()
    result = []
    for section in sections:
        result.append({
            'id': section.id,
            'name': section.name
        })
    return jsonify(result)

@sections_bp.route('/<int:section_id>', methods=['GET'])
def get_section(section_id):
    """Get a specific section by ID"""
    section = Section.query.get_or_404(section_id)
    return jsonify({
        'id': section.id,
        'name': section.name
    })

@sections_bp.route('/', methods=['POST'])
def create_section():
    """Create a new section"""
    data = request.get_json()
    
    if not data or 'name' not in data:
        return jsonify({'error': 'Name is required'}), 400
    
    new_section = Section(name=data['name'])
    
    try:
        db.session.add(new_section)
        db.session.commit()
        return jsonify({
            'id': new_section.id,
            'name': new_section.name,
            'message': 'Section created successfully'
        }), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@sections_bp.route('/<int:section_id>', methods=['PUT'])
def update_section(section_id):
    """Update an existing section"""
    section = Section.query.get_or_404(section_id)
    data = request.get_json()
    
    if not data or 'name' not in data:
        return jsonify({'error': 'Name is required'}), 400
    
    try:
        section.name = data['name']
        db.session.commit()
        return jsonify({
            'id': section.id,
            'name': section.name,
            'message': 'Section updated successfully'
        })
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@sections_bp.route('/<int:section_id>', methods=['DELETE'])
def delete_section(section_id):
    """Delete a section"""
    section = Section.query.get_or_404(section_id)
    
    try:
        db.session.delete(section)
        db.session.commit()
        return jsonify({'message': f'Section {section_id} deleted successfully'})
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500
