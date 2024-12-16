"""
HIKVISION Video Data Recovery
Author: Dane Wullen
Date: 2024
Version: 0.2
NO WARRANTY, SOFWARE IS PROVIDED 'AS IS'


© 2024 Dane Wullen
"""

import os
from .ewfhandler import EWFHandler
from .physicaldiskhandler import PhysicalDiskHandler
from .rawhandler import RawHandler


class DiskImage:
    def __init__(self, filepath):
        self.filepath = filepath
        self.handler = None
        self.offset = 0

        if self.filepath.lower().endswith(".e01"):
            self.handler = EWFHandler(filepath)
        elif self.filepath.startswith("/dev/") or self.filepath.startswith("\\\\.\\PhysicalDrive"):
            self.handler = PhysicalDiskHandler(filepath)
        else:
            self.handler = RawHandler(filepath)

    def read(self, size):
        data = self.handler.read(self.offset, size)
        self.offset += size
        self.seek(self.offset)
        return data

    def seek(self, offset, whence=os.SEEK_SET):
        self.offset = offset
        self.handler.seek(self.offset)

    def skip(self, bytes):
        self.offset += bytes
        self.handler.seek(self.offset)

    def close(self):
        self.handler.close()
