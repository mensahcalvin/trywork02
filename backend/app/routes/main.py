from flask import Blueprint, render_template, jsonify
from app.models.destination import Destination
from app import db

bp = Blueprint('main', __name__)

@bp.route('/')
def home():
    return render_template('home.html')

@bp.route('/api/destinations')
def get_destinations():
    destinations = Destination.query.all()
    return jsonify([destination.to_dict() for destination in destinations])

@bp.route('/api/destinations/<int:id>')
def get_destination(id):
    destination = Destination.query.get_or_404(id)
    return jsonify(destination.to_dict()) 