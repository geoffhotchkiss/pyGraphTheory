#! /usr/bin/env python

import pygame
import math

class Edge:
	""" An edge. """
	def __init__(self, surface, vertex1, vertex2, color, label = ""):
		self.surface = surface
		self.vertex1 = vertex1
		self.vertex2 = vertex2
		self.color = color
		self.label = label
	
	def draw(self):
		pygame.draw.line(self.surface, self.color, self.vertex1.center, 
						self.vertex2.center)

class Vertex:
	""" A vertex. """
	def __init__(self, surface, center, radius, color, label = ""):
		self.surface = surface
		self.center = center
		self.radius = radius
		self.color = color
		self.label = label
	
	def selected(self, event):
		""" Returns true iff the vertex was clicked on. """
		h, k = self.center
		x, y = event.pos 
		distance = math.sqrt( math.pow(x-h, 2) + math.pow(y-k, 2) )
		return distance <= self.radius
	
	def draw(self):
		pygame.draw.circle(self.surface, self.color, self.center, 
							self.radius)


width = 800
height = 600
radius = 5
current_vertex = previous_vertex = 0
vertex_color = (255, 255, 255)
edge_color = (0, 255, 0)
vertex_set = []
edge_set = []

title = "Graph Drawing"

screen = pygame.display.set_mode((width, height))
pygame.display.set_caption(title)
clock = pygame.time.Clock()

running = True

while running:
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			running = False
		elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
			placed = False
			for vertex in vertex_set:
				placed = vertex.selected(event)
				if placed:
					previous_vertex = current_vertex
					current_vertex = vertex
					print "You selected the vertex centered at (%d, %d) " %\
							event.pos
					break
			if not placed:
				previous_vertex = current_vertex
				current_vertex = Vertex(screen, event.pos, radius,
										vertex_color)
				vertex_set.append(current_vertex)
		elif event.type == pygame.MOUSEBUTTONDOWN:
			print "You are pressing the mouse button"
		elif event.type == pygame.KEYDOWN and event.key == pygame.K_e:
			if current_vertex != 0 and previous_vertex != 0:
				current_edge = Edge(screen, current_vertex, 
									previous_vertex, edge_color)
				edge_set.append(current_edge)
		elif event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
			del vertex_set[:]
			del edge_set[:]
			previous_vertex = current_vertex = 0
			screen.fill((0, 0, 0))
	for vertex in vertex_set:
		vertex.draw()
	for edge in edge_set:
		edge.draw()
	pygame.display.flip()
	clock.tick(240)
