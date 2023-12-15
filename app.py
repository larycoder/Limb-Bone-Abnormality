from flask import Flask, render_template, url_for, redirect, request, flash,send_file
from flask_login import login_required, logout_user, LoginManager, current_user, login_user
from function.connect import db
from function.models import User,Folder,File
from werkzeug.security import generate_password_hash, check_password_hash
import os

app = Flask(__name__)
app.config['SECRET_KEY'] = 'a secrect key'
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:@localhost:3307/Account'
app.config['CREATE FOLDER FOR USER'] = 'C:/folder_data'
db.init_app(app)
login_manager = LoginManager()
login_manager.login_view = 'login'
login_manager.init_app(app)

@login_manager.user_loader
def load_user(id):
    return User.query.get(int(id))

@app.route('/')
def start():
    return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        
            username = request.form.get('username')
            password = request.form.get('password')
            user = User.query.filter_by(username=username).first()
            if user:
                if check_password_hash(user.password, password):
                    flash('Logged in successfully!', category='success')
                    login_user(user, remember=True)
                    return redirect(url_for('home'))
                else:
                    flash('Incorrect password! Try again!', category='error')
            else:
                flash('User does not exist!', category='error')
    return render_template("login.html", user=current_user)

@app.route('/sign-up', methods=['GET', 'POST'])
def sign_up():
    if request.method == 'POST':
        
            email = request.form.get('email')
            username = request.form.get('username')
            password = request.form.get('password')
            re_password = request.form.get('re-password')

            user = User.query.filter_by(username=username).first()
            if user:
                flash('Username already exists', category='error')
            elif len(email) < 4:
                flash('Email must be greater than 4 characters', category='error')
            elif len(username) < 2:
                flash('Username must be greater than 1 character', category='error')
            elif password != re_password:
                flash('Passwords do not match!', category='error')
            elif len(password) < 7:
                flash('Password must be greater than 7 characters', category='error')
            else:
                folder_path = os.path.join(app.config['CREATE FOLDER FOR USER'], username)
                if not os.path.exists(folder_path):
                    os.makedirs(folder_path)
                    print('Created folder successs')
                    print(folder_path)
                else:
                    print('Folder already exists')
                new_user = User(
                    email=email,
                    username=username,
                    password=generate_password_hash(password, method='pbkdf2:sha256')
                )
                db.session.add(new_user)
                db.session.commit()
                # Create a folder for the new user
                

                login_user(new_user, remember=True)
                flash('Sign up successful!', category='success')
                return redirect(url_for('login'))

    return render_template('sign_up.html', user=current_user)

@app.route('/home')
@login_required
def home():
    folders = Folder.query.filter_by(user_id=current_user.id).all()
    files = File.query.filter_by(user_id = current_user.id).all()
    return render_template("home.html",folders = folders, user = current_user, files = files)
@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))

@app.route('/folder', methods = ['POST'])
@login_required
def folder():
    if request.method == 'POST':
        if 'folderName' in request.form:
            folder_name = request.form['folderName']
            if folder_name == '':
                flash('No folder name provied!', category= 'error')
            else:
                user_folder_path = os.path.join(app.config['CREATE FOLDER FOR USER'], current_user.username)
                print(user_folder_path)
                if not os.path.exists(user_folder_path):
                    os.makedirs(user_folder_path)
                    print("Created folder successfully")
                else:
                    print("Folder already exists")

                #Create a folder name for user
                folder_path = os.path.join(user_folder_path, folder_name)
                os.makedirs(folder_path)

                # Add folder to database
                new_folder = Folder(path = folder_path,name= folder_name, user_id = current_user.id)
                db.session.add(new_folder)
                db.session.commit()

            
                flash("Folder create successfully", category= 'success')
                
    return redirect(url_for('home'))

@app.route('/folder/<folder_id>', methods=['GET', 'POST'])
@login_required
def get_folder(folder_id):
    folder = Folder.query.get_or_404(folder_id)
    file = File.query.filter_by(folder_id=folder.id).first()
    print(folder.id)
    

    if request.method == 'POST':
        if 'folderName' in request.form:
            subfolder_name = request.form['folderName']
            if subfolder_name == '':
                flash('No folder name provided!', category='error')
            else:
                user_folder_path = os.path.join(app.config['CREATE FOLDER FOR USER'], current_user.username)
                folder_path = os.path.join(user_folder_path, subfolder_name)

                if not os.path.exists(folder_path):
                    os.makedirs(folder_path)
                    print("Created subfolder successfully")
                else:
                    print("Subfolder already exists")

                # Add subfolder to the database
                new_folder = Folder(path=folder_path, name=subfolder_name, user_id=current_user.id, parent_folder_id = folder.id)
                db.session.add(new_folder)
                db.session.commit()

                flash("Subfolder created successfully", category='success')



        if 'inputFile' in request.files:
            sub_file = request.files['inputFile']
            print(sub_file.filename)

            if sub_file.filename == '':
                flash("No file selected!", category='error')
            else:
                user_file_path = os.path.join(app.config['CREATE FOLDER FOR USER'], current_user.username)
                subfolder_path = folder.path  # Get the subfolder path
                combined_path = os.path.join(user_file_path, subfolder_path)  # Combine user folder path and subfolder path
                file_path = os.path.join(combined_path, sub_file.filename)

                if not os.path.exists(combined_path):
                    os.makedirs(combined_path)

                # Save the uploaded file to the specified path
                sub_file.save(file_path)

                # Add the file to the database
                parent_folder_id = folder.parent_folder_id
                new_file = File(name=sub_file.filename, path=file_path, user_id=current_user.id, folder_id=parent_folder_id)
                db.session.add(new_file)
                db.session.commit()

                flash('Subfile uploaded successfully!', category='success')


    subfolders = Folder.query.filter_by(parent_folder_id=folder.id).all()
    subfiles = File.query.filter_by(folder_id=folder.id).all()
    return render_template('folder.html', folder=folder, subfolders=subfolders, file = file, subfiles = subfiles)
        

@app.route('/upload-file', methods=['POST', 'GET'])
@login_required
def upload_file():
    if request.method == 'POST':
        if 'inputFile' in request.files:
            file = request.files['inputFile']
            print(f"file: {file}")
            print(f"file name: {file.filename}")
            
            if file.filename == '':
                flash('No file selected!', category='error')
            else:
                # Create the user's folder path
                user_file_path = os.path.join(app.config['CREATE FOLDER FOR USER'], current_user.username)
                if os.path.exists(user_file_path):
                    # Save the uploaded file to the user's folder
                    file_path = os.path.join(user_file_path, file.filename)
                    print(file_path)
                    file.save(file_path)

                    # Add the file to the database
                    new_file = File(name=file.filename,path = file_path, user_id = current_user.id)
                    db.session.add(new_file)
                    db.session.commit()

            flash('File uploaded successfully!', category='success')
    return redirect(url_for('home'))

@app.route('/file/<file_id>', methods = ['GET', 'POST'])
@login_required
def get_file(file_id):
    file = File.query.get_or_404(file_id)
    print(file.folder.path)
    


if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(host='0.0.0.0', port=5000, debug=True)