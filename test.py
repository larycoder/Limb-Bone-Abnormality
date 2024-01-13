import subprocess
i
# path = "bash.sh"
# arg1 = "arg1"
# arg2 = "arg2"

# try:
#     subprocess.run(["bash", path, arg1, arg2])
#     print("Bash script executed successfully.")
# except subprocess.CalledProcessError as e:
#     print(f"Error executing Bash script: {e}")

# Define the command to execute the tool script with the "fatsq" file
command = "./bash.sh HG001.hiseq4000.wes_truseq.50x.R1.fastq.gz"

# Execute the command
subprocess.run(command, shell=True)
