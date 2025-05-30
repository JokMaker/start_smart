# This file is the entry point for running the Flask application.
# It imports the create_app function from the app module and runs the application.
# The application will run in debug mode, which is useful for development.
# To run the application, use the command: python run.py
# Note: Make sure to have Flask installed and the app module properly set up.

from app import create_app

app = create_app()

if __name__ == '__main__':
    app.run(debug=True)
