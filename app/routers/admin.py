from flask import Blueprint, render_template, request, jsonify, flash, redirect, url_for, current_app, session, send_file, make_response
from app import db
from app.models import (
    Project, Developer, City, Locality, Amenity, Approval, ProjectApproval, Tower, 
    User, UnitType, PropertyUnit, Review, Notification, ProjectMedia,
    ProjectDocument, UserInterest, SearchLog, PropertyComparison, PriceHistory, BalconyDetail, DoorWindowSpec,
    ProjectAmenity, UnitRoomDetail
)
from sqlalchemy import func
from datetime import datetime, timedelta
from werkzeug.utils import secure_filename
import os
import pandas as pd
import io
try:
    import pdfkit
    PDFKIT_AVAILABLE = True
except ImportError:
    PDFKIT_AVAILABLE = False
from flask import session, redirect, url_for, render_template, request, flash
from werkzeug.security import generate_password_hash, check_password_hash
from app.models import User

admin = Blueprint('admin', __name__, url_prefix='/admin')

@admin.route('/')
@admin.route('/dashboard')
def dashboard():
    """Admin Dashboard"""
    # Get statistics
    stats = {
        'total_projects': Project.query.count(),
        'total_developers': Developer.query.count(),
        'total_users': User.query.count(),
        'total_reviews': Review.query.count(),
        'active_projects': Project.query.filter_by(is_active=True).count(),
        'pending_approvals': ProjectApproval.query.filter_by(status='pending').count(),
        'total_revenue': db.session.query(func.sum(PropertyUnit.total_price)).scalar() or 0,
        'recent_projects': Project.query.order_by(Project.created_at.desc()).limit(5).all()
    }
    # Calculate average revenue per project (avoid division by zero)
    avg_revenue = stats['total_revenue'] / (stats['total_projects'] if stats['total_projects'] else 1)
    
    # Get recent activities
    recent_activities = []
    
    # Recent projects
    recent_projects = Project.query.order_by(Project.created_at.desc()).limit(3).all()
    for project in recent_projects:
        recent_activities.append({
            'type': 'project',
            'title': f'New project "{project.name}" added',
            'time': project.created_at,
            'icon': 'fas fa-project-diagram'
        })
    
    # Recent reviews
    recent_reviews = Review.query.order_by(Review.created_at.desc()).limit(3).all()
    for review in recent_reviews:
        recent_activities.append({
            'type': 'review',
            'title': f'New review for project "{review.project.name}"',
            'time': review.created_at,
            'icon': 'fas fa-star'
        })
    
    # Sort activities by time
    recent_activities.sort(key=lambda x: x['time'], reverse=True)
    recent_activities = recent_activities[:10]
    
    return render_template('admin/dashboard.html', stats=stats, avg_revenue=avg_revenue, recent_activities=recent_activities)

# Projects Routes
@admin.route('/projects')
def projects():
    """List all projects"""
    page = request.args.get('page', 1, type=int)
    search = request.args.get('search', '')
    status = request.args.get('status', '')
    
    query = Project.query
    
    if search:
        query = query.filter(Project.name.ilike(f'%{search}%'))
    
    if status:
        query = query.filter(Project.status == status)
    
    projects = query.order_by(Project.created_at.desc()).paginate(
        page=page, per_page=10, error_out=False
    )
    
    return render_template('admin/projects/index.html', projects=projects, search=search, status=status)

@admin.route('/projects/new', methods=['GET', 'POST'])
def new_project():
    """Create new project"""
    if request.method == 'POST':
        data = request.form.to_dict()
        action = request.form.get('action')
        # Convert checkbox to boolean
        data['is_active'] = 'is_active' in request.form
        # Handle file uploads
        if 'master_plan' in request.files:
            file = request.files['master_plan']
            if file and file.filename:
                filename = secure_filename(file.filename)
                file.save(os.path.join(current_app.config['UPLOAD_FOLDER'], filename))
                data['master_plan_url'] = filename
        if 'brochure' in request.files:
            file = request.files['brochure']
            if file and file.filename:
                filename = secure_filename(file.filename)
                file.save(os.path.join(current_app.config['UPLOAD_FOLDER'], filename))
                data['brochure_url'] = filename
        if action == 'draft':
            session['project_draft'] = data
            flash('Draft saved! You can resume it later.', 'info')
            return redirect(url_for('admin.new_project'))
        else:
            session.pop('project_draft', None)
            data.pop('is_draft', None)  # Remove is_draft if present
            # Prepare a new dict for Project fields with correct types
            project_data = {}
            # Numbers and decimals
            for field in [
                'total_land_area', 'unit_density', 'open_area_percentage', 'park_area', 'clubhouse_area',
                'min_price', 'max_price', 'price_per_sqft', 'latitude', 'longitude', 'approach_road_width',
                'nearest_metro_distance', 'airport_distance']:
                value = data.get(field, None)
                if value == '' or value is None:
                    project_data[field] = None
                else:
                    try:
                        project_data[field] = float(value)
                    except Exception:
                        project_data[field] = None
            # Integers
            for field in ['total_units', 'developer_id', 'locality_id']:
                value = data.get(field, None)
                if value == '' or value is None:
                    project_data[field] = None
                else:
                    try:
                        project_data[field] = int(value)
                    except Exception:
                        project_data[field] = None
            # Dates
            from datetime import datetime
            for field in ['launch_date', 'possession_date', 'completion_date']:
                value = data.get(field, None)
                if value == '' or value is None:
                    project_data[field] = None
                else:
                    try:
                        project_data[field] = datetime.strptime(value, '%Y-%m-%d').date()
                    except Exception:
                        project_data[field] = None
            # Booleans
            project_data['is_active'] = data.get('is_active', False)
            # Strings and other fields
            for field in [
                'name', 'project_type', 'property_type', 'status', 'currency', 'address',
                'rera_number', 'rera_website', 'rera_status', 'description', 'highlights',
                'master_plan_url', 'brochure_url', 'meta_title', 'meta_description']:
                value = data.get(field, None)
                project_data[field] = value if value != '' else None
            project = Project(**project_data)
            db.session.add(project)
            db.session.commit()
            flash('Project created successfully!', 'success')
            return redirect(url_for('admin.projects'))
    # GET: pre-fill form with draft if present
    draft = session.get('project_draft')
    developers = Developer.query.all()
    localities = Locality.query.all()
    return render_template('admin/projects/new.html', developers=developers, localities=localities, draft=draft)

@admin.route('/projects/<int:project_id>')
def view_project(project_id):
    """View project details"""
    project = Project.query.get_or_404(project_id)
    return render_template('admin/projects/view.html', project=project)

@admin.route('/projects/<int:project_id>/edit', methods=['GET', 'POST'])
def edit_project(project_id):
    """Edit project"""
    project = Project.query.get_or_404(project_id)
    
    if request.method == 'POST':
        data = request.form.to_dict()
        # Convert booleans
        data['is_active'] = 'is_active' in request.form
        # Convert numbers and decimals
        for field in [
            'total_land_area', 'unit_density', 'open_area_percentage', 'park_area', 'clubhouse_area',
            'min_price', 'max_price', 'price_per_sqft', 'latitude', 'longitude', 'approach_road_width',
            'nearest_metro_distance', 'airport_distance']:
            if data.get(field):
                try:
                    data[field] = float(data[field])
                except Exception:
                    data[field] = None
            else:
                data[field] = None
        # Convert integers
        for field in ['total_units', 'developer_id', 'locality_id']:
            if data.get(field):
                try:
                    data[field] = int(data[field])
                except Exception:
                    data[field] = None
            else:
                data[field] = None
        # Convert dates
        from datetime import datetime
        for field in ['launch_date', 'possession_date', 'completion_date']:
            if data.get(field):
                try:
                    data[field] = datetime.strptime(data[field], '%Y-%m-%d').date()
                except Exception:
                    data[field] = None
            else:
                data[field] = None
        # Handle file uploads
        if 'master_plan' in request.files:
            file = request.files['master_plan']
            if file and file.filename:
                filename = secure_filename(file.filename)
                file.save(os.path.join(current_app.config['UPLOAD_FOLDER'], filename))
                data['master_plan_url'] = filename
        if 'brochure' in request.files:
            file = request.files['brochure']
            if file and file.filename:
                filename = secure_filename(file.filename)
                file.save(os.path.join(current_app.config['UPLOAD_FOLDER'], filename))
                data['brochure_url'] = filename
        # Update all fields
        for key, value in data.items():
            if hasattr(project, key):
                setattr(project, key, value)
        db.session.commit()
        flash('Project updated successfully!', 'success')
        return redirect(url_for('admin.projects'))
    
    developers = Developer.query.all()
    localities = Locality.query.all()
    
    return render_template('admin/projects/edit.html', project=project, developers=developers, localities=localities)

@admin.route('/projects/<int:project_id>/delete', methods=['POST', 'DELETE'])
@admin.route('/projects/<int:project_id>/delete/', methods=['POST', 'DELETE'])
def delete_project(project_id):
    """Delete project"""
    project = Project.query.get_or_404(project_id)
    db.session.delete(project)
    db.session.commit()
    if request.method == 'DELETE' or request.is_json or request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        return jsonify({'success': True, 'message': 'Project deleted successfully!'})
    flash('Project deleted successfully!', 'success')
    return redirect(url_for('admin.projects'))

# Developers Routes
@admin.route('/developers')
def developers():
    """List all developers"""
    page = request.args.get('page', 1, type=int)
    search = request.args.get('search', '')
    
    query = Developer.query
    
    if search:
        query = query.filter(Developer.name.ilike(f'%{search}%'))
    
    developers = query.order_by(Developer.created_at.desc()).paginate(
        page=page, per_page=10, error_out=False
    )
    
    return render_template('admin/developers/index.html', developers=developers, search=search)

@admin.route('/developers/new', methods=['GET', 'POST'])
def new_developer():
    """Create new developer"""
    if request.method == 'POST':
        data = request.form.to_dict()
        
        # Handle logo upload
        if 'logo' in request.files:
            file = request.files['logo']
            if file and file.filename:
                filename = secure_filename(file.filename)
                file.save(os.path.join(current_app.config['UPLOAD_FOLDER'], filename))
                data['logo_url'] = filename
        
        developer = Developer(**data)
        db.session.add(developer)
        db.session.commit()
        
        flash('Developer created successfully!', 'success')
        return redirect(url_for('admin.developers'))
    
    return render_template('admin/developers/new.html')

@admin.route('/developers/<int:developer_id>')
def view_developer(developer_id):
    """View developer details"""
    developer = Developer.query.get_or_404(developer_id)
    return render_template('admin/developers/view.html', developer=developer)

@admin.route('/developers/<int:developer_id>/edit', methods=['GET', 'POST'])
def edit_developer(developer_id):
    """Edit developer"""
    developer = Developer.query.get_or_404(developer_id)
    
    if request.method == 'POST':
        data = request.form.to_dict()
        
        # Handle logo upload
        if 'logo' in request.files:
            file = request.files['logo']
            if file and file.filename:
                filename = secure_filename(file.filename)
                file.save(os.path.join(current_app.config['UPLOAD_FOLDER'], filename))
                data['logo_url'] = filename
        
        for key, value in data.items():
            if hasattr(developer, key):
                setattr(developer, key, value)
        
        db.session.commit()
        flash('Developer updated successfully!', 'success')
        return redirect(url_for('admin.developers'))
    
    return render_template('admin/developers/edit.html', developer=developer)

@admin.route('/developers/<int:developer_id>/delete', methods=['POST'])
def delete_developer(developer_id):
    """Delete developer"""
    developer = Developer.query.get_or_404(developer_id)
    db.session.delete(developer)
    db.session.commit()
    flash('Developer deleted successfully!', 'success')
    return redirect(url_for('admin.developers'))

# Cities Routes
@admin.route('/cities')
def cities():
    """List all cities"""
    page = request.args.get('page', 1, type=int)
    search = request.args.get('search', '')
    
    query = City.query
    
    if search:
        query = query.filter(City.name.ilike(f'%{search}%'))
    
    cities = query.order_by(City.name).paginate(
        page=page, per_page=10, error_out=False
    )
    
    return render_template('admin/cities/index.html', cities=cities, search=search)

@admin.route('/cities/new', methods=['GET', 'POST'])
def new_city():
    """Create new city"""
    if request.method == 'POST':
        data = request.form.to_dict()
        city = City(**data)
        db.session.add(city)
        db.session.commit()
        flash('City created successfully!', 'success')
        return redirect(url_for('admin.cities'))
    
    return render_template('admin/cities/new.html')

