from flask import Blueprint, request, jsonify
from app import db
from app.models.developer import Developer
from sqlalchemy.exc import IntegrityError

developers = Blueprint('developers', __name__)

@developers.route('/developers', methods=['POST'])
def create_developer():
    """Create a new developer"""
    data = request.get_json()
    
    if not data or 'name' not in data:
        return jsonify({'error': 'Name is required'}), 400
    
    developer = Developer(**data)
    
    # Validate developer data
    errors = developer.validate()
    if errors:
        return jsonify({'errors': errors}), 400
    
    try:
        db.session.add(developer)
        db.session.commit()
        return jsonify(developer.to_dict()), 201
    except IntegrityError as e:
        db.session.rollback()
        return jsonify({'error': 'Database error occurred'}), 400
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@developers.route('/developers', methods=['GET'])
def get_developers():
    """Get all developers with optional pagination"""
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 10, type=int)
    
    developers = Developer.query.paginate(
        page=page, 
        per_page=per_page,
        error_out=False
    )
    
    return jsonify({
        'developers': [dev.to_dict() for dev in developers.items],
        'total': developers.total,
        'pages': developers.pages,
        'current_page': developers.page
    })

@developers.route('/developers/<int:developer_id>', methods=['GET'])
def get_developer(developer_id):
    """Get a specific developer by ID"""
    developer = Developer.query.get_or_404(developer_id)
    return jsonify(developer.to_dict())

@developers.route('/developers/<int:developer_id>', methods=['PUT'])
def update_developer(developer_id):
    """Update a developer"""
    developer = Developer.query.get_or_404(developer_id)
    data = request.get_json()
    
    if not data:
        return jsonify({'error': 'No data provided'}), 400
    
    developer.update_from_dict(data)
    
    # Validate updated data
    errors = developer.validate()
    if errors:
        return jsonify({'errors': errors}), 400
    
    try:
        db.session.commit()
        return jsonify(developer.to_dict())
    except IntegrityError as e:
        db.session.rollback()
        return jsonify({'error': 'Database error occurred'}), 400
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@developers.route('/developers/<int:developer_id>', methods=['DELETE'])
def delete_developer(developer_id):
    """Delete a developer"""
    developer = Developer.query.get_or_404(developer_id)
    
    # Check if developer has any projects
    if developer.projects:
        return jsonify({
            'error': 'Cannot delete developer with existing projects'
        }), 400
    
    try:
        db.session.delete(developer)
        db.session.commit()
        return '', 204
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@developers.route('/developers/<int:developer_id>/projects', methods=['GET'])
def get_developer_projects(developer_id):
    """Get all projects for a specific developer"""
    developer = Developer.query.get_or_404(developer_id)
    return jsonify([project.to_dict() for project in developer.projects])

@developers.route('/developers/<int:developer_id>/update-counts', methods=['POST'])
def update_developer_counts(developer_id):
    """Update project counts for a developer"""
    developer = Developer.query.get_or_404(developer_id)
    developer.update_project_counts()
    return jsonify(developer.to_dict()) 