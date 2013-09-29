from celery import task

from bulbs.neo4jserver import Graph
g = Graph()

@task
def delete_node(id):
	el = g.vertices.delete(id)
