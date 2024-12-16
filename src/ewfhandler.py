"""
HIKVISION Video Data Recovery
Author: Dane Wullen
Date: 2024
Version: 0.2
NO WARRANTY, SOFWARE IS PROVIDED 'AS IS'


© 2024 Dane Wullen
"""

import pyewf

class EWFHandler:
    def __init__(self, filepath):
        self.file = pyewf.handle()
        self.file.open([filepath])

    def read(self, offset, size):
        self.seek(offset)
        return self.file.read(size)

    def seek(self, offset):
        self.file.seek(offset, 0)