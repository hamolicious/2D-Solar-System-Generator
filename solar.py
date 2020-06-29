import pygame
from random import randint
from vector_class import Vector2D

class Sun():
    def __init__(self, screen_size, depth):
        self.pos = Vector2D(screen_size[0]/2, screen_size[1]/2)
        self.r = screen_size[0]/15

        self.colour = [255, 255, 0]

        self.children = []
        for _ in range(randint(2, 5)):
            self.children.append(Planet(self, depth-1))

    def draw(self, screen, delta_time, cam_pos):
        pygame.draw.circle(screen, self.colour, ((self.pos + cam_pos).get()), int(self.r))

        if abs(cam_pos.x) + abs(cam_pos.y) < self.r : draw_line = True
        else                                : draw_line = False

        for child in self.children:
            child.draw(screen, delta_time, cam_pos, draw_line)

class Planet():
    def __init__(self, parent, depth):
        self.parent = parent
        self.rel_angle = randint(0, 360)
        self.rel_delta_angle = randint(-35, 25) + 5
        self.distance = randint(int(parent.r*2), int(parent.r*5))
        self.r = randint(int(parent.r*0.5), int(parent.r*0.8))

        self.colour = [randint(50, 255) for _ in range(3)]

        self.pos = Vector2D.from_angle(self.rel_angle)
        self.pos.mult(self.distance)
        self.pos.add(self.parent.pos)

        self.children = []
        if depth > 0:
            for _ in range(randint(0, 2)):
                self.children.append(Planet(self, depth-1))

    def draw(self, screen, delta_time, cam_pos, draw_line):
        self.rel_angle += self.rel_delta_angle * delta_time

        self.pos = Vector2D.from_angle(self.rel_angle)
        self.pos.mult(self.distance)
        self.pos.add(self.parent.pos)

        if draw_line:
            pygame.draw.aaline(screen, [20, 20, 20], (self.pos + cam_pos).get(), (self.parent.pos + cam_pos).get(), 1)
        pygame.draw.circle(screen, self.colour, ((self.pos + cam_pos).get()), int(self.r))

        for child in self.children:
            child.draw(screen, delta_time, cam_pos, draw_line)





