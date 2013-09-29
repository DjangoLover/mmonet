from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response
from django import forms


from .models import *
from .tasks import *
from bulbs.neo4jserver import Graph
from django.template import RequestContext

g = Graph()
g.add_proxy('nd', NetworkDevice)
g.add_proxy('i', Interface)

g.add_proxy('l', Link)

g.add_proxy('contains', Contains)
g.add_proxy('connects', Connects)


class NetworkDeviceForm(forms.Form):
	name = forms.CharField()
	ip=forms.CharField()
	virtual = forms.BooleanField(required=False)

class InterfaceForm(forms.Form):
	name = forms.CharField()


class ConnectionForm(forms.Form):
	ns = g.nd.get_all()
	if ns is not None:
		ns = [x for x in ns]
		xs = x.outV()
		if xs is not None:
			NETWORK_CHOICES = [(x.name, [(y.eid, y.name) for y in x.outV() ]) for x in ns]
	connection_from = forms.ChoiceField(choices = NETWORK_CHOICES)
	connection_to = forms.ChoiceField(choices=NETWORK_CHOICES)

	link_type=forms.ChoiceField(choices=[("L1", "Layer 1"),("L2", "Layer 2"),("L3","Layer 3")])
gs = {
		"NetworkDevice":g.nd,
		"Interface":g.i
	}

fs = {
		"NetworkDevice":NetworkDeviceForm,
		"Interface":InterfaceForm
	}
fields = {
		"NetworkDevice":["name","ip", "virtual"],
		"Interface":["name"],
}


def index(request):
	l = g.nd.get_all()
	if l is None:
		nds = []
	else:
		nds = [x for x in l]
	return render_to_response('inventory.html', {"nodes":nds})


def delete(request):
	delete_node.delay(request.REQUEST.get('uuid'))
	return HttpResponseRedirect('/inventory')


def add(request):
	t = request.REQUEST.get('t')
	i = request.REQUEST.get('in')
	if i is not None and i != "":
		i = gs.get(t).get(i)
	if request.REQUEST.get('name') is not None:
		f = fs.get(t)(request.REQUEST)
		if f.is_valid():
			kwargs = {}
			for field in fields.get(t):
				kwargs[field] = request.REQUEST.get(field)
			d = gs.get(t).create(**kwargs)
			if i is not None and i != "":
				g.contains.create(i,d)

			return HttpResponseRedirect('/inventory')
	else:
		f = fs.get(t)()
	return render_to_response('form.html', RequestContext(request, {"t":t, "form":f, "in":i.eid if i is not None else ""}))

def connect(request):
	f = request.REQUEST.get('connection_from')
	t = request.REQUEST.get('connection_to')
	if f is not None and t is not None:
		l = g.l.create()
		g.connects.create(f,l)
		g.connects.create(l,t)
		return HttpResponseRedirect('/inventory')
	else:
		f = ConnectionForm()
		return render_to_response('form.html', RequestContext(request, {"form":f}))

