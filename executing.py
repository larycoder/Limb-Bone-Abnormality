import subprocess
from bs4 import BeautifulSoup

def execute_file(folder, current_user):
    command = f"../folder_data/{current_user.username}/whole_genome_script_for_server.sh {folder.path}"
    command = f"screen -dm -S {folder.name} bash -c '{command}'"
    # Execute the command
    subprocess.run(command, shell=True, check=True)
    read_html("templates/folder.html","non_color")
    
def check_screen_session(name):
    try:
        screen=subprocess.run(['screen','-list'], capture_output=True, text=True)
        return name in screen.stdout
    except Exception as e:
        print(f"Error: {e}")
        return False
    
def read_html(html_file, element_class):
    try:
        with open(html_file, 'r') as file:
            # Read the content of the HTML file
            html_content = file.read()

        # Parse the HTML content
        soup = BeautifulSoup(html_content, 'html.parser')

        # Find the element by its id
        element = soup.find(class_=element_class)

        # Check if the element is found
        if element:
            element['src']="../static/images/step2_color.png"
            return True
        else:
            return None

    except Exception as e:
        print(f"Error: {e}")
        return False
