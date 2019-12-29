import os
import sys
import re
import subprocess

def copy(indir,keywords,outdir):
    if not os.path.exists(outdir):
        os.mkdir(outdir)
    for(root,dir,files) in os.walk(indir):
        for file in files:
            path=os.path.join(root,file)
            if re.search(keywords,path):
                subprocess.call('cp %s %s'%(path,outdir),shell=True)

if __name__ == '__main__':
    if len(sys.argv)!=4:
        print("usage:python3 %s inputdir keywords outdir"%(sys.argv[0]))
        print("Email:fanyucai1@126.com")
    else:
        indir=sys.argv[1]
        keywords=sys.argv[2]
        outdir=sys.argv[3]
        copy(indir, keywords, outdir)
