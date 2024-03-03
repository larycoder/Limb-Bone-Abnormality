import subprocess

def execute_file(folder, current_user):
    print("Start to execute")
    command = f"../folder_data/{current_user.username}/whole_genome_script_for_server.sh {folder.path}"
    command = f"screen -dm -S {folder.name} bash -c '{command}'"
    # Execute the command
    subprocess.run(command, shell=True, check=True)