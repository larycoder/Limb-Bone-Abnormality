import subprocess
import os
from function.models import File
from function.connect import db

def execute_file(folder, current_user):
    folder_id = folder.id
    
    command = f"../folder_data/{current_user.username}/whole_genome_script_for_server.sh {folder.path}"
    command = f"screen -dm -S {folder.name} bash -c '{command}'"
    # Execute the command
    subprocess.run(command, shell=True, check=True)