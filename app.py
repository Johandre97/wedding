# app.py

from flask import Flask, render_template, request, redirect, url_for, flash
import os
from dotenv import load_dotenv
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

app = Flask(__name__)
app.template_folder = './templates'
app.static_folder = './static'

load_dotenv()

app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_POOL_TIMEOUT'] = 3600  # 30 days * 24 hours * 60 minutes * 60 seconds
app.config['SQLALCHEMY_ENGINE_OPTIONS'] = {
    'pool_pre_ping': True,  # Automatically reconnect on connection loss
}
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')


db = SQLAlchemy(app)
migrate = Migrate(app, db)


class Guest(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), nullable=False, unique=True)
    guests_count = db.Column(db.Integer, nullable=False)
    message = db.Column(db.Text)


def current_page():
    return {'current_page': request.endpoint}

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/rsvp', methods=['POST'])
def rsvp():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        guests_count = request.form['guests_count']
        message = request.form['message']

        try:
            # Check if the guest with the same email already exists
            existing_guest = Guest.query.filter_by(email=email).first()

            if existing_guest:
                flash('You have already reserved with this email address.', 'danger')
                return redirect(url_for('index'))

            # If the guest is not found, create a new guest record
            new_guest = Guest(name=name, email=email, guests_count=guests_count, message=message)

            # Add the new guest to the session and commit the transaction
            db.session.add(new_guest)
            db.session.commit()

            flash('Thank you for your reservation!', 'success')
            return redirect(url_for('index'))

        except Exception as e:
            flash('An error occurred while processing your reservation. Please try again later.', 'danger')
            print(f"Error occurred: {str(e)}")
            return redirect(url_for('index'))



@app.route('/<string:page_name>')
def html_page(page_name):
    return render_template(page_name + '.html', current_page=page_name)


# Create a Flask application context
with app.app_context():
    # Create database tables
    db.create_all()

if __name__ == '__main__':
    app.run()