import paramiko
from scp import SCPClient

Host = '192.168.1.100'
user = "admin"
passwd = "87838"
port =22

ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect(Host,port,user, passwd)
scpclient = SCPClient(ssh.get_transport())
remotepath='/tmp/test.txt'
localpath='test.txt'
scpclient.put(localpath, remotepath) # 上传到服务器指定文件
localpath1 = 'get.txt'
scpclient.get(remotepath, localpath1) #从服务器中获取文件
ssh.close()