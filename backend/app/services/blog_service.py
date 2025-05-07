from app import db
from datetime import datetime
import os
from werkzeug.utils import secure_filename

class BlogPost(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    content = db.Column(db.Text, nullable=False)
    destination_id = db.Column(db.Integer, db.ForeignKey('destination.id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)  # Will be implemented later
    image_path = db.Column(db.String(255))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    likes = db.Column(db.Integer, default=0)
    comments = db.relationship('BlogComment', backref='post', lazy=True, cascade='all, delete-orphan')

    def to_dict(self):
        return {
            'id': self.id,
            'title': self.title,
            'content': self.content,
            'destination_id': self.destination_id,
            'user_id': self.user_id,
            'image_path': self.image_path,
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat(),
            'likes': self.likes,
            'comments_count': len(self.comments)
        }

class BlogComment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    post_id = db.Column(db.Integer, db.ForeignKey('blog_post.id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)  # Will be implemented later
    content = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def to_dict(self):
        return {
            'id': self.id,
            'post_id': self.post_id,
            'user_id': self.user_id,
            'content': self.content,
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat()
        }

class BlogService:
    ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}
    UPLOAD_FOLDER = 'static/uploads/blog'

    @staticmethod
    def allowed_file(filename):
        return '.' in filename and \
               filename.rsplit('.', 1)[1].lower() in BlogService.ALLOWED_EXTENSIONS

    @staticmethod
    def create_post(title, content, destination_id, user_id, image_file=None):
        """Create a new blog post"""
        image_path = None
        if image_file and BlogService.allowed_file(image_file.filename):
            filename = secure_filename(image_file.filename)
            # Create unique filename using timestamp
            timestamp = datetime.utcnow().strftime('%Y%m%d_%H%M%S')
            filename = f"{timestamp}_{filename}"
            image_path = os.path.join(BlogService.UPLOAD_FOLDER, filename)
            # Ensure upload directory exists
            os.makedirs(os.path.dirname(image_path), exist_ok=True)
            image_file.save(image_path)

        post = BlogPost(
            title=title,
            content=content,
            destination_id=destination_id,
            user_id=user_id,
            image_path=image_path
        )
        db.session.add(post)
        db.session.commit()
        return post

    @staticmethod
    def get_post_by_id(post_id):
        """Get a specific blog post by ID"""
        return BlogPost.query.get_or_404(post_id)

    @staticmethod
    def update_post(post_id, **kwargs):
        """Update a blog post"""
        post = BlogPost.query.get_or_404(post_id)
        for key, value in kwargs.items():
            if hasattr(post, key):
                setattr(post, key, value)
        post.updated_at = datetime.utcnow()
        db.session.commit()
        return post

    @staticmethod
    def delete_post(post_id):
        """Delete a blog post and its associated image"""
        post = BlogPost.query.get_or_404(post_id)
        if post.image_path and os.path.exists(post.image_path):
            os.remove(post.image_path)
        db.session.delete(post)
        db.session.commit()
        return True

    @staticmethod
    def get_all_posts():
        """Get all blog posts ordered by creation date"""
        return BlogPost.query.order_by(BlogPost.created_at.desc()).all()

    @staticmethod
    def get_posts_by_destination(destination_id):
        """Get all blog posts for a specific destination"""
        return BlogPost.query.filter_by(destination_id=destination_id)\
            .order_by(BlogPost.created_at.desc()).all()

    @staticmethod
    def add_comment(post_id, user_id, content):
        """Add a comment to a blog post"""
        comment = BlogComment(
            post_id=post_id,
            user_id=user_id,
            content=content
        )
        db.session.add(comment)
        db.session.commit()
        return comment

    @staticmethod
    def delete_comment(comment_id):
        """Delete a comment"""
        comment = BlogComment.query.get_or_404(comment_id)
        db.session.delete(comment)
        db.session.commit()
        return True

    @staticmethod
    def like_post(post_id):
        """Increment the like count for a post"""
        post = BlogPost.query.get_or_404(post_id)
        post.likes += 1
        db.session.commit()
        return post.likes

    @staticmethod
    def search_posts(query):
        """Search blog posts by title or content"""
        return BlogPost.query.filter(
            (BlogPost.title.ilike(f'%{query}%')) |
            (BlogPost.content.ilike(f'%{query}%'))
        ).order_by(BlogPost.created_at.desc()).all() 