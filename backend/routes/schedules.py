from flask import Blueprint, jsonify, request
from models import db, Schedule, Teacher, Section, Subject
from scripts.moga_schedule import create_moga_schedule
from scripts.hill_climbing import create_hill_climbing_schedule
from scripts.simple_genetic import create_simple_genetic_schedule
from scripts.ant_colony import create_ant_colony_schedule

schedules_bp = Blueprint('schedules', __name__)

@schedules_bp.route('/', methods=['GET'])
def get_all_schedules():
    """Get all schedules"""
    schedules = Schedule.query.all()
    result = []
    for schedule in schedules:
        result.append({
            'id': schedule.id,
            'day': schedule.day,
            'time_slot': schedule.time_slot,
            'teacher': schedule.teacher.name if schedule.teacher else None,
            'section': schedule.section.name if schedule.section else None,
            'subject': schedule.subject.name if schedule.subject else None
        })
    return jsonify(result)


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
        return jsonify({
            'status': 'error',
            'message': str(e)
        }), 500
