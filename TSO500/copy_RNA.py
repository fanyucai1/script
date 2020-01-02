import os
import paramiko
from scp import SCPClient
Host = '192.168.1.118'
user = "root"
passwd = "2ghlmcl1hblsqT"
port =22

def run(out_prefix,local_file):
    To_dir="/media/BMC-to-GC/TSO500/2019.12.31.RNA/%s"%(out_prefix)
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect(Host, port, user, passwd)
    ssh.exec_command('mkdir -p %s'%(To_dir))
    scpclient = SCPClient(ssh.get_transport())
    scpclient.put(local_file, recursive=True,remote_path=To_dir) # 上传到服务器指定文件
    ssh.close()
if __name__=="__main__":
    root_file="/data/TSO500/RNA.2019.12.31/"
    for(root,dirs,files) in os.walk(root_file):
        for file in files:
            tmp=os.path.join(root,file)
            if tmp.endswith("_Fusions.csv") or tmp.endswith("_HighConfidenceVariants.csv") or tmp.endswith("_PublishedFusions.csv") or tmp.endswith("_SpliceVariants.vcf"):
                prefix=tmp.split("/")[-4]
                run(prefix,tmp)