import subprocess
from flask import redirect, url_for

def execute_file(folder, current_user):
    command = f"../folder_data/{current_user.username}/whole_genome_script_for_server.sh {folder.path}"
    command = f"screen -dm -S {folder.name} bash -c '{command}'"
    # Execute the command
    subprocess.run(command, shell=True, check=True)
    return redirect(url_for('get_folder'))