from flask import Flask, request, render_template, redirect, session, make_response, url_for
import secrets
import re
import os
import uuid

from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from selenium import webdriver
from selenium.common.exceptions import InvalidArgumentException, WebDriverException

app = Flask(__name__)
app.secret_key = secrets.token_bytes()

CHAL = {
    'domain': os.getenv('HOSTNAME', 'localhost:24013'),
}

messages = {}

NAUGHTY_PATTERN = re.compile('<.*((script)|img).*>', re.IGNORECASE)

# Route for handling the login page logic
@app.route('/', methods=['GET', 'POST'])
def login():
    hint = None
    if request.method == 'POST':
        if request.form.get('username') == 'uwustudent' and request.form.get('password') == 'uwuuwu':
            session['username'] = 'uwustudent'
            return redirect('/send')
        elif request.form.get('username') and request.form.get('password'):
            hint = 'Invalid credentials. Please try again.'
        else:
            hint = 'Please fill in the credentials and try again.'
    return render_template('index.html', hint=hint)

@app.route('/send', methods=['GET', 'POST'])
def new_message():
    if session.get('username') != 'uwustudent':
        return redirect('/')
    if request.method == 'GET':
        return render_template('send_message.html')
    elif request.method == 'POST':
        message = request.form.get('message')
        hint = None
        message_url = None
        if re.match(NAUGHTY_PATTERN, message):
            hint = 'You are too naughty! The principal will not read your messages!'
        elif not message:
            hint = 'Please enter something before submitting your messages.'
        else:
            message_id = uuid.uuid4()
            messages[message_id] = message
            message_url = url_for('show_message', id=message_id)
            hint = 'Your message has been delivered to the principal.'
        return render_template('send_message.html', hint=hint, message_url=message_url, host=request.host)

@app.route('/messages/<uuid:id>', methods=['GET'])
def show_message(id):
    if request.remote_addr != '127.0.0.1':
        return make_response('Only the principal can view the messages!', 403)
    message = messages.get(id)
    if not message:
        return make_response('No such message!', 404)
    return render_template('message.html', message=message)

@app.route('/logout', methods=['GET'])
def logout():
    if 'username' in session:
        del session['username']
    return redirect('/')

limiter = Limiter(
    get_remote_address,
    app=app,
    default_limits=[],
    storage_uri='memory://',
)

CHROME_ARGS = [
    '--headless=old',
    '--disable-dev-shm-usage',
    '--no-sandbox',
    '--disable-setuid-sandbox',
    '--disable-gpu',
    '--no-gpu',
    '--disable-default-apps',
    '--disable-translate',
    '--disable-device-discovery-notifications',
    '--disable-software-rasterizer',
    '--disable-xss-auditor',
]

@app.route('/visit', methods=['GET'])
def visit_get():
    return render_template('visit.html')

@app.route('/visit', methods=['POST'])
@limiter.limit('1 per 20 seconds')
def visit():
    url = request.form.get('url')
    if url:
        options = webdriver.ChromeOptions()
        for arg in CHROME_ARGS:
            options.add_argument(arg)
        driver = webdriver.Chrome(options=options)
        try:
            try:
                with open('flag', 'r') as f:
                    flag = f.readline()
            except FileNotFoundError:
                return make_response('Flag does not exist! Please contact us on Discord ASAP.', 500)
            driver.get('http://'+CHAL['domain']+'/')
            driver.add_cookie({'name': 'super_secret', 'value': flag,})
            driver.get(url)
            driver.set_page_load_timeout(10)
        except InvalidArgumentException:
            return render_template('visit.html', hint='Please enter a URL!')
        except WebDriverException as e:
            return render_template('visit.html', hint=f'Something went wrong: {e.msg}')
        else:
            return render_template('visit.html', hint='Your URL has been visited.')
        finally:
            driver.quit()
    else:
        return render_template('visit.html', hint='No URL given!')
