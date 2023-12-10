from flask import Blueprint, redirect, render_template,request,flash,jsonify
from werkzeug.security import generate_password_hash as generate_file
from flask_login import  login_required, current_user
from .models import File,Folder,User
from . import db
import json

views = Blueprint('views', __name__)

@views.route('/home', methods = ['GET', 'POST'])
@login_required
def home():
    if request.method == 'POST':
        # Check if the folder exists
        if 'folderName' in request.form:
            folder_name = request.form['folderName']
            # folder_path = f"Limb-Bone-Abnormality/User_data/{folder_name}"
            # Create new folder
            new_folder = Folder(name = folder_name, path = folder_name, user_id = current_user.id)
            db.session.add(new_folder)
            db.session.commit()
            flash('Folder create successfully!', category= 'success')
        # Check if the file exists
        if 'inputFile' in request.files:
            file = request.files['inputFile']
            folder_id = int(request.form['folderId'])
            file_data = file.read()
            file_data = generate_file(file_data, method='pbkdf2:sha256')

        # file = request.files['inputFile'] 

        # file_data = file.read()
        # file_data=generate_file(file_data, method='pbkdf2:sha256')

            # Add file into database
            new_file = File(data=file_data, user_id=current_user.id, folder_id = folder_id)
            db.session.add(new_file)
            db.session.commit()

            flash('File uploaded successfully!', category='success')
         # Fetch user's folders and files from the database
    folders = Folder.query.filter_by(user_id=current_user.id).all()
    # print(f"folder: {folders}")
    # print("Hello Na")
    files = File.query.filter_by(user_id=current_user.id).all()
    # print(f"file: {files}")
    return render_template('home.html', user=current_user, folders=folders, files=files)

@views.route('/admin')
@login_required
def admin():
    admin=User.query.filter(User.role!=1).all()
    return render_template('admin.html',user=admin)

@views.route('/delete-file', methods=['POST'])
def delete_file():
    try:
        file = json.loads(request.data)
        fileId = file['fileId']
        file = File.query.get(fileId)
        if file:
            if file.user_id == current_user.id:
                db.session.delete(file)
                db.session.commit()
        else:
            raise ValueError("File not found")

        return jsonify({})
    except Exception as e:
        print(f"Error deleting file: {e}")
        return jsonify({'error': 'An error occurred while deleting the file.'}), 500
    
@views.route('/delete-user', methods=['POST'])
def rm_user():
    try:
        user_data = json.loads(request.data)
        rm_user = user_data['userId']
        # print(f"User+data: {user_data}")
        # print(f"rm: {rm_user}")
        if current_user.role==1:
            user_to_delete=User.query.get(rm_user)
            # print(f"user: {user_to_delete}")
            if user_to_delete:
                # db.session.delete(user_to_delete)
                # db.session.commit()
                db.session.delete(user_to_delete)
                db.session.commit()
                return jsonify({})
            else:
                raise ValueError(f"User with id {rm_user} not found")
        else:
            raise ValueError("You do not have permission to delete this user.")
    except Exception as e:
        print(f"Error removing user: {e}")
        return jsonify({'error': 'An error occurred while removing the user.'}), 500
    
@views.route('/delete-folder', methods=['POST'])
def delete_folder():
    try:
        folder = json.loads(request.data)
        folder_id = folder['folderId']
        folder = Folder.query.get(folder_id)
        if folder:
            if folder.user_id == current_user.id:
                db.session.delete(folder)
                db.session.commit()
        else:
            raise ValueError("Folder not found")

        return jsonify({})
    except Exception as e:
        print(f"Error deleting folder: {e}")
        return jsonify({'error': 'An error occurred while deleting the folder.'}), 500