import requests
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
from bs4 import BeautifulSoup
import random
import re
import os
import time
from multiprocessing import Process, Pool
#######################################
dict={}
outfile = open("omim.final.tsv", "w")
infile=open("omim.tsv","r")
for line in infile:
    line=line.strip()
    array=line.split()
    if array[1]=="_" and array[2]=="_" and array[3]=="_" and array[4]=="_" and array[5]=="_":
        pass
    else:
        dict[line] = line
infile.close()
for key in dict:
    outfile.write("%s\n"%(key))
outfile.close()