@admin.route('/cities/<int:city_id>/edit', methods=['GET', 'POST'])
def edit_city(city_id):
    """Edit city"""
    city = City.query.get_or_404(city_id)
    
    if request.method == 'POST':
        data = request.form.to_dict()
        for key, value in data.items():
            if hasattr(city, key):
                setattr(city, key, value)
        
        db.session.commit()
        flash('City updated successfully!', 'success')
        return redirect(url_for('admin.cities'))
    
    return render_template('admin/cities/edit.html', city=city)

@admin.route('/cities/<int:city_id>/delete', methods=['POST'])
def delete_city(city_id):
    """Delete city"""
    city = City.query.get_or_404(city_id)
    db.session.delete(city)
    db.session.commit()
    flash('City deleted successfully!', 'success')
    return redirect(url_for('admin.cities'))

@admin.route('/cities/<int:city_id>')
def view_city(city_id):
    city = City.query.get_or_404(city_id)
    return render_template('admin/cities/view.html', city=city)

# Amenities Routes
@admin.route('/amenities')
def amenities():
    """List all amenities"""
    page = request.args.get('page', 1, type=int)
    search = request.args.get('search', '')
    
    query = Amenity.query
    
    if search:
        query = query.filter(Amenity.name.ilike(f'%{search}%'))
    
    amenities = query.order_by(Amenity.name).paginate(
        page=page, per_page=10, error_out=False
    )
    
    return render_template('admin/amenities/index.html', amenities=amenities, search=search)

@admin.route('/amenities/new', methods=['GET', 'POST'])
def new_amenity():
    """Create new amenity"""
    if request.method == 'POST':
        data = request.form.to_dict()
        data['is_active'] = 'is_active' in request.form
        data['is_rare'] = 'is_rare' in request.form
        amenity = Amenity(**data)
        db.session.add(amenity)
        db.session.commit()
        flash('Amenity created successfully!', 'success')
        return redirect(url_for('admin.amenities'))
    
    return render_template('admin/amenities/new.html')

@admin.route('/amenities/<int:amenity_id>/edit', methods=['GET', 'POST'])
def edit_amenity(amenity_id):
    """Edit amenity"""
    amenity = Amenity.query.get_or_404(amenity_id)
    
    if request.method == 'POST':
        data = request.form.to_dict()
        data['is_active'] = 'is_active' in request.form
        data['is_rare'] = 'is_rare' in request.form
        for key, value in data.items():
            if key in ['is_active', 'is_rare']:
                setattr(amenity, key, value)
            elif hasattr(amenity, key):
                setattr(amenity, key, value)
        db.session.commit()
        flash('Amenity updated successfully!', 'success')
        return redirect(url_for('admin.amenities'))
    
    return render_template('admin/amenities/edit.html', amenity=amenity)

@admin.route('/amenities/<int:amenity_id>/delete', methods=['POST'])
def delete_amenity(amenity_id):
    """Delete amenity"""
    amenity = Amenity.query.get_or_404(amenity_id)
    db.session.delete(amenity)
    db.session.commit()
    flash('Amenity deleted successfully!', 'success')
    return redirect(url_for('admin.amenities'))

@admin.route('/amenities/<int:amenity_id>')
def view_amenity(amenity_id):
    amenity = Amenity.query.get_or_404(amenity_id)
    return render_template('admin/amenities/view.html', amenity=amenity)

# Approvals Routes
@admin.route('/approvals')
def approvals():
    """List all approvals"""
    page = request.args.get('page', 1, type=int)
    category = request.args.get('category', '')
    
    query = Approval.query
    
    if category:
        query = query.filter(Approval.category == category)
    
    approvals = query.order_by(Approval.approval_id.desc()).paginate(
        page=page, per_page=10, error_out=False
    )
    
    return render_template('admin/approvals/index.html', approvals=approvals, category=category)

@admin.route('/approvals/new', methods=['GET', 'POST'])
def new_approval():
    """Create new approval"""
    if request.method == 'POST':
        data = request.form.to_dict()
        data['is_mandatory'] = 'is_mandatory' in request.form
        approval = Approval(**data)
        db.session.add(approval)
        db.session.commit()
        flash('Approval created successfully!', 'success')
        return redirect(url_for('admin.approvals'))
    
    return render_template('admin/approvals/new.html')

@admin.route('/approvals/<int:approval_id>/edit', methods=['GET', 'POST'])
def edit_approval(approval_id):
    """Edit approval"""
    approval = Approval.query.get_or_404(approval_id)
    
    if request.method == 'POST':
        data = request.form.to_dict()
        data['is_mandatory'] = 'is_mandatory' in request.form
        for key, value in data.items():
            if hasattr(approval, key):
                setattr(approval, key, value)
        
        db.session.commit()
        flash('Approval updated successfully!', 'success')
        return redirect(url_for('admin.approvals'))
    
    return render_template('admin/approvals/edit.html', approval=approval)

@admin.route('/approvals/<int:approval_id>/delete', methods=['POST'])
def delete_approval(approval_id):
    """Delete approval"""
    approval = Approval.query.get_or_404(approval_id)
    db.session.delete(approval)
    db.session.commit()
    flash('Approval deleted successfully!', 'success')
    return redirect(url_for('admin.approvals'))

@admin.route('/approvals/<int:approval_id>')
def view_approval(approval_id):
    approval = Approval.query.get_or_404(approval_id)
    return render_template('admin/approvals/view.html', approval=approval)

# Towers Routes
@admin.route('/towers')
def towers():
    """List all towers"""
    page = request.args.get('page', 1, type=int)
    search = request.args.get('search', '')
    
    query = Tower.query
    
    if search:
        query = query.filter(Tower.name.ilike(f'%{search}%'))
    
    towers = query.order_by(Tower.created_at.desc()).paginate(
        page=page, per_page=10, error_out=False
    )
    
    return render_template('admin/towers/index.html', towers=towers, search=search)

@admin.route('/towers/new', methods=['GET', 'POST'])
def new_tower():
    """Create new tower"""
    if request.method == 'POST':
        data = request.form.to_dict()
        # Convert project_id to int
        data['project_id'] = int(data['project_id']) if data.get('project_id') else None
        # Convert booleans
        for field in ['has_power_backup', 'has_water_backup', 'has_fire_safety', 'is_active']:
            data[field] = field in request.form
        tower = Tower(**data)
        db.session.add(tower)
        db.session.commit()
        flash('Tower created successfully!', 'success')
        return redirect(url_for('admin.towers'))
    
    projects = Project.query.all()
    return render_template('admin/towers/new.html', projects=projects)

@admin.route('/towers/<int:tower_id>/edit', methods=['GET', 'POST'])
def edit_tower(tower_id):
    """Edit tower"""
    tower = Tower.query.get_or_404(tower_id)
    
    if request.method == 'POST':
        data = request.form.to_dict()
        # Convert project_id to int
        data['project_id'] = int(data['project_id']) if data.get('project_id') else None
        # Convert booleans
        for field in ['has_power_backup', 'has_water_backup', 'has_fire_safety', 'is_active']:
            data[field] = field in request.form
        for key, value in data.items():
            if hasattr(tower, key):
                setattr(tower, key, value)
        db.session.commit()
        flash('Tower updated successfully!', 'success')
        return redirect(url_for('admin.towers'))
    
    projects = Project.query.all()
    return render_template('admin/towers/edit.html', tower=tower, projects=projects)

@admin.route('/towers/<int:tower_id>/delete', methods=['POST'])
def delete_tower(tower_id):
    """Delete tower"""
    tower = Tower.query.get_or_404(tower_id)
    db.session.delete(tower)
    db.session.commit()
    flash('Tower deleted successfully!', 'success')
    return redirect(url_for('admin.towers'))

@admin.route('/towers/<int:tower_id>')
def view_tower(tower_id):
    tower = Tower.query.get_or_404(tower_id)
    return render_template('admin/towers/view.html', tower=tower)

# Users Routes
@admin.route('/users')
def users():
    """List all users"""
    page = request.args.get('page', 1, type=int)
    search = request.args.get('search', '')
    
    query = User.query
    
    if search:
        query = query.filter(User.first_name.ilike(f'%{search}%') | User.last_name.ilike(f'%{search}%'))
    
    users = query.order_by(User.created_at.desc()).paginate(
        page=page, per_page=10, error_out=False
    )
    
    return render_template('admin/users/index.html', users=users, search=search)

@admin.route('/users/new', methods=['GET', 'POST'])
def new_user():
    """Create new user"""
    if request.method == 'POST':
        data = request.form.to_dict()
        user = User(**data)
        db.session.add(user)
        db.session.commit()
        flash('User created successfully!', 'success')
        return redirect(url_for('admin.users'))
    
    return render_template('admin/users/new.html')

@admin.route('/users/<int:user_id>/edit', methods=['GET', 'POST'])
def edit_user(user_id):
    """Edit user"""
    user = User.query.get_or_404(user_id)
    
    if request.method == 'POST':
        data = request.form.to_dict()
        for key, value in data.items():
            if hasattr(user, key):
                setattr(user, key, value)
        
        db.session.commit()
        flash('User updated successfully!', 'success')
        return redirect(url_for('admin.users'))
    
    return render_template('admin/users/edit.html', user=user)

@admin.route('/users/<int:user_id>/delete', methods=['POST'])
def delete_user(user_id):
    """Delete user"""
    user = User.query.get_or_404(user_id)
    db.session.delete(user)
    db.session.commit()
    flash('User deleted successfully!', 'success')
    return redirect(url_for('admin.users'))

@admin.route('/users/<int:user_id>')
def view_user(user_id):
    user = User.query.get_or_404(user_id)
    return render_template('admin/users/view.html', user=user)

# Unit Types Routes
@admin.route('/unit-types')
def unit_types():
    """List all unit types"""
    page = request.args.get('page', 1, type=int)
    search = request.args.get('search', '')
    
    query = UnitType.query
    
    if search:
        query = query.filter(UnitType.name.ilike(f'%{search}%'))
    
    unit_types = query.order_by(UnitType.created_at.desc()).paginate(
        page=page, per_page=10, error_out=False
    )
    
    return render_template('admin/unit_types/index.html', unit_types=unit_types, search=search)

@admin.route('/unit-types/new', methods=['GET', 'POST'])
def new_unit_type():
    """Create new unit type"""
    if request.method == 'POST':
        data = request.form.to_dict()
        unit_type = UnitType(**data)
        db.session.add(unit_type)
        db.session.commit()
        flash('Unit type created successfully!', 'success')
        return redirect(url_for('admin.unit_types'))
    
    projects = Project.query.all()
    return render_template('admin/unit_types/new.html', projects=projects)

@admin.route('/unit-types/<int:unit_type_id>/edit', methods=['GET', 'POST'])
def edit_unit_type(unit_type_id):
    """Edit unit type"""
    unit_type = UnitType.query.get_or_404(unit_type_id)
    
    if request.method == 'POST':
        data = request.form.to_dict()
        for key, value in data.items():
            if hasattr(unit_type, key):
                setattr(unit_type, key, value)
        
        db.session.commit()
        flash('Unit type updated successfully!', 'success')
        return redirect(url_for('admin.unit_types'))
    
    projects = Project.query.all()
    return render_template('admin/unit_types/edit.html', unit_type=unit_type, projects=projects)

@admin.route('/unit-types/<int:unit_type_id>/delete', methods=['POST'])
def delete_unit_type(unit_type_id):
    """Delete unit type"""
    unit_type = UnitType.query.get_or_404(unit_type_id)
    db.session.delete(unit_type)
    db.session.commit()
    flash('Unit type deleted successfully!', 'success')
    return redirect(url_for('admin.unit_types'))

@admin.route('/unit-types/<int:unit_type_id>')
def view_unit_type(unit_type_id):
    unit_type = UnitType.query.get_or_404(unit_type_id)
    return render_template('admin/unit_types/view.html', unit_type=unit_type)

# Property Units Routes
@admin.route('/property-units')
def property_units():
    """List all property units"""
    page = request.args.get('page', 1, type=int)
    search = request.args.get('search', '')
    
    query = PropertyUnit.query
    
    if search:
        query = query.filter(PropertyUnit.unit_number.ilike(f'%{search}%'))
    
    property_units = query.order_by(PropertyUnit.created_at.desc()).paginate(
        page=page, per_page=10, error_out=False
    )
    
    return render_template('admin/property_units/index.html', property_units=property_units, search=search)

