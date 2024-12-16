"""
HIKVISION Video Data Recovery
Author: Dane Wullen
Date: 2024
Version: 0.2
NO WARRANTY, SOFWARE IS PROVIDED 'AS IS'


© 2024 Dane Wullen
"""

class HikBTree:

    def __init__(self):
        self.signatur = ""
        self.created_time = 0
        self.footer_offset = 0
        self.page_list_offset = 0
        self.page_one_offset = 0
        self.page_list = []

    def __str__(self):
       return ("Signature: {}".format(self.signatur) + "\n" +
        "Creation date: {}".format(self.created_time) + "\n" +
        "Offset to footer: {}".format(self.footer_offset) + "\n" +
        "Offset to page list: {}".format(self.page_list_offset) + "\n" +
        "Offset to page 1: {}".format(self.page_one_offset) + "\n" +
        "Page list: {}".format(str(self.page_list)) + "\n")

    def __repr__(self):
        print(self)

    def set_signatur(self, signatur):
        self.signatur = signatur

    def get_signatur(self):
        return self.signatur

    def set_created_time(self, created_time):
        self.created_time = created_time

    def get_created_time(self):
        return self.created_time

    def set_footer_offset(self, footer_offset):
        self.footer_offset = footer_offset

    def get_footer_offset(self):
        return self.footer_offset

    def set_page_list_offset(self, page_list_offset):
        self.page_list_offset = page_list_offset

    def get_page_list_offset(self):
        return self.page_list_offset

    def set_page_one_offset(self, page_one_offset):
        self.page_one_offset = page_one_offset

    def get_page_one_offset(self):
        return self.page_one_offset

    def set_page_list(self, page_list):
        self.page_list = page_list

    def get_page_list(self):
        return self.page_list

    def add_hikpage(self, hikpage):
        self.page_list.append(hikpage)