import paramiko
import time
from olt_info import Olt_pm

olt = Olt_pm()
slot = 1
pon = 12
 
try:
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect(olt.ip_host(), username=olt.user_login(), password=olt.passwd_login())
    shell = ssh.invoke_shell()
except Exception as e:
    print(f"Erro ao conectar a OLT: {e}")
    exit(1)

shell.send("enable\n")
shell.send("config\n")
shell.send(f"interface gpon 0/{slot}\n")
shell.send(f"display ont info {pon} all\n")

time.sleep(5)  # Aguarda o save completar
output = shell.recv(65535).decode('utf-8')
print(output)
ssh.close()

