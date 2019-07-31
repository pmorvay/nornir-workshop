from pprint import pprint
from colorama import Fore
import time

from nornir import InitNornir
from nornir.plugins.functions.text import print_result
from nornir.plugins.tasks.networking import netmiko_send_command





def get_commands(task, commands):
    for command in commands:
        task.run(task=netmiko_send_command, command_string=command)

nr = InitNornir(config_file="config.yaml")

#london_devices = nr.filter(F(groups__contains="London"))
result = nr.run(task=get_commands, commands=["show ip int br", "show arp"])
print_result(result)
nr.close_connections()