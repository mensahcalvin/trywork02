from app import db
from datetime import datetime

class Event(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=False)
    location = db.Column(db.String(100), nullable=False)
    start_date = db.Column(db.DateTime, nullable=False)
    end_date = db.Column(db.DateTime, nullable=False)
    image_url = db.Column(db.String(200))
    category = db.Column(db.String(50), nullable=False)  # e.g., 'Cultural', 'Festival', 'Music'
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def to_dict(self):
        return {
            'id': self.id,
            'title': self.title,
            'description': self.description,
            'location': self.location,
            'start_date': self.start_date.isoformat(),
            'end_date': self.end_date.isoformat(),
            'image_url': self.image_url,
            'category': self.category,
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat()
        }

class EventService:
    @staticmethod
    def get_all_events():
        """Get all events"""
        return Event.query.all()

    @staticmethod
    def get_event_by_id(event_id):
        """Get a specific event by ID"""
        return Event.query.get_or_404(event_id)

    @staticmethod
    def create_event(title, description, location, start_date, end_date, category, image_url=None):
        """Create a new event"""
        event = Event(
            title=title,
            description=description,
            location=location,
            start_date=start_date,
            end_date=end_date,
            category=category,
            image_url=image_url
        )
        db.session.add(event)
        db.session.commit()
        return event

    @staticmethod
    def update_event(event_id, **kwargs):
        """Update an event"""
        event = Event.query.get_or_404(event_id)
        for key, value in kwargs.items():
            if hasattr(event, key):
                setattr(event, key, value)
        event.updated_at = datetime.utcnow()
        db.session.commit()
        return event

    @staticmethod
    def delete_event(event_id):
        """Delete an event"""
        event = Event.query.get_or_404(event_id)
        db.session.delete(event)
        db.session.commit()
        return True

    @staticmethod
    def get_upcoming_events():
        """Get all upcoming events"""
        return Event.query.filter(Event.start_date > datetime.utcnow()).order_by(Event.start_date).all()

    @staticmethod
    def get_events_by_category(category):
        """Get all events in a specific category"""
        return Event.query.filter_by(category=category).all()

    @staticmethod
    def get_events_by_location(location):
        """Get all events in a specific location"""
        return Event.query.filter_by(location=location).all()

    @staticmethod
    def search_events(query):
        """Search events by title, description, or location"""
        return Event.query.filter(
            (Event.title.ilike(f'%{query}%')) |
            (Event.description.ilike(f'%{query}%')) |
            (Event.location.ilike(f'%{query}%'))
        ).all() 