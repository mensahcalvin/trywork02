from flask import Blueprint, render_template, request, jsonify, redirect, url_for, flash
from flask_login import login_required, current_user
from app.models.user import User
from app.models.blog import BlogPost, BlogComment
from app import db
from datetime import datetime
from flask_wtf.csrf import CSRFProtect
from sqlalchemy.exc import SQLAlchemyError

admin_bp = Blueprint('admin', __name__, url_prefix='/admin')
csrf = CSRFProtect()

def admin_required(f):
    def decorated_function(*args, **kwargs):
        if not current_user.is_authenticated or not current_user.is_admin:
            flash('You do not have permission to access this page.', 'danger')
            return redirect(url_for('main.home'))
        return f(*args, **kwargs)
    decorated_function.__name__ = f.__name__
    return decorated_function

@admin_bp.route('/dashboard')
@login_required
@admin_required
def dashboard():
    # Get statistics
    total_users = User.query.count()
    total_posts = BlogPost.query.count()
    total_comments = BlogComment.query.count()
    recent_users = User.query.order_by(User.date_joined.desc()).limit(5).all()
    recent_posts = BlogPost.query.order_by(BlogPost.date_posted.desc()).limit(5).all()
    
    return render_template('admin/dashboard.html',
                         total_users=total_users,
                         total_posts=total_posts,
                         total_comments=total_comments,
                         recent_users=recent_users,
                         recent_posts=recent_posts)

@admin_bp.route('/users')
@login_required
@admin_required
def users():
    page = request.args.get('page', 1, type=int)
    users = User.query.paginate(page=page, per_page=10)
    return render_template('admin/users.html', users=users)

@admin_bp.route('/users/<int:user_id>', methods=['GET', 'POST'])
@login_required
@admin_required
def user_detail(user_id):
    user = User.query.get_or_404(user_id)
    if request.method == 'POST':
        try:
            is_active = request.form.get('is_active')
            is_admin = request.form.get('is_admin')
            
            if is_active is not None:
                user.is_active = is_active == 'true'
            if is_admin is not None:
                user.is_admin = is_admin == 'true'
                
            db.session.commit()
            flash('User updated successfully', 'success')
        except SQLAlchemyError as e:
            db.session.rollback()
            flash('Error updating user. Please try again.', 'danger')
            return redirect(url_for('admin.user_detail', user_id=user_id))
            
        return redirect(url_for('admin.user_detail', user_id=user_id))
    return render_template('admin/user_detail.html', user=user)

@admin_bp.route('/posts')
@login_required
@admin_required
def posts():
    page = request.args.get('page', 1, type=int)
    posts = BlogPost.query.paginate(page=page, per_page=10)
    return render_template('admin/posts.html', posts=posts)

@admin_bp.route('/posts/<int:post_id>', methods=['GET', 'POST'])
@login_required
@admin_required
def post_detail(post_id):
    post = BlogPost.query.get_or_404(post_id)
    if request.method == 'POST':
        try:
            is_published = request.form.get('is_published')
            is_featured = request.form.get('is_featured')
            
            if is_published is not None:
                post.is_published = is_published == 'true'
            if is_featured is not None:
                post.is_featured = is_featured == 'true'
                
            db.session.commit()
            flash('Post updated successfully', 'success')
        except SQLAlchemyError as e:
            db.session.rollback()
            flash('Error updating post. Please try again.', 'danger')
            return redirect(url_for('admin.post_detail', post_id=post_id))
            
        return redirect(url_for('admin.post_detail', post_id=post_id))
    return render_template('admin/post_detail.html', post=post)

@admin_bp.route('/comments')
@login_required
@admin_required
def comments():
    page = request.args.get('page', 1, type=int)
    comments = BlogComment.query.paginate(page=page, per_page=10)
    return render_template('admin/comments.html', comments=comments)

@admin_bp.route('/comments/<int:comment_id>', methods=['POST'])
@login_required
@admin_required
def delete_comment(comment_id):
    try:
        comment = BlogComment.query.get_or_404(comment_id)
        db.session.delete(comment)
        db.session.commit()
        flash('Comment deleted successfully', 'success')
    except SQLAlchemyError as e:
        db.session.rollback()
        flash('Error deleting comment. Please try again.', 'danger')
    return redirect(url_for('admin.comments'))

@admin_bp.route('/api/stats')
@login_required
@admin_required
def get_stats():
    try:
        # Get user growth data
        users = User.query.order_by(User.date_joined).all()
        user_growth = {}
        for user in users:
            month = user.date_joined.strftime('%Y-%m')
            user_growth[month] = user_growth.get(month, 0) + 1
        
        # Get post activity data
        posts = BlogPost.query.order_by(BlogPost.date_posted).all()
        post_activity = {}
        for post in posts:
            month = post.date_posted.strftime('%Y-%m')
            post_activity[month] = post_activity.get(month, 0) + 1
        
        # Sort the data by month
        user_growth = dict(sorted(user_growth.items()))
        post_activity = dict(sorted(post_activity.items()))
        
        return jsonify({
            'user_growth': user_growth,
            'post_activity': post_activity
        })
    except SQLAlchemyError as e:
        return jsonify({'error': 'Error fetching statistics'}), 500 