import subprocess

path = "bash.sh"
arg1 = "arg1"
arg2 = "arg2"

try:
    subprocess.run(["bash", path, arg1, arg2])
    print("Bash script executed successfully.")
except subprocess.CalledProcessError as e:
    print(f"Error executing Bash script: {e}")
