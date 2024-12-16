"""
HIKVISION Video Data Recovery
Author: Dane Wullen
Date: 2024
Version: 0.2
NO WARRANTY, SOFWARE IS PROVIDED 'AS IS'


© 2024 Dane Wullen
"""

class PhysicalDiskHandler:
    def __init__(self, devicepath):
        self.file = open(devicepath, "rb")

    def read(self, offset, size):
        self.seek(offset)
        return self.file.read(size)

    def seek(self, offset):
        self.file.seek(offset, 0)

    def close(self):
        self.file.close()
