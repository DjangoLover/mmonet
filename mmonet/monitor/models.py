from bulbs.model import Node, Relationship
from bulbs.property import String, Integer, DateTime, Bool, Float, Null
from bulbs.utils import current_datetime




	
def uuidify():
	from uuid import uuid4
	return str(uuid4())





class Measure(Node):
	element_type = "Measure"
	uuid = String(default=uuidify)
	frequency = Integer()
	operation = String()

class Trigger(Node):
	element_type = "Trigger"
	uuid = String(default=uuidify)	
	formula = String()

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
