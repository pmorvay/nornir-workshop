#!/usr/bin/env python3


#export NET_TEXTFSM=/Users/pmorvay/Documents/Cisco/Devnet/misc/nornir/ntc-templates/templates

from pprint import pprint
from colorama import Fore
import time

from nornir import InitNornir
nr = InitNornir(config_file="config.yaml")
pprint(nr.inventory.hosts)

pprint(nr.inventory.groups)


from nornir.plugins.functions.text import print_result
from nornir.plugins.tasks.networking import netmiko_send_command

results = nr.run(task=netmiko_send_command, command_string="show ip int brief | ex una")
print_result(results)


# remove text_fsm
# NET_TEXTFSM=
results = nr.run(task=netmiko_send_command, command_string="show version", use_textfsm=True)
print_result(results)

from nornir.plugins.tasks.networking import napalm_get
results = nr.run(
    task=napalm_get, getters=["facts", "interfaces"]
)
print_result(results)

for host in nr.inventory.hosts.values():
    print(f"{host.name} connections: {host.connections}")

nr.close_connections()
print(f"{Fore.RED}All connections have been closed{Fore.RESET}", end="\n\n")

for host in nr.inventory.hosts.values():
    print(f"{host.name} connections: {host.connections}")

    from nornir.core.filter import F

    print(list(nr.filter(F(locator="R1.New York")).inventory.hosts.keys()))
    print(list(nr.filter(F(groups__contains="London")).inventory.hosts.keys()))
    print(list(nr.filter(F(groups__contains="London") & F(tags__contains="isr4400")).inventory.hosts.keys()))
    print(list(nr.filter(F(groups__contains="London") & F(tags__all=["isr4400", "edge"])).inventory.hosts.keys()))
    print(list(nr.filter(F(ntp__servers__contains="1.2.3.4")).inventory.hosts.keys()))



from nornir.plugins.functions.text import print_result
from nornir.plugins.tasks.networking import netmiko_send_command

london_devices = nr.filter(F(groups__contains="London"))
result = london_devices.run(task=netmiko_send_command, command_string="show ip route")
print_result(result)

from nornir.plugins.functions.text import print_result
from nornir.plugins.tasks.networking import netmiko_send_command


def get_commands(task, commands):
    for command in commands:
        task.run(task=netmiko_send_command, command_string=command)


london_devices = nr.filter(F(groups__contains="London"))
result = london_devices.run(task=get_commands, commands=["show ip int br", "show arp"])
print_result(result)
nr.close_connections()