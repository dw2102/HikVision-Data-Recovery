"""
HIKVISION Video Data Recovery
Author: Dane Wullen
Date: 2024
Version: 0.2
NO WARRANTY, SOFWARE IS PROVIDED 'AS IS'


© 2024 Dane Wullen
"""

class RawHandler:
    def __init__(self, filepath):
        self.file = open(filepath, "rb")

    def read(self, offset, size):
        self.seek(offset)
        return self.file.read(size)

    def seek(self, offset):
        self.file.seek(offset, 0)

    def close(self):
        self.file.close()
        