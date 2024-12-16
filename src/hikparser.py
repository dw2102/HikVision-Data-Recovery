"""
HIKVISION Video Data Recovery
Author: Dane Wullen
Date: 2024
Version: 0.2
NO WARRANTY, SOFWARE IS PROVIDED 'AS IS'


© 2024 Dane Wullen
"""

import uuid

from .hikpageentry import HikPageEntry
from .hikbtree import HikBTree
from .hikmastersector import HikMasterSector
from .hikdatablockentry import HikDataBlockEntry
from .diskimage import DiskImage

import datetime
import hashlib

class HikParser(Exception):

    def set_pos(self, pos):
        self.diskimage.seek(pos)

    def skip_bytes(self, offset):
        self.diskimage.skip(offset)

    def __init__(self, filename):
        self.diskimage = DiskImage(filename)
        self.master_sector = HikMasterSector()
        self.hikbtree = HikBTree()
        self.hikbtree.page_list = []

    def get_total_blocks(self):
        total = 0
        for page in self.hikbtree.get_page_list():
            total += len(page.data_blocks)

        return total

    def hex_to_string(self, hex):
        return bytes.fromhex(str(hex)[2:])

    def from_byte_to_string(self, bytestring):
        return bytestring.decode("utf-8")

    def from_byte_to_int(self, bytestring, byteorder):
        return int.from_bytes(bytestring, byteorder=byteorder)

    def hex_to_ascii(self, hex):
        return bytes.fromhex(str(hex)[2:]).decode("windows-1252").strip(' \t\n\r')

    def read_master_sector(self):
        """
           Reads master sector of HIKVISION systems and write its content into class.
           Initial position should always be Offset 528 Byte.
        """

        self.set_pos(528)
        self.master_sector.signatur = self.from_byte_to_string(self.diskimage.read(32))

        if not self.master_sector.check_signatur():
            raise Exception('SignatureException: Signature not equal to HIKVISION@HANGZHOU!')

        self.skip_bytes(24)
        self.master_sector.hdd_cap = self.from_byte_to_int(self.diskimage.read(8), "little")
        self.skip_bytes(16)
        self.master_sector.sys_log_offset = self.from_byte_to_int(self.diskimage.read(8), "little")
        self.master_sector.sys_log_size = self.from_byte_to_int(self.diskimage.read(8), "little")
        self.skip_bytes(8)
        self.master_sector.video_data_area_offset = self.from_byte_to_int(self.diskimage.read(8), "little")
        self.skip_bytes(8)
        self.master_sector.data_block_size = self.from_byte_to_int(self.diskimage.read(8), "little")
        self.master_sector.data_block_total = self.from_byte_to_int(self.diskimage.read(4), "little")
        self.skip_bytes(4)
        self.master_sector.hikbtree1_offset = self.from_byte_to_int(self.diskimage.read(8), "little")
        self.master_sector.hikbtree1_size = self.from_byte_to_int(self.diskimage.read(4), "little")
        self.skip_bytes(4)
        self.master_sector.hikbtree2_offset = self.from_byte_to_int(self.diskimage.read(8), "little")
        self.master_sector.hikbtree2_size = self.from_byte_to_int(self.diskimage.read(4), "little")
        self.skip_bytes(60)
        # UTC Timestamp
        self.master_sector.init_time = datetime.datetime.fromtimestamp(self.from_byte_to_int(self.diskimage.read(4),
                                                                                             "little"))\
            .strftime('%d.%m.%Y %H:%M:%S')

    def read_hikbtree(self):
        """
            Reads the first of the two HISBTREES and writes to class.
            Initial offset for HIBKTREE is located in master sector.
        """

        self.set_pos(self.master_sector.hikbtree1_offset)
        # Skip 16 unused bytes
        self.skip_bytes(16)
        self.hikbtree.signatur = self.from_byte_to_string(self.diskimage.read(8))
        self.skip_bytes(36)
        self.hikbtree.created_time = datetime.datetime.fromtimestamp(self.from_byte_to_int(self.diskimage.read(4),
                                                                                           "little"))\
            .strftime('%d.%m.%Y %H:%M:%S'),
        self.hikbtree.footer_offset = self.from_byte_to_int(self.diskimage.read(8), "little")
        self.skip_bytes(8)
        self.hikbtree.page_list_offset = self.from_byte_to_int(self.diskimage.read(8), "little")
        self.hikbtree.page_one_offset = self.from_byte_to_int(self.diskimage.read(8), "little")

    def read_page_list(self):
        """ Reads page list page for page and writes content into list."""

        self.set_pos(self.hikbtree.page_list_offset)
        self.skip_bytes(24)
        first_page_offset = self.from_byte_to_int(self.diskimage.read(8), "little")
        self.skip_bytes(64)
        # self.skip_bytes(96)
        page_offset = self.from_byte_to_int(self.diskimage.read(8), "little")

        # Add first page to entries
        page = HikPageEntry()
        page.offset_to_page = first_page_offset
        page.data_blocks = []
        self.hikbtree.add_hikpage(page)

        while page_offset != 0:
            page = HikPageEntry()
            page.offset_to_page = page_offset
            self.skip_bytes(8)
            page.channel = self.from_byte_to_int(self.diskimage.read(2), "big")
            self.skip_bytes(6)
            page.start_time = self.from_byte_to_int(self.diskimage.read(4), "little")
            page.end_time = self.from_byte_to_int(self.diskimage.read(4), "little")
            page.data_offset = self.from_byte_to_int(self.diskimage.read(8), "little")
            page.data_blocks = []
            self.hikbtree.add_hikpage(page)
            self.skip_bytes(8)
            page_offset = self.from_byte_to_int(self.diskimage.read(8), "little")

    def read_page_entries(self):
        for page in self.hikbtree.get_page_list():
            self.set_pos(page.offset_to_page)
            self.skip_bytes(96)
            unused_bytes = self.from_byte_to_int(self.diskimage.read(8), "little")
            # Same as 0xFFFFFFFFFFFFFFFF
            while unused_bytes == 18446744073709551615:
                data_block = HikDataBlockEntry()
                data_block.existence_of_file = self.diskimage.read(8)
                data_block.channel = self.from_byte_to_int(self.diskimage.read(2), "big")
                self.skip_bytes(6)
                data_block.start_time = self.from_byte_to_int(self.diskimage.read(4), "little")
                data_block.end_time = self.from_byte_to_int(self.diskimage.read(4), "little")
                data_block.data_offset = self.from_byte_to_int(self.diskimage.read(8), "little")
                page.data_blocks.append(data_block)
                self.skip_bytes(8)
                unused_bytes = self.from_byte_to_int(self.diskimage.read(8), "little")

    def extract_block(self, dir):
        i = 1
        for page in self.hikbtree.get_page_list():
            j = 1
            for datablock in page.data_blocks:
                length = self.master_sector.data_block_size
                #with open(self.filename, 'rb') as f1:
                #f1.seek(datablock.data_offset)
                fileName = dir + "\\" + datetime.datetime.utcfromtimestamp(datablock.start_time).strftime(
                    '%Y-%m-%d_%H-%M-%S') + "-" + \
                           datetime.datetime.utcfromtimestamp(datablock.end_time).strftime('%Y-%m-%d_%H-%M-%S') + \
                           "_ch_" + str(datablock.channel) + \
                           "_id_" + str(uuid.uuid4())

                fileNameMD5 = fileName + ".md5"
                fileName = fileName + ".mp4"

                md5Hash = hashlib.md5()
                self.diskimage.seek(datablock.data_offset)
                with open(fileName, 'wb') as f2:
                    while length:
                        chunk = min(1024 * 1024, length)
                        data = self.diskimage.read(chunk)
                        f2.write(data)
                        length -= chunk
                        md5Hash.update(data)
                    print("Block {} of page {} extracted!".format(j, i))
                with open (fileNameMD5, 'w') as f3:
                    f3.write(md5Hash.hexdigest())
                f2.close()
                f3.close()
                j += 1
                #f1.close()
            i += 1

    def print_hikpagelist(self, dir):
        with open(dir + "\\HIKPageList.csv", "w", newline="") as file:
            i = 1
            file.write("Page;Channel;Starttime;Endtime;Offset\n")
            for page in self.hikbtree.get_page_list():
                output = "{};{};{};{};{}".format(
                    str(i),
                    page.channel,
                    datetime.datetime.utcfromtimestamp(page.start_time).strftime('%d.%m.%Y %H:%M:%S'),
                    datetime.datetime.utcfromtimestamp(page.end_time).strftime('%d.%m.%Y %H:%M:%S'),
                    page.offset_to_page
                )
                file.write(output + "\n")
                i += 1
        file.close()

    def print_hikbtree(self, dir):
        with open(dir + "\\HIKBTree.txt", "w", newline="") as file:
            file.write("Signature: {}\n".format(self.hikbtree.signatur))
            file.write("Creation date: {}\n".format(self.hikbtree.created_time))
            file.write("Offset to footer: {}\n".format(self.hikbtree.footer_offset))
            file.write("Offset to page list: {}\n".format(self.hikbtree.page_list_offset))
            file.write("Offset to first page: {}\n".format(self.hikbtree.page_one_offset))
        file.close()

    def print_hikpages(self, dir):
        with open(dir + "\\HIKPages.csv", "w", newline="") as file:
            i = 1
            file.write("Page;Datablock;Channel;Starttime;Endtime;Offset\n")
            for page_entry in self.hikbtree.get_page_list():
                j = 1
                for page in page_entry.data_blocks:
                    output = "{};{};{};{};{};{}".format(
                        str(i),
                        str(j),
                        int.from_bytes(self.hex_to_string(page.channel), byteorder="big"),
                        datetime.datetime.utcfromtimestamp(page.start_time).strftime('%d.%m.%Y %H:%M:%S'),
                        datetime.datetime.utcfromtimestamp(page.end_time).strftime('%d.%m.%Y %H:%M:%S'),
                        page.data_offset
                    )
                    file.write(output + "\n")
                    j += 1
                j = 0
                i += 1
        file.close()

    def print_master_sector(self, dir):
        with open(dir + "\\HIKMasterSector.txt", "w", newline="") as file:
            file.write("Signature: {}\n".format(self.master_sector.signatur))
            file.write("Hard disk size: {}\n".format(self.master_sector.hdd_cap))
            file.write("Offset to system logs: {}\n".format(self.master_sector.sys_log_offset))
            file.write("System log size: {}\n".format(self.master_sector.sys_log_size))
            file.write("Offset to video data area: {}\n".format(self.master_sector.video_data_area_offset))
            file.write("data block size: {}\n".format(self.master_sector.data_block_size))
            file.write("Total data blocks: {}\n".format(self.master_sector.data_block_total))
            file.write("Offset to HIKBTree 1: {}\n".format(self.master_sector.hikbtree1_offset))
            file.write("Size of HIKBTree 1: {}\n".format(self.master_sector.hikbtree1_size))
            file.write("Offset to HIKBTree 2: {}\n".format(self.master_sector.hikbtree2_offset))
            file.write("Size of HIKBTree 2: {}\n".format(self.master_sector.hikbtree2_size))
            file.write("Creation date: {}\n".format(self.master_sector.init_time))
        file.close()





