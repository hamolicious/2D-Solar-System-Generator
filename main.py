import pygame
from time import time
from solar import Sun, randint
from vector_class import Vector2D
from math import degrees

#region pygame init
pygame.init()
size = (1000, 600)
screen = pygame.display.set_mode(size)
screen.fill([255, 255, 255])
pygame.display.set_icon(screen)
clock, fps = pygame.time.Clock(), 0
delta_time = 0
#endregion

planet_recursion_depth = 5
sun = Sun(size, planet_recursion_depth)

bg = pygame.image.load('Data/background.png').convert()

space_ship_idle = pygame.image.load('Data/space_ship_idle.png')
space_ship_moving = pygame.image.load('Data/space_ship_moving.png')
cam_pos = Vector2D()
heading_angle = 90
cam_vel = Vector2D()
cam_speed = 2
cam_max_speed = 2
cam_rot_speed = 0.7

def controll_camera():
    global heading_angle

    forward_vec = Vector2D.from_angle(heading_angle)
    forward_vec.mult(cam_speed)
    forward_vec.mult(delta_time)

    accel = False ; is_forward = False
    if key[pygame.K_w]:
        cam_vel.add(forward_vec)
        accel = is_forward = True
    if key[pygame.K_s]:
        cam_vel.sub(forward_vec)
        accel = True

    if not accel:
        cam_vel.mult(0.995)
    
    if key[pygame.K_a]:
        heading_angle -= cam_rot_speed
    if key[pygame.K_d]:
        heading_angle += cam_rot_speed
    
    if abs(cam_vel.x) > cam_max_speed:
        if cam_vel.x < 0:
            polarity = -1
        else:
            polarity = 1

        cam_vel.x = cam_max_speed * polarity

    if abs(cam_vel.y) > cam_max_speed:
        if cam_vel.y < 0:
            polarity = -1
        else:
            polarity = 1

        cam_vel.y = cam_max_speed * polarity

    cam_pos.add(cam_vel)

    if cam_pos.dist([0, 0]) > max(size)*1.5 : cam_pos.mult(-1)

    return is_forward

key_block = False
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            quit()

    key = pygame.key.get_pressed()
    start_time = time()
    screen.blit(bg, (0, 0))

    if key[pygame.K_SPACE]:
        if not key_block : sun = Sun(size, planet_recursion_depth)

        cam_pos = Vector2D()
        cam_vel = Vector2D()
        heading_angle = 90

        key_block = True
    else:
        key_block = False
    
    accel = controll_camera()
    if accel : image = space_ship_moving
    else     : image = space_ship_idle

    sun.draw(screen, delta_time, cam_pos)
    screen.blit(pygame.transform.rotate(image, -(heading_angle-90)), ((size[0]/2) - 8, (size[1]/2) - 16))

    pygame.display.update()
    clock.tick(fps)
    delta_time = time() - start_time
    pygame.display.set_caption(f'Framerate: {int(clock.get_fps())}')




