# Download-IOCBucket
Python 2.7 program to download all IOCs and avoid unnecessary requests to IOCBucket.com

There is currently no "download all" so this will download all [IOC](http://openioc.org/) and [YARA](http://plusvic.github.io/yara/) files on [IOCBucket.com](https://www.iocbucket.com/).

Requirements:

- BeautifulSoup
- pyOpenSSL
- ndg-httpsclient 
- pyasn1

Installable via pip

Usage:

1) Modify the variable ioc_data_path to reflect the directory where you want to download the IOCs
2) Run the script (eg. python download_iobucket.py)
