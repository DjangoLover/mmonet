from celery import task



from bulbs.neo4jserver import Graph

from .models import * 

import pyping
g = Graph()
g.add_proxy('m', Measure)
g.add_proxy('t', Trigger)
g.add_proxy('tv', TriggerValue)

@task
def run():
	print "run"
	for measure in g.m.get_all():
		print measure.operation
		evaluate.delay(measure.operation, measure.uuid)
	for trigger in g.t.get_all():
		control.delay(trigger)


@task
def evaluate(op, base):
	print "evaluate"
	print op
	print base
	ops = op.split(')')[0]
	ops = ops.split('(')
	op = ops[0]
	arg = ops[1]
	print op

	if op == "rtt":
		print "going..."
		rtt(arg, base)
	elif op == "snmp_get":
		snmp_get.delay(*arg.split(","))

@task
def rtt(address, base):
	print "rtt"
	print address
	print base
	r = pyping.ping(address, count=1)
	print r
	store("/var/mmonet/"+base+".ping.rtt", r.min_rtt)
	store("/var/mmonet/"+base+".ping.loss", r.packet_lost)
	

@task
def control(trigger):
	pass

@task
def snmp_get(oid, ipaddress, port, community="public"):
	pass

@task
def snmp_walk(oid, ipaddress, port, community="public"):
	pass

@task
def ssh(script, username, key, ip, port=22):
	pass

@task
def nmap(ip):
	pass

@task
def store(file, data):
	print "store"
	import whisper
	try:
		whisper.create(file, [(1,60*60*24), (10, 60*60*24), (60, 60*60*24*30) ])
	except:
		pass
	print "update"
	whisper.update(file, data)
