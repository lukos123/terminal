import os
import time
from colorama import Fore,  Style
import shutil
from generate_javascript import generate_javascript
from subprocess import call
import stat
import subprocess
import psutil
import keyboard
def on_rm_error(func, path, exc_info):
        os.chmod(path, stat.S_IWRITE)
        os.unlink(path)
def ls(command, now_directory, minus):
    dirs = []
    files = []
    try:
        for i in os.listdir(now_directory):
            pathToDir = os.path.join(now_directory, i)
            if i != '.git':
                if os.path.isdir(pathToDir):

                    dirs.append([pathToDir, i])
                else:
                    files.append([pathToDir, i])
        for i in files:
            print(f'{Fore.GREEN}{minus}{Fore.CYAN}{i[1]}{Style.RESET_ALL}')
        for i in dirs:
            print(f'{Fore.GREEN}{minus}{Fore.YELLOW}{i[1]}{Style.RESET_ALL}')
            if len(command) == 2:
                if command[1] == 'a':
                    ls(command, i[0], '    '+minus)
    except Exception as p:
        pass


def git(command_global, path_to_git):
    command = []

    for i in command_global:
        if len(command_global) == 1:
            command.append('git')
            break
        if i != 'git':

            command.append(i)

    if command[0] == 'add':
        os.system(f'{path_to_git} add .')
        os.system(f'{path_to_git} status')
    elif command[0] == 'init':
        os.system(f'{path_to_git} init')
        os.system(f'echo "# {command[1]}" >> README.md')
        os.system(f'echo "" >> .gitignore')
    else:
        command_end = f'{path_to_git} '
        for i in command:
            command_end += f'{i} '

        os.system(command_end)


def html(command, now_directory, path_to_git):
    if command[1] == '!':
        if not os.path.exists('html-template'):
            os.system(
                f'{path_to_git} clone https://github.com/lukos123/html-template.git')
        dir = os.path.join(now_directory, "html-template")
        files = os.listdir(dir)
        for i in files:
            if i == '.git':
                while True:
                    call(['attrib', '-H', os.path.join(dir, i)])
                    break
                shutil.rmtree(os.path.join(dir, i), onerror=on_rm_error)
            elif i == '.gitignore':
                os.remove(os.path.join(dir, i))
            elif i == 'README.md':
                os.remove(os.path.join(dir, i))
            else:
                os.replace(os.path.join(dir, i),
                           os.path.join(now_directory, i))
        shutil.rmtree(os.path.join(now_directory, "html-template"))
    elif command[1] == 'js':
        if len(command) > 2:
            generate_javascript(command[2])
            print('generate javascript end')

def python(command, now_directory, path_to_python):
    if len(command) > 1:

        file_path = command[1]

        # Get the initial modification time of the file
        initial_mtime = os.stat(os.path.join(
            now_directory, file_path)).st_mtime
        current_pid = os.getpid()
        subprocess.Popen(
            [path_to_python, os.path.join(now_directory, file_path)])
        while True:
            # Get the current modification time of the file
            current_mtime = os.stat(os.path.join(
                now_directory, file_path)).st_mtime

            # Compare the modification time
            if current_mtime != initial_mtime:
                # File has been modified, find and kill the python process

                for process in psutil.process_iter():
                    try:
                        # print(process.name(), '|', process.cmdline())
                        if process.name() == 'python.exe':
                            for cmdline in process.cmdline():
                                # print(
                                #     cmdline+' | ' + os.path.join(now_directory, file_path))
                                if cmdline == os.path.join(now_directory, file_path):
                                    print('end')
                                    process.kill()
                    except Exception as er:
                        print(er)

                # Run the script again
                subprocess.Popen(
                    [path_to_python, os.path.join(now_directory, file_path)])

                # Update the initial modification time
                initial_mtime = current_mtime

        # Sleep for 1 second
            time.sleep(1)
            if keyboard.is_pressed('space'):
                for process in psutil.process_iter():
                    try:
                        
                        if process.name() == 'python.exe':
                            for cmdline in process.cmdline():
                                
                                if cmdline == os.path.join(now_directory, file_path):
                                    print('end')
                                    process.kill()
                                    subprocess.Popen(
                                        [path_to_python, os.path.join(now_directory, file_path)])
                    except Exception as er:
                        print(er)

            if keyboard.is_pressed('esc'):
                for process in psutil.process_iter():
                    try:
                        
                        if process.name() == 'python.exe':
                            for cmdline in process.cmdline():
                                
                                if cmdline == os.path.join(now_directory, file_path):
                                    print('end')
                                    process.kill()
                    except Exception as er:
                        print(er)
                break
    else:
        os.system(f'{path_to_python}')

def pip(command,pathToPip):
    commandEnd = ''
    if len(command) > 1:
        for i in command:
            if i == 'pip':
                commandEnd += f'{pathToPip} '
            else:
                commandEnd += f'{i} '

        os.system(commandEnd)
    else:

        os.system(f'{pathToPip}')

def py_installer(now_directory,  command, path_to_pyinstaller):
    if len(command) < 2:
        for n, i in enumerate(os.listdir(now_directory)):
            print(f'{n+1}:{i}')
        file = input('>>')
        try:
            os.system(
                            f'{path_to_pyinstaller} -F "{os.listdir(now_directory)[int(file)-1]}"')
            name_file = os.path.splitext(
                            os.listdir(now_directory)[int(file)-1])[0]

            os.replace(os.path.join(now_directory, f'dist\\{name_file}.exe'), os.path.join(
                            now_directory, f'{name_file}.exe'))
            while True:
                call(['attrib', '-H', os.path.join(now_directory, 'dist')])
                break
            shutil.rmtree(os.path.join(
                            now_directory, 'dist'), onerror=on_rm_error)
            while True:
                call(
                                ['attrib', '-H', os.path.join(now_directory, 'build')])
                break
            shutil.rmtree(os.path.join(
                            now_directory, 'build'), onerror=on_rm_error)
            os.remove(os.path.join(now_directory, f'{name_file}.spec'))
        except Exception as e:
            print(e)
    else:
        try:
                        # print(f'{path_to_pyinstaller} -F "{command[1]}"')
            os.system(
                            f'{path_to_pyinstaller} -F "{command[1]}"')

            name_file = os.path.splitext(command[1])[0]

            os.replace(os.path.join(now_directory, f'dist\\{name_file}.exe'), os.path.join(
                            now_directory, f'{name_file}.exe'))
            while True:
                call(['attrib', '-H', os.path.join(now_directory, 'dist')])
                break
            shutil.rmtree(os.path.join(
                            now_directory, 'dist'), onerror=on_rm_error)
            while True:
                call(
                                ['attrib', '-H', os.path.join(now_directory, 'build')])
                break
            shutil.rmtree(os.path.join(
                            now_directory, 'build'), onerror=on_rm_error)
            os.remove(os.path.join(now_directory, f'{name_file}.spec'))
        except Exception as e:
            print(e)

def new(now_directory):
    subprocess.Popen(
                    f'start cmd.exe /c start /B C:\\Users\\Kobyshev\\AppData\\Local\\Programs\\Python\\Python310\\python.exe C:/explorer/pythonGit.py {now_directory}', shell=True)