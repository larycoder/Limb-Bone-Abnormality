import json
import shutil
from flask import Flask, jsonify, render_template, url_for, redirect, request, flash,send_file
from flask_login import login_required, logout_user, LoginManager, current_user, login_user
from function.connect import db
from function.models import User,Folder,File
from werkzeug.security import generate_password_hash, check_password_hash
import os
import uuid

app = Flask(__name__)
app.config['SECRET_KEY'] = 'a secrect key'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///Account.db'
app.config['CREATE FOLDER FOR USER'] = '../folder_data'
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
            role=user.role
            if role==2:
                if check_password_hash(user.password, password):
                    flash('Logged in successfully!', category='success')
                    login_user(user, remember=True)
                    return redirect(url_for('home'))
                else:
                    flash('Incorrect password! Try again!', category='error')
            elif role==1:
                login_user(user,remember=False)
                return redirect(url_for("admin"))
        else:
            flash('User does not exist!', category='error')
    return render_template("login.html")

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
    print(f"folder: {folders}")
    files = File.query.filter_by(user_id = current_user.id).all()
    print(f"file: {files}")
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
    if request.method == 'POST':
        if 'folderName' in request.form:
            subfolder_name = request.form['folderName']
            if subfolder_name == '':
                flash('No folder name provided!', category='error')
            else:
                user_folder_path = f"{folder.path}"
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
            
            if sub_file.filename == '':
                flash("No file selected!", category='error')
            else:
                user_file_path = f"{folder.path}"
                print(f"file: {user_file_path}")
                file_path = os.path.join(user_file_path, sub_file.filename)

                # Save the uploaded file to the specified path
                sub_file.save(file_path)

                # Add the file to the database
                new_file = File(name=sub_file.filename, path=file_path, user_id=current_user.id, folder_id=folder.id)
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
                print(f"path: {user_file_path}")
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
    file_path = file.path

    with open(file_path, 'r', encoding='utf-8') as file_obj:
        file_contents = file_obj.read()
    return render_template('file.html', file=file, file_contents=file_contents)
    
@app.route('/file/<file_id>/updateFile', methods=['GET', 'POST'])
def updateFile(file_id):
    file=File.query.filter_by(id=file_id).first()
    print(f"file id: {file.id}")
    file_path=file.path
    data=json.loads(request.data)['data']
    with open(file_path,'w', encoding='utf-8') as file_obj:
        file_obj.write(data)
    return jsonify({})
    
# Admin
@app.route('/admin', methods=['POST','GET'])
def admin():
    admin=User.query.filter(User.role!=1).all()
    return render_template('admin.html',user=admin)

@app.route('/delete-user', methods=['POST'])
def rm_user():
    try:
        user_data = json.loads(request.data)
        rm_user = user_data['userId']
        print(f"User data: {user_data}")
        print(f"rm: {rm_user}")
        print(f"current user: {current_user}")
        print(f"current user name: {current_user.username}")
        print(f"role: {current_user.role}")
        if current_user.role==1:
            user_to_delete=User.query.filter_by(id=rm_user).first()
            file_to_delete=File.query.filter_by(user_id=rm_user).all()
            folder_to_delete=Folder.query.filter_by(user_id=rm_user).all()
            # print(f"user: {user_to_delete}")
            if user_to_delete:
                for file_obj in file_to_delete:
                    db.session.delete(file_obj)
                for folder_obj in folder_to_delete:
                    db.session.delete(folder_obj)
                db.session.delete(user_to_delete)
                db.session.commit()
                shutil.rmtree(f"../folder_data/{user_to_delete.username}")
                return jsonify({})
            else:
                raise ValueError(f"User with id {rm_user} not found")
        else:
            raise ValueError("You do not have permission to delete this user.")
    except Exception as e:
        print(f"Error removing user: {e}")
        return jsonify({'error': 'An error occurred while removing the user.'}), 500
    
