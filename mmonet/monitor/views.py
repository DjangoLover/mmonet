from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response
from django import forms

from .models import *
from inventory.models import *
from monitor.tasks import *
from bulbs.neo4jserver import Graph
from django.template import RequestContext
g = Graph()

g.add_proxy('nd', NetworkDevice)
g.add_proxy('i', Interface)
g.add_proxy('l', Link)
g.add_proxy('m', Measure)
g.add_proxy('t', Trigger)
g.add_proxy('tv', TriggerValue)

g.add_proxy('connects', Connects)
g.add_proxy('measures', Measures)
g.add_proxy('has_trigger', HasTrigger)
g.add_proxy('has_value', HasValue)
g.add_proxy('has_state', HasState)



class MeasureForm(forms.Form):
	component = forms.ChoiceField(choices = [
		("Nodes",[(x.eid,x.name) for x in g.nd.get_all()]), 
		("Links", [(z.eid,"%s-%s <-> %s-%s" % (
			[b for b in [a for a in z.inV()][0].inV()][0].name,
			[a for a in z.inV()][0].name,
			[b for b in [a for a in z.outV()][0].inV()][0].name,
			[a for a in z.outV()][0].name)
		) for z in g.l.get_all()]),
		("Interfaces",[(u.eid, "%s-%s" % (
			[a for a in u.inV()][0].name,
			u.name)
		) for u in g.i.get_all()]),
	])
	frequency = forms.IntegerField()
	name = forms.CharField()
	operation = forms.CharField()

class TriggerForm(forms.Form):
	measure = forms.ChoiceField(choices = [
		(x.eid,x.name) for x in g.m.get_all()
		])

class TriggerValueForm(forms.Form):
	trigger_type=forms.ChoiceField(choices = [
	])

	trigger_value = forms.CharField()




def index(request):
	measures = g.m.get_all()
	if measures is not None:
		measures = [x for x in measures]
	else:
		measures = []
	return render_to_response('monitor.html', {"measures":measures})

def add_measure(request):
	if request.method == "POST":
		f = MeasureForm(request.REQUEST)
		if f.is_valid():
			d = g.m.create(frequency = request.REQUEST.get('frequency'), operation = request.REQUEST.get('operation'), name=request.REQUEST.get('name'))
			i = g.nd.get(request.REQUEST.get('component'))
			g.measures.create(d,i)
			return HttpResponseRedirect('/monitor')
	else:
		f = MeasureForm()
	return render_to_response('form.html', RequestContext(request, { "form":f}))

def delete(request):
	eid = request.REQUEST.get('eid')
	g.vertices.delete(eid)
	return HttpResponseRedirect('/monitor')

def add_trigger(request):
	if request.method == "POST":
		f = TriggerForm(request.REQUEST)
		if f.is_valid():
			d = g.t.create()
			i = g.m.get(request.REQUEST.get('measure'))
			g.has_trigger.create(d,i)
			return HttpResponseRedirect('/monitor')
	else:
		f = TriggerForm()
	return render_to_response('form.html', RequestContext(request, { "form":f}))

def add_trigger_value(request):
	pass