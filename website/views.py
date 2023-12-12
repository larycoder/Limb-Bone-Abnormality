from flask import Blueprint, redirect, render_template,request,flash,jsonify,url_for,abort,send_file
from werkzeug.security import generate_password_hash as generate_file
from flask_login import  login_required, current_user
from .models import File,Folder,User
from . import db
import json
import os
import shutil
import datetime as dt
import pathlib
from werkzeug.utils import safe_join
views = Blueprint('views', __name__)
@views.route('/home', methods = ['GET', 'POST'],defaults = {"reqPath": ""})
@views.route("/home/<path:reqPath>")
@login_required
def home(reqPath):
    
    if request.method == 'POST':
        # Check if the folder name is provided
        if 'folderName' in request.form:
            folder_name = request.form['folderName']
            if folder_name == '':
                flash('No folder name provided!', category='error')
            else:
                # Create the user's folder path
                user_folder_path = os.path.join('C:/folder_data', current_user.folder_user)
                if not os.path.exists(user_folder_path):
                    os.makedirs(user_folder_path)
                    print('Created folder successfully')
                else:
                    print('Folder already exists')

                # Create the new folder
                folder_path = os.path.join(user_folder_path, folder_name)
                os.makedirs(folder_path)

                # Add the folder to the database
                new_folder = Folder(name=folder_name, path=folder_path, user_id=current_user.id)
                db.session.add(new_folder)
                db.session.commit()
            flash('Folder create successfully!', category= 'success')
         # Check if the folder exists
        if 'inputFile' in request.files:
            file = request.files['inputFile']
            if file.filename == '':
                flash('No file selected!', category='error')
            else:
                # Create the user's folder path
                user_file_path = os.path.join('C:/folder_data', current_user.folder_user)
                if not os.path.exists(user_file_path):
                    os.makedirs(user_file_path)
                    print('Created user folder successfully')
                else:
                    print('User folder already exists')

                # Save the uploaded file to the user's folder
                file_path = os.path.join(user_file_path, file.filename)
                file.save(file_path)

                # Add the file to the database
                new_file = File(data=file.filename,path = file_path ,user_id=current_user.id)
                db.session.add(new_file)
                db.session.commit()

            flash('File uploaded successfully!', category='success')
         # Fetch user's folders and files from the database
    folders = Folder.query.filter_by(user_id=current_user.id).all()
    # print(f"folder: {folders}")
    # print("Hello Na")
    files = File.query.filter_by(user_id=current_user.id).all()
    def fObjFromScan(x):
        fIcon = 'bi bi-folder-fill' if os.path.isdir(x.path) else getIconClassForFileName(x.name)
        fileStat = x.stat()
        fBytes = getReadableByteSize(fileStat.st_size)
        fTime = getTimeStampString(fileStat.st_mtime)
        return {
            'name': x.name,
            'size': fBytes,
            'mTime': fTime,
            'fIcon': fIcon,
            'fLink': url_for('views.home', reqPath=os.path.relpath(x.path, name_path)).replace("\\", "/")
        }
    
    name_path = pathlib.Path('C:/folder_data') / current_user.folder_user
    absPath = safe_join(name_path, reqPath)


    if not os.path.exists(absPath):
        abort(404)

    if os.path.isfile(absPath):
        return send_file(absPath)

    name_folder = [fObjFromScan(x) for x in os.scandir(absPath)]
    # print(f"file: {files}")
    return render_template('home.html', user=current_user, folders=folders, files=files , name_folder = name_folder)



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
                # Delete the file from the user's folder
                if os.path.exists(file.data):
                    os.remove(file.data)
                    print('File deleted from folder successfully')
                else:
                    print('File not found in folder')

                # Delete the file entry from the database
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
                if os.path.exists(folder.path):
                    shutil.rmtree(folder.path)
                    print("Remove folder successfully")
                else:
                    print("Folder not found!")
                db.session.delete(folder)
                db.session.commit()
        else:
            raise ValueError("Folder not found")

        return jsonify({})
    except Exception as e:
        print(f"Error deleting folder: {e}")
        return jsonify({'error': 'An error occurred while deleting the folder.'}), 500
    



def getTimeStampString(tSec: float) -> str:
    tObj = dt.datetime.fromtimestamp(tSec)
    tStr = dt.datetime.strftime(tObj, '%Y-%m-%d %H:%M:%S')
    return tStr
def getReadableByteSize(num, suffix = 'B') -> str:
    for unit in ['', 'K', 'M', 'G', 'T', 'P', 'E', 'Z']:
        if abs(num) < 1024.0:
            return "%3.1f%s%s" % (num,unit,suffix)
        num /= 1024.0
    return "%.1f%s%s" % (num, 'Y', suffix)
def getIconClassForFileName(fName):
    fileExt = pathlib.Path(fName).suffix
    fileExt = fileExt[1:] if fileExt.startswith(".") else fileExt
    fileTypes = ["txt"]
    fileIconClass = f"bi bi-filetype-{fileExt}" if fileExt in fileTypes else "bi bi-file-earmark"
    return fileIconClass