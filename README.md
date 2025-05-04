# Explore Ghana Tourism Platform

## Overview

**Explore Ghana** is a Flask-based web application designed to showcase the rich tourism opportunities within Ghana. Whether you're a local looking for new adventures or a potential visitor planning a trip, this platform provides a space to discover destinations, read and share experiences, and connect with the beauty of Ghana.

## Features

* **User Authentication:** Secure registration and login system for users to create accounts and engage with the platform.
* **Blog System:** Users can share their travel experiences in Ghana through blog posts, including text and visuals.
* **Destination Information:** Comprehensive information about various tourist destinations across Ghana, including descriptions, images, and potentially location details.
* **Experience Sharing:** A dedicated space for users to share their personal experiences, tips, and recommendations related to traveling in Ghana.
* **Comment System:** Users can engage with blog posts and shared experiences by leaving comments and participating in discussions.

## Setup Instructions

Follow these steps to get the Explore Ghana platform up and running on your local machine:

1.  **Create a Virtual Environment:**
    It's recommended to use a virtual environment to isolate the project dependencies. Open your terminal or command prompt and navigate to the project directory. Then, run the following commands:

    ```bash
    python -m venv venv
    source venv/bin/activate   # On macOS and Linux
    # On Windows:
    # venv\Scripts\activate
    ```

2.  **Install Dependencies:**
    Install all the necessary Python packages listed in the `requirements.txt` file using pip:

    ```bash
    pip install -r requirements.txt
    ```

3.  **Set Up Environment Variables:**
    Create a `.env` file in the root directory of the project. This file will store sensitive information and configuration settings. Add the following content to your `.env` file:

    ```
    FLASK_APP=app.py
    FLASK_ENV=development
    SECRET_KEY=your-secret-key-here
    DATABASE_URL=sqlite:///explore_ghana.db
    ```

    * `FLASK_APP`: Specifies the main application file.
    * `FLASK_ENV`: Sets the environment to 'development' for debugging purposes. You might change this to 'production' for a live deployment.
    * `SECRET_KEY`: A secret key used by Flask for securely signing session cookies. **Replace `your-secret-key-here` with a strong, unique key.**
    * `DATABASE_URL`: Defines the connection string for the database. In this case, it's using a SQLite database named `explore_ghana.db` which will be created in the project directory.

4.  **Initialize the Database:**
    Set up the database tables required by the application. Run the Flask shell and execute the database creation commands:

    ```bash
    flask shell
    ```

    Once the shell is open, enter the following Python code:

    ```python
    from app import db
    db.create_all()
    exit()
    ```

    This will create the necessary tables in your `explore_ghana.db` file.

5.  **Run the Application:**
    Start the Flask development server using the following command:

    ```bash
    flask run
    ```

    The application will now be accessible in your web browser at `http://localhost:5000`.

## Project Structure

The project is organized into the following directories and files: