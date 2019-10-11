import paramiko
from scp import SCPClient
import os
import sys

Host = '192.168.1.118'
user = "root"
passwd = "2ghlmcl1hblsqT"
port =22

def run(local_file,To_dir):
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect(Host, port, user, passwd)
    scpclient = SCPClient(ssh.get_transport())
    scpclient.put(local_file, To_dir) # 上传到服务器指定文件
    ssh.close()