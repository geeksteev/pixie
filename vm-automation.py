import requests
import argparse

requests.packages.urllib3.disable_warnings()    # Supress SSL warnings

def proxmox_session(username, password):
    creds = {
        'username':username,
        'password':password
    }
    
    r = requests.post('https://192.168.1.10:8006/api2/json/access/ticket', data=creds, verify=False)

    cookie = {
        "PVEAuthCookie":r.json()["data"]["ticket"]
    }
    return cookie

def get_json_version(cookie):
    r = requests.get('https://192.168.1.10:8006/api2/json/version', cookies=cookie, verify=False)
    return r.json()["data"]["release"]

def get_vm_status(cookie, id):
    url = f'https://192.168.1.10:8006/api2/json/nodes/proxmox/lxc/{id}/status/current'
    r = requests.get(url, cookies=cookie, verify=False)
    return r.json()

def clone_vm(cookie, node, id):
    url = f'https://192.168.1.10:8006/api2/json/nodes/proxmox/lxc/{id}/clone'

    vm_data = {
        'newid': '333', # New VM ID
        'node': node
    }

    r = requests.post(url, data=vm_data, cookies=cookie, verify=False)
    return r.status_code


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('-u', '--username', help='Enter the username.', required=True)
    parser.add_argument('-p', '--password', help='Enter the password.', required=True)
    parser.add_argument('-n', '--node', help='Enter the node to connect to.', required=False)
    parser.add_argument('-i', '--id', help='Enter the VM ID', required=False)
    
args = parser.parse_args()

print(clone_vm(proxmox_session(args.username, args.password), args.node, args.id))