@app.route('/delete', methods = ['POST'])
def delete():
    try:

        even = json.loads(request.data)
        id = even['Id']
        folder=Folder.query.filter_by(id = id, user_id=current_user.id).first()
        file = File.query.filter_by(id = id, user_id=current_user.id).first()
        if file:
            if file.user_id == current_user.id and file.folder_id is None:
                file_to_delete=file.path
                # Delete the file from the user's folder
                if os.path.exists(file_to_delete):
                    os.remove(file_to_delete)
                    print('File deleted from folder successfully')
                    # Delete the file entry from the database
                    db.session.delete(file)
                    db.session.commit()
                else:
                    print('File not found in folder')
        elif folder:
            if folder.user_id==current_user.id:
                folder_to_delete=folder.path
                if os.path.exists(folder_to_delete):
                    shutil.rmtree(folder_to_delete)
                    print('Folder deleted successfully')
                    db.session.delete(folder)
                    db.session.commit()
                else:
                    print('Folder can not find')

        else:
            raise ValueError("File not found")

        return jsonify({})
    except Exception as e:
        print(f"Error deleting file: {e}")
        return jsonify({'error': 'An error occurred while deleting the file.'}), 500
    
@app.route('/delete-subfile', methods=['POST'])
def delete_subfile():
    try:
        event = json.loads(request.data)
        file_id = event['Id']
        file = File.query.filter_by(id=file_id, user_id=current_user.id).first()

        if file:
            if file.user_id == current_user.id:
                folder = Folder.query.get(file.folder_id)
                if folder and is_file_in_folder(file, folder):
                    file_to_delete = file.path
                    if os.path.exists(file_to_delete):
                        os.remove(file_to_delete)
                        print('File deleted from folder successfully')
                        db.session.delete(file)
                        db.session.commit()
                    else:
                        print('File not found in folder')
                else:
                    print('You do not have permission to delete this file')
            else:
                print('You do not have permission to delete this file')
        else:
            raise ValueError('File not found')

        return jsonify({})
    except Exception as e:
        print(f"Error deleting file: {e}")
        return jsonify({'error': 'An error occurred while deleting the file.'}), 500
    
@app.route('/delete-folder', methods=['POST'])
def delete_folder():
    try:
        event = json.loads(request.data)
        folder_id = event['Id']
        delete_folder_recursive(folder_id)
    except Exception as e:
        print(f"Error deleting folder: {e}")
        return jsonify({'error': 'An error occurred while deleting the folder.'}), 500
    return jsonify({})

@app.route('/forgot', methods=['GET', 'POST'])
def forgot():
    if request.method == 'POST':
        email = request.form["email"]
        users = User.query.filter_by(email = email).first()
        if users:
            return redirect(url_for('reset_password', email=email))
        else:
            flash("The email does not match", category= 'error')
            return render_template('forgot.html')
    
    return render_template('forgot.html')

@app.route('/reset-password', methods=['GET', 'POST'])
def reset_password():
    email = request.args.get('email')
    
    if request.method == 'POST':
        # Handle the password reset form submission
        password = request.form['password']
        re_password = request.form['re-password']
        
        # Validate the password and re_password
        if password != re_password:
            flash('Passwords do not match!', category='error')
        elif len(password) < 7:
            flash('Password must be greater than 7 characters', category='error')
        else:
            # Update the user's password in the database
            user = User.query.filter_by(email=email).first()
            if user:
                hashed_password = generate_password_hash(password)
                user.password = hashed_password
                db.session.commit()
                flash("Your password has been reset successfully.", category='success')
                return redirect(url_for('login'))
            else:
                flash("User not found.", category='error')
    
    return render_template('reset_password.html', email=email)


def is_file_in_folder(file, folder):
    # Check if the file's folder matches the specified folder or any of its subfolders
    if file.folder_id == folder.id:
        return True
    elif folder.subfolders:
        for subfolder in folder.subfolders:
            if is_file_in_folder(file, subfolder):
                return True
    return False

def delete_folder_recursive(folder_id):
    folder = Folder.query.get(folder_id)
    if folder is None:
        return

    # Check if any subfolders have the same parent_folder_id as the current folder
    subfolders = Folder.query.filter_by(parent_folder_id=folder_id).all()
    for subfolder in subfolders:
        delete_folder_recursive(subfolder.id)

    # Delete files in the current folder
    delete_files_in_folder(folder.id)

    # Delete the current folder
    db.session.delete(folder)
    db.session.commit()

def delete_files_in_folder(folder_id):
    files = File.query.filter_by(folder_id=folder_id).all()
    for file in files:
        db.session.delete(file)
    db.session.commit()


if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(host='0.0.0.0', port=5000, debug=True)