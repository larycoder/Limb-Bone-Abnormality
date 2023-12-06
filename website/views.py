from flask import Blueprint, redirect, render_template,request,flash,jsonify
from werkzeug.security import generate_password_hash as generate_file
from flask_login import  login_required, current_user
from .models import File
from . import db
import json

views = Blueprint('views', __name__)

@views.route('/home', methods = ['GET', 'POST'])
@login_required
def home():
    if request.method == 'POST':
        file = request.files['inputFile'] 

        if not file or file.filename == '':
            flash('No file selected!', category='error')
        else:
            file_data = file.read()
            # file_data=generate_file(file_data, method='pbkdf2:sha256')
            # Add file into database
            new_file = File(data=file_data, user_id=current_user.id)
            db.session.add(new_file)
            db.session.commit()

            flash('File uploaded successfully!', category='success')

    return render_template('home.html', user=current_user)

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