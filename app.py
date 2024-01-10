import json
import shutil
from flask import Flask, jsonify, render_template, url_for, redirect, request, flash,send_file
from flask_login import login_required, logout_user, LoginManager, current_user, login_user
from function.connect import db
from function.models import User,Folder,File
from werkzeug.security import generate_password_hash, check_password_hash
import os
import subprocess
import pandas as pd

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
    return redirect(url_for('homepage'))

@app.route('/homepage')
def homepage():
    return render_template('index.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        user = User.query.filter_by(username=username).first()
        if user:
            if check_password_hash(user.password, password):
                role=user.role
                if role==2:
                        flash('Logged in successfully!', category='success')
                        login_user(user, remember=True)
                        return redirect(url_for('home'))
                elif role==1:
                    login_user(user,remember=False)
                    return redirect(url_for("admin"))
            else:
                flash('Incorrect password! Try again!', category='error')
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
                    source_file_path="whole_genome_script_for_server.sh"
                    destination_folder_path=folder_path
                    copy_and_paste_file(source_file_path, destination_folder_path)
                    source_file_path="hg38.fa"
                    copy_and_paste_file(source_file_path, destination_folder_path)
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
    flash("Log out success")
    return redirect(url_for('homepage'))

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
                if not os.path.exists(user_folder_path):
                    os.makedirs(user_folder_path)
                    print("Created folder successfully")
                else:
                    print("Folder already exists")

                #Create a folder name for user
                folder_path = os.path.join(user_folder_path, folder_name)

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

        if 'inputFile1' in request.files:
            sub_file = request.files['inputFile1']
            
            if sub_file.filename == '':
                flash("No file selected!", category='error')
            else:
                file_name=f"{folder.name}_1.fastq.gz"
                path=os.path.join(app.config['CREATE FOLDER FOR USER'], current_user.username)
                path+=f"/{file_name}"
                # Save the uploaded file to the specified path
                sub_file.save(path)

                # Add the file to the database
                new_file = File(name=file_name, path=path, user_id=current_user.id, folder_id=folder.id)
                db.session.add(new_file)
                db.session.commit()

                flash('Subfile uploaded successfully!', category='success')

        if 'inputFile2' in request.files:
            sub_file = request.files['inputFile2']
            
            if sub_file.filename == '':
                flash("No file selected!", category='error')
            else:
                file_name=f"{folder.name}_2.fastq.gz"
                path=os.path.join(app.config['CREATE FOLDER FOR USER'], current_user.username)
                path+=f"/{file_name}"
                # Save the uploaded file to the specified path
                sub_file.save(path)

                # Add the file to the database
                new_file = File(name=file_name, path=path, user_id=current_user.id, folder_id=folder.id)
                db.session.add(new_file)
                db.session.commit()

                flash('Subfile uploaded successfully!', category='success')


    subfolders = Folder.query.filter_by(parent_folder_id=folder.id).all()
    subfiles = File.query.filter_by(folder_id=folder.id).all()
    output=[]
    files=[]
    for file in subfiles:
        if file.name.endswith(".csv"):
            output.append(file)
        else:
            files.append(file)
    return render_template('folder.html', folder=folder, subfolders=subfolders, file = file, subfiles = files, output=output, user = current_user)
        
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

    df = pd.read_csv(file_path)
    if request.method == 'POST':
        # Lấy danh sách các cột được chọn từ form
        selected_columns = request.form.getlist('columns')

        # Tạo DataFrame mới chỉ với các cột được chọn
        selected_df = df[selected_columns]
        selected_df=selected_df.head(20)

        # Chuyển đổi DataFrame thành HTML
        table_html = selected_df.to_html(classes='table table-striped', index=False)

        # Render template với dữ liệu HTML
        return render_template('display_columns.html', table_html=table_html, columns=df.columns, user = current_user, file = file)

    # Nếu là request GET, hiển thị form chọn cột
    return render_template('select_columns.html', columns=df.columns,user = current_user)


    
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

@app.route('/download/<file_id>')
def download_file(file_id):
    file = File.query.get_or_404(file_id)
    file_path = file.path
    print(file_path)
    return send_file(file_path, as_attachment=True, mimetype='application/pdf')

@app.route('/execute', methods = ['POST'])
def execute_fatsq():
    event = json.loads(request.data)
    id = event['Id']
    folder = Folder.query.filter_by(id = id).first()
    files = File.query.filter_by(folder_id = folder.id).order_by(File.name).all()

    file_names = []
    for file in files:
        file_names.append(file.path)
    if len(file_names) >= 2:
        file1_name = file_names[0].split("_1")
        file2_name = file_names[1].split("_2")
    else:
        # Handle case when there are not enough files
        return jsonify({"error": "Not enough files in the folder"})
    
    output_file_path = os.path.join(f"{app.config['CREATE FOLDER FOR USER']}/{current_user.username}",f"{folder.name}.csv")
    folder_id = folder.id
    command = f"{app.config['CREATE FOLDER FOR USER']}/{current_user.username}/whole_genome_script_for_server.sh {file1_name[0]} {file2_name[0]} > {output_file_path}"

    # Execute the command
    subprocess.run(command, shell=True)
    
    # Add the output file to the database
    new_file = File(name=f"{folder.name}.csv", path=output_file_path, user_id=current_user.id, folder_id=folder_id)
    db.session.add(new_file)
    db.session.commit()
    return jsonify({"success": True})

@app.route('/upload')
def upload():
    return render_template('upload_file.html', user = current_user)
@app.route('/sub-upload/<folder_id>')
def subupload(folder_id):
    folder = Folder.query.get_or_404(folder_id)
    return render_template('upload_subfile.html', user = current_user, folder = folder)

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
    folder = Folder.query.filter_by(id=folder_id).first()
    if folder is None:
        return jsonify({"Status":"Fail"})

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

def copy_and_paste_file(source_file, destination_folder):
    try:
        if os.path.isfile(source_file):
            if not os.path.exists(destination_folder):
                os.makedirs(destination_folder)

            # create full path to the right dictionary 
            destination_path = os.path.join(destination_folder, os.path.basename(source_file))

            # Paste to the folder path
            shutil.copy2(source_file, destination_path)

            print("Create file successfully")
        else:
            print("Fail to create a file")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(host='0.0.0.0', port=5000, debug=True)
