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
outfile = open("omim.final.tsv", "a+")
infile=open("omim.tsv","r")
for line in infile:
    line=line.strip()
    array=line.split()
    if array[1]=="_" and array[2]=="_" and array[3]=="_" and array[4]=="_" and array[5]=="_":
        dict[array[0]]=1
    else:
        outfile.write("%s\n"%(line))
infile.close()
outfile.close()