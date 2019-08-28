import operator
infile=open("/home/fanyucai/test/UMI/TS19340NF_S2.UMI_1.sequence")
dict={}
for line in infile:
    line=line.strip()
    if line in dict:
        dict[line]+=1
    else:
        dict[line]=1
infile.close()


b = sorted(dict.items(), key=operator.itemgetter(1),reverse=True)

num=0
for i in range(130):
    print(b[i])