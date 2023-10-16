import requests
import argparse

requests.packages.urllib3.disable_warnings()    # Supress SSL warnings (until I issue a cert to Proxmox...me hopes)

def proxmox_session(username, password):    # Request and return cookies for authentication
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
    url = 'https://192.168.1.10:8006/api2/json/access/ticket'   # Builds the ticket request URL
    
    creds = {   # Places the creds into a dictionary
        'username':username,
        'password':password
    }
    
    r = requests.post(url, data=creds, verify=False)    # Summons Cookie Monster
    
    return r.json()['data']['CSRFPreventionToken'], r.json()['data']['ticket'] # Returns the Cookie and CSRF Prevention Token

# def get_vm_info(cookie):  # Lists VM or Container information. (Note: Proxmox refers to both VMs and Containers as "VMs")
#     url = 'https://192.168.1.10:8006/api2/json/cluster/resources/proxmox/'
#     r = requests.session().get(url, cookies=cookie, verify=False)
#     print(r.json())

def delete_vm(cookie):
    url = 'https://192.168.1.10:8006/api2/json/api2/json/nodes/proxmox/lxc/211'

    delete = requests.session().get(url, cookies=cookie, verify=False)
    
    return delete.status_code


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('-u', '--username', help='Enter the username.', required=True)
    parser.add_argument('-p', '--password', help='Enter the password.', required=True)
    parser.add_argument('-n', '--node', help='Enter the node to connect to.', required=False)
    parser.add_argument('-i', '--id', help='Enter the VM ID', required=False)
    
args = parser.parse_args()

delete_vm(proxmox_session(args.username, args.password))