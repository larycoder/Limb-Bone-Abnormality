from flask import Flask, render_template, request, abort, jsonify, redirect, url_for
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity
import database as db

app = Flask(__name__)

# Set up Flask to use JWT
app.config['JWT_SECRET_KEY']='adminTest'
jwt=JWTManager(app)

@app.route('/')
def index():
    return redirect(url_for('sign_in'))

def check_login(username, password):
    if db.check(username, password):
        return True
    return False

@app.route('/login', methods=['POST'])
def login():
    username=request.form.get('username','')
    password=request.form.get('password','')
    status=False
    if check_login(username, password):
        status=True
    return render_template('main.html', data=jsonify({'username':username,'status':status}).get_json())

@app.route('/register', methods=['POST'])
def checkUser():
    username=request.form.get('username')
    if db.duplicate(username):
        return render_template('/')
    return redirect(url_for('sign_up'))
    
@app.route('/sign_up')
def sign_up():
    return render_template('sign_up.html')

@app.route('/sign_in')
def sign_in():
    return render_template('login.html')

@app.errorhandler(403)
def forbidden(e):
    return '403 You do not have permission to access'

@app.errorhandler(505)
def server_error(e):
    return '500 Internal Server Error'

@app.errorhandler(404)
def not_found(e):
    return "404 NOT FOUND"

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=2103)