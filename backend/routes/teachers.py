from flask import Blueprint, jsonify, request
from models import db, Teacher

teachers_bp = Blueprint('teachers', __name__)

@teachers_bp.route('/', methods=['GET'])
def get_all_teachers():
    """Get all teachers"""
    teachers = Teacher.query.all()
    result = [{
        'id': teacher.id,
        'name': teacher.name,
        'subject': {
            'id': teacher.subject.id,
            'name': teacher.subject.name,
            'code': teacher.subject.code
        } if teacher.subject else None
    } for teacher in teachers]
    
    return jsonify(result)

@teachers_bp.route('/<int:teacher_id>', methods=['GET'])
def get_teacher(teacher_id):
    """Get a teacher by ID"""
    teacher = Teacher.query.get(teacher_id)
    
    if not teacher:
        return jsonify({'error': 'Teacher not found'}), 404
    
    result = {
        'id': teacher.id,
        'name': teacher.name,
        'subject': {
            'id': teacher.subject.id,
            'name': teacher.subject.name,
            'code': teacher.subject.code
        } if teacher.subject else None
    }
    
    return jsonify(result)

@teachers_bp.route('/subject/<int:subject_id>', methods=['GET'])
def get_teachers_by_subject(subject_id):
    """Get all teachers teaching a specific subject"""
    teachers = Teacher.query.filter_by(subject_id=subject_id).all()
    
    result = [{
        'id': teacher.id,
        'name': teacher.name
    } for teacher in teachers]
    
    return jsonify(result)
