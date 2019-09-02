import os
import re
import sys
import subprocess

def run(genefuse,outdir,prefix):
    if not os.path.exists(outdir):
        os.mkdir(outdir)
    out=outdir+"/"+prefix
    infile=open(genefuse,"r")
    outfile=open("%s.tsv"%(out),"w")
    outfile.write("Chr_Left\tPos_Left\tGene_Left\tChr_Right\tPos_Right\tGene_right\tUnique_Read_Depth\tInfo_left\tInfo_right\n")
    p1=re.compile(r'(chr[\d\dXY])')
    p2=re.compile(r'unique:(\d+)')
    num=0
    for line in infile:
        line=line.strip()
        if line.startswith("#Fusion:"):
            num+=1
            array=line.split("___")
            array1=array[0].split(":")
            Gene_Left=array1[1].split("_")[0]
            Pos_Left=array1[-1]

            array2 = array[1].split(":")
            Pos_Right=array2[3].split(" ")[0]
            Gene_Right=array2[0].split("_")[0]
            Unique_Read_Depth=p2.findall(line)[0]
            chr=p1.findall(line)
            outfile.write("%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\n"%(chr[0],Pos_Left,Gene_Left,chr[1],Pos_Right,Gene_Right,Unique_Read_Depth,array[0],array[1]))
    outfile.close()
    if num==0:
        subprocess.check_call("rm -rf %s.tsv"%(out),shell=True)
        print("Sample %s not find fuse."%(prefix))
if __name__=="__main__":
    if len(sys.argv)!=4:
        print("usage:python3 %s genefuse_out.txt outdir prefix\n"%(sys.argv[0]))
        print("#Email:fanyucai1@126.com")
    else:
        genefuse=sys.argv[1]
        outdir=sys.argv[2]
        prefix=sys.argv[3]
        run(genefuse,outdir,prefix)