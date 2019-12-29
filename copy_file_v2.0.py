import argparse
import paramiko
from scp import SCPClient
import os

Host = '192.168.1.118'
user = "root"
passwd = "2ghlmcl1hblsqT"
port =22
root_dir="/media/BMC-to-GC/TSO500/2019.12.28/"

def run(out_prefix,local_file):
    To_dir=root_dir+"/"+out_prefix
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect(Host, port, user, passwd)
    ssh.exec_command('mkdir -p %s'%(To_dir))
    scpclient = SCPClient(ssh.get_transport())
    scpclient.put(local_file, recursive=True,remote_path=To_dir) # 上传到服务器指定文件
    ssh.close()

from_dir="/data/TSO500/2019.12.28.2/"
def scan_file():
    for(root,dirs,files) in os.walk(from_dir):
        for file in files:
            tmp=os.path.join(root,file)
            if tmp.endswith(".annovar.tsv") or tmp.endswith(".cnv.tsv"):
                run(tmp.split("/")[-3],tmp)
            if tmp.endswith("stitched.bam") or tmp.endswith("stitched.bam.bai"):
                run(tmp.split("/")[-2],tmp)
            if tmp.endswith("MetricsReport.tsv") or tmp.endswith("_BiomarkerReport.txt"):
                run(tmp.split("/")[-4],tmp)
if __name__=="__main__":
    scan_file()