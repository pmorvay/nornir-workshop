#!/usr/bin/env python
# to start ./ex6_yaml_data.py -f ex6_yaml_data_2.yaml
from jinja2 import Template
import yaml
from argparse import ArgumentParser
from pprint import pprint

parser = ArgumentParser("Specifying the YAML File")
parser.add_argument("-f", "--file",
                    help="Please Specify the YAML file.",
                    required=True)
args = parser.parse_args()
file_name = args.file

with open(file_name) as f:
    yaml_data = yaml.safe_load(f.read())

with open("nornir_inventory.j2") as f:
    config_in = Template(f.read())
with open("hosts.yaml", 'w') as write_file:

    for device in yaml_data["hostnames"]:
        config_out = config_in.render(hostname = device["name"])
        write_file.write(config_out)
print("example: \n" + config_out)