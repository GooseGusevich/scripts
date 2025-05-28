
#Example python3 search_directory.py [URL] [extension]

import requests 
import sys 

sub_list = open("/home/vadim/Downloads/wordlist2-1626415171030.txt").read() 
directories = sub_list.splitlines()

for dir in directories:
    dir_enum = f"{sys.argv[1]}/{dir}.{sys.argv[2]}" 
    r = requests.get(dir_enum)
    if r.status_code==404: 
        pass
    else:
        print("Valid directory:" ,dir_enum)

