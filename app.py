import json
import shutil
from flask import Flask, jsonify, render_template, url_for, redirect, request, flash,send_file
from flask_login import login_required, logout_user, LoginManager, current_user, login_user
from function.connect import db
from function.models import User,Folder,File
from werkzeug.security import generate_password_hash, check_password_hash
import os
import pandas as pd

app = Flask(__name__)
app.config['SECRET_KEY'] = 'a secrect key'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///Account.db'
folder_data_dir = '../folder_data'
source_file_path="whole_genome_script_for_server.sh"

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
@app.route('/demo')
def demo():
    return render_template('demo.html')
@app.route('/pipeline')
def pipeline():
    return render_template('pipeline.html')
@app.route('/homepage')
def homepage():
    current_user.role=0
    return render_template('index.html')
@app.route('/ourstory')
def ourstory():
    return render_template('ourstory.html')
@app.route("/aboutus")
def about_us():
    return render_template('about_us.html')


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

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        user = User.query.filter_by(username=username).first()
        if user:
            if check_password_hash(user.password, password):
                role=user.role
                if role==2 or role==3:
                        flash('Logged in successfully!', category='success')
                        login_user(user, remember=False)
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
            folder_path = os.path.join(folder_data_dir, username)
            if not os.path.exists(folder_path):
                os.makedirs(folder_path)
                destination_folder_path=folder_path
                copy_and_paste_file(source_file_path, destination_folder_path)
            new_user = User(
                email=email,
                username=username,
                password=generate_password_hash(password, method='pbkdf2:sha256')
            )
            db.session.add(new_user)
            db.session.commit()
           
            flash('Sign up successful!', category='success')
            return redirect(url_for('login'))
    return render_template('sign_up.html')

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
                folder_path = os.path.join(f"{folder_data_dir}/{current_user.username}", folder_name)
                folder=Folder.query.filter_by(path=folder_path).first()
                if folder==None:

                    # Add folder to database
                    new_folder = Folder(path = folder_path,name= folder_name, user_id = current_user.id)
                    db.session.add(new_folder)
                    db.session.commit()
                    flash("Folder create successfully", category= 'success')
                else:
                    flash("Folder already exists",category='error')
                
    return redirect(url_for('home'))

@app.route('/folder/<folder_id>', methods=['GET', 'POST'])
@login_required
def get_folder(folder_id):
    folder = Folder.query.get_or_404(folder_id)
    file = File.query.filter_by(folder_id=folder.id).first()
    if request.method == 'POST':

        if 'inputFile1' in request.files:
            sub_file = request.files['inputFile1']
            
            if sub_file.filename != '':
                file_name=f"{folder.name}_1.fastq.gz"
                path=os.path.join(folder_data_dir, current_user.username)
                path+=f"/{file_name}"
                file=File.query.filter_by(path=path).first()
                if file==None:
                    # Save the uploaded file to the specified path
                    sub_file.save(path)

                    # Add the file to the database
                    new_file = File(name=file_name, path=path, user_id=current_user.id, folder_id=folder.id)
                    db.session.add(new_file)
                    db.session.commit()

                    flash('Subfile uploaded successfully!', category='success')

        if 'inputFile2' in request.files:
            sub_file = request.files['inputFile2']
            
            if sub_file.filename != '':
                file_name=f"{folder.name}_2.fastq.gz"
                path=os.path.join(folder_data_dir, current_user.username)
                path+=f"/{file_name}"
                file=File.query.filter_by(path=path).first()
                if file==None:
                    # Save the uploaded file to the specified path
                    sub_file.save(path)

                    # Add the file to the database
                    new_file = File(name=file_name, path=path, user_id=current_user.id, folder_id=folder.id)
                    db.session.add(new_file)
                    db.session.commit()

                    flash('Subfile uploaded successfully!', category='success')
    
    if os.path.exists(f"{folder.path}.indels.hg19_multianno.csv"):
        file=File.query.filter_by(name=f"{folder.name}.indels.hg19_multianno.csv").first()
        if file==None:
            output_file_path1=f"{folder.path}.indels.hg19_multianno.csv"
            output_file_path2=f"{folder.path}.SNPs.hg19_multianno.csv"
            new_file = File(name=f"{folder.name}.indels.hg19_multianno.csv", path=output_file_path1, user_id=current_user.id, folder_id=folder_id)
            db.session.add(new_file)
            new_file = File(name=f"{folder.name}.SNPs.hg19_multianno.csv", path=output_file_path2, user_id=current_user.id, folder_id=folder_id)
            db.session.add(new_file)
            db.session.commit()

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

