import sys


def run(genelist,annovarfile,outdir,prefix):
    dict={}
    infile=open(genelist,"r")
    for line in infile:
        line=line.strip()
        array=line.split("\t")
        dict[array[0]]=1
    infile.close()

    infile=open(annovarfile,"r")
    outfile=open("%s/%s.annovar.tsv"%(outdir,prefix),"w")
    for line in infile:
        if line.startswith("Chr"):
            outfile.write("%s\n"%(line))
        else:
            array=line.split("\t")
            if array[6] in dict:
                outfile.write("%s\n" % (line))
            else:
                pass
    outfile.close()
    infile.close()


if __name__=="__main__":
    if len(sys.argv)!=5:
        print("python3 %s genelist annovarfile outdir prefix"%(sys.argv[0]))
        print("\nEmail:fanyucai1@126.com")
        print("2019.7.11")
    else:
        genelist=sys.argv[1]
        annovarfile=sys.argv[2]
        outdir=sys.argv[3]
        prefix=sys.argv[4]
        run(genelist, annovarfile, outdir, prefix)