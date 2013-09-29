from celery import task

from bulbs.neo4jserver import Graph
g = Graph()

@task
def ping(ipaddress, base):
	import pyping
	r = pyping.ping(ipaddress, count=1)
	store.delay(base+".ping.rtt", r.min_rtt)
	store.delay(base+".ping.loss", r.packet_lost)

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
	import whisper
	whisper.update(file, data)