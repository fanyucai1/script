file1=open("all.txt","r")
file2=open("gene.list","r")
dict={}
for line in file1:
    line=line.strip()
    dict[line]=1
for line in file2:
    line = line.strip()
    if line in dict:
        pass
    else:
        print (line)