@app.route('/file/<file_id>', methods = ['GET', 'POST'])
@login_required
def get_file(file_id):
    file = File.query.get_or_404(file_id)
    file_path = file.path

    df = pd.read_csv(file_path)
    if request.method == 'POST':
        # Take requests from form
        selected_columns = request.form.getlist('columns')
        
        # Create dataframe for all the columns have choosed
        selected_df=df[selected_columns]
        temp_file_path = f'{folder_data_dir}/{current_user.username}/temp_selected_data.csv'
        selected_df.to_csv(temp_file_path, index=False)
        selected_df=selected_df.head(20)

        # Conver dataframe to html
        table_html=selected_df.to_html(classes='table table-striped', index=False)

        # Send data to user
        return render_template('display_columns.html', table_html=table_html, columns=df.columns, user=current_user, file=file)
    return render_template('select_columns.html', columns=df.columns,user = current_user)
    
@app.route('/delete-subfile', methods=['POST'])
@login_required
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
                        flash('File deleted from folder successfully',category='success')
                        db.session.delete(file)
                        db.session.commit()
                    else:
                        flash('File not found in folder',category='error')
                else:
                    flash('File not found in folder',category='error')
            else:
                flash('You do not have permission to delete this file',category='error')
        else:
            raise ValueError('File not found')

        return jsonify({})
    except Exception as e:
        flash(f"Error deleting file: {e}",category='error')
        return jsonify({'Status': 'Error occurred while deleting the file.'}), 500
    
@app.route('/delete-folder', methods=['POST'])
@login_required
def delete_folder():
    try:
        event = json.loads(request.data)
        folder_id = event['Id']
        delete_folder_recursive(folder_id)
        flash('Delete successfully',category='success')
        return jsonify({'Status':'Success to delete folder'})
    except Exception as e:
        flash(f"Error deleting folder: {e}",category='error')
        return jsonify({'Status': 'Error occurred while deleting the folder.'}), 500

@app.route('/reset',methods=['POST','GET'])
@login_required
def reset():
    if request.method=='POST':
        password=request.form["password"]
        user=User.query.filter_by(username=current_user.username).first()
        if check_password_hash(user.password, password):
            return redirect(url_for('reset_password', email=user.email))
    return render_template("reset.html")

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

@app.route('/download/<file_id>',methods=['GET'])
@login_required
def download_file(file_id):
    return send_file(path_or_file=f"{folder_data_dir}/{current_user.username}/temp_selected_data.csv", as_attachment=True, mimetype="text/csv")
    
@app.route('/execute', methods = ['POST'])
@login_required
def execute_fatsq():
    from executing import execute_file
    event=json.loads(request.data)
    id=event['Id']
    folder=Folder.query.filter_by(id = id).first()
    try:
        execute_file(folder, current_user)
        return jsonify({"Status":"True"})
    except:
        return jsonify({"Status":"False"})

# Admin
@app.route('/admin', methods=['POST','GET'])
@login_required
def admin():
    admin=User.query.filter(User.role!=1).all()
    return render_template('admin.html',user=admin)

@app.route('/create_user',methods=['POST','GET'])
@login_required
def create_user():
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
            folder_path = os.path.join(folder_data_dir, username)
            if not os.path.exists(folder_path):
                os.makedirs(folder_path)
                source_file_path="whole_genome_script_for_server.sh"
                destination_folder_path=folder_path
                copy_and_paste_file(source_file_path, destination_folder_path)
            new_user = User(
                email=email,
                username=username,
                password=generate_password_hash(password, method='pbkdf2:sha256')
            )
            db.session.add(new_user)
            db.session.commit()

        return redirect(url_for('admin'))

    return render_template('add_user.html', user=current_user)

@app.route("/change_role", methods=["POST"])
@login_required
def change_role():
    try:
        user_data=json.loads(request.data)
        user_id=user_data['userId']
        user=User.query.filter_by(id=user_id).first()
        if user.role==2:
            user.role=3
        elif user.role==3:
            user.role=2
        db.session.commit()
        return jsonify({"Status":"Successfully"})
    except Exception as e:
        print(f"Error removing user: {e}")
        return jsonify({'error': 'An error occurred while removing the user.'}), 500

@app.route('/delete-user', methods=['POST'])
@login_required
def rm_user():
    try:
        user_data = json.loads(request.data)
        rm_user = user_data['userId']
        user_to_delete=User.query.filter_by(id=rm_user).first()
        file_to_delete=File.query.filter_by(user_id=rm_user).all()
        folder_to_delete=Folder.query.filter_by(user_id=rm_user).all()
        if user_to_delete:
            for file_obj in file_to_delete:
                db.session.delete(file_obj)
            for folder_obj in folder_to_delete:
                db.session.delete(folder_obj)
            db.session.delete(user_to_delete)
            db.session.commit()
            shutil.rmtree(f"{folder_data_dir}/{user_to_delete.username}")
            return jsonify({"Status":"Delete success"})
        else:
            raise ValueError(f"User with id {rm_user} not found")
    except Exception as e:
        flash("Error removing user: {e}",category='error')
        return jsonify({'Status': 'Error occurred while removing the user.'}), 500

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
        os.remove(file.path)
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
