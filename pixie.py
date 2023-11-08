import requests
import argparse

requests.packages.urllib3.disable_warnings()    # Supress SSL warnings (until I issue a cert to Proxmox...me hopes)

def proxmox_session(username, password, node):    # Request and return cookies for authentication
#               .---. .---. 
#              :     : o   :    COOOOKIE!
#          _..-:   o :     :-.._    /
#      .-''  '  `---' `---' "   ``-.    
#    .'   "   '  "  .    "  . '  "  `.  
#   :   '.---.,,.,...,.,.,.,..---.  ' ;
#   `. " `.                     .' " .'      <-- Cookie Monster (nom)
#    `.  '`.                   .' ' .'
#     `.    `-._           _.-' "  .'  .----.
#       `. "    '"--...--"'  . ' .'  .'  o   `.
#       .'`-._'    " .     " _.-'`. :       o  :
#     .'      ```--.....--'''    ' `:_ o       :
#   .'    "     '         "     "   ; `.;";";";'
#  ;         '       "       '     . ; .' ; ; ;
# ;     '         '       '   "    .'      .-'
# '  "     "   '      "           "    _.-'
    url = 'https://' + node + ':8006/api2/json/access/ticket'   # Builds the ticket request URL
    
    creds = {   # Places the creds into a dictionary
        'username':username,
        'password':password
    }
    
    r = requests.post(url, data=creds, verify=False)    # Summons Cookie Monster
    
    return r.json()['data']['CSRFPreventionToken'], r.json()['data']['ticket'] # Returns the Cookie and CSRF Prevention Token

def start_vm(node, vmid, request):
    url = "https://" + node + ":8006/api2/json/nodes/proxmox/lxc/" + vmid + "/status/start" 
    header = {
        'CSRFPreventionToken': request[0]
    }
    cookie = {
        'PVEAuthCookie': request[1]
    }
    
    r = requests.post(url, headers=header, cookies=cookie, verify=False)
    return r.status_code

def stop_vm(node, vmid, request):
    url = "https://" + node + ":8006/api2/json/nodes/proxmox/lxc/" + vmid + "/status/stop" 
    header = {
        'CSRFPreventionToken': request[0]
    }
    cookie = {
        'PVEAuthCookie': request[1]
    }
    
    r = requests.post(url, headers=header, cookies=cookie, verify=False)
    return r.status_code

def delete_vm(node, vmid, request):
    url = "https://" + node + ":8006/api2/json/nodes/proxmox/lxc/" + vmid 
    header = {
        'CSRFPreventionToken': request[0]
    }
    cookie = {
        'PVEAuthCookie': request[1]
    }
    
    r = requests.delete(url, headers=header, cookies=cookie, verify=False)
    return r.status_code    

def create_container(node, vmid, request):
    url = "https://" + node + ":8006/api2/json/nodes/proxmox/lxc/" 
    
    header = {
        'CSRFPreventionToken': request[0]
    }
    cookie = {
        'PVEAuthCookie': request[1]
    }
    
    container_data = {
        'net0' : 'name=eth0,bridge=vmbr0',
        'ostemplate': 'Data:vztmpl/ubuntu-23.04-standard_23.04-1_amd64.tar.gz',
        'storage': 'Data',
        'vmid': vmid
    }
    
    r = requests.post(url, headers=header, cookies=cookie, data=container_data, verify=False)
    
    return r.status_code

def get_vm_info(node, vmid, request):
    url = "https://" + node + ":8006/api2/json/nodes/proxmox/lxc/302/status" 
    header = {
        'CSRFPreventionToken': request[0]
    }
    cookie = {
        'PVEAuthCookie': request[1]
    }
    r = requests.get(url, headers=header, cookies=cookie, verify=False)
    
    print(r.content) 


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('-u', '--username', help='Enter the username.', required=True)
    parser.add_argument('-p', '--password', help='Enter the password.', required=True)
    parser.add_argument('-n', '--node', help='Enter the node to connect to.', required=False)
    parser.add_argument('-i', '--id', help='Enter the VM ID', required=False)
    
args = parser.parse_args()
