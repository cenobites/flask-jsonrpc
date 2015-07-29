import os
import sys
import time
import subprocess


class FlaskTestServer(object):

    def __init__(self):
        self.process = None

    def __enter__(self):
        return self.run()

    def __exit__(self, type, value, traceback):
        self.kill()

    def run(self):
        if not self.process is None:
            try:
                self.kill()
            except OSError:
                pass
        exe =  os.path.join(os.path.dirname(os.path.abspath(__file__)), 'apptest.py')
        self.process = subprocess.Popen([sys.executable, exe, '--run'])
        time.sleep(1)
        return self.process

    def kill(self, process=None):
        process = process if not process is None else self.process
        if not process is None and not process.poll() is None:
            process.wait()
            process.terminate()
            time.sleep(1)
            if not process.poll() is None:
                process.kill()
        if not process is None and process.poll() is None:
            process.kill()
            time.sleep(1)
        self.process = None

flask_server = FlaskTestServer()
