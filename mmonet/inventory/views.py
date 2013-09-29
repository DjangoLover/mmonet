from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response
from django import forms


from .models import *
from .tasks import *
from bulbs.neo4jserver import Graph
g = Graph()
g.add_proxy('nd', NetworkDevice)
g.add_proxy('i', Interface)

g.add_proxy('contains', Contains)


class NetworkDeviceForm(forms.Form):
	name = forms.CharField()
	ip=forms.CharField()
	virtual = forms.BooleanField(required=False)

class InterfaceForm(forms.Form):
	name = forms.CharField()


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
	if i is not None:
		i = gs.get(t).get(i)
	if request.REQUEST.get('name') is not None:
		f = fs.get(t)(request.REQUEST)
		if f.is_valid():
			kwargs = {}
			for field in fields:
				kwargs[field] = request.REQUEST.get(field)
			d = gs.get(t).create(**kwargs)
			if i is not None:
				g.contains.create(i,d)
			return HttpResponseRedirect('/inventory')
	else:
		f = fs.get(t)()
	return render_to_response('form.html', {"t":t, "form":f})

