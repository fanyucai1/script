import subprocess

cmd="export PATH=/software/exonerate/bin/:/software/wgsim/wgsim/:/software/velvet/velvet_1.2.10/:/software/samtools/samtools-1.2:/software/Bcftools/bcftools-1.2/:/software/bwa/bwa-0.7.12/:/software/picard/:$PATH"
cmd+=" && /software/python2/Python-v2.7.9/bin/python /software/python2/Python-v2.7.9/bin/addsnv.py "
cmd+="-f /data/Project/fanyucai/CAP/mapping/test.q20.bam "
cmd+="-r /data/Database/hg19/ucsc.hg19.fasta "
cmd+="-v /data/Project/fanyucai/CAP/snv_10 "
cmd+="--maxdepth 25000 "
cmd+="--minmutreads 2 "
cmd+="--force --ignoresnps "
cmd+="-p 10 "
cmd+="-o out.bam "
cmd+="--aligner mem "
cmd+="--picardjar /software/picard/picard.jar"
subprocess.check_call(cmd,shell=True)

cmd = "/software/samtools/samtools-1.9/bin/samtools index out.bam"
subprocess.check_call(cmd, shell=True)
cmd="/software/python3/Python-v3.7.0/bin/python3.7 ~/script/vardict/vardict_single.py 0 out.bam /data/Project/fanyucai/CAP/bed/panel_27.bed test ./"
subprocess.check_call(cmd, shell=True)
