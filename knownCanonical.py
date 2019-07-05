file1="/data/Database/knownCanonical/LRG_RefSeqGene"#ftp://ftp.ncbi.nlm.nih.gov/refseq/H_sapiens/RefSeqGene/
file2="/data/Database/knownCanonical/appris_data.principal.txt"#http://appris.bioinfo.cnio.es
genelist="/data/Panel275/gene_list/gene_275.list"
dict={}
infile=open(genelist,"r")
for line in infile:
    line = line.strip()
    array = line.split("\t")
    dict[array[0]]=[]

infile1=open(file1,"r")
for line in infile1:
    line=line.strip()
    array=line.split("\t")
    if array[8]=="reference standard":
        if array[2] in dict:
            dict[array[2]].append(array[5])
infile1.close()

for key in dict:
    if len(dict[key])<1:
        print (key)