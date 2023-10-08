# app.py

from flask import Flask, render_template, request, redirect, url_for, flash
import os
from dotenv import load_dotenv
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from email.message import EmailMessage
from string import Template
import smtplib

app = Flask(__name__)
app.template_folder = './templates'
app.static_folder = './static'

load_dotenv()

#  Database set-up from environment variables
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Database configuration
app.config['SQLALCHEMY_POOL_TIMEOUT'] = 3600  # Set database time-out to 1 hour
app.config['SQLALCHEMY_ENGINE_OPTIONS'] = {
    'pool_pre_ping': True,  # Automatically reconnect on connection loss
}
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')

#  Initialize database with SQL Alchemy
db = SQLAlchemy(app)
migrate = Migrate(app, db)

# Load your SMTP email and password from environment variables
smtp_email = os.getenv("SMTP_EMAIL")
smtp_password = os.getenv("SMTP_PASSWORD")


# Define a guest model for the database
class Guest(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), nullable=False, unique=True)
    guests_count = db.Column(db.Integer, nullable=False)
    message = db.Column(db.Text)

# Send Email Function


def send_email(subject, recipients, content, cc=None):
    html_template = Template(content)
    html_content = html_template.substitute()

    message = EmailMessage()
    message['from'] = 'Our Wedding - Mailer'
    message['subject'] = subject
    message.set_content(html_content, 'html')

    message['to'] = recipients

    with smtplib.SMTP(host='smtp.gmail.com', port=587) as smtp:
        smtp.ehlo()
        smtp.starttls()
        smtp.login(smtp_email, smtp_password)
        smtp.send_message(message)


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
        message = request.form['message']

        try:
            # Check if the guest with the same email already exists
            existing_guest = Guest.query.filter_by(email=email).first()

            if existing_guest:
                flash('You have already reserved with this email address.', 'danger')
                return redirect(url_for('index'))

            # Create a new guest record for the main guest
            main_guest = Guest(name=name, email=email, guests_count=1, message=message)

            # Add the main guest to the session
            db.session.add(main_guest)

            # Collect guest information for guests 2 to numGuests
            for i in range(2, 5):  # Assuming a maximum of 4 guests, adjust as needed
                guest_name = request.form.get(f'guest_name_{i}')
                guest_email = request.form.get(f'guest_email_{i}')
                guest_message = request.form.get(f'guest_message_{i}')
                if guest_name and guest_email:
                    guest_record = Guest(
                        name=guest_name,
                        email=guest_email,
                        guests_count=1,
                        message=guest_message
                    )
                    db.session.add(guest_record)

            db.session.commit()

            flash('Thank you for your reservation!', 'success')
            return redirect(url_for('index'))

        except Exception as e:
            flash('An error occurred while processing your reservation. Please try again later.', 'danger')
            print(f"Error occurred: {str(e)}")
            return redirect(url_for('index'))
# Contact form route


@app.route('/contact', methods=['GET', 'POST'])
def contact():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        message = request.form['message']

        # Send an email to your desired recipients
        # Replace with your email address or a list of recipients
        recipients = ['johandrehdb@gmail.com', 'lnaude101@gmail.com']

        # Construct the HTML content for the email
        email_subject = 'Contact Form Submission'
        email_content = f"Name: {name}<br>Email: {email}<br>Message: {message}"

        try:
            send_email(email_subject, recipients, email_content)

            flash('Your message has been sent!', 'success')
            return redirect(url_for('contact'))

        except Exception as e:
            flash(
                'An error occurred while sending your message. Please try again later.', 'danger')
            print(f"Error occurred: {str(e)}")

    # Replace 'contact.html' with the actual template file
    return render_template('contact.html')


@app.route('/<string:page_name>')
def html_page(page_name):
    return render_template(page_name + '.html', current_page=page_name)


# Create a Flask application context
with app.app_context():
    # Create database tables
    db.create_all()

if __name__ == '__main__':
    app.run()
