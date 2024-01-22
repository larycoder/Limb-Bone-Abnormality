import subprocess
import os
from function.models import File
from function.connect import db

def execute_file(folder, current_user):
    folder_id = folder.id
    
    command = f"../folder_data/{current_user.username}/whole_genome_script_for_server.sh {folder.path}"
    command = f"screen -dm -S {folder.name} bash -c '{command}'"
    # Execute the command
    subprocess.run(command, shell=True)
    
    output_file_path1=f"{folder.path}.indels.hg19_multianno.csv"
    output_file_path2=f"{folder.path}.SNPs.hg19_multianno.csv"
    new_file = File(name=f"{folder.name}.indels.hg19_multianno.csv", path=output_file_path1, user_id=current_user.id, folder_id=folder_id)
    db.session.add(new_file)
    new_file = File(name=f"{folder.name}.SNPs.hg19_multianno.csv", path=output_file_path2, user_id=current_user.id, folder_id=folder_id)
    db.session.add(new_file)
    db.session.commit()