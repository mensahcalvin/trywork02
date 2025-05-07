from app import db
from datetime import datetime

class Itinerary(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text)
    start_date = db.Column(db.DateTime, nullable=False)
    end_date = db.Column(db.DateTime, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    items = db.relationship('ItineraryItem', backref='itinerary', lazy=True, cascade='all, delete-orphan')

    def to_dict(self):
        return {
            'id': self.id,
            'title': self.title,
            'description': self.description,
            'start_date': self.start_date.isoformat(),
            'end_date': self.end_date.isoformat(),
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat(),
            'items': [item.to_dict() for item in self.items]
        }

class ItineraryItem(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    itinerary_id = db.Column(db.Integer, db.ForeignKey('itinerary.id'), nullable=False)
    destination_id = db.Column(db.Integer, db.ForeignKey('destination.id'), nullable=False)
    date = db.Column(db.DateTime, nullable=False)
    notes = db.Column(db.Text)
    order = db.Column(db.Integer, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def to_dict(self):
        return {
            'id': self.id,
            'itinerary_id': self.itinerary_id,
            'destination_id': self.destination_id,
            'date': self.date.isoformat(),
            'notes': self.notes,
            'order': self.order,
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat()
        }

class ItineraryService:
    @staticmethod
    def create_itinerary(title, description, start_date, end_date):
        """Create a new itinerary"""
        itinerary = Itinerary(
            title=title,
            description=description,
            start_date=start_date,
            end_date=end_date
        )
        db.session.add(itinerary)
        db.session.commit()
        return itinerary

    @staticmethod
    def get_itinerary_by_id(itinerary_id):
        """Get a specific itinerary by ID"""
        return Itinerary.query.get_or_404(itinerary_id)

    @staticmethod
    def update_itinerary(itinerary_id, **kwargs):
        """Update an itinerary"""
        itinerary = Itinerary.query.get_or_404(itinerary_id)
        for key, value in kwargs.items():
            if hasattr(itinerary, key):
                setattr(itinerary, key, value)
        itinerary.updated_at = datetime.utcnow()
        db.session.commit()
        return itinerary

    @staticmethod
    def delete_itinerary(itinerary_id):
        """Delete an itinerary"""
        itinerary = Itinerary.query.get_or_404(itinerary_id)
        db.session.delete(itinerary)
        db.session.commit()
        return True

    @staticmethod
    def add_item_to_itinerary(itinerary_id, destination_id, date, notes=None, order=None):
        """Add a destination to an itinerary"""
        if order is None:
            # Get the highest order number and increment by 1
            max_order = db.session.query(db.func.max(ItineraryItem.order)).filter_by(itinerary_id=itinerary_id).scalar()
            order = (max_order or 0) + 1

        item = ItineraryItem(
            itinerary_id=itinerary_id,
            destination_id=destination_id,
            date=date,
            notes=notes,
            order=order
        )
        db.session.add(item)
        db.session.commit()
        return item

    @staticmethod
    def update_item_order(itinerary_id, item_id, new_order):
        """Update the order of an item in the itinerary"""
        item = ItineraryItem.query.filter_by(id=item_id, itinerary_id=itinerary_id).first_or_404()
        item.order = new_order
        db.session.commit()
        return item

    @staticmethod
    def remove_item_from_itinerary(itinerary_id, item_id):
        """Remove an item from an itinerary"""
        item = ItineraryItem.query.filter_by(id=item_id, itinerary_id=itinerary_id).first_or_404()
        db.session.delete(item)
        db.session.commit()
        return True

    @staticmethod
    def get_user_itineraries():
        """Get all itineraries (in the future, this will be filtered by user)"""
        return Itinerary.query.order_by(Itinerary.start_date).all() 