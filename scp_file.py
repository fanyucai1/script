import paramiko
from scp import SCPClient
import sys

Host = '192.168.1.118'
user = "root"
passwd = "2ghlmcl1hblsqT"
port =22

def run(local_dir,To_dir):
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect(Host, port, user, passwd)
    scpclient = SCPClient(ssh.get_transport())
    scpclient.put(local_dir, recursive=True,remote_path=To_dir) # 上传到服务器指定文件
    ssh.close()

if __name__=="__main__":
    if len(sys.argv)!=3:
        print("python3 %s local_dir remote_dir"%(sys.argv[0]))
        print("Emai:fanyucai1@126.com")
    else:
        local_dir=sys.argv[1]
        To_dir=sys.argv[2]
        run(local_dir, To_dir)