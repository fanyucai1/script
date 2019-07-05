file1="/data/Database/knownCanonical/LRG_RefSeqGene"#ftp://ftp.ncbi.nlm.nih.gov/refseq/H_sapiens/RefSeqGene/
file2="/data/Database/knownCanonical/appris_data.principal.txt"#http://appris.bioinfo.cnio.es
genelist="/data/Panel275/gene_list/gene_275.list"
dict={}
infile=open(genelist,"r")
for line in infile:
    line = line.strip()
    array = line.split("\t")
    dict[array[0]]=[]
infile.close()
############################
infile1=open(file1,"r")
for line in infile1:
    line=line.strip()
    array=line.split("\t")
    if array[-1]=="reference standard":
        if array[2] in dict:
            dict[array[2]].append(array[5])
infile1.close()
##########################
dict1={}
for key in dict:
    if dict[key]==[]:
        dict1[key] = []
##########################
infile2=open(file2,"r")
for line in infile2:
    line = line.strip()
    array = line.split("\t")
    if array[0] in dict1 and array[-1]=="PRINCIPAL:1":
        print("PRINCIPAL:1", array[0])
        dict[array[0]].append(array[2])
        continue
infile2.close()
dict2={}
for key in dict:
    if dict[key]==[]:
        dict2[key] = []
############################
infile2=open(file2,"r")
for line in infile2:
    line = line.strip()
    array = line.split("\t")
    if array[0] in dict2 and array[-1]=="PRINCIPAL:2":
        dict[array[0]].append(array[2])
        print("PRINCIPAL:2",array[0])
        continue
infile2.close()
dict3={}
for key in dict:
    if dict[key]==[]:
        dict3[key] = []
##############################
infile2=open(file2,"r")
for line in infile2:
    line = line.strip()
    array = line.split("\t")
    if array[0] in dict3 and array[-1]=="PRINCIPAL:3":
        dict[array[0]].append(array[2])
        print("PRINCIPAL:3", array[0])
        continue
infile2.close()
dict4={}
for key in dict:
    if dict[key]==[]:
        dict4[key] = []
############################################
infile2=open(file2,"r")
for line in infile2:
    line = line.strip()
    array = line.split("\t")
    if array[0] in dict4 and array[-1]=="PRINCIPAL:4":
        dict[array[0]].append(array[2])
        print("PRINCIPAL:4", array[0])
        continue
infile2.close()
dict5={}
for key in dict:
    if dict[key]==[]:
        dict5[key] = []
############################################
infile2=open(file2,"r")
for line in infile2:
    line = line.strip()
    array = line.split("\t")
    if array[0] in dict5 and array[-1]=="PRINCIPAL:5":
        dict[array[0]].append(array[2])
        print("PRINCIPAL:5", array[0])
        continue
infile2.close()
for key in dict:
    if dict[key]==[]:
        print(key,"not find known canonical transcript")