@admin.route('/property-units/new', methods=['GET', 'POST'])
def new_property_unit():
    """Create new property unit"""
    if request.method == 'POST':
        data = request.form.to_dict()
        property_unit = PropertyUnit(**data)
        db.session.add(property_unit)
        db.session.commit()
        flash('Property unit created successfully!', 'success')
        return redirect(url_for('admin.property_units'))
    
    projects = Project.query.all()
    towers = Tower.query.all()
    unit_types = UnitType.query.all()
    
    return render_template('admin/property_units/new.html', projects=projects, towers=towers, unit_types=unit_types)

@admin.route('/property-units/<int:unit_id>/edit', methods=['GET', 'POST'])
def edit_property_unit(unit_id):
    """Edit property unit"""
    property_unit = PropertyUnit.query.get_or_404(unit_id)
    
    if request.method == 'POST':
        data = request.form.to_dict()
        for key, value in data.items():
            if hasattr(property_unit, key):
                setattr(property_unit, key, value)
        
        db.session.commit()
        flash('Property unit updated successfully!', 'success')
        return redirect(url_for('admin.property_units'))
    
    projects = Project.query.all()
    towers = Tower.query.all()
    unit_types = UnitType.query.all()
    
    return render_template('admin/property_units/edit.html', property_unit=property_unit, projects=projects, towers=towers, unit_types=unit_types)

@admin.route('/property-units/<int:unit_id>/delete', methods=['POST'])
def delete_property_unit(unit_id):
    """Delete property unit"""
    property_unit = PropertyUnit.query.get_or_404(unit_id)
    db.session.delete(property_unit)
    db.session.commit()
    flash('Property unit deleted successfully!', 'success')
    return redirect(url_for('admin.property_units'))

@admin.route('/property-units/<int:unit_id>')
def view_property_unit(unit_id):
    property_unit = PropertyUnit.query.get_or_404(unit_id)
    return render_template('admin/property_units/view.html', property_unit=property_unit)

# Reviews Routes
@admin.route('/reviews')
def reviews():
    """List all reviews"""
    page = request.args.get('page', 1, type=int)
    rating = request.args.get('rating', '')
    
    query = Review.query
    
    if rating:
        query = query.filter(Review.rating == int(rating))
    
    reviews = query.order_by(Review.created_at.desc()).paginate(
        page=page, per_page=10, error_out=False
    )
    
    return render_template('admin/reviews/index.html', reviews=reviews, rating=rating)

@admin.route('/reviews/new', methods=['GET', 'POST'])
def new_review():
    """Create new review"""
    from app.models import Project, Developer, User, Review
    if request.method == 'POST':
        data = request.form.to_dict()
        data['is_verified'] = 'is_verified' in request.form
        # Convert IDs to int
        for field in ['project_id', 'developer_id', 'user_id', 'rating', 'construction_quality_rating', 'amenities_rating', 'location_rating', 'value_for_money_rating']:
            if data.get(field):
                try:
                    data[field] = int(data[field])
                except Exception:
                    data[field] = None
            else:
                data[field] = None
        review = Review(**data)
        db.session.add(review)
        db.session.commit()
        flash('Review created successfully!', 'success')
        return redirect(url_for('admin.reviews'))
    projects = Project.query.all()
    developers = Developer.query.all()
    users = User.query.all()
    return render_template('admin/reviews/new.html', projects=projects, developers=developers, users=users)

@admin.route('/reviews/<int:review_id>/edit', methods=['GET', 'POST'])
def edit_review(review_id):
    """Edit review"""
    from app.models import Project, Developer, User, Review
    review = Review.query.get_or_404(review_id)
    if request.method == 'POST':
        data = request.form.to_dict()
        data['is_verified'] = 'is_verified' in request.form
        # Convert IDs to int
        for field in ['project_id', 'developer_id', 'user_id', 'rating', 'construction_quality_rating', 'amenities_rating', 'location_rating', 'value_for_money_rating']:
            if data.get(field):
                try:
                    data[field] = int(data[field])
                except Exception:
                    data[field] = None
            else:
                data[field] = None
        for key, value in data.items():
            if hasattr(review, key):
                setattr(review, key, value)
        db.session.commit()
        flash('Review updated successfully!', 'success')
        return redirect(url_for('admin.reviews'))
    projects = Project.query.all()
    developers = Developer.query.all()
    users = User.query.all()
    return render_template('admin/reviews/edit.html', review=review, projects=projects, developers=developers, users=users)

@admin.route('/reviews/<int:review_id>/delete', methods=['POST'])
def delete_review(review_id):
    """Delete review"""
    review = Review.query.get_or_404(review_id)
    db.session.delete(review)
    db.session.commit()
    flash('Review deleted successfully!', 'success')
    return redirect(url_for('admin.reviews'))

@admin.route('/reviews/<int:review_id>')
def view_review(review_id):
    review = Review.query.get_or_404(review_id)
    return render_template('admin/reviews/view.html', review=review)

# Notifications Routes
@admin.route('/notifications')
def notifications():
    """List all notifications"""
    page = request.args.get('page', 1, type=int)
    is_read = request.args.get('is_read', '')
    
    query = Notification.query
    
    if is_read:
        query = query.filter(Notification.is_read == (is_read == 'true'))
    
    notifications = query.order_by(Notification.created_at.desc()).paginate(
        page=page, per_page=10, error_out=False
    )
    
    return render_template('admin/notifications/index.html', notifications=notifications, is_read=is_read)

@admin.route('/notifications/new', methods=['GET', 'POST'])
def new_notification():
    """Create new notification"""
    from app.models import Project, User, Notification
    if request.method == 'POST':
        data = request.form.to_dict()
        # Convert booleans
        data['is_read'] = 'is_read' in request.form
        data['is_sent'] = 'is_sent' in request.form
        # Convert IDs to int
        for field in ['user_id', 'related_project_id']:
            if data.get(field):
                try:
                    data[field] = int(data[field])
                except Exception:
                    data[field] = None
            else:
                data[field] = None
        notification = Notification(**data)
        db.session.add(notification)
        db.session.commit()
        flash('Notification created successfully!', 'success')
        return redirect(url_for('admin.notifications'))
    users = User.query.all()
    projects = Project.query.all()
    return render_template('admin/notifications/new.html', users=users, projects=projects)

@admin.route('/notifications/<int:notification_id>/edit', methods=['GET', 'POST'])
def edit_notification(notification_id):
    """Edit notification"""
    from app.models import Project, User, Notification
    notification = Notification.query.get_or_404(notification_id)
    if request.method == 'POST':
        data = request.form.to_dict()
        # Convert booleans
        data['is_read'] = 'is_read' in request.form
        data['is_sent'] = 'is_sent' in request.form
        # Convert IDs to int
        for field in ['user_id', 'related_project_id']:
            if data.get(field):
                try:
                    data[field] = int(data[field])
                except Exception:
                    data[field] = None
            else:
                data[field] = None
        for key, value in data.items():
            if hasattr(notification, key):
                setattr(notification, key, value)
        db.session.commit()
        flash('Notification updated successfully!', 'success')
        return redirect(url_for('admin.notifications'))
    users = User.query.all()
    projects = Project.query.all()
    return render_template('admin/notifications/edit.html', notification=notification, users=users, projects=projects)

@admin.route('/notifications/<int:notification_id>/delete', methods=['POST'])
def delete_notification(notification_id):
    """Delete notification"""
    notification = Notification.query.get_or_404(notification_id)
    db.session.delete(notification)
    db.session.commit()
    flash('Notification deleted successfully!', 'success')
    return redirect(url_for('admin.notifications'))

@admin.route('/notifications/<int:notification_id>')
def view_notification(notification_id):
    notification = Notification.query.get_or_404(notification_id)
    return render_template('admin/notifications/view.html', notification=notification)

# Media Routes
@admin.route('/media')
def media():
    """List all media"""
    page = request.args.get('page', 1, type=int)
    media_type = request.args.get('type', '')
    
    query = ProjectMedia.query
    
    if media_type:
        query = query.filter(ProjectMedia.media_type == media_type)
    
    media = query.order_by(ProjectMedia.created_at.desc()).paginate(
        page=page, per_page=12, error_out=False
    )
    
    return render_template('admin/media/index.html', media=media, media_type=media_type)

@admin.route('/media/new', methods=['GET', 'POST'])
def new_media():
    """Upload new media"""
    if request.method == 'POST':
        data = request.form.to_dict()
        # Convert is_active checkbox to boolean
        data['is_active'] = 'is_active' in request.form
        # Convert project_id to int if present
        if data.get('project_id'):
            try:
                data['project_id'] = int(data['project_id'])
            except Exception:
                data['project_id'] = None
        else:
            data['project_id'] = None
        # Handle file upload for media_url
        if 'media_url' in request.files:
            file = request.files['media_url']
            if file and file.filename:
                filename = secure_filename(file.filename)
                file.save(os.path.join(current_app.config['UPLOAD_FOLDER'], filename))
                data['media_url'] = filename
            else:
                data['media_url'] = None
        media = ProjectMedia(**data)
        db.session.add(media)
        db.session.commit()
        flash('Media uploaded successfully!', 'success')
        return redirect(url_for('admin.media'))
    projects = Project.query.all()
    return render_template('admin/media/new.html', projects=projects)

@admin.route('/media/<int:media_id>/edit', methods=['GET', 'POST'])
def edit_media(media_id):
    """Edit media"""
    media = ProjectMedia.query.get_or_404(media_id)
    if request.method == 'POST':
        data = request.form.to_dict()
        # Convert is_active checkbox to boolean
        data['is_active'] = 'is_active' in request.form
        # Convert project_id to int if present
        if data.get('project_id'):
            try:
                data['project_id'] = int(data['project_id'])
            except Exception:
                data['project_id'] = None
        else:
            data['project_id'] = None
        # Handle file upload for media_url (optional)
        if 'media_url' in request.files:
            file = request.files['media_url']
            if file and file.filename:
                filename = secure_filename(file.filename)
                file.save(os.path.join(current_app.config['UPLOAD_FOLDER'], filename))
                data['media_url'] = filename
            else:
                data['media_url'] = media.media_url  # keep current file if blank
        else:
            data['media_url'] = media.media_url
        # Update all fields
        for key, value in data.items():
            if hasattr(media, key):
                setattr(media, key, value)
        db.session.commit()
        flash('Media updated successfully!', 'success')
        return redirect(url_for('admin.media'))
    projects = Project.query.all()
    return render_template('admin/media/edit.html', media=media, projects=projects)

@admin.route('/media/<int:media_id>/delete', methods=['POST'])
def delete_media(media_id):
    """Delete media"""
    media = ProjectMedia.query.get_or_404(media_id)
    db.session.delete(media)
    db.session.commit()
    flash('Media deleted successfully!', 'success')
    return redirect(url_for('admin.media'))

@admin.route('/media/<int:media_id>')
def view_media(media_id):
    media = ProjectMedia.query.get_or_404(media_id)
    return render_template('admin/media/view.html', media=media)

# Documents Routes
@admin.route('/documents')
def documents():
    """List all documents"""
    page = request.args.get('page', 1, type=int)
    doc_type = request.args.get('type', '')
    
    query = ProjectDocument.query
    
    if doc_type:
        query = query.filter(ProjectDocument.document_type == doc_type)
    
    documents = query.order_by(ProjectDocument.created_at.desc()).paginate(
        page=page, per_page=10, error_out=False
    )
    
    return render_template('admin/documents/index.html', documents=documents, doc_type=doc_type)

@admin.route('/documents/new', methods=['GET', 'POST'])
def new_document():
    """Upload new document"""
    if request.method == 'POST':
        data = request.form.to_dict()
        # Convert is_public checkbox to boolean
        data['is_public'] = 'is_public' in request.form
        # Convert project_id to int if present
        if data.get('project_id'):
            try:
                data['project_id'] = int(data['project_id'])
            except Exception:
                data['project_id'] = None
        else:
            data['project_id'] = None
        # Handle file upload for file_url, file_size, file_type
        if 'file_url' in request.files:
            file = request.files['file_url']
            if file and file.filename:
                filename = secure_filename(file.filename)
                file.save(os.path.join(current_app.config['UPLOAD_FOLDER'], filename))
                data['file_url'] = filename
                data['file_size'] = file.content_length or os.path.getsize(os.path.join(current_app.config['UPLOAD_FOLDER'], filename))
                data['file_type'] = file.mimetype
            else:
                data['file_url'] = None
                data['file_size'] = None
                data['file_type'] = None
        else:
            data['file_url'] = None
            data['file_size'] = None
            data['file_type'] = None
        # Ensure file_size is int or None
        try:
            if data.get('file_size') in [None, '', 'None']:
                data['file_size'] = None
            else:
                data['file_size'] = int(data['file_size'])
        except Exception:
            data['file_size'] = None
        # Ensure download_count is int or 0
        try:
            if data.get('download_count') in [None, '', 'None']:
                data['download_count'] = 0
            else:
                data['download_count'] = int(data['download_count'])
        except Exception:
            data['download_count'] = 0
        document = ProjectDocument(**data)
        db.session.add(document)
        db.session.commit()
        flash('Document uploaded successfully!', 'success')
        return redirect(url_for('admin.documents'))
    projects = Project.query.all()
    return render_template('admin/documents/new.html', projects=projects)

