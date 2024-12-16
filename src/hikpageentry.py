"""
HIKVISION Video Data Recovery
Author: Dane Wullen
Date: 2024
Version: 0.2
NO WARRANTY, SOFWARE IS PROVIDED 'AS IS'


© 2024 Dane Wullen
"""

import datetime

class HikPageEntry:

    def __init__(self):
        self.offset_to_page = 0
        self.channel = 0
        self.start_time = 0
        self.end_time = 0
        self.data_offset = 0
        self.data_blocks = []

    def __str__(self):
        return ("Offset to page: {}".format(self.offset_to_page) + "\n" +
        "Channel: {}".format(self.channel) + "\n" +
        "Start time: {}".format(datetime.datetime.utcfromtimestamp(self.start_time).strftime('%Y-%m-%d_%H-%M-%S')) + "\n" +
        "End time: {}".format(datetime.datetime.utcfromtimestamp(self.end_time).strftime('%Y-%m-%d_%H-%M-%S')) + "\n" +
        "Offset to datablock: {}".format(self.data_offset) + "\n" +
        "Total datablocks: {}".format("\n" + str(self.data_blocks)))

    def __repr__(self):
        return str(self)

    def set_offset_to_page(self, offset_to_page):
        self.offset_to_page = offset_to_page

    def get_offset_to_page(self):
        return self.offset_to_page

    def set_channel(self, channel):
        self.channel = channel

    def get_channel(self):
        return self.channel

    def set_start_end_time(self, start_end_time):
        self.start_end_time = start_end_time

    def get_start_end_time(self):
        return self.start_end_time

    def set_end_time(self, end_time):
        self.end_time = end_time

    def get_end_time(self):
        return self.end_time

    def set_data_offset(self, data_offset):
        self.data_offset = data_offset

    def get_data_offset(self):
        return self.data_offset

    def append_data_block(self, data_block):
        self.data_blocks.append(data_block)