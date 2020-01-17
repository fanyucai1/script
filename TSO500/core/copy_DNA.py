import os
import paramiko
from scp import SCPClient
import argparse
Host = '192.168.1.118'
user = "root"
passwd = "2ghlmcl1hblsqT"
port =22

def run(out_prefix,local_file):
    To_dir="/media/BMC-to-GC/TSO500/%s"%(out_prefix)
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect(Host, port, user, passwd)
    ssh.exec_command('mkdir -p %s'%(To_dir))
    scpclient = SCPClient(ssh.get_transport())
    scpclient.put(local_file, recursive=True,remote_path=To_dir) # 上传到服务器指定文件
    ssh.close()

def copy_DNA(root_dir,prefix):
    for(root,dirs,files) in os.walk(root_dir):
        for file in files:
            tmp=os.path.join(root,file)
            if tmp.endswith("annovar.tsv")or tmp.endswith("cnv.tsv"):
                run(prefix, tmp)
            if tmp.endswith("MetricsReport.tsv") or tmp.endswith("BiomarkerReport.txt"):
                run(prefix, tmp)
            if tmp.endswith("stitched.bam") or tmp.endswith("stitched.bam.bai"):
                run(prefix,tmp)
