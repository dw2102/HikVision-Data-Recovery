# HikVision Data Recovery

Script to recover / get video files from NVR hard drive which uses the HikVision filesystem. 

Based on the paper from Jaehyeok Han, Doowon Jeong and Sangjin Lee (Korean University)

https://www.researchgate.net/publication/285429692_Analysis_of_the_HIKVISION_DVR_file_system

You'll need a encase or dd image or access to a raw disk.

Usage:

__main__.py [-h] -m MODE -i INPUT -d DIR

optional arguments:
  -h, --help            show this help message and exit
  -m MODE, --mode MODE  Information (i) or extraction (e)
  -i INPUT, --input INPUT
                        Inputfile (.dd, .e01 or physical disk)
  -d DIR, --dir DIR     Output-Directory for logs and/or videos

Output of all tables (page list, information etc) in .csv files.

© 2024 Dane Wullen

NO WARRANTY, SOFWARE IS PROVIDED 'AS IS'
