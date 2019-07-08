#Email:fanyucai1@126.com
import os

def vardict(vcf,outdir,prefix):
    if not os.path.exists(outdir):
        os.mkdir(outdir)
    out=outdir+"/"+prefix
    infile=open(vcf,"r")
    outfile=open("%s.vcf",w)
    for line in infile:
        line=line.strip()
        if not line.startswith("#"):



        else:
