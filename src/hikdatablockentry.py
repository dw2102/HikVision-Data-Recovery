"""
HIKVISION Video Data Recovery
Author: Dane Wullen
Date: 2024
Version: 0.2
NO WARRANTY, SOFWARE IS PROVIDED 'AS IS'


© 2024 Dane Wullen
"""

class HikDataBlockEntry:

    def __init__(self):
        self.unused = 0
        self.existence_of_file = 0
        self.channel = 0
        self.start_time = 0
        self.end_time = 0
        self.data_offset = 0
        self.unknown = 0

    def __str__(self):
        return ("File exsists: {}".format(self.existence_of_file) + "\n" +
        "Channel: {}".format(self.channel) + "\n" +
        "Start time: {}".format(self.start_time) + "\n" +
        "End time: {}".format(self.end_time) + "\n" +
        "Offset to datablock: {}".format(self.data_offset) + "\n")

    def __repr__(self):
       return self.__str__()

    def set_unused(self, unused):
        self.unused = unused

    def get_unused(self):
        return self.unused

    def set_existence_of_file(self, existence_of_file):
        self.existence_of_file = existence_of_file

    def get_existence_of_file(self):
        return self.existence_of_file

    def set_channel(self, channel):
        self.channel = channel

    def get_channel(self):
        return self.channel

    def set_start_end_time(self, start_end_time):
        self.start_end_time = start_end_time

    def get_start_end_time(self):
        return self.start_end_time

    def set_data_offset(self, data_offset):
        self.data_offset = data_offset

    def get_data_offset(self):
        return self.data_offset

    def set_unknown(self, unknown):
        self.unknown = unknown

    def get_unknown(self):
        return self.unknown