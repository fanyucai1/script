import sys
def split_gene(genelist,annovar,out):
    dict = {}
    infile = open(genelist, "r")
    for line in infile:
        line = line.strip()
        dict[line] = 1
    infile.close()
    infile = open(annovar, "r")
    outfile = open(out, "w")
    num = 0
    for line in infile:
        line = line.strip()
        num += 1
        if num == 1:
            outfile.write("%s\n" % (line))
        else:
            array = line.split()
            if array[6] in dict:
                outfile.write("%s\n" % (line))
    infile.close()
    outfile.close()

if __name__=="__main__":
    if len(sys.argv)!=4:
        print("python split.py genelist annovarfile outfile\n")
        sys.exit(-1)
    genelist=sys.argv[1]
    annovar=sys.argv[2]
    out=sys.argv[3]
    split_gene(genelist,annovar,out)