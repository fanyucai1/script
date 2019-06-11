import os
import argparse

parser=argparse.ArgumentParser("")
parser.add_argument("-t","--tmsi", nargs="+",required=True)
parser.add_argument("-n","--nmsi", nargs="+",required=True)
args=parser.parse_args()
dict1,id={},{}
sample1=[]
sample2=[]
def dict2d(dict, key_a, key_b, val):
    if key_a in dict:
        dict[key_a].update({key_b: val})
    else:
        dict.update({key_a: {key_b: val}})
############################################
for i in args.tmsi:
    infile1=open(i,"r")
    basename=os.path.basename(i)
    filename=basename.split(".")
    sample1.append(filename[0])
    for line in infile1:
        line=line.strip()
        array=line.split()
        tmp=array[0]+"_"+array[1]
        dict1[tmp]=1
        dict2d(id,filename[0],tmp,1)
    infile1.close()
##########################################
for j in args.nmsi:
    infile1=open(j,"r")
    basename = os.path.basename(j)
    filename = basename.split(".")#sampleID
    sample2.append(filename[0])
    for line in infile1:
        line=line.strip()
        array=line.split()
        tmp=array[0]+"_"+array[1]
        dict1[tmp]=1#site
        dict2d(id, filename[0], tmp, 1)
    infile1.close()
###########################################
outfile=open("msi_stat.tsv","w")
for key1 in dict1:
    outfile.write(key1)
    for key2 in sample1:
        if id[key2][key1]==1:
            outfile.write("\t1")
        else:
            outfile.write("\t.")
    outfile.write("\n")
for key1 in dict1:
    outfile.write(key1)
    for key2 in sample2:
        if id[key2][key1]==1:
            outfile.write("\t1")
        else:
            outfile.write("\t.")
    outfile.write("\n")
outfile.close()
