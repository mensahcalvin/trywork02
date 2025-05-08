from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime
app = Flask(__name__)
app.config['SECRET_KEY'] = 'your-secret-key-here'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///explore_ghana.db'
db = SQLAlchemy(app)
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

# User Model
class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(128))
    blog_posts = db.relationship('BlogPost', backref='author', lazy=True)
    comments = db.relationship('Comment', backref='author', lazy=True)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

# BlogPost Model
class BlogPost(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    content = db.Column(db.Text, nullable=False)
    date_posted = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    comments = db.relationship('Comment', backref='post', lazy=True)

# Comment Model
class Comment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.Text, nullable=False)
    date_posted = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    post_id = db.Column(db.Integer, db.ForeignKey('blog_post.id'), nullable=False)

# Tourist Site Model
class TouristSite(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=False)
    location = db.Column(db.String(100), nullable=False)
    region = db.Column(db.String(50), nullable=False)
    category = db.Column(db.String(50), nullable=False)  # e.g., Historical, Natural, Cultural
    image_url = db.Column(db.String(200))
    latitude = db.Column(db.Float)
    longitude = db.Column(db.Float)
    rating = db.Column(db.Float)
    entry_fee = db.Column(db.String(50))
    opening_hours = db.Column(db.String(100))
    best_time_to_visit = db.Column(db.String(100))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# Routes
@app.route('/')
def home():
    return render_template('home.html')

@app.route('/destinations')
def destinations():
    return render_template('destinations.html')

@app.route('/accommodations')
def accommodations():
    return render_template('accommodations.html')

@app.route('/transportation')
def transportation():
    return render_template('transportation.html')

@app.route('/events')
def events():
    return render_template('events.html')

@app.route('/itinerary')
@login_required
def itinerary():
    return render_template('itinerary.html')

@app.route('/map')
def map():
    return render_template('map.html')

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/blog')
def blog():
    posts = BlogPost.query.order_by(BlogPost.date_posted.desc()).all()
    return render_template('blog.html', posts=posts)

@app.route('/blog/new', methods=['GET', 'POST'])
@login_required
def new_post():
    if request.method == 'POST':
        title = request.form.get('title')
        content = request.form.get('content')
        post = BlogPost(title=title, content=content, author=current_user)
        db.session.add(post)
        db.session.commit()
        flash('Your post has been created!', 'success')
        return redirect(url_for('blog'))
    return render_template('create_post.html')

@app.route('/blog/<int:post_id>')
def post(post_id):
    post = BlogPost.query.get_or_404(post_id)
    return render_template('post.html', post=post)

