import pygame
import numpy as np

pygame.init()

width = 640
height = 640

running = True
image = None

def mandelbrot(p0,p1, width, height):
    x0,y0=p0
    x1,y1=p1
    result = np.zeros((width,height))
    for y in np.arange(0,height):
        yy = y0+float(y)/height*(y1-y0)        
        for x in np.arange(0,width):
            xx = x0+float(x)/width*(x1-x0)
            # at this point (xx,yy) is c in the mandelbrot equation.
            # for now just test whether it's inside the unit circle.
            if xx**2+yy**2<1.0:
                result[x,y]=1.0
    return result


def toImage(nparray):
    Z = 255 * nparray  # np array is assumed to range from 0 to 1.
    return pygame.surfarray.make_surface(Z)

def updateViewport(p0,p1,key):
    (x0,y0)=p0
    (x1,y1)=p1
    if key == pygame.K_a or key == pygame.K_z:
        zoom = 1.1 if key == pygame.K_a else 1.0/1.1
        x0new = (x1+x0)/2-zoom*(x1-x0)/2
        y0new = (y1+y0)/2-zoom*(y1-y0)/2
        x1new = x0new + zoom*(x1-x0)
        y1new = y0new + zoom*(y1-y0)
        return (x0new,y0new),(x1new,y1new)
    else:        
        tx = 0.1*(x1-x0)*(1 if key==pygame.K_RIGHT else -1 if key == pygame.K_LEFT else 0)
        ty = 0.1*(y1-y0)*(1 if key==pygame.K_DOWN else -1 if key == pygame.K_UP else 0)
        return (x0+tx,y0+ty),(x1+tx,y1+ty)

display = pygame.display.set_mode((width, height))
p0 = (-2,-2)
p1 = (2,2)

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            p0,p1 = updateViewport(p0,p1,event.key)
            print('updated viewport',p0,p1)
            image=None

    if image is None:
        image = mandelbrot(p0,p1,width,height)
    display.blit(toImage(image), (0, 0))
    pygame.display.update()
pygame.quit()
