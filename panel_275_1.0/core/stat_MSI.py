import os
import subprocess
import re
MSIsensor = "export LD_LIBRARY_PATH=/software/gcc/gcc-v6.5.0/lib64/:LD_LIBRARY_PATH && /software/MSIsensor/msisensor-ML/msisensor"
models = "/software/MSIsensor/msisensor-ML/models_hg19_275genes"
def run(indir):
    ##################################################tumor only analysis
    outfile=open("%s/MSI/total.tsv"%(indir),"w")
    outfile.write("SampleID\tTotal_Number_of_Sites\tNumber_of_Somatic_Sites\t%\n")
    for (root,dirs,files) in os.walk(indir):
        for file in files:
            tmp=os.path.join(root,file)
            p1=re.compile(r'[/](BJ19T\S+)[/]')
            p=re.compile(r'[/](BJ19T\S+\d+).bam$')
            a=p.findall(tmp)
            b=p1.findall(tmp)
            if a != []:
                cmd = "%s msi -t %s -o %s/MSI/%s.msi.tsv -M %s -d %s/1030c0aa35ca5c263daeae866ad18632" % (MSIsensor, tmp, indir, b[0],models, models)
                subprocess.check_call(cmd,shell=True)
                infile=open("%s/MSI/%s.msi.tsv"%(indir,b[0]),"r")
                num=0
                for line in infile:
                    num+=1
                    if num!=1:
                        outfile.write("%s\t%s"%(b[0],line))
                infile.close()
    outfile.close()
    ##################################################pairs analysis
    outfile = open("%s/MSI/total.tsv" % (indir), "w")
    outfile.write("SampleID\tTotal_Number_of_Sites\tNumber_of_Somatic_Sites\t%\n")


if __name__=="__main__":
    run("/data/Panel275/")