@admin.route('/documents/<int:document_id>/edit', methods=['GET', 'POST'])
def edit_document(document_id):
    """Edit document"""
    document = ProjectDocument.query.get_or_404(document_id)
    if request.method == 'POST':
        data = request.form.to_dict()
        # Convert is_public checkbox to boolean
        data['is_public'] = 'is_public' in request.form
        # Convert project_id to int if present
        if data.get('project_id'):
            try:
                data['project_id'] = int(data['project_id'])
            except Exception:
                data['project_id'] = None
        else:
            data['project_id'] = None
        # Handle file upload for file_url, file_size, file_type (optional)
        if 'file_url' in request.files:
            file = request.files['file_url']
            if file and file.filename:
                filename = secure_filename(file.filename)
                file.save(os.path.join(current_app.config['UPLOAD_FOLDER'], filename))
                data['file_url'] = filename
                data['file_size'] = file.content_length or os.path.getsize(os.path.join(current_app.config['UPLOAD_FOLDER'], filename))
                data['file_type'] = file.mimetype
            else:
                data['file_url'] = document.file_url
                data['file_size'] = document.file_size
                data['file_type'] = document.file_type
        else:
            data['file_url'] = document.file_url
            data['file_size'] = document.file_size
            data['file_type'] = document.file_type
        # Ensure file_size is int or None
        try:
            if data.get('file_size') in [None, '', 'None']:
                data['file_size'] = None
            else:
                data['file_size'] = int(data['file_size'])
        except Exception:
            data['file_size'] = None
        # Ensure download_count is int or 0
        try:
            if data.get('download_count') in [None, '', 'None']:
                data['download_count'] = 0
            else:
                data['download_count'] = int(data['download_count'])
        except Exception:
            data['download_count'] = 0
        # Update all fields
        for key, value in data.items():
            if hasattr(document, key):
                setattr(document, key, value)
        db.session.commit()
        flash('Document updated successfully!', 'success')
        return redirect(url_for('admin.documents'))
    projects = Project.query.all()
    return render_template('admin/documents/edit.html', document=document, projects=projects)

@admin.route('/documents/<int:document_id>/delete', methods=['POST'])
def delete_document(document_id):
    """Delete document"""
    document = ProjectDocument.query.get_or_404(document_id)
    db.session.delete(document)
    db.session.commit()
    flash('Document deleted successfully!', 'success')
    return redirect(url_for('admin.documents'))

@admin.route('/documents/<int:document_id>')
def view_document(document_id):
    document = ProjectDocument.query.get_or_404(document_id)
    return render_template('admin/documents/view.html', document=document)

@admin.route('/documents/export/<export_type>')
def export_documents(export_type):
    """Export documents data as CSV, Excel, or PDF"""
    import pandas as pd
    from io import BytesIO, StringIO
    documents = ProjectDocument.query.all()
    data = []
    for d in documents:
        data.append({
            'ID': d.document_id,
            'Project': d.project.name if d.project else '',
            'Title': d.title or '',
            'Description': d.description or '',
            'File Name': d.file_name or '',
            'File Type': d.file_type or '',
            'File Size': d.file_size or '',
            'Download Count': d.download_count or 0,
            'Is Public': 'Yes' if d.is_public else 'No',
            'Created': d.created_at.strftime('%Y-%m-%d') if d.created_at else '',
        })
    df = pd.DataFrame(data)
    if export_type == 'csv':
        output = StringIO()
        df.to_csv(output, index=False)
        output.seek(0)
        return send_file(BytesIO(output.getvalue().encode()), mimetype='text/csv', as_attachment=True, download_name='documents.csv')
    elif export_type == 'excel':
        output = BytesIO()
        with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
            df.to_excel(writer, index=False, sheet_name='Documents')
        output.seek(0)
        return send_file(output, mimetype='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet', as_attachment=True, download_name='documents.xlsx')
    elif export_type == 'pdf':
        if not PDFKIT_AVAILABLE:
            flash('PDF export is not available. Please install pdfkit.', 'danger')
            return redirect(url_for('admin.documents'))
        html = df.to_html(index=False)
        pdf = pdfkit.from_string(html, False)
        return send_file(BytesIO(pdf), mimetype='application/pdf', as_attachment=True, download_name='documents.pdf')
    else:
        flash('Invalid export type.', 'danger')
        return redirect(url_for('admin.documents'))

 
