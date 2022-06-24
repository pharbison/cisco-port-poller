import yaml
import socket
from netmiko import ConnectHandler

class Poller:
  def __init__(self, file_inventory):
    self.file_inventory = file_inventory

  def __load_inventory(self):
    with open(self.file_inventory) as f:
      self.inventory = yaml.safe_load(f.read())
    self.credentials = self.inventory['common_vars']

  def __switch_online(self, host, port):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    result = sock.connect_ex((host, port))
    if result == 0:
      return True
    else:
      return False

  def __poll_switch(self, device):
    with ConnectHandler(**device) as net_connect:
      data = net_connect.send_command("show interface status", use_textfsm=True)
      if data is not None:
        return data
    
  def __format_port(self, port, hostname, ip_addr):
    port.update({'port_name': port['name']})
    port.update({ 'name': hostname })
    port.update({ 'ip_addr': ip_addr })
    return port

  def poll_switches(self):
    data = []
    self.__load_inventory()
    for device in self.inventory['hosts']:
      device.update(self.credentials)
      hostname = device['hostname']
      del device['hostname']
      print("Connecting to " + hostname)
      if 'port' not in device: device.update({'port': 22})
      if(self.__switch_online(device['host'], device['port'])):
        ports = self.__poll_switch(device)
        for port in ports:
          port = self.__format_port(port, hostname, device['host'])
          data.append(port)
      else:
        print("Unable to connect to {}".format(hostname))
    return data