import paramiko
import time
from olt_info import Olt_ma
from tqdm import tqdm

olt = Olt_ma() # OLT MONTE ALGRE

slot = _
pon = _
vlan = 100 # VLAN MONTE ALEGRE
id = _

# CONFERIR O SCRIPT É O CERTO PARA A OLT, O SLOT,A PON E O ID INICIAL ANTES DE EXECUTAR
onts = [    
    {"sn": "", "id": id, "desc": "MIGRACAO_OLT"}, # 1
    {"sn": "", "id": id+1, "desc": "MIGRACAO_OLT"}, # 2
    {"sn": "", "id": id+2, "desc": "MIGRACAO_OLT"}, # 3
    {"sn": "", "id": id+3, "desc": "MIGRACAO_OLT"}, # 4
    {"sn": "", "id": id+4, "desc": "MIGRACAO_OLT"}, # 5
    {"sn": "", "id": id+5, "desc": "MIGRACAO_OLT"}, # 6 
    {"sn": "", "id": id+6, "desc": "MIGRACAO_OLT"}, # 7
    {"sn": "", "id": id+7, "desc": "MIGRACAO_OLT"}, # 8
    {"sn": "", "id": id+8, "desc": "MIGRACAO_OLT"}, # 9
    {"sn": "", "id": id+9, "desc": "MIGRACAO_OLT"}, # 10
    {"sn": "", "id": id+10, "desc": "MIGRACAO_OLT"}, # 11
    {"sn": "", "id": id+11, "desc": "MIGRACAO_OLT"}, # 12
    {"sn": "", "id": id+12, "desc": "MIGRACAO_OLT"}, # 13
    {"sn": "", "id": id+13, "desc": "MIGRACAO_OLT"}, # 14
    {"sn": "", "id": id+14, "desc": "MIGRACAO_OLT"}, # 15
    # {"sn": "", "id": id+15, "desc": "MIGRACAO_OLT"}, # 16
]

try:
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect(olt.ip_host(), username=olt.user_login(), password=olt.passwd_login())
    shell = ssh.invoke_shell()
    print("CONEXÃO ESTABELECIDA COM SUCESSO \n")
except Exception as e:
    print(f"Erro ao conectar a OLT: {e}")
    exit(1)

print(f"ENTRANDO NA INTERFACE 0/{slot} \n")
shell.send("enable\n")
shell.send("config\n")
shell.send(f"interface gpon 0/{slot}\n")

# Adicionar 
for ont in onts:
    print(f"ONT ADD - SN: {ont['sn']}")
    shell.send(f"ont add {pon} {ont['id']} sn-auth {ont['sn']} omci ont-lineprofile-id {vlan} ont-srvprofile-id {vlan} desc \"{ont['desc']}\"\n")
    shell.send("\n")
    
print("\n")
# Configurar VLAN nativa
for ont in onts:
    print(f"ONT PORT NATIVE-VLAN - SN: {ont['sn']}")
    shell.send(f"ont port native-vlan {pon} {ont['id']} eth 1 vlan {vlan} priority 0\n")

shell.send("quit\n")

print("\n")
# Criar service-ports
for ont in onts:
    print(f"SERVICE-PONT VLAN - SN: {ont['sn']}")
    shell.send(f"service-port vlan {vlan} gpon 0/{slot}/{pon} ont {ont['id']} gemport 2 multi-service user-vlan {vlan} tag-transform translate\n")
    shell.send("\n")  

print("\n")
# Salvar configuração
# print("SALVANDO AS ALTERAÇÕES NA OLT")
shell.send("save\n")
shell.send("\n")  # Responde "Yes" à confirmação, se necessário
for _ in tqdm(range(120), desc="SALVANDO AS ALTERAÇÕES NA OLT"):
        time.sleep(1)  # Aguarda o save completar
output = shell.recv(65535).decode('utf-8')
print(output)
ssh.close()
print("PROCESSO FINALIZADO. \nCONEXÃO COM A OLT FECHADA.")