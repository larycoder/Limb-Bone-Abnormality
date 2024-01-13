import subprocess
import os
from function.models import File
from function.connect import db

def execute_test(folder, current_user):
    output_file_path = os.path.join(f"../folder_data/{current_user.username}",f"{folder.name}.csv")
    folder_id = folder.id
    command = f"../folder_data/{current_user.username}/whole_genome_script_for_server.sh {folder.name}"
    command = f"screen -dm -S {folder.name} bash -c '{command}'"
    # Execute the command
    subprocess.run(command, shell=True)
    
    # Add the output file to the database
    new_file = File(name=f"{folder.name}.csv", path=output_file_path, user_id=current_user.id, folder_id=folder_id)
    db.session.add(new_file)
    db.session.commit()