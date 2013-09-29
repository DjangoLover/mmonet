from bulbs.model import Node, Relationship
from bulbs.property import String, Integer, DateTime, Bool, Float, Null
from bulbs.utils import current_datetime

	
def uuidify():
	from uuid import uuid4
	return str(uuid4())

class NetworkDeviceType(Node):
	element_type = "NetworkDeviceType"
	uuid = String(default=uuidify)
	name = String()

class DeviceType(Node):
	element_type = "DeviceType"
	uuid = String(default=uuidify)
	name = String()


class LinkType(Node):
	element_type = "LinkType"
	uuid = String(default=uuidify)
	name = String()


class Facility(Node):
	element_type = "Facility"
	uuid = String(default=uuidify)
	name = String()

class Rack(Node):
	element_type = "Rack"
	uuid = String(default=uuidify)
	name = String()

	lon=Float()
	lat = Float()

class NetworkDevice(Node):
	element_type = "NetworkDevice"
	uuid = String(default=uuidify)
	name = String()

	ip = String(nullable=False)
	virtual = Bool(default=False)

class SSHAgent(Node):
	element_type = "SSHAgent"
	uuid = String(default=uuidify)
	username = String(nullable=False)
	key = String(nullable=False)

	host_key=String()

	def run_command(command):
		import paramiko
		client = paramiko.SSHClient()
		if self.host_key is None:
			client.set_missing_host_key_policy(paramiko.client.AutoAddPolicy())
		client.load_system_host_keys()
		client.connect(self.device.ip)
		stdin, stdout, stderr = client.exec_command(command)
		return stdin, stdout, stderr

class Service(Node):
	element_type = "Service"
	uuid = String(default=uuidify)
	name = String()

	service_type = String()

class Storage(Node):
	element_type = "Storage"
	uuid = String(default=uuidify)
	name = String()

class Interface(Node):
	element_type = "Interface"
	uuid = String(default=uuidify)
	name = String()
	
class Link(Node):
	element_type = "Link"
	uuid = String(default=uuidify)
	bidirectional = Bool(default=True)



class Connects(Relationship):
	label="connects"

class Contains(Relationship):
	label="contains"

