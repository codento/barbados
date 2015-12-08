"""
Based on answer on stackoverflow:
http://stackoverflow.com/questions/1407474/does-python-logging-handlers-rotatingfilehandler-allow-creation-of-a-group-writa
"""

import os
import stat

import logging
from logging import handlers


class GroupWriteRotatingFileHandler(handlers.RotatingFileHandler):
    def _open(self):
        umask = os.umask(0o002)
        rtv = logging.handlers.RotatingFileHandler._open(self)
        os.umask(umask)
        return rtv

    def doRollover(self):
        """
        Override base class method to make the new log file group writable.
        """
        # Rotate the file first.
        handlers.RotatingFileHandler.doRollover(self)

        # Add group write to the current permissions.
        currMode = os.stat(self.baseFilename).st_mode
        os.chmod(self.baseFilename, currMode | stat.S_IWGRP)

