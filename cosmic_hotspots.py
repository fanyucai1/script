#Email:fanyucai1@126.com
import re
import sys
def hotspots(cosmic_vcf,hotspots_vcf):
    infile=open(cosmic_vcf,"r")
    outfile=open(hotspots_vcf,"w")
    for line in infile:
        line=line.strip()
        if not line.startswith("#"):
            pattern=re.compile(r'CNT=(\d+)')
            a=pattern.findall(line)
            if int(a[0])>=50:
                outfile.write("%s\n"%(line))
        else:
            outfile.write("%s\n" % (line))
    infile.close()
    outfile.close()

if __name__=="__main__":
    if len(sys.argv)!=3:
        print("Usage:python3 %s cosmic_vcf hotspots_vcf\n"%(sys.argv[0]))
        print("Copyright:fanyucai")
        print("Version:1.0")
        sys.exit(-1)
    vcf1=sys.argv[1]
    vcf2=sys.argv[2]
    hotspots(vcf1,vcf2)