@app.route('/blog/<int:post_id>/comment', methods=['POST'])
@login_required
def comment(post_id):
    post = BlogPost.query.get_or_404(post_id)
    content = request.form.get('content')
    comment = Comment(content=content, author=current_user, post=post)
    db.session.add(comment)
    db.session.commit()
    flash('Your comment has been added!', 'success')
    return redirect(url_for('post', post_id=post.id))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        user = User.query.filter_by(username=username).first()
        
        if user and user.check_password(password):
            login_user(user)
            return redirect(url_for('home'))
        flash('Invalid username or password')
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form.get('username')
        email = request.form.get('email')
        password = request.form.get('password')
        
        if User.query.filter_by(username=username).first():
            flash('Username already exists')
            return redirect(url_for('register'))
        
        user = User(username=username, email=email)
        user.set_password(password)
        db.session.add(user)
        db.session.commit()
        
        return redirect(url_for('login'))
    return render_template('register.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('home'))

@app.route('/search')
def search():
    query = request.args.get('q', '')
    if query:
        # Search in destinations, accommodations, and blog posts
        destinations = BlogPost.query.filter(
            (BlogPost.title.ilike(f'%{query}%')) | 
            (BlogPost.content.ilike(f'%{query}%'))
        ).all()
        return render_template('search_results.html', query=query, results=destinations)
    return redirect(url_for('home'))

# API Routes for Tourist Sites
@app.route('/api/tourist-sites', methods=['GET'])
def get_tourist_sites():
    # Get query parameters for filtering
    region = request.args.get('region')
    category = request.args.get('category')
    min_rating = request.args.get('min_rating')
    
    # Start with base query
    query = TouristSite.query
    
    # Apply filters if provided
    if region:
        query = query.filter(TouristSite.region == region)
    if category:
        query = query.filter(TouristSite.category == category)
    if min_rating:
        query = query.filter(TouristSite.rating >= float(min_rating))
    
    # Get all matching sites
    sites = query.all()
    
    # Convert to JSON
    sites_json = [{
        'id': site.id,
        'name': site.name,
        'description': site.description,
        'location': site.location,
        'region': site.region,
        'category': site.category,
        'image_url': site.image_url,
        'latitude': site.latitude,
        'longitude': site.longitude,
        'rating': site.rating,
        'entry_fee': site.entry_fee,
        'opening_hours': site.opening_hours,
        'best_time_to_visit': site.best_time_to_visit
    } for site in sites]
    
    return jsonify(sites_json)

@app.route('/api/tourist-sites/<int:site_id>', methods=['GET'])
def get_tourist_site(site_id):
    site = TouristSite.query.get_or_404(site_id)
    return jsonify({
        'id': site.id,
        'name': site.name,
        'description': site.description,
        'location': site.location,
        'region': site.region,
        'category': site.category,
        'image_url': site.image_url,
        'latitude': site.latitude,
        'longitude': site.longitude,
        'rating': site.rating,
        'entry_fee': site.entry_fee,
        'opening_hours': site.opening_hours,
        'best_time_to_visit': site.best_time_to_visit
    })

@app.route('/api/tourist-sites/regions', methods=['GET'])
def get_regions():
    regions = db.session.query(TouristSite.region).distinct().all()
    return jsonify([region[0] for region in regions])

@app.route('/api/tourist-sites/categories', methods=['GET'])
def get_categories():
    categories = db.session.query(TouristSite.category).distinct().all()
    return jsonify([category[0] for category in categories])

# Sample data insertion route (for development only)
@app.route('/api/tourist-sites/seed', methods=['POST'])
def seed_tourist_sites():
    sample_sites = [
        {
            'name': 'Cape Coast Castle',
            'description': 'A UNESCO World Heritage Site, this castle was a major slave trading post.',
            'location': 'Cape Coast',
            'region': 'Central Region',
            'category': 'Historical',
            'image_url': 'https://example.com/cape-coast-castle.jpg',
            'latitude': 5.1036,
            'longitude': -1.2417,
            'rating': 4.8,
            'entry_fee': 'GHC 50',
            'opening_hours': '9:00 AM - 5:00 PM',
            'best_time_to_visit': 'November to March'
        },
        {
            'name': 'Kakum National Park',
            'description': 'Famous for its canopy walkway through the rainforest.',
            'location': 'Cape Coast',
            'region': 'Central Region',
            'category': 'Natural',
            'image_url': 'https://example.com/kakum-park.jpg',
            'latitude': 5.3500,
            'longitude': -1.3833,
            'rating': 4.7,
            'entry_fee': 'GHC 60',
            'opening_hours': '8:00 AM - 4:00 PM',
            'best_time_to_visit': 'All year round'
        },
        {
            'name': 'Mole National Park',
            'description': 'Ghana\'s largest wildlife refuge, home to elephants, antelopes, and more.',
            'location': 'Larabanga',
            'region': 'Northern Region',
            'category': 'Natural',
            'image_url': 'https://example.com/mole-park.jpg',
            'latitude': 9.3000,
            'longitude': -1.8500,
            'rating': 4.6,
            'entry_fee': 'GHC 80',
            'opening_hours': '6:00 AM - 6:00 PM',
            'best_time_to_visit': 'December to April'
        }
    ]
    
    for site_data in sample_sites:
        site = TouristSite(**site_data)
        db.session.add(site)
    
    db.session.commit()
    return jsonify({'message': 'Sample tourist sites added successfully'})

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True) 