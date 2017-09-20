#!/usr/bin/python

######################################################
# IOC Downloader for IOCBucket.com
# March 2015 by Stephen Genusa
# http://development.genusa.com
#
# requires pyOpenSSL ndg-httpsclient pyasn1
######################################################

import os
import re
import sys
import base64
import requests
from BeautifulSoup import BeautifulSoup

# Change this path to reflect the pathname where the IOC files are stored
ioc_data_path = '/sec-fs/data/IOCs'

IOC_BUCKET = 'https://www.iocbucket.com'

def main(ioc_data_path):
    
    # Get a list of the existing IOCs
    ioc_files = os.listdir(ioc_data_path)
    
    # Request a list of the current IOCs on IOCBucket.com
    print "Requesting list of current IOCs on IOCBucket.com"
    ioc_search_http_request = requests.post(IOC_BUCKET + '/search', {'search':''})
    
    # Parse the HTML
    soup = BeautifulSoup(ioc_search_http_request.content)
    
    # Grab the A elements
    links = soup.findAll("a")
    
    # Avoid the URL duplication by saving a list of IOC hashes already checked for
    hashes_already_checked = []
    
    # For each HREF
    for link in links:
        href = link.get("href")
        if href != None and href.find('/iocs/') > -1:
            
            ioc_already_exists = False
            # Parse out just the hash
            ioc_search_hash = href.replace('/iocs/', '')
            # See if the file already exists in the local IOC directory
            for ioc_file in ioc_files:
                if ioc_file.find(ioc_search_hash) > -1:
                    ioc_already_exists = True
                    break
            # If it does not exist then grab the IOC description page        
            if not ioc_already_exists and not ioc_search_hash in hashes_already_checked:
                ioc_href = IOC_BUCKET + href
                print "\nGetting new IOC", ioc_href
                ioc_http_request = requests.get(ioc_href)
                # Find the base64 encoded URL for the download if it exists
                match = re.search("Base64\.decode\('(.{10,100}?)'", ioc_http_request.content, re.DOTALL | re.MULTILINE)
                if match:
                    base64d_url = match.groups(0)[0]
                    # Decode the IOC download URL
                    real_url = IOC_BUCKET + base64.b64decode(base64d_url)
                    # Grab the IOC file via HTTP
                    ioc_http_request = requests.get(real_url)
                    # Avoid duplication by saving the hash to our check-list
                    hashes_already_checked.append(ioc_search_hash)
                    # If the file actually exists (ecaf59784723054267f5c06f34d5315e2f00cec2 does not)
                    #   then save it to the proper filename
                    if 'content-disposition' in ioc_http_request.headers:
                        ioc_filename = ioc_http_request.headers['content-disposition'].split('; ')[1].replace('filename=', '').replace('"', '').replace('/', '_').replace('\\', '_').replace('?', '_')
                        if not os.path.isfile(os.path.join(ioc_data_path, ioc_filename)):
                            open(os.path.join(ioc_data_path, ioc_filename), "wb").write(ioc_http_request.content)
                            print "New IOC saved", ioc_filename
                    else:
                        # This means there is an IOC page but no IOC file behind it
                        print "Invalid IOC pointer. IOC does not exist:", href
            else: # A file with the hash already exists so skip it
                # Avoid duplication by saving the hash to our check-list
                hashes_already_checked.append(ioc_search_hash)
                sys.stdout.write('.')       
    print "\nDone downloading IOCs from IOCBucket.com"


if __name__ == "__main__":
    main(ioc_data_path)
