"""
HIKVISION Video Data Recovery
Author: Dane Wullen
Date: 2024
Version: 0.2
NO WARRANTY, SOFWARE IS PROVIDED 'AS IS'


© 2024 Dane Wullen
"""

class HikMasterSector:

    def __init__(self):
        self.signatur = ""
        self.hdd_cap = 0
        self.sys_log_offset = 0
        self.sys_log_size = 0
        self.video_data_area_offset = 0
        self.data_block_size = 0
        self.data_block_total = 0
        self.hikbtree1_offset = 0
        self.hikbtree2_offset = 0
        self.hikbtree1_size = 0
        self.hikbtree2_size = 0
        self.init_time = 0

    def __str__(self):
        return ("Signature: {}".format(self.signatur) + "\n" +
        "Hard disk size: {}".format(self.hdd_cap) + "\n" +
        "Offset to system logs: {}".format(self.sys_log_offset) + "\n" +
        "System log size: {}".format(self.sys_log_size) + "\n" +
        "Offset to video data area: {}".format(self.video_data_area_offset) + "\n" +
        "Video datablock size: {}".format(self.data_block_size) + "\n" +
        "Total video datablocks: {}".format(self.data_block_total) + "\n" +
        "Offset to HIKBTREE 1: {}".format(self.hikbtree1_offset) + "\n" +
        "HIKBTREE 1 size: {}".format(self.hikbtree1_size) + "\n" +
        "Offset to HIKBTREE 2: {}".format(self.hikbtree2_offset) + "\n" +
        "HIKBTREE 2 size: {}".format(self.hikbtree2_size) + "\n" +
        "System init: {}".format(self.init_time) + "\n")


    def check_signatur(self):
        if "HIKVISION@HANGZHOU" not in self.signatur:
           return False
        return True

    def set_hdd_cap(self, hdd_cap):
        self.hdd_cap = hdd_cap

    def get_hdd_cap(self):
        return self.hdd_cap

    def set_sys_log_offset(self, sys_log_offset):
        self.sys_log_offset = sys_log_offset

    def get_sys_log_offset(self):
        return self.sys_log_offset

    def set_sys_log_size(self, sys_log_size):
        self.sys_log_size = sys_log_size

    def get_set_sys_log_size(self):
        return self.video_data_area_offset

    def set_video_data_area_offset(self, video_data_area_offset):
        self.video_data_area_offset = video_data_area_offset

    def get_video_data_area_offset(self):
        return self.video_data_area_offset

    def set_data_block_size(self, data_block_size):
        self.data_block_size = data_block_size

    def getdata_block_size(self):
        return self.data_block_size

    def set_data_block_total(self, data_block_total):
        self.data_block_total = data_block_total

    def get_data_block_total(self):
        return self.data_block_total

    def set_hikbtree1_offset(self, hikbtree1_offset):
        self.hikbtree1_offset = hikbtree1_offset

    def get_hikbtree1_offset(self):
        return self.hikbtree1_offset

    def set_hikbtree2_offset(self, hikbtree2_offset):
        self.hikbtree2_offset = hikbtree2_offset

    def get_hikbtree2_offset(self):
        return self.hikbtree2_offset

    def set_hikbtree1_size(self, hikbtree1_size):
        self.hikbtree1_size = hikbtree1_size

    def get_hikbtree1_size(self):
        return self.hikbtree1_size

    def set_hikbtree2_size(self, hikbtree2_size):
        self.hikbtree2_size = hikbtree2_size

    def get_hikbtree2_size(self):
        return self.hikbtree2_size

