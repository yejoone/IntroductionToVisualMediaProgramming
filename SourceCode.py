import pygame
import numpy as np

RED = (255, 0, 0)

FPS = 60   # frames per second

WINDOW_WIDTH = 1400
WINDOW_HEIGHT = 800

def getRegularPolygon(nV, radius=1.):
    angle_step = 360. / nV 
    half_angle = angle_step / 2.

    vertices = []
    for k in range(nV):
        degree = angle_step * k 
        radian = np.deg2rad(degree + half_angle)
        x = radius * np.cos(radian)
        y = radius * np.sin(radian)
        vertices.append( [x, y] )
    #
    print("list:", vertices)

    vertices = np.array(vertices)
    print('np.arr:', vertices)
    return vertices

def update_list(alist):
    for a in alist:
        a.update()
#
def draw_list(alist, screen):
    for a in alist:
        a.draw(screen)
#

def Rmat(degree):
    rad = np.deg2rad(degree) 
    c = np.cos(rad)
    s = np.sin(rad)
    R = np.array([ [c, -s, 0],
                   [s,  c, 0], [0,0,1]])
    return R

def Tmat(tx, ty):
    Translation = np.array( [
        [1, 0, tx],
        [0, 1, ty],
        [0, 0, 1]
    ])
    return Translation
#

def draw(P, H, screen, color=(100, 200, 200)):
    R = H[:2,:2]
    T = H[:2, 2]
    Ptransformed = P @ R.T + T 
    pygame.draw.polygon(screen, color=color, 
                        points=Ptransformed, width=3)
    return
#


def main():
    pygame.init() # initialize the engine

    sound = pygame.mixer.Sound("assets/diyong.mp3")
    screen = pygame.display.set_mode( (WINDOW_WIDTH, WINDOW_HEIGHT) )
    clock = pygame.time.Clock()

    w = 300
    h = 40
    X = np.array([ [0,0], [w, 0], [w, h], [0, h] ])
    G = np.array([ [0,0], [30, 0], [30, 10], [0, 10] ])

    position = [WINDOW_WIDTH/2, WINDOW_HEIGHT - 100]
    jointangle1 = 0
    jointangle2 = 0
    jointangle3 = 0
    grip1 = 0
    grip2 = 0
    space_key_pressed = False

    tick = 0
    done = False
    while not done:
        tick += 1
        #  input handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = True

        key = pygame.key.get_pressed()

        if key[pygame.K_SPACE]:
            if not space_key_pressed:
                grip1 += 15
                grip2 -= 15
                space_key_pressed = True
            else:
                grip1 -= 15
                grip2 += 15
                space_key_pressed = False  
                
        elif key[pygame.K_s]:
            jointangle1 += 5
        elif key[pygame.K_a]:
            jointangle1 -= 5
        elif key[pygame.K_f]:
            jointangle2 += 5
        elif key[pygame.K_d]:
            jointangle2 -= 5
        elif key[pygame.K_h]:
            jointangle3 += 5
        elif key[pygame.K_g]:
            jointangle3 -= 5 

        # drawing
        screen.fill( (200, 254, 219))

        # base
        pygame.draw.circle(screen, (255,0,0), position, radius=3)
        H0 = Tmat(position[0], position[1]) @ Tmat(0, -h)
        draw(X, H0, screen, (0,0,0)) # base

        # arm 1
        H1 = H0 @ Tmat(w/2, 0)  
        x, y = H1[0,2], H1[1,2] # joint position
        pygame.draw.circle(screen, (255,0,0), (x,y), radius=3) # joint position
        H12 = H1 @ Tmat(0, h/2) @ Rmat(jointangle1) @ Tmat(0, -h/2)    
        draw(X, H12, screen, (200,200,0)) # arm 1, 90 degree

        # arm 2
        H2 = H12 @ Tmat(w, 0) @ Tmat(0, h/2) # joint 2
        x, y = H2[0,2], H2[1,2]
        pygame.draw.circle(screen, (255,0,0), (x,y), radius=3) # joint position
        H21 = H2 @ Rmat(jointangle2) @ Tmat(0, -h/2)
        draw(X, H21, screen, (0,0, 200))

        # arm 3
        H3= H21 @ Tmat(w, 0) @ Tmat(0, h/2) # joint 3
        x, y = H3[0,2], H3[1,2]
        pygame.draw.circle(screen, (255,0,0), (x,y), radius=3) # joint position
        H31 = H3 @ Rmat(jointangle3) @ Tmat(0, -h/2)
        draw(X, H31, screen, (0,0, 200))

        #grip1
        H4= H31 @ Tmat(w, 0) @ Tmat(0, h/2) 
        H41 = H4 @ Tmat(0, -h/2)
        H41 = H4 @ Rmat(grip1) @ Tmat(0, -h/2)
        draw(G, H41, screen, (0,0, 200))

        #grip2
        H5= H31 @ Tmat(w, 30) @ Tmat(0, h/2) 
        H51 = H5 @ Tmat(0, -h/2)
        H51 = H5 @ Rmat(grip2) @ Tmat(0, -h/2)
        draw(G, H51, screen, (0,0, 200))

        pygame.display.flip()
        clock.tick(FPS)
    # end of while
# end of main()

if __name__ == "__main__":
    main()