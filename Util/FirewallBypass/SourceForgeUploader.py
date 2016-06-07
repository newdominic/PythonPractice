import paramiko
import scp

ssh_client = paramiko.SSHClient()
ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())

ssh_client.connect('web.sourceforge.net', username='account', password='password')

scp = scp.SCPClient(ssh_client.get_transport())

scp.put('path_to_file')
print '[+] File is uploaded.'

scp.close()