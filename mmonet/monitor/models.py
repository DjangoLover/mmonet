from bulbs.model import Node, Relationship
from bulbs.property import String, Integer, DateTime, Bool, Float, Null
from bulbs.utils import current_datetime

import datetime

import os 
	
def uuidify():
	from uuid import uuid4
	return str(uuid4())


import json



class Measure(Node):
	element_type = "Measure"
	uuid = String(default=uuidify)
	name = String()
	operation = String()

	def data(self, t = datetime.datetime.now() - datetime.timedelta(minutes=30)):
		ret = []
		import whisper
		for fn in os.listdir("/var/mmonet/"):
			if fn.startswith(self.uuid):
				print fn
				ret.append(whisper.fetch("/var/mmonet/"+fn, t))
				print ret
		return json.dumps(zip(*ret))




class Trigger(Node):
	element_type = "Trigger"
	uuid = String(default=uuidify)	

class TriggerValue(Node):
	element_type = "TriggerValue"
	uuid = String(default=uuidify)	
	trigger_type = String()
	trigger_value = String()





class Measures(Relationship):
	label="measures"

class HasTrigger(Relationship):
	label="has_trigger"

class HasValue(Relationship):
	label="has_value"

class HasState(Relationship):
	label="has_state"
