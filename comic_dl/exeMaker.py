import subprocess

command = 'pyinstaller --onefile --hidden-import=queue --icon="Logo.ico" "__main__.py"'
print(command)
subprocess.call(command)