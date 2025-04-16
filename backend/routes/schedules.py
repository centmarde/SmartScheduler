from flask import Blueprint, jsonify, request
from models import db, Schedule, Teacher, Section, Subject
from scripts.moga_schedule import create_moga_schedule
from scripts.hill_climbing import create_hill_climbing_schedule
from scripts.simple_genetic import create_simple_genetic_schedule
from scripts.ant_colony import create_ant_colony_schedule

schedules_bp = Blueprint('schedules', __name__)

@schedules_bp.route('/', methods=['GET'])
def get_all_schedules():
    """Get all schedules with related data"""
    schedules = Schedule.query.all()
    result = []
    
    for schedule in schedules:
        schedule_data = {
            'id': schedule.id,
            'day': schedule.day,
            'time_slot': schedule.time_slot,
        }
        
        # Include teacher if available
        if schedule.teacher:
            schedule_data['teacher'] = {
                'id': schedule.teacher.id,
                'name': schedule.teacher.name
            }
            
        # Include section if available
        if schedule.section:
            schedule_data['section'] = {
                'id': schedule.section.id,
                'name': schedule.section.name
            }
            
        # Include subject if available
        if schedule.subject:
            schedule_data['subject'] = {
                'id': schedule.subject.id,
                'name': schedule.subject.name,
                'code': schedule.subject.code
            }
            
        result.append(schedule_data)
    
    return jsonify(result)

@schedules_bp.route('/teacher/<int:teacher_id>', methods=['GET'])
def get_teacher_schedule(teacher_id):
    """Get schedule for a specific teacher"""
    schedules = Schedule.query.filter_by(teacher_id=teacher_id).all()
    result = []
    
    for schedule in schedules:
        schedule_data = {
            'id': schedule.id,
            'day': schedule.day,
            'time_slot': schedule.time_slot,
        }
        
        # Include section if available
        if schedule.section:
            schedule_data['section'] = {
                'id': schedule.section.id,
                'name': schedule.section.name
            }
            
        # Include subject if available
        if schedule.subject:
            schedule_data['subject'] = {
                'id': schedule.subject.id,
                'name': schedule.subject.name,
                'code': schedule.subject.code
            }
            
        result.append(schedule_data)
    
    return jsonify(result)

@schedules_bp.route('/section/<int:section_id>', methods=['GET'])
def get_section_schedule(section_id):
    """Get schedule for a specific section"""
    schedules = Schedule.query.filter_by(section_id=section_id).all()
    result = []
    
    for schedule in schedules:
        schedule_data = {
            'id': schedule.id,
            'day': schedule.day,
            'time_slot': schedule.time_slot,
        }
        
        # Include teacher if available
        if schedule.teacher:
            schedule_data['teacher'] = {
                'id': schedule.teacher.id,
                'name': schedule.teacher.name
            }
            
        # Include subject if available
        if schedule.subject:
            schedule_data['subject'] = {
                'id': schedule.subject.id,
                'name': schedule.subject.name,
                'code': schedule.subject.code
            }
            
        result.append(schedule_data)
    
    return jsonify(result)

@schedules_bp.route('/', methods=['POST'])
def create_schedule():
    """Create a new schedule entry"""
    data = request.get_json()
    
    # Validate required fields
    required_fields = ['day', 'time_slot']
    for field in required_fields:
        if field not in data:
            return jsonify({'error': f'Missing required field: {field}'}), 400
    
    # Create new schedule
    new_schedule = Schedule(
        day=data['day'],
        time_slot=data['time_slot'],
        teacher_id=data.get('teacher_id'),
        section_id=data.get('section_id'),
        subject_id=data.get('subject_id')
    )
    
    try:
        db.session.add(new_schedule)
        db.session.commit()
        
        # Return created schedule with related data
        result = {
            'id': new_schedule.id,
            'day': new_schedule.day,
            'time_slot': new_schedule.time_slot,
        }
        
        if new_schedule.teacher:
            result['teacher'] = {
                'id': new_schedule.teacher.id,
                'name': new_schedule.teacher.name
            }
            
        if new_schedule.section:
            result['section'] = {
                'id': new_schedule.section.id,
                'name': new_schedule.section.name
            }
            
        if new_schedule.subject:
            result['subject'] = {
                'id': new_schedule.subject.id,
                'name': new_schedule.subject.name,
                'code': new_schedule.subject.code
            }
        
        return jsonify(result), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@schedules_bp.route('/generate/moga', methods=['POST'])
