import subprocess
import os

def node_init():
    # start command(npm run dev) via python module

    # get current working directory
    current_path = os.path.dirname(os.path.abspath(__file__))

    # build full path
    command = 'npm run dev'
    command_path = os.path.join(current_path, command)

    # use subprocess to run command
    process = subprocess.Popen(command_path, shell=True)

    # no need to await the process
    # process.wait()

    # when process killed, kill the process which is running node
    @atexit.register
    def terminate_process():
        process.terminate()
