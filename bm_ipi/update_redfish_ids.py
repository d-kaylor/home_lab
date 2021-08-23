#!/usr/bin/env python

import requests
import yaml
import re


REDFISH_HOST = "http://192.168.0.1:8000"
NODES = ["master-1", "master-2", "master-3", "worker-1", "worker-2", "worker-3"]
DOMAIN = "ocp4.lab.local"
CONFIG = '/home/dkaylor/bm_ipi/install-config.yaml'


def get_system(system_path=None):
    if system_path:
        rf_path = f'{REDFISH_HOST}{system_path}'
    else: # Get all systems
        rf_path = f'{REDFISH_HOST}/redfish/v1/Systems'
    r = requests.get(rf_path, stream=True)
    return r.json()


with open(CONFIG) as f:
    config = yaml.load(f, Loader=yaml.SafeLoader)

for member in get_system()['Members']:
    system = get_system(member['@odata.id'])
    if '.ocp4.lab.local' in system['Name']:
        rf_name = system['Name'].replace('.ocp4.lab.local', '')
        rf_id = system['Id']
        index, host = [(i,h) for (i,h) in enumerate(config['platform']['baremetal']['hosts']) if h['name']==rf_name][0]
        old_id = config['platform']['baremetal']['hosts'][index]['bmc']['address'].split('/')[-1]
        config['platform']['baremetal']['hosts'][index]['bmc']['address'] = config['platform']['baremetal']['hosts'][index]['bmc']['address'].replace(old_id, rf_id)
        
with open(CONFIG, 'w') as f:
    yaml.dump(config, f, sort_keys=False)
