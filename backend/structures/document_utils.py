"""
Shared utility functions and data
"""

__author__ = "Jason Beach"
__version__ = "0.1.0"
__license__ = "MIT"


import signal
from typing import Any


MAX_PAGE_EXTRACT = None
MAX_CONTENT_SIZE = 1e+8    #in bytes => 100MB
ALLOWED_EXTENSIONS = {'.zip'}


class timeout:
  """Timeout function after duration of seconds
  
  This uses `signal` and so is only useable on linux.
  
  Usage:
  with timeout(seconds=3):
    time.sleep(4)
  """
  def __init__(self, seconds=1, error_message='Timeout'):
        self.seconds = seconds
        self.error_message = error_message
  def handle_timeout(self, signum, frame):
        raise TimeoutError(self.error_message)
  def __enter__(self):
        signal.signal(signal.SIGALRM, self.handle_timeout)
        signal.alarm(self.seconds)
  def __exit__(self, type, value, traceback):
        signal.alarm(0)


def load_svg(filepath):
     """Load svg image from filepath."""
     image = ''
     with open(filepath, 'r') as f:
          image = f.read()
     return image