@admin.route('/projects/export/<string:export_type>')
def export_projects(export_type):
    # Query all projects (no pagination)
    projects = Project.query.order_by(Project.created_at.desc()).all()
    data = []
    for p in projects:
        data.append({
            'Name': p.name,
            'Developer': p.developer.name if p.developer else '',
            'Type': p.property_type,
            'Status': p.status,
            'Location': (p.locality.name + (', ' + p.locality.city.name if p.locality and p.locality.city else '')) if p.locality else '',
            'Price Range': f"{p.min_price or ''} - {p.max_price or ''}",
            'Units': p.total_units,
            'Created': p.created_at.strftime('%Y-%m-%d') if p.created_at else ''
        })
    df = pd.DataFrame(data)
    if export_type == 'excel':
        output = io.BytesIO()
        with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
            df.to_excel(writer, index=False)
        output.seek(0)
        return send_file(output, as_attachment=True, download_name='projects.xlsx', mimetype='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    elif export_type == 'csv':
        output = io.StringIO()
        df.to_csv(output, index=False)
        output.seek(0)
        return send_file(io.BytesIO(output.getvalue().encode()), as_attachment=True, download_name='projects.csv', mimetype='text/csv')
    elif export_type == 'pdf':
        if not PDFKIT_AVAILABLE:
            return 'PDF export requires pdfkit and wkhtmltopdf installed.', 501
        # Render a simple HTML table for PDF
        html = '<h2>Projects List</h2>' + df.to_html(index=False, border=0)
        pdf = pdfkit.from_string(html, False)
        response = make_response(pdf)
        response.headers['Content-Type'] = 'application/pdf'
        response.headers['Content-Disposition'] = 'attachment; filename=projects.pdf'
        return response
    else:
        return 'Invalid export type', 400

 
@admin.route('/developers/export/<string:export_type>')
def export_developers(export_type):
    # Query all developers (no pagination)
    developers = Developer.query.order_by(Developer.created_at.desc()).all()
    data = []
    for d in developers:
        data.append({
            'Name': d.name,
            'Established Year': d.established_year or '',
            'Email': d.contact_email or '',
            'Phone': d.contact_phone or '',
            'Website': d.website_url or '',
            'Address': d.address or '',
            'Total Projects': d.total_projects or 0,
            'Completed Projects': d.completed_projects or 0,
            'Ongoing Projects': d.ongoing_projects or 0,
            'Rating': d.rating or '',
            'Total Reviews': d.total_reviews or 0,
            'Verified': 'Yes' if d.is_verified else 'No',
            'Created': d.created_at.strftime('%Y-%m-%d') if d.created_at else ''
        })
    df = pd.DataFrame(data)
    if export_type == 'excel':
        output = io.BytesIO()
        with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
            df.to_excel(writer, index=False)
        output.seek(0)
        return send_file(output, as_attachment=True, download_name='developers.xlsx', mimetype='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    elif export_type == 'csv':
        output = io.StringIO()
        df.to_csv(output, index=False)
        output.seek(0)
        return send_file(io.BytesIO(output.getvalue().encode()), as_attachment=True, download_name='developers.csv', mimetype='text/csv')
    elif export_type == 'pdf':
        if not PDFKIT_AVAILABLE:
            return 'PDF export requires pdfkit and wkhtmltopdf installed.', 501
        html = '<h2>Developers List</h2>' + df.to_html(index=False, border=0)
        pdf = pdfkit.from_string(html, False)
        response = make_response(pdf)
        response.headers['Content-Type'] = 'application/pdf'
        response.headers['Content-Disposition'] = 'attachment; filename=developers.pdf'
        return response
    else:
        return 'Invalid export type', 400

 
@admin.route('/cities/export/<string:export_type>')
def export_cities(export_type):
    cities = City.query.order_by(City.name).all()
    data = []
    for c in cities:
        data.append({
            'City Name': c.name,
            'State': c.state,
            'Country': c.country,
            'Created': c.created_at.strftime('%Y-%m-%d') if c.created_at else ''
        })
    df = pd.DataFrame(data)
    if export_type == 'excel':
        output = io.BytesIO()
        with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
            df.to_excel(writer, index=False)
        output.seek(0)
        return send_file(output, as_attachment=True, download_name='cities.xlsx', mimetype='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    elif export_type == 'csv':
        output = io.StringIO()
        df.to_csv(output, index=False)
        output.seek(0)
        return send_file(io.BytesIO(output.getvalue().encode()), as_attachment=True, download_name='cities.csv', mimetype='text/csv')
    elif export_type == 'pdf':
        if not PDFKIT_AVAILABLE:
            return 'PDF export requires pdfkit and wkhtmltopdf installed.', 501
        html = '<h2>Cities List</h2>' + df.to_html(index=False, border=0)
        pdf = pdfkit.from_string(html, False)
        response = make_response(pdf)
        response.headers['Content-Type'] = 'application/pdf'
        response.headers['Content-Disposition'] = 'attachment; filename=cities.pdf'
        return response
    else:
        return 'Invalid export type', 400

 
@admin.route('/amenities/export/<string:export_type>')
def export_amenities(export_type):
    amenities = Amenity.query.order_by(Amenity.name).all()
    data = []
    for a in amenities:
        data.append({
            'Amenity Name': a.name,
            'Category': a.category,
            'Description': a.description or '',
            'Icon': a.icon_url or '',
            'Status': 'Active' if a.is_active else 'Inactive',
            'Created': a.created_at.strftime('%Y-%m-%d') if a.created_at else ''
        })
    df = pd.DataFrame(data)
    if export_type == 'excel':
        output = io.BytesIO()
        with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
            df.to_excel(writer, index=False)
        output.seek(0)
        return send_file(output, as_attachment=True, download_name='amenities.xlsx', mimetype='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    elif export_type == 'csv':
        output = io.StringIO()
        df.to_csv(output, index=False)
        output.seek(0)
        return send_file(io.BytesIO(output.getvalue().encode()), as_attachment=True, download_name='amenities.csv', mimetype='text/csv')
    elif export_type == 'pdf':
        if not PDFKIT_AVAILABLE:
            return 'PDF export requires pdfkit and wkhtmltopdf installed.', 501
        html = '<h2>Amenities List</h2>' + df.to_html(index=False, border=0)
        pdf = pdfkit.from_string(html, False)
        response = make_response(pdf)
        response.headers['Content-Type'] = 'application/pdf'
        response.headers['Content-Disposition'] = 'attachment; filename=amenities.pdf'
        return response
    else:
        return 'Invalid export type', 400

 
@admin.route('/approvals/export/<export_type>')
def export_approvals(export_type):
    """Export approvals data as CSV, Excel, or PDF"""
    import pandas as pd
    from io import BytesIO, StringIO
    approvals = Approval.query.all()
    data = []
    for approval in approvals:
        data.append({
            'ID': approval.approval_id,
            'Project': approval.project.name if approval.project else '',
            'Type': approval.approval_type or '',
            'Title': approval.title or '',
            'Description': approval.description or '',
            'Status': approval.status or '',
            'Issued By': approval.issued_by or '',
            'Issued Date': approval.issued_date.strftime('%Y-%m-%d') if approval.issued_date else '',
            'Expiry Date': approval.expiry_date.strftime('%Y-%m-%d') if approval.expiry_date else '',
            'Active': 'Yes' if approval.is_active else 'No',
            'Created': approval.created_at.strftime('%Y-%m-%d') if approval.created_at else '',
        })
    df = pd.DataFrame(data)
    if export_type == 'csv':
        output = StringIO()
        df.to_csv(output, index=False)
        output.seek(0)
        return send_file(BytesIO(output.getvalue().encode()), mimetype='text/csv', as_attachment=True, download_name='approvals.csv')
    elif export_type == 'excel':
        output = BytesIO()
        with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
            df.to_excel(writer, index=False, sheet_name='Approvals')
        output.seek(0)
        return send_file(output, mimetype='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet', as_attachment=True, download_name='approvals.xlsx')
    elif export_type == 'pdf':
        # Optional: implement PDF export if pdfkit is available
        if not PDFKIT_AVAILABLE:
            flash('PDF export is not available. Please install pdfkit.', 'danger')
            return redirect(url_for('admin.approvals'))
        html = df.to_html(index=False)
        pdf = pdfkit.from_string(html, False)
        return send_file(BytesIO(pdf), mimetype='application/pdf', as_attachment=True, download_name='approvals.pdf')
    else:
        flash('Invalid export type.', 'danger')
        return redirect(url_for('admin.approvals'))

 
@admin.route('/towers/export/<export_type>')
def export_towers(export_type):
    """Export towers data as CSV, Excel, or PDF"""
    import pandas as pd
    from io import BytesIO, StringIO
    towers = Tower.query.all()
    data = []
    for tower in towers:
        data.append({
            'ID': tower.tower_id,
            'Project': tower.project.name if tower.project else '',
            'Name': tower.name or '',
            'Floors': tower.floors or '',
            'Units': tower.units or '',
            'Has Power Backup': 'Yes' if tower.has_power_backup else 'No',
            'Has Water Backup': 'Yes' if tower.has_water_backup else 'No',
            'Has Fire Safety': 'Yes' if tower.has_fire_safety else 'No',
            'Active': 'Yes' if tower.is_active else 'No',
            'Created': tower.created_at.strftime('%Y-%m-%d') if tower.created_at else '',
        })
    df = pd.DataFrame(data)
    if export_type == 'csv':
        output = StringIO()
        df.to_csv(output, index=False)
        output.seek(0)
        return send_file(BytesIO(output.getvalue().encode()), mimetype='text/csv', as_attachment=True, download_name='towers.csv')
    elif export_type == 'excel':
        output = BytesIO()
        with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
            df.to_excel(writer, index=False, sheet_name='Towers')
        output.seek(0)
        return send_file(output, mimetype='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet', as_attachment=True, download_name='towers.xlsx')
    elif export_type == 'pdf':
        if not PDFKIT_AVAILABLE:
            flash('PDF export is not available. Please install pdfkit.', 'danger')
            return redirect(url_for('admin.towers'))
        html = df.to_html(index=False)
        pdf = pdfkit.from_string(html, False)
        return send_file(BytesIO(pdf), mimetype='application/pdf', as_attachment=True, download_name='towers.pdf')
    else:
        flash('Invalid export type.', 'danger')
        return redirect(url_for('admin.towers'))

 
@admin.route('/users/export/<export_type>')
def export_users(export_type):
    """Export users data as CSV, Excel, or PDF"""
    import pandas as pd
    from io import BytesIO, StringIO
    users = User.query.all()
    data = []
    for user in users:
        data.append({
            'ID': user.user_id,
            'First Name': user.first_name or '',
            'Last Name': user.last_name or '',
            'Full Name': user.full_name,
            'Email': user.email,
            'Phone': user.phone or '',
            'Role': 'Admin' if user.is_admin else 'User',
            'Active': 'Yes' if user.is_active else 'No',
            'Created': user.created_at.strftime('%Y-%m-%d') if user.created_at else '',
        })
    df = pd.DataFrame(data)
    if export_type == 'csv':
        output = StringIO()
        df.to_csv(output, index=False)
        output.seek(0)
        return send_file(BytesIO(output.getvalue().encode()), mimetype='text/csv', as_attachment=True, download_name='users.csv')
    elif export_type == 'excel':
        output = BytesIO()
        with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
            df.to_excel(writer, index=False, sheet_name='Users')
        output.seek(0)
        return send_file(output, mimetype='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet', as_attachment=True, download_name='users.xlsx')
    elif export_type == 'pdf':
        if not PDFKIT_AVAILABLE:
            flash('PDF export is not available. Please install pdfkit.', 'danger')
            return redirect(url_for('admin.users'))
        html = df.to_html(index=False)
        pdf = pdfkit.from_string(html, False)
        return send_file(BytesIO(pdf), mimetype='application/pdf', as_attachment=True, download_name='users.pdf')
    else:
        flash('Invalid export type.', 'danger')
        return redirect(url_for('admin.users'))

 
@admin.route('/unit-types/export/<export_type>')
def export_unit_types(export_type):
    """Export unit types data as CSV, Excel, or PDF"""
    import pandas as pd
    from io import BytesIO, StringIO
    unit_types = UnitType.query.all()
    data = []
    for unit_type in unit_types:
        data.append({
            'ID': unit_type.unit_type_id,
            'Name': unit_type.name or '',
            'Category': unit_type.category or '',
            'Area (sqft)': unit_type.area_sqft or '',
            'Beds': unit_type.beds or '',
            'Baths': unit_type.baths or '',
            'Active': 'Yes' if unit_type.is_active else 'No',
            'Created': unit_type.created_at.strftime('%Y-%m-%d') if unit_type.created_at else '',
        })
    df = pd.DataFrame(data)
    if export_type == 'csv':
        output = StringIO()
        df.to_csv(output, index=False)
        output.seek(0)
        return send_file(BytesIO(output.getvalue().encode()), mimetype='text/csv', as_attachment=True, download_name='unit_types.csv')
    elif export_type == 'excel':
        output = BytesIO()
        with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
            df.to_excel(writer, index=False, sheet_name='UnitTypes')
        output.seek(0)
        return send_file(output, mimetype='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet', as_attachment=True, download_name='unit_types.xlsx')
    elif export_type == 'pdf':
        if not PDFKIT_AVAILABLE:
            flash('PDF export is not available. Please install pdfkit.', 'danger')
            return redirect(url_for('admin.unit_types'))
        html = df.to_html(index=False)
        pdf = pdfkit.from_string(html, False)
        return send_file(BytesIO(pdf), mimetype='application/pdf', as_attachment=True, download_name='unit_types.pdf')
    else:
        flash('Invalid export type.', 'danger')
        return redirect(url_for('admin.unit_types'))

 
@admin.route('/property-units/export/<export_type>')
def export_property_units(export_type):
    """Export property units data as CSV, Excel, or PDF"""
    import pandas as pd
    from io import BytesIO, StringIO
    property_units = PropertyUnit.query.all()
    data = []
    for unit in property_units:
        data.append({
            'ID': unit.unit_id,
            'Project': unit.project.name if unit.project else '',
            'Tower': unit.tower.name if unit.tower else '',
            'Unit Type': unit.unit_type.name if unit.unit_type else '',
            'Unit Number': unit.unit_number or '',
            'Floor': unit.floor or '',
            'Area (sqft)': unit.area_sqft or '',
            'Status': unit.status or '',
            'Active': 'Yes' if unit.is_active else 'No',
            'Created': unit.created_at.strftime('%Y-%m-%d') if unit.created_at else '',
        })
    df = pd.DataFrame(data)
    if export_type == 'csv':
        output = StringIO()
        df.to_csv(output, index=False)
        output.seek(0)
        return send_file(BytesIO(output.getvalue().encode()), mimetype='text/csv', as_attachment=True, download_name='property_units.csv')
    elif export_type == 'excel':
        output = BytesIO()
        with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
            df.to_excel(writer, index=False, sheet_name='PropertyUnits')
        output.seek(0)
        return send_file(output, mimetype='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet', as_attachment=True, download_name='property_units.xlsx')
    elif export_type == 'pdf':
        if not PDFKIT_AVAILABLE:
            flash('PDF export is not available. Please install pdfkit.', 'danger')
            return redirect(url_for('admin.property_units'))
        html = df.to_html(index=False)
        pdf = pdfkit.from_string(html, False)
        return send_file(BytesIO(pdf), mimetype='application/pdf', as_attachment=True, download_name='property_units.pdf')
    else:
        flash('Invalid export type.', 'danger')
        return redirect(url_for('admin.property_units'))

 
@admin.route('/notifications/export/<export_type>')
def export_notifications(export_type):
    """Export notifications data as CSV, Excel, or PDF"""
    import pandas as pd
    from io import BytesIO, StringIO
    notifications = Notification.query.all()
    data = []
    for n in notifications:
        data.append({
            'ID': n.notification_id,
            'User': n.user.full_name if n.user else '',
            'Type': n.type or '',
            'Title': n.title or '',
            'Message': n.message or '',
            'Project': n.related_project.name if n.related_project else '',
            'Read': 'Yes' if n.is_read else 'No',
            'Sent': 'Yes' if n.is_sent else 'No',
            'Created': n.created_at.strftime('%Y-%m-%d') if n.created_at else '',
        })
    df = pd.DataFrame(data)
    if export_type == 'csv':
        output = StringIO()
        df.to_csv(output, index=False)
        output.seek(0)
        return send_file(BytesIO(output.getvalue().encode()), mimetype='text/csv', as_attachment=True, download_name='notifications.csv')
    elif export_type == 'excel':
        output = BytesIO()
        with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
            df.to_excel(writer, index=False, sheet_name='Notifications')
        output.seek(0)
        return send_file(output, mimetype='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet', as_attachment=True, download_name='notifications.xlsx')
    elif export_type == 'pdf':
        if not PDFKIT_AVAILABLE:
            flash('PDF export is not available. Please install pdfkit.', 'danger')
            return redirect(url_for('admin.notifications'))
        html = df.to_html(index=False)
        pdf = pdfkit.from_string(html, False)
        return send_file(BytesIO(pdf), mimetype='application/pdf', as_attachment=True, download_name='notifications.pdf')
    else:
        flash('Invalid export type.', 'danger')
        return redirect(url_for('admin.notifications'))

 
@admin.route('/media/export/<export_type>')
def export_media(export_type):
    """Export media data as CSV, Excel, or PDF"""
    import pandas as pd
    from io import BytesIO, StringIO
    media_items = ProjectMedia.query.all()
    data = []
    for m in media_items:
        data.append({
            'ID': m.media_id,
            'Project': m.project.name if m.project else '',
            'Type': m.media_type or '',
            'Category': m.media_category or '',
            'Title': m.title or '',
            'Description': m.description or '',
            'URL': m.media_url or '',
            'Active': 'Yes' if m.is_active else 'No',
            'Created': m.created_at.strftime('%Y-%m-%d') if m.created_at else '',
        })
    df = pd.DataFrame(data)
    if export_type == 'csv':
        output = StringIO()
        df.to_csv(output, index=False)
        output.seek(0)
        return send_file(BytesIO(output.getvalue().encode()), mimetype='text/csv', as_attachment=True, download_name='media.csv')
    elif export_type == 'excel':
        output = BytesIO()
        with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
            df.to_excel(writer, index=False, sheet_name='Media')
        output.seek(0)
        return send_file(output, mimetype='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet', as_attachment=True, download_name='media.xlsx')
    elif export_type == 'pdf':
        if not PDFKIT_AVAILABLE:
            flash('PDF export is not available. Please install pdfkit.', 'danger')
            return redirect(url_for('admin.media'))
        html = df.to_html(index=False)
        pdf = pdfkit.from_string(html, False)
        return send_file(BytesIO(pdf), mimetype='application/pdf', as_attachment=True, download_name='media.pdf')
    else:
        flash('Invalid export type.', 'danger')
        return redirect(url_for('admin.media'))

# Localities Routes
@admin.route('/localities')
def localities():
    page = request.args.get('page', 1, type=int)
    search = request.args.get('search', '')
    query = Locality.query
    if search:
        query = query.filter(Locality.name.ilike(f'%{search}%'))
    localities = query.order_by(Locality.created_at.desc()).paginate(page=page, per_page=10, error_out=False)
    return render_template('admin/localities/index.html', localities=localities, search=search)

@admin.route('/localities/new', methods=['GET', 'POST'])
def new_locality():
    cities = City.query.all()
    if request.method == 'POST':
        data = request.form.to_dict()
        data['city_id'] = int(data['city_id']) if data.get('city_id') else None
        data['latitude'] = float(data['latitude']) if data.get('latitude') else None
        data['longitude'] = float(data['longitude']) if data.get('longitude') else None
        locality = Locality(**data)
        db.session.add(locality)
        db.session.commit()
        flash('Locality created successfully!', 'success')
        return redirect(url_for('admin.localities'))
    return render_template('admin/localities/new.html', cities=cities)

@admin.route('/localities/<int:locality_id>/edit', methods=['GET', 'POST'])
def edit_locality(locality_id):
    locality = Locality.query.get_or_404(locality_id)
    cities = City.query.all()
    if request.method == 'POST':
        data = request.form.to_dict()
        data['city_id'] = int(data['city_id']) if data.get('city_id') else None
        data['latitude'] = float(data['latitude']) if data.get('latitude') else None
        data['longitude'] = float(data['longitude']) if data.get('longitude') else None
        for key, value in data.items():
            if hasattr(locality, key):
                setattr(locality, key, value)
        db.session.commit()
        flash('Locality updated successfully!', 'success')
        return redirect(url_for('admin.localities'))
    return render_template('admin/localities/edit.html', locality=locality, cities=cities)

@admin.route('/localities/<int:locality_id>')
def view_locality(locality_id):
    locality = Locality.query.get_or_404(locality_id)
    return render_template('admin/localities/view.html', locality=locality)

@admin.route('/localities/<int:locality_id>/delete', methods=['POST'])
def delete_locality(locality_id):
    locality = Locality.query.get_or_404(locality_id)
    db.session.delete(locality)
    db.session.commit()
    flash('Locality deleted successfully!', 'success')
    return redirect(url_for('admin.localities'))

@admin.route('/localities/export/<export_type>')
def export_localities(export_type):
    import pandas as pd
    from io import BytesIO, StringIO
    localities = Locality.query.all()
    data = []
    for l in localities:
        data.append({
            'ID': l.locality_id,
            'Name': l.name,
            'City': l.city.name if l.city else '',
            'Type': l.locality_type or '',
            'Pincode': l.pincode or '',
            'Latitude': l.latitude or '',
            'Longitude': l.longitude or '',
            'Description': l.description or '',
            'Created': l.created_at.strftime('%Y-%m-%d') if l.created_at else ''
        })
    df = pd.DataFrame(data)
    if export_type == 'csv':
        output = StringIO()
        df.to_csv(output, index=False)
        output.seek(0)
        return send_file(BytesIO(output.getvalue().encode()), mimetype='text/csv', as_attachment=True, download_name='localities.csv')
    else:
        flash('Invalid export type.', 'danger')
        return redirect(url_for('admin.localities'))

# Balcony Details Routes
@admin.route('/balcony-details')
def balcony_details():
    page = request.args.get('page', 1, type=int)
    search = request.args.get('search', '')
    query = BalconyDetail.query
    if search:
        query = query.filter(BalconyDetail.balcony_name.ilike(f'%{search}%'))
    balcony_details = query.order_by(BalconyDetail.created_at.desc()).paginate(page=page, per_page=10, error_out=False)
    return render_template('admin/balcony_details/index.html', balcony_details=balcony_details, search=search)

@admin.route('/balcony-details/new', methods=['GET', 'POST'])
def new_balcony_detail():
    from app.models import UnitType
    unit_types = UnitType.query.all()
    if request.method == 'POST':
        data = request.form.to_dict()
        data['unit_type_id'] = int(data['unit_type_id']) if data.get('unit_type_id') else None
        for field in ['balcony_length', 'balcony_width', 'balcony_area']:
            data[field] = float(data[field]) if data.get(field) else None
        for field in ['balcony_sequence']:
            data[field] = int(data[field]) if data.get(field) else None
        for field in ['has_provision_for_washing_machine', 'has_provision_for_drying', 'has_safety_grill']:
            data[field] = field in request.form
        balcony = BalconyDetail(**data)
        db.session.add(balcony)
        db.session.commit()
        flash('Balcony detail created successfully!', 'success')
        return redirect(url_for('admin.balcony_details'))
    return render_template('admin/balcony_details/new.html', unit_types=unit_types)

@admin.route('/balcony-details/<int:balcony_id>/edit', methods=['GET', 'POST'])
def edit_balcony_detail(balcony_id):
    from app.models import UnitType
    balcony = BalconyDetail.query.get_or_404(balcony_id)
    unit_types = UnitType.query.all()
    if request.method == 'POST':
        data = request.form.to_dict()
        data['unit_type_id'] = int(data['unit_type_id']) if data.get('unit_type_id') else None
        for field in ['balcony_length', 'balcony_width', 'balcony_area']:
            data[field] = float(data[field]) if data.get(field) else None
        for field in ['balcony_sequence']:
            data[field] = int(data[field]) if data.get(field) else None
        for field in ['has_provision_for_washing_machine', 'has_provision_for_drying', 'has_safety_grill']:
            data[field] = field in request.form
        for key, value in data.items():
            if hasattr(balcony, key):
                setattr(balcony, key, value)
        db.session.commit()
        flash('Balcony detail updated successfully!', 'success')
        return redirect(url_for('admin.balcony_details'))
    return render_template('admin/balcony_details/edit.html', balcony=balcony, unit_types=unit_types)

@admin.route('/balcony-details/<int:balcony_id>')
def view_balcony_detail(balcony_id):
    balcony = BalconyDetail.query.get_or_404(balcony_id)
    return render_template('admin/balcony_details/view.html', balcony=balcony)

@admin.route('/balcony-details/<int:balcony_id>/delete', methods=['POST'])
def delete_balcony_detail(balcony_id):
    balcony = BalconyDetail.query.get_or_404(balcony_id)
    db.session.delete(balcony)
    db.session.commit()
    flash('Balcony detail deleted successfully!', 'success')
    return redirect(url_for('admin.balcony_details'))

@admin.route('/balcony-details/export/<export_type>')
def export_balcony_details(export_type):
    import pandas as pd
    from io import BytesIO, StringIO
    balcony_details = BalconyDetail.query.all()
    data = []
    for b in balcony_details:
        data.append({
            'ID': b.balcony_id,
            'Unit Type': b.unit_type.type_name if b.unit_type else '',
            'Name': b.balcony_name or '',
            'Sequence': b.balcony_sequence or '',
            'Length': b.balcony_length or '',
            'Width': b.balcony_width or '',
            'Area': b.balcony_area or '',
            'Connected Room': b.connected_room or '',
            'Access Type': b.access_type or '',
            'Type': b.balcony_type or '',
            'Washing Machine': 'Yes' if b.has_provision_for_washing_machine else 'No',
            'Drying': 'Yes' if b.has_provision_for_drying else 'No',
            'Safety Grill': 'Yes' if b.has_safety_grill else 'No',
            'Facing': b.facing_direction or '',
            'View Description': b.view_description or '',
            'Floor Level': b.floor_level or '',
            'Created': b.created_at.strftime('%Y-%m-%d') if b.created_at else ''
        })
    df = pd.DataFrame(data)
    if export_type == 'csv':
        output = StringIO()
        df.to_csv(output, index=False)
        output.seek(0)
        return send_file(BytesIO(output.getvalue().encode()), mimetype='text/csv', as_attachment=True, download_name='balcony_details.csv')
    else:
        flash('Invalid export type.', 'danger')
        return redirect(url_for('admin.balcony_details'))

# Door/Window Specs Routes
@admin.route('/door-window-specs')
def door_window_specs():
    page = request.args.get('page', 1, type=int)
    search = request.args.get('search', '')
    query = DoorWindowSpec.query
    if search:
        query = query.filter(DoorWindowSpec.item_type.ilike(f'%{search}%'))
    door_window_specs = query.order_by(DoorWindowSpec.created_at.desc()).paginate(page=page, per_page=10, error_out=False)
    return render_template('admin/door_window_specs/index.html', door_window_specs=door_window_specs, search=search)

@admin.route('/door-window-specs/new', methods=['GET', 'POST'])
def new_door_window_spec():
    from app.models import UnitType
    unit_types = UnitType.query.all()
    if request.method == 'POST':
        data = request.form.to_dict()
        data['unit_type_id'] = int(data['unit_type_id']) if data.get('unit_type_id') else None
        for field in ['width', 'height', 'thickness', 'glass_thickness']:
            data[field] = float(data[field]) if data.get(field) else None
        for field in ['is_security_door', 'has_grill']:
            data[field] = field in request.form
        spec = DoorWindowSpec(**data)
        db.session.add(spec)
        db.session.commit()
        flash('Door/Window spec created successfully!', 'success')
        return redirect(url_for('admin.door_window_specs'))
    return render_template('admin/door_window_specs/new.html', unit_types=unit_types)

@admin.route('/door-window-specs/<int:spec_id>/edit', methods=['GET', 'POST'])
def edit_door_window_spec(spec_id):
    from app.models import UnitType
    spec = DoorWindowSpec.query.get_or_404(spec_id)
    unit_types = UnitType.query.all()
    if request.method == 'POST':
        data = request.form.to_dict()
        data['unit_type_id'] = int(data['unit_type_id']) if data.get('unit_type_id') else None
        for field in ['width', 'height', 'thickness', 'glass_thickness']:
            data[field] = float(data[field]) if data.get(field) else None
        for field in ['is_security_door', 'has_grill']:
            data[field] = field in request.form
        for key, value in data.items():
            if hasattr(spec, key):
                setattr(spec, key, value)
        db.session.commit()
        flash('Door/Window spec updated successfully!', 'success')
        return redirect(url_for('admin.door_window_specs'))
    return render_template('admin/door_window_specs/edit.html', spec=spec, unit_types=unit_types)

@admin.route('/door-window-specs/<int:spec_id>')
def view_door_window_spec(spec_id):
    spec = DoorWindowSpec.query.get_or_404(spec_id)
    return render_template('admin/door_window_specs/view.html', spec=spec)

@admin.route('/door-window-specs/<int:spec_id>/delete', methods=['POST'])
def delete_door_window_spec(spec_id):
    spec = DoorWindowSpec.query.get_or_404(spec_id)
    db.session.delete(spec)
    db.session.commit()
    flash('Door/Window spec deleted successfully!', 'success')
    return redirect(url_for('admin.door_window_specs'))

@admin.route('/door-window-specs/export/<export_type>')
def export_door_window_specs(export_type):
    import pandas as pd
    from io import BytesIO, StringIO
    specs = DoorWindowSpec.query.all()
    data = []
    for s in specs:
        data.append({
            'ID': s.spec_id,
            'Unit Type': s.unit_type.type_name if s.unit_type else '',
            'Item Type': s.item_type or '',
            'Location': s.location or '',
            'Width': s.width or '',
            'Height': s.height or '',
            'Thickness': s.thickness or '',
            'Material': s.material or '',
            'Finish': s.finish or '',
            'Brand': s.brand or '',
            'Grade': s.grade or '',
            'Security Door': 'Yes' if s.is_security_door else 'No',
            'Grill': 'Yes' if s.has_grill else 'No',
            'Opening Type': s.opening_type or '',
            'Lock Type': s.lock_type or '',
            'Handle Type': s.handle_type or '',
            'Handle Material': s.handle_material or '',
            'Glass Type': s.glass_type or '',
            'Glass Thickness': s.glass_thickness or '',
            'Created': s.created_at.strftime('%Y-%m-%d') if s.created_at else ''
        })
    df = pd.DataFrame(data)
    if export_type == 'csv':
        output = StringIO()
        df.to_csv(output, index=False)
        output.seek(0)
        return send_file(BytesIO(output.getvalue().encode()), mimetype='text/csv', as_attachment=True, download_name='door_window_specs.csv')
    else:
        flash('Invalid export type.', 'danger')
        return redirect(url_for('admin.door_window_specs'))

# Price History Routes
@admin.route('/price-history')
def price_history():
    page = request.args.get('page', 1, type=int)
    search = request.args.get('search', '')
    query = PriceHistory.query
    if search:
        query = query.filter(PriceHistory.change_reason.ilike(f'%{search}%'))
    price_history = query.order_by(PriceHistory.created_at.desc()).paginate(page=page, per_page=10, error_out=False)
    return render_template('admin/price_history/index.html', price_history=price_history, search=search)

@admin.route('/price-history/new', methods=['GET', 'POST'])
def new_price_history():
    from app.models import Project, UnitType
    projects = Project.query.all()
    unit_types = UnitType.query.all()
    if request.method == 'POST':
        data = request.form.to_dict()
        data['project_id'] = int(data['project_id']) if data.get('project_id') else None
        data['unit_type_id'] = int(data['unit_type_id']) if data.get('unit_type_id') else None
        for field in ['old_price', 'new_price', 'old_price_per_sqft', 'new_price_per_sqft', 'change_percentage']:
            data[field] = float(data[field]) if data.get(field) else None
        for field in ['effective_date']:
            if data.get(field):
                from datetime import datetime
                data[field] = datetime.strptime(data[field], '%Y-%m-%d').date()
            else:
                data[field] = None
        ph = PriceHistory(**data)
        db.session.add(ph)
        db.session.commit()
        flash('Price history record created successfully!', 'success')
        return redirect(url_for('admin.price_history'))
    return render_template('admin/price_history/new.html', projects=projects, unit_types=unit_types)

@admin.route('/price-history/<int:price_history_id>/edit', methods=['GET', 'POST'])
def edit_price_history(price_history_id):
    from app.models import Project, UnitType
    ph = PriceHistory.query.get_or_404(price_history_id)
    projects = Project.query.all()
    unit_types = UnitType.query.all()
    if request.method == 'POST':
        data = request.form.to_dict()
        data['project_id'] = int(data['project_id']) if data.get('project_id') else None
        data['unit_type_id'] = int(data['unit_type_id']) if data.get('unit_type_id') else None
        for field in ['old_price', 'new_price', 'old_price_per_sqft', 'new_price_per_sqft', 'change_percentage']:
            data[field] = float(data[field]) if data.get(field) else None
        for field in ['effective_date']:
            if data.get(field):
                from datetime import datetime
                data[field] = datetime.strptime(data[field], '%Y-%m-%d').date()
            else:
                data[field] = None
        for key, value in data.items():
            if hasattr(ph, key):
                setattr(ph, key, value)
        db.session.commit()
        flash('Price history record updated successfully!', 'success')
        return redirect(url_for('admin.price_history'))
    return render_template('admin/price_history/edit.html', ph=ph, projects=projects, unit_types=unit_types)

@admin.route('/price-history/<int:price_history_id>')
def view_price_history(price_history_id):
    ph = PriceHistory.query.get_or_404(price_history_id)
    return render_template('admin/price_history/view.html', ph=ph)

@admin.route('/price-history/<int:price_history_id>/delete', methods=['POST'])
def delete_price_history(price_history_id):
    ph = PriceHistory.query.get_or_404(price_history_id)
    db.session.delete(ph)
    db.session.commit()
    flash('Price history record deleted successfully!', 'success')
    return redirect(url_for('admin.price_history'))

@admin.route('/price-history/export/<export_type>')
def export_price_history(export_type):
    import pandas as pd
    from io import BytesIO, StringIO
    price_history = PriceHistory.query.all()
    data = []
    for ph in price_history:
        data.append({
            'ID': ph.price_history_id,
            'Project': ph.project.name if ph.project else '',
            'Unit Type': ph.unit_type.type_name if ph.unit_type else '',
            'Old Price': ph.old_price or '',
            'New Price': ph.new_price or '',
            'Old Price/Sqft': ph.old_price_per_sqft or '',
            'New Price/Sqft': ph.new_price_per_sqft or '',
            'Change %': ph.change_percentage or '',
            'Reason': ph.change_reason or '',
            'Effective Date': ph.effective_date.strftime('%Y-%m-%d') if ph.effective_date else '',
            'Created': ph.created_at.strftime('%Y-%m-%d') if ph.created_at else ''
        })
    df = pd.DataFrame(data)
    if export_type == 'csv':
        output = StringIO()
        df.to_csv(output, index=False)
        output.seek(0)
        return send_file(BytesIO(output.getvalue().encode()), mimetype='text/csv', as_attachment=True, download_name='price_history.csv')
    else:
        flash('Invalid export type.', 'danger')
        return redirect(url_for('admin.price_history'))

@admin.route('/project-amenities')
def project_amenities():
    page = request.args.get('page', 1, type=int)
    search = request.args.get('search', '')
    query = ProjectAmenity.query
    if search:
        query = query.join(Project).join(Amenity).filter(
            (Project.name.ilike(f'%{search}%')) |
            (Amenity.name.ilike(f'%{search}%')) |
            (ProjectAmenity.description.ilike(f'%{search}%'))
        )
    project_amenities = query.order_by(ProjectAmenity.created_at.desc()).paginate(page=page, per_page=10, error_out=False)
    return render_template('admin/project_amenities/index.html', project_amenities=project_amenities, search=search)

@admin.route('/project-amenities/export/<export_type>')
def export_project_amenities(export_type):
    import pandas as pd
    from io import BytesIO, StringIO
    project_amenities = ProjectAmenity.query.all()
    data = []
    for pa in project_amenities:
        data.append({
            'Project': pa.project.name if pa.project else '',
            'Amenity': pa.amenity.name if pa.amenity else '',
            'Is Available': 'Yes' if pa.is_available else 'No',
            'Description': pa.description or '',
            'Area Size': pa.area_size or '',
            'Capacity': pa.capacity or '',
            'Operating Hours': pa.operating_hours or '',
            'Created': pa.created_at.strftime('%Y-%m-%d') if pa.created_at else ''
        })
    df = pd.DataFrame(data)
    if export_type == 'csv':
        output = StringIO()
        df.to_csv(output, index=False)
        output.seek(0)
        return send_file(BytesIO(output.getvalue().encode()), mimetype='text/csv', as_attachment=True, download_name='project_amenities.csv')
    else:
        flash('Invalid export type.', 'danger')
        return redirect(url_for('admin.project_amenities'))

@admin.route('/project-amenities/<int:project_id>/<int:amenity_id>')
def view_project_amenity(project_id, amenity_id):
    pa = ProjectAmenity.query.filter_by(project_id=project_id, amenity_id=amenity_id).first_or_404()
    return render_template('admin/project_amenities/view.html', pa=pa)

@admin.route('/project-amenities/<int:project_id>/<int:amenity_id>/edit', methods=['GET', 'POST'])
def edit_project_amenity(project_id, amenity_id):
    pa = ProjectAmenity.query.filter_by(project_id=project_id, amenity_id=amenity_id).first_or_404()
    if request.method == 'POST':
        data = request.form.to_dict()
        pa.is_available = 'is_available' in request.form
        pa.description = data.get('description', '')
        pa.area_size = float(data['area_size']) if data.get('area_size') else None
        pa.capacity = int(data['capacity']) if data.get('capacity') else None
        pa.operating_hours = data.get('operating_hours', '')
        db.session.commit()
        flash('Project amenity updated successfully!', 'success')
        return redirect(url_for('admin.project_amenities'))
    return render_template('admin/project_amenities/edit.html', pa=pa)

@admin.route('/project-amenities/<int:project_id>/<int:amenity_id>/delete', methods=['POST'])
def delete_project_amenity(project_id, amenity_id):
    pa = ProjectAmenity.query.filter_by(project_id=project_id, amenity_id=amenity_id).first_or_404()
    db.session.delete(pa)
    db.session.commit()
    flash('Project amenity deleted successfully!', 'success')
    return redirect(url_for('admin.project_amenities'))

@admin.route('/project-amenities/new', methods=['GET', 'POST'])
def new_project_amenity():
    projects = Project.query.all()
    amenities = Amenity.query.all()
    if request.method == 'POST':
        data = request.form.to_dict()
        data['project_id'] = int(data['project_id']) if data.get('project_id') else None
        data['amenity_id'] = int(data['amenity_id']) if data.get('amenity_id') else None
        data['is_available'] = 'is_available' in request.form
        data['area_size'] = float(data['area_size']) if data.get('area_size') else None
        data['capacity'] = int(data['capacity']) if data.get('capacity') else None
        pa = ProjectAmenity(
            project_id=data['project_id'],
            amenity_id=data['amenity_id'],
            is_available=data['is_available'],
            description=data.get('description', ''),
            area_size=data.get('area_size'),
            capacity=data.get('capacity'),
            operating_hours=data.get('operating_hours', '')
        )
        db.session.add(pa)
        db.session.commit()
        flash('Project amenity added successfully!', 'success')
        return redirect(url_for('admin.project_amenities'))
    return render_template('admin/project_amenities/new.html', projects=projects, amenities=amenities)

@admin.route('/project-approvals')
def project_approvals():
    page = request.args.get('page', 1, type=int)
    search = request.args.get('search', '')
    query = ProjectApproval.query
    if search:
        query = query.join(Project).join(Approval).filter(
            (Project.name.ilike(f'%{search}%')) |
            (Approval.name.ilike(f'%{search}%')) |
            (ProjectApproval.status.ilike(f'%{search}%'))
        )
    project_approvals = query.order_by(ProjectApproval.created_at.desc()).paginate(page=page, per_page=10, error_out=False)
    return render_template('admin/project_approvals/index.html', project_approvals=project_approvals, search=search)

@admin.route('/project-approvals/export/<export_type>')
def export_project_approvals(export_type):
    import pandas as pd
    from io import BytesIO, StringIO
    project_approvals = ProjectApproval.query.all()
    data = []
    for pa in project_approvals:
        data.append({
            'Project': pa.project.name if pa.project else '',
            'Approval': pa.approval.name if pa.approval else '',
            'Status': pa.status or '',
            'Approval Number': pa.approval_number or '',
            'Approval Date': pa.approval_date.strftime('%Y-%m-%d') if pa.approval_date else '',
            'Expiry Date': pa.expiry_date.strftime('%Y-%m-%d') if pa.expiry_date else '',
            'Issuing Authority': pa.issuing_authority or '',
            'Document URL': pa.document_url or '',
            'Notes': pa.notes or '',
            'Created': pa.created_at.strftime('%Y-%m-%d') if pa.created_at else ''
        })
    df = pd.DataFrame(data)
    if export_type == 'csv':
        output = StringIO()
        df.to_csv(output, index=False)
        output.seek(0)
        return send_file(BytesIO(output.getvalue().encode()), mimetype='text/csv', as_attachment=True, download_name='project_approvals.csv')
    else:
        flash('Invalid export type.', 'danger')
        return redirect(url_for('admin.project_approvals'))

@admin.route('/project-approvals/new', methods=['GET', 'POST'])
def new_project_approval():
    projects = Project.query.all()
    approvals = Approval.query.all()
    if request.method == 'POST':
        data = request.form.to_dict()
        data['project_id'] = int(data['project_id']) if data.get('project_id') else None
        data['approval_id'] = int(data['approval_id']) if data.get('approval_id') else None
        # Dates
        from datetime import datetime
        for field in ['approval_date', 'expiry_date']:
            if data.get(field):
                try:
                    data[field] = datetime.strptime(data[field], '%Y-%m-%d').date()
                except Exception:
                    data[field] = None
            else:
                data[field] = None
        pa = ProjectApproval(
            project_id=data['project_id'],
            approval_id=data['approval_id'],
            status=data.get('status', ''),
            approval_number=data.get('approval_number', ''),
            approval_date=data.get('approval_date'),
            expiry_date=data.get('expiry_date'),
            issuing_authority=data.get('issuing_authority', ''),
            document_url=data.get('document_url', ''),
            notes=data.get('notes', '')
        )
        db.session.add(pa)
        db.session.commit()
        flash('Project approval added successfully!', 'success')
        return redirect(url_for('admin.project_approvals'))
    return render_template('admin/project_approvals/new.html', projects=projects, approvals=approvals)

@admin.route('/project-approvals/<int:project_id>/<int:approval_id>')
def view_project_approval(project_id, approval_id):
    pa = ProjectApproval.query.filter_by(project_id=project_id, approval_id=approval_id).first_or_404()
    return render_template('admin/project_approvals/view.html', pa=pa)

@admin.route('/project-approvals/<int:project_id>/<int:approval_id>/edit', methods=['GET', 'POST'])
def edit_project_approval(project_id, approval_id):
    pa = ProjectApproval.query.filter_by(project_id=project_id, approval_id=approval_id).first_or_404()
    projects = Project.query.all()
    approvals = Approval.query.all()
    if request.method == 'POST':
        data = request.form.to_dict()
        pa.status = data.get('status', '')
        pa.approval_number = data.get('approval_number', '')
        from datetime import datetime
        for field in ['approval_date', 'expiry_date']:
            if data.get(field):
                try:
                    setattr(pa, field, datetime.strptime(data[field], '%Y-%m-%d').date())
                except Exception:
                    setattr(pa, field, None)
            else:
                setattr(pa, field, None)
        pa.issuing_authority = data.get('issuing_authority', '')
        pa.document_url = data.get('document_url', '')
        pa.notes = data.get('notes', '')
        db.session.commit()
        flash('Project approval updated successfully!', 'success')
        return redirect(url_for('admin.project_approvals'))
    return render_template('admin/project_approvals/edit.html', pa=pa, projects=projects, approvals=approvals)

@admin.route('/project-approvals/<int:project_id>/<int:approval_id>/delete', methods=['POST'])
def delete_project_approval(project_id, approval_id):
    pa = ProjectApproval.query.filter_by(project_id=project_id, approval_id=approval_id).first_or_404()
    db.session.delete(pa)
    db.session.commit()
    flash('Project approval deleted successfully!', 'success')
    return redirect(url_for('admin.project_approvals'))

@admin.route('/unit-room-details', endpoint='unit_room_details')
def unit_room_details():
    page = request.args.get('page', 1, type=int)
    search = request.args.get('search', '')
    query = UnitRoomDetail.query
    if search:
        query = query.join(UnitType).filter(
            (UnitType.type_name.ilike(f'%{search}%')) |
            (UnitRoomDetail.room_name.ilike(f'%{search}%'))
        )
    unit_room_details = query.order_by(UnitRoomDetail.created_at.desc()).paginate(page=page, per_page=10, error_out=False)
    return render_template('admin/unit_room_details/index.html', unit_room_details=unit_room_details, search=search)

@admin.route('/unit-room-details/export/<export_type>')
def export_unit_room_details(export_type):
    import pandas as pd
    from io import BytesIO, StringIO
    unit_room_details = UnitRoomDetail.query.all()
    data = []
    for rd in unit_room_details:
        data.append({
            'ID': rd.room_detail_id,
            'Unit Type': rd.unit_type.type_name if rd.unit_type else '',
            'Room Type': rd.room_type or '',
            'Room Name': rd.room_name or '',
            'Sequence': rd.room_sequence or '',
            'Length': rd.room_length or '',
            'Width': rd.room_width or '',
            'Area': rd.room_area or '',
            'Shape': rd.room_shape or '',
            'Attached Bath': 'Yes' if rd.has_attached_bathroom else 'No',
            'Balcony': 'Yes' if rd.has_balcony_access else 'No',
            'Wardrobe': 'Yes' if rd.has_wardrobe else 'No',
            'Window': 'Yes' if rd.has_window else 'No',
            'Natural Light': rd.natural_light_rating or '',
            'Ventilation': rd.ventilation_rating or '',
            'Door Count': rd.door_count or '',
            'Flooring': rd.flooring_type or '',
            'Ceiling': rd.ceiling_type or '',
            'Privacy': rd.privacy_level or '',
            'Position': rd.position_in_unit or '',
            'Created': rd.created_at.strftime('%Y-%m-%d') if rd.created_at else ''
        })
    df = pd.DataFrame(data)
    if export_type == 'csv':
        output = StringIO()
        df.to_csv(output, index=False)
        output.seek(0)
        return send_file(BytesIO(output.getvalue().encode()), mimetype='text/csv', as_attachment=True, download_name='unit_room_details.csv')
    else:
        flash('Invalid export type.', 'danger')
        return redirect(url_for('admin.unit_room_details'))

@admin.route('/unit-room-details/new', methods=['GET', 'POST'])
def new_unit_room_detail():
    unit_types = UnitType.query.all()
    if request.method == 'POST':
        data = request.form.to_dict()
        data['unit_type_id'] = int(data['unit_type_id']) if data.get('unit_type_id') else None
        for field in ['room_sequence', 'window_count', 'door_count', 'electrical_points', 'fan_points', 'ac_points', 'light_points']:
            data[field] = int(data[field]) if data.get(field) else None
        for field in ['room_length', 'room_width', 'room_area', 'wardrobe_area', 'window_total_area', 'door_width', 'door_height', 'window_width', 'window_height', 'ceiling_height']:
            data[field] = float(data[field]) if data.get(field) else None
        for field in ['has_attached_bathroom', 'has_balcony_access', 'has_wardrobe', 'has_window', 'has_geyser_provision', 'has_exhaust_fan', 'has_chimney_provision']:
            data[field] = field in request.form
        rd = UnitRoomDetail(
            unit_type_id=data['unit_type_id'],
            room_type=data.get('room_type', ''),
            room_name=data.get('room_name', ''),
            room_sequence=data.get('room_sequence'),
            room_length=data.get('room_length'),
            room_width=data.get('room_width'),
            room_area=data.get('room_area'),
            room_shape=data.get('room_shape', ''),
            has_attached_bathroom=data.get('has_attached_bathroom', False),
            has_balcony_access=data.get('has_balcony_access', False),
            has_wardrobe=data.get('has_wardrobe', False),
            wardrobe_type=data.get('wardrobe_type', ''),
            wardrobe_area=data.get('wardrobe_area'),
            has_window=data.get('has_window', False),
            window_count=data.get('window_count'),
            window_total_area=data.get('window_total_area'),
            natural_light_rating=data.get('natural_light_rating', ''),
            ventilation_rating=data.get('ventilation_rating', ''),
            door_count=data.get('door_count'),
            door_type=data.get('door_type', ''),
            door_material=data.get('door_material', ''),
            door_width=data.get('door_width'),
            door_height=data.get('door_height'),
            window_type=data.get('window_type', ''),
            window_material=data.get('window_material', ''),
            window_width=data.get('window_width'),
            window_height=data.get('window_height'),
            electrical_points=data.get('electrical_points'),
            fan_points=data.get('fan_points'),
            ac_points=data.get('ac_points'),
            light_points=data.get('light_points'),
            flooring_type=data.get('flooring_type', ''),
            flooring_brand=data.get('flooring_brand', ''),
            ceiling_type=data.get('ceiling_type', ''),
            ceiling_height=data.get('ceiling_height'),
            has_geyser_provision=data.get('has_geyser_provision', False),
            has_exhaust_fan=data.get('has_exhaust_fan', False),
            has_chimney_provision=data.get('has_chimney_provision', False),
            privacy_level=data.get('privacy_level', ''),
            position_in_unit=data.get('position_in_unit', '')
        )
        db.session.add(rd)
        db.session.commit()
        flash('Unit room detail added successfully!', 'success')
        return redirect(url_for('admin.unit_room_details'))
    return render_template('admin/unit_room_details/new.html', unit_types=unit_types)

@admin.route('/unit-room-details/<int:room_detail_id>')
def view_unit_room_detail(room_detail_id):
    rd = UnitRoomDetail.query.get_or_404(room_detail_id)
    return render_template('admin/unit_room_details/view.html', rd=rd)

@admin.route('/unit-room-details/<int:room_detail_id>/edit', methods=['GET', 'POST'], endpoint='edit_unit_room_detail')
def edit_unit_room_detail(room_detail_id):
    rd = UnitRoomDetail.query.get_or_404(room_detail_id)
    unit_types = UnitType.query.all()
    if request.method == 'POST':
        data = request.form.to_dict()
        for field in ['room_sequence', 'window_count', 'door_count', 'electrical_points', 'fan_points', 'ac_points', 'light_points']:
            setattr(rd, field, int(data[field]) if data.get(field) else None)
        for field in ['room_length', 'room_width', 'room_area', 'wardrobe_area', 'window_total_area', 'door_width', 'door_height', 'window_width', 'window_height', 'ceiling_height']:
            setattr(rd, field, float(data[field]) if data.get(field) else None)
        for field in ['has_attached_bathroom', 'has_balcony_access', 'has_wardrobe', 'has_window', 'has_geyser_provision', 'has_exhaust_fan', 'has_chimney_provision']:
            setattr(rd, field, field in request.form)
        rd.unit_type_id = int(data['unit_type_id']) if data.get('unit_type_id') else None
        rd.room_type = data.get('room_type', '')
        rd.room_name = data.get('room_name', '')
        rd.room_shape = data.get('room_shape', '')
        rd.wardrobe_type = data.get('wardrobe_type', '')
        rd.natural_light_rating = data.get('natural_light_rating', '')
        rd.ventilation_rating = data.get('ventilation_rating', '')
        rd.door_type = data.get('door_type', '')
        rd.door_material = data.get('door_material', '')
        rd.window_type = data.get('window_type', '')
        rd.window_material = data.get('window_material', '')
        rd.flooring_type = data.get('flooring_type', '')
        rd.flooring_brand = data.get('flooring_brand', '')
        rd.ceiling_type = data.get('ceiling_type', '')
        rd.privacy_level = data.get('privacy_level', '')
        rd.position_in_unit = data.get('position_in_unit', '')
        db.session.commit()
        flash('Unit room detail updated successfully!', 'success')
        return redirect(url_for('admin.unit_room_details'))
    return render_template('admin/unit_room_details/edit.html', rd=rd, unit_types=unit_types)

@admin.route('/unit-room-details/<int:room_detail_id>/delete', methods=['POST'])
def delete_unit_room_detail(room_detail_id):
    rd = UnitRoomDetail.query.get_or_404(room_detail_id)
    db.session.delete(rd)
    db.session.commit()
    flash('Unit room detail deleted successfully!', 'success')
    return redirect(url_for('admin.unit_room_details'))

# User Interests Routes
@admin.route('/user-interests')
def user_interests():
    """List all user interests"""
    page = request.args.get('page', 1, type=int)
    search = request.args.get('search', '')
    query = UserInterest.query
    if search:
        query = query.filter(
            (UserInterest.interest_type.ilike(f'%{search}%')) |
            (UserInterest.status.ilike(f'%{search}%'))
        )
    user_interests = query.order_by(UserInterest.created_at.desc()).paginate(
        page=page, per_page=10, error_out=False
    )
    return render_template('admin/user_interests/index.html', user_interests=user_interests, search=search)

@admin.route('/user-interests/new', methods=['GET', 'POST'])
def new_user_interest():
    """Create new user interest"""
    if request.method == 'POST':
        data = request.form.to_dict()
        # Convert empty strings to None for numeric fields
        for field in ['budget_min', 'budget_max', 'assigned_to', 'user_id', 'project_id', 'unit_type_id']:
            if data.get(field) == '':
                data[field] = None
        interest = UserInterest(
            user_id=data.get('user_id'),
            project_id=data.get('project_id'),
            unit_type_id=data.get('unit_type_id'),
            interest_type=data.get('interest_type'),
            preferred_contact_method=data.get('preferred_contact_method'),
            preferred_contact_time=data.get('preferred_contact_time'),
            budget_min=data.get('budget_min'),
            budget_max=data.get('budget_max'),
            preferred_floors=data.get('preferred_floors'),
            specific_requirements=data.get('specific_requirements'),
            status=data.get('status'),
            assigned_to=data.get('assigned_to'),
            notes=data.get('notes'),
            created_at=datetime.utcnow()
        )
        db.session.add(interest)
        db.session.commit()
        flash('User interest created successfully!', 'success')
        return redirect(url_for('admin.user_interests'))
    users = User.query.filter_by(is_active=True).order_by(User.first_name, User.last_name).all()
    projects = Project.query.order_by(Project.name).all()
    unit_types = UnitType.query.filter_by(is_active=True).order_by(UnitType.type_name).all()
    return render_template('admin/user_interests/new.html', users=users, projects=projects, unit_types=unit_types)

@admin.route('/user-interests/<int:interest_id>')
def view_user_interest(interest_id):
    interest = UserInterest.query.get_or_404(interest_id)
    return render_template('admin/user_interests/view.html', interest=interest)

@admin.route('/user-interests/<int:interest_id>/edit', methods=['GET', 'POST'])
def edit_user_interest(interest_id):
    interest = UserInterest.query.get_or_404(interest_id)
    if request.method == 'POST':
        data = request.form.to_dict()
        for key, value in data.items():
            if hasattr(interest, key):
                setattr(interest, key, value)
        db.session.commit()
        flash('User interest updated successfully!', 'success')
        return redirect(url_for('admin.user_interests'))
    users = User.query.filter_by(is_active=True).order_by(User.first_name, User.last_name).all()
    projects = Project.query.order_by(Project.name).all()
    unit_types = UnitType.query.filter_by(is_active=True).order_by(UnitType.type_name).all()
    return render_template('admin/user_interests/edit.html', interest=interest, users=users, projects=projects, unit_types=unit_types)

@admin.route('/user-interests/<int:interest_id>/delete', methods=['POST'])
def delete_user_interest(interest_id):
    interest = UserInterest.query.get_or_404(interest_id)
    db.session.delete(interest)
    db.session.commit()
    flash('User interest deleted successfully!', 'success')
    return redirect(url_for('admin.user_interests'))

@admin.route('/user-interests/export/<export_type>')
def export_user_interests(export_type):
    """Export user interests as CSV"""
    interests = UserInterest.query.all()
    if export_type == 'csv':
        import csv
        from io import StringIO
        si = StringIO()
        cw = csv.writer(si)
        cw.writerow(['interest_id', 'user_id', 'project_id', 'unit_type_id', 'interest_type', 'preferred_contact_method', 'preferred_contact_time', 'budget_min', 'budget_max', 'preferred_floors', 'specific_requirements', 'status', 'assigned_to', 'notes', 'created_at'])
        for i in interests:
            cw.writerow([
                i.interest_id, i.user_id, i.project_id, i.unit_type_id, i.interest_type, i.preferred_contact_method, i.preferred_contact_time, i.budget_min, i.budget_max, i.preferred_floors, i.specific_requirements, i.status, i.assigned_to, i.notes, i.created_at
            ])
        output = make_response(si.getvalue())
        output.headers["Content-Disposition"] = "attachment; filename=user_interests.csv"
        output.headers["Content-type"] = "text/csv"
        return output
    flash('Unsupported export type', 'danger')
    return redirect(url_for('admin.user_interests'))

 