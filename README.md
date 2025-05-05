# Explore Ghana - Travel Guide Application

A comprehensive travel guide application for exploring Ghana's rich culture, beautiful landscapes, and vibrant cities.

## Features

- Browse popular destinations in Ghana
- View detailed information about each destination
- Plan your trip itinerary
- Explore cultural events and festivals
- Modern and responsive user interface

## Project Structure

```
backend/
├── app/
│   ├── models/          # Database models
│   │   ├── __init__.py
│   │   └── destination.py
│   ├── routes/          # API routes and endpoints
│   │   ├── __init__.py
│   │   └── main.py
│   ├── services/        # Business logic
│   ├── utils/           # Utility functions
│   └── __init__.py      # Flask application factory
├── templates/           # HTML templates
├── static/             # Static files (CSS, JS, images)
├── config.py           # Application configuration
├── run.py              # Application entry point
└── requirements.txt    # Python dependencies
```

## Setup Instructions

### Prerequisites

- Python 3.8 or higher
- pip (Python package manager)
- Virtual environment (recommended)

### Installation

1. Clone the repository:
```bash
git clone <repository-url>
cd explore-ghana
```

2. Create and activate a virtual environment:
```bash
# Windows
python -m venv venv
venv\Scripts\activate

# Unix/MacOS
python -m venv venv
source venv/bin/activate
```

3. Install dependencies:
```bash
pip install -r backend/requirements.txt
```

4. Create a `.env` file in the backend directory with the following content:
```
FLASK_APP=run.py
FLASK_ENV=development
SECRET_KEY=your-secret-key-here
DATABASE_URL=sqlite:///app.db
```

5. Initialize the database:
```bash
cd backend
flask db init
flask db migrate -m "Initial migration"
flask db upgrade
```

### Running the Application

1. Start the Flask development server:
```bash
python backend/run.py
```

2. Open your web browser and navigate to:
```
http://localhost:5000
```

## API Endpoints

- `GET /` - Home page
- `GET /api/destinations` - Get all destinations
- `GET /api/destinations/<id>` - Get a specific destination

## Technologies Used

- Backend:
  - Flask (Python web framework)
  - SQLAlchemy (ORM)
  - Flask-Migrate (Database migrations)
  - Python-dotenv (Environment variable management)

- Frontend:
  - HTML5
  - CSS3
  - Bootstrap 5
  - JavaScript

## Contributing

1. Fork the repository
2. Create a new branch for your feature
3. Make your changes
4. Submit a pull request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Contact

For any questions or suggestions, please open an issue in the repository.