from app import db
from app.models.destination import Destination
from datetime import datetime

class DestinationService:
    @staticmethod
    def get_all_destinations():
        """Get all destinations"""
        return Destination.query.all()

    @staticmethod
    def get_destination_by_id(destination_id):
        """Get a specific destination by ID"""
        return Destination.query.get_or_404(destination_id)

    @staticmethod
    def create_destination(name, description, location, image_url=None):
        """Create a new destination"""
        destination = Destination(
            name=name,
            description=description,
            location=location,
            image_url=image_url
        )
        db.session.add(destination)
        db.session.commit()
        return destination

    @staticmethod
    def update_destination(destination_id, **kwargs):
        """Update a destination"""
        destination = Destination.query.get_or_404(destination_id)
        for key, value in kwargs.items():
            if hasattr(destination, key):
                setattr(destination, key, value)
        destination.updated_at = datetime.utcnow()
        db.session.commit()
        return destination

    @staticmethod
    def delete_destination(destination_id):
        """Delete a destination"""
        destination = Destination.query.get_or_404(destination_id)
        db.session.delete(destination)
        db.session.commit()
        return True

    @staticmethod
    def search_destinations(query):
        """Search destinations by name or location"""
        return Destination.query.filter(
            (Destination.name.ilike(f'%{query}%')) |
            (Destination.location.ilike(f'%{query}%'))
        ).all()

    @staticmethod
    def get_destinations_by_location(location):
        """Get all destinations in a specific location"""
        return Destination.query.filter_by(location=location).all() 