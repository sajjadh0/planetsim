import math
import pygame
import sys 

pygame.init()


width, height= 1500,800
win= pygame.display.set_mode((width, height))
pygame.display.set_caption("Planet Simulation")

camera_x, camera_y = 0, 0




class Planet:
    AU= (149.6e6 * 1000)
    G= 6.67428e-11
    scale= 50/AU 
    timestep= 3600*24

    def __init__(self, x, y, radius, colour, mass):
        self.x=x
        self.y= y
        self.radius= radius
        self.colour= colour
        self.mass= mass
        self.orbit = []
        self.sun= False
        self.distance= 0

        self.x_vel=0
        self.y_vel=0

    def draw(self, win):
        x= self.x* self.scale+ width/2
        y=self.y*self.scale+ height/2
        pygame.draw.circle(win, self.colour, (x,y), self.radius)
        

    def attraction(self, other):
        other_x, other_y= other.x, other.y
        distance_x= other_x - self.x
        distance_y= other_y - self.y
        distance= math.sqrt(distance_x**2 + distance_y**2)

        if other.sun:
            self.distance_to_sun= distance

        force= self.G* self.mass*other.mass/distance**2
        theta =  math.atan2(distance_y, distance_x)
        force_x= math.cos(theta)*force
        force_y= math.sin(theta)*force
        return force_x, force_y
    


    def position(self, planets):
        total_fx= total_fy= 0
        for planet in planets:
            if self==planet:
                continue
            
            fx, fy= self.attraction(planet)
            total_fx += fx
            total_fy += fy

        self.x_vel += total_fx/self.mass* self.timestep
        self.y_vel += total_fy/self.mass* self.timestep

        self.x += self.x_vel* self.timestep
        self.y += self.y_vel* self.timestep
        self.orbit.append((self.x,self.y))




def main():
    run= True
    clock = pygame.time.Clock()
    sun= Planet(0,0, 10, (255, 255, 0),1.98892* 10**30)
    sun.sun= True

    mercury = Planet(0.387 * Planet.AU, 0, 6, (64, 64, 64), 3.30 * 10**23)
    mercury.y_vel = -47.4 * 1000

    venus = Planet(0.723 * Planet.AU, 0, 12, (255, 255, 255), 4.8685 * 10**24)
    venus.y_vel = -35.02 * 1000

    earth = Planet(-1 * Planet.AU, 0, 14, (0, 0, 255), 5.9742 * 10**24)
    earth.y_vel = 29.783 * 1000

    mars = Planet(-1.524 * Planet.AU, 0, 8, (255, 0, 0), 6.39 * 10**23)
    mars.y_vel = 24.077 * 1000

    # jupiter= Planet(-5.20* Planet.AU, 0, 22, (255, 165, 0), 1.898* 10**27)
    # jupiter.y_vel = 13.07 *1000
    #
    # saturn= Planet(-9.58*Planet.AU, 0, 21, (218, 165, 32), 5.683* 10**26)
    # saturn.y_vel=9.69 *1000
    #
    # neptune= Planet(-30.07*Planet.AU, 0, 16,  (0, 0, 128), 1.024* 10**26)
    # neptune.y_vel=5.43 *1000
    #
    # uranus= Planet(-19.22*Planet.AU,0, 16, (135, 206, 235), 8.681*10**25)
    # uranus.y_vel= 6.81 *1000
    # planets= [sun, mercury, venus, earth, mars, jupiter, saturn, neptune, uranus]

    while run:
        clock.tick(150)
        # win.fill((0,0,0))

        for event in pygame.event.get():
            if event.type== pygame.QUIT:
                run= False

        mouse_x, mouse_y = pygame.mouse.get_pos()        

        camera_x = mouse_x - width // 2
        camera_y = mouse_y - height // 2

        win.fill((0,0,0))



        for planet in planets:
            planet.position(planets)
            planet.draw(win)

        pygame.display.flip()
        pygame.display.update()

    pygame.quit()
    # sys.exit()

main()