def generate_schedules():
    """Generate schedules using MOGA algorithm"""
    try:
        # Clear existing schedules if specified
        if request.json and request.json.get('clear_existing', False):
            Schedule.query.delete()
            db.session.commit()
        
        # Generate schedules using MOGA algorithm
        num_schedules, metrics, execution_time = create_moga_schedule(
            db.session, 
            Section, 
            Subject, 
            Teacher, 
            Schedule
        )
        
        db.session.commit()
        
        return jsonify({
            'status': 'success',
            'message': f'{num_schedules} schedules generated successfully',
            'data': {
                'count': num_schedules,
                'metrics': metrics,
                'execution_time_seconds': round(execution_time, 2)
            }
        }), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({
            'status': 'error',
            'message': str(e)
        }), 500

@schedules_bp.route('/generate/hill-climbing', methods=['POST'])
def generate_schedules_hill_climbing():
    """Generate schedules using Hill Climbing algorithm"""
    try:
        # Clear existing schedules if specified
        if request.json and request.json.get('clear_existing', False):
            Schedule.query.delete()
            db.session.commit()
        
        # Generate schedules using Hill Climbing algorithm
        num_schedules, metrics, execution_time = create_hill_climbing_schedule(
            db.session, 
            Section, 
            Subject, 
            Teacher, 
            Schedule
        )
        
        db.session.commit()
        
        return jsonify({
            'status': 'success',
            'message': f'{num_schedules} schedules generated successfully using Hill Climbing',
            'data': {
                'count': num_schedules,
                'algorithm': 'hill-climbing',
                'metrics': metrics,
                'execution_time_seconds': round(execution_time, 2)
            }
        }), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({
            'status': 'error',
            'message': str(e)
        }), 500

@schedules_bp.route('/generate/simple-genetic', methods=['POST'])
def generate_schedules_simple_genetic():
    """Generate schedules using Simple Genetic algorithm"""
    try:
        # Clear existing schedules if specified
        if request.json and request.json.get('clear_existing', False):
            Schedule.query.delete()
            db.session.commit()
        
        # Generate schedules using Simple Genetic algorithm
        num_schedules, metrics, execution_time = create_simple_genetic_schedule(
            db.session, 
            Section, 
            Subject, 
            Teacher, 
            Schedule
        )
        
        db.session.commit()
        
        return jsonify({
            'status': 'success',
            'message': f'{num_schedules} schedules generated successfully using Simple Genetic Algorithm',
            'data': {
                'count': num_schedules,
                'algorithm': 'simple-genetic',
                'metrics': metrics,
                'execution_time_seconds': round(execution_time, 2)
            }
        }), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({
            'status': 'error',
            'message': str(e)
        }), 500

@schedules_bp.route('/generate/ant-colony', methods=['POST'])
def generate_schedules_ant_colony():
    """Generate schedules using Ant Colony Optimization algorithm"""
    try:
        # Clear existing schedules if specified
        if request.json and request.json.get('clear_existing', False):
            Schedule.query.delete()
            db.session.commit()
        
        # Generate schedules using Ant Colony Optimization
        num_schedules, metrics, execution_time = create_ant_colony_schedule(
            db.session, 
            Section, 
            Subject, 
            Teacher, 
            Schedule
        )
        
        db.session.commit()
        
        return jsonify({
            'status': 'success',
            'message': f'{num_schedules} schedules generated successfully using Ant Colony Optimization',
            'data': {
                'count': num_schedules,
                'algorithm': 'ant-colony',
                'metrics': metrics,
                'execution_time_seconds': round(execution_time, 2)
            }
        }), 201
    except Exception as e:
        db.session.rollback()
        import traceback
        error_details = traceback.format_exc()
        print(f"Ant Colony Error: {str(e)}\n{error_details}")
        return jsonify({
            'status': 'error',
            'message': str(e),
            'details': error_details if request.json and request.json.get('debug', False) else None
        }), 500
