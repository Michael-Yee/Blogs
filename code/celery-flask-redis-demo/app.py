import os
import logging

from celery import Celery
from flask import Flask, request, render_template, session, redirect, url_for, jsonify
from flask_httpauth import HTTPBasicAuth
from flask_mail import Mail, Message
from werkzeug.security import generate_password_hash, check_password_hash

# Initialize Flask
app = Flask(__name__)
app.config['SECRET_KEY'] = 'Welcome123!'

# Initialize basic auth
auth = HTTPBasicAuth()

# Celery configuration
app.config['CELERY_BROKER_URL'] = 'redis://localhost:6379/0'
app.config['CELERY_RESULT_BACKEND'] = 'redis://localhost:6379/0'

# Initialize Celery
celery = Celery(app.name, broker=app.config['CELERY_BROKER_URL'])

# Flask-Mail configuration
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USE_SSL'] = True
app.config['MAIL_USERNAME'] = os.environ.get('MAIL_USERNAME')
app.config['MAIL_PASSWORD'] = os.environ.get('MAIL_PASSWORD')
app.config['MAIL_DEFAULT_SENDER'] = 'donation@receipt.com'

# Initialize Mail
mail = Mail(app)

# Initialize Logger
logging.basicConfig(filename = 'app.log', format='%(asctime)s - %(message)s', level=logging.INFO)
log = logging.getLogger(__name__)


users = {
    "mike": generate_password_hash("yee"),
}


@auth.verify_password
def verify_password(username, password):
    if username in users and \
            check_password_hash(users.get(username), password):
        return username


def create_pdf():
    pass


def get_pdf_path():
    pass


@celery.task(bind=True)
def send_async_email(self, email_data):
    # Background task to send an email with Flask-Mail
    msg = Message(subject=email_data['subject'],
                  sender=app.config['MAIL_DEFAULT_SENDER'],
                  recipients=[email_data['to']])
    msg.body = email_data['body']
    with app.open_resource('receipts/example.jpg') as fp:
        msg.attach('donation_receipt.jpeg', 'image/jpeg', fp.read())
    with app.app_context():
        mail.send(msg)


@app.route('/ping')
def ping():
    return jsonify({'ping': 'pong'})


@app.route('/', methods=['GET', 'POST'])
@auth.login_required
def index():
    if request.method == 'GET':
        return render_template('index.html', email=session.get('email', ''))
    email = request.form['email']
    session['email'] = email

    # send the email
    email_data = {
        'subject': 'Donation Receipt',
        'to': email,
        'body': 'Thank you for your donation.'
    }
    send_async_email.delay(email_data)
    log.info('Sent donation receipt to email: {email}'.format(email=email_data['to']))

    return redirect(url_for('index'))


@app.route('/status/<task_id>')
@auth.login_required
def taskstatus(task_id):
    task = send_async_email.AsyncResult(task_id)
    if task.state == 'PENDING':
        response = {
            'state': task.state,
            'current': 0,
            'total': 1,
            'status': 'Pending...'
        }
    elif task.state != 'FAILURE':
        response = {
            'state': task.state,
            'current': task.info.get('current', 0),
            'total': task.info.get('total', 1),
            'status': task.info.get('status', '')
        }
        if 'result' in task.info:
            response['result'] = task.info['result']
    else:
        # something went wrong in the background job
        response = {
            'state': task.state,
            'current': 1,
            'total': 1,
            'status': str(task.info),  # this is the exception raised
        }
    return jsonify(response)


if __name__ == '__main__':
    app.run(debug=True)
