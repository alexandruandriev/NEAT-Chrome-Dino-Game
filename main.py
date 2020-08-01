import pygame
import time
import random
from datetime import datetime
import neat
import os

pygame.init()
class Line:
    def __init__(self,x,y,width,height = 3):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
    def move(self,speed):
        self.x -= speed
        if (self.x + self.width) < 0:
            self.x = random.randrange(1920,5000,50)

class ObstacleManager:
    obstacles = []

    def __init__(self,OBSTACLES):
        self.obs_images = OBSTACLES

    
    

    def createObstacle(self,offset = 0,spawnPos = 2000):

        choice = random.randrange(0,3)
        offset += random.randrange(1000,1200,50)
        cactus = Obstacle(self.obs_images[choice],spawnPos + offset,1080 * 0.8 - self.obs_images[choice].get_height())
        self.obstacles.append(cactus)

    def restart(self):
        self.obstacles = []

    def main(self):
        if len(self.obstacles) > 0 :
            pass
        # If there are no obstacles , it creates 6 initial ones        
        else:   
            self.createObstacle()
            for x in range(0,6):                  
                self.createObstacle(offset = self.obstacles[x].get_width(),spawnPos = self.obstacles[x].x)
        # Returns passed variable
        
        
        



        

                
class Obstacle:
    def __init__(self,img,x,y,passed = False):
        self.x = x
        self.y = y 
        self.img = img
        self.spawnPos = x
        self.passed = passed

    def move(self,speed):
        if self.x  < (0 - self.img.get_width()) :  #Return true if the obstacles is out of the screen
            return True
        
        self.x -= speed
    def get_width(self):
        return self.img.get_width()


       

    def draw(self,screen):
         screen.blit(self.img,(self.x,self.y))

class Dino:
    ANIMATION_TIME = 30
    MAX_JUMP = 600
    def __init__(self,IMGS,x,y):
        self.img = IMGS[0] 
        self.IMGS = IMGS
        self.STARTING_Y = y
        self.x = x
        self.y = y 
        self.count = 0 
        self.img_count = 0
        self.vel = 0
        self.jumped = False
        
           
    def move(self):
        if self.jumped == True:
            if self.y >= self.MAX_JUMP:
                self.vel -= 2
            else:
                self.vel += 2
            self.y = self.y + self.vel

        if self.y >= self.STARTING_Y:
            self.jumped = False
            self.y = self.STARTING_Y
            self.vel = 0    
            #Jump ended
      
       
    def jump(self):
        if self.jumped == False:
            self.vel = -7
            self.jumped = True

    
    def display(self,screen):
        self.img_count += 1 

        if self.img_count < self.ANIMATION_TIME:
            self.img = self.IMGS[1]
        elif self.img_count < self.ANIMATION_TIME * 2:
            self.img = self.IMGS[2]
        elif self.img_count < self.ANIMATION_TIME * 3:
            self.img_count = 0
 
        screen.blit(self.img,(self.x,self.y))
        
#Fonts
default_font = pygame.font.Font('freesansbold.ttf', 50)        

#Screen variables
HEIGHT = 1080
WIDTH = 1920
#Screen settings
screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)

pygame.display.set_caption("Tigan de atac")

#White Background Color
white = (255,255,255)
black = (0,0,0)
screen.fill(white)

SPEED = 8




#Images

IMGS = [pygame.transform.scale(pygame.image.load('./data/dino0000.png'), (96, 112)),pygame.transform.scale(pygame.image.load('./data/dinorun0000.png'), (96, 112)),pygame.transform.scale(pygame.image.load('./data/dinorun0001.png'), (96, 112))]
CACTUSES = [pygame.image.load('./data/cactusSmall0000.png'),pygame.image.load('./data/cactusBig0000.png'),pygame.image.load('./data/cactusSmallMany0000.png')]





# GAME FUNCTIONS
def restart(ObstacleManager):
    ObstacleManager.restart()

def drawRoad(screen):
    """
    return : Y position of the road
    """
    pygame.draw.rect(screen,black,(0,HEIGHT * 0.8,WIDTH,3))
    return HEIGHT * 0.8

def draw_lines(screen,lines):
    if len(lines) > 0:
        for line in lines:
            line.move(SPEED)
            pygame.draw.rect(screen,black,(line.x,line.y,line.width,line.height))      
    else:
        line_width = random.randrange(5,100)
        line_y = random.randrange(HEIGHT * 0.8,HEIGHT) 
        line_x = random.randrange(1920,3000)
            
        NewLine = Line(line_x,line_y,line_width)
        lines.append(NewLine)        
        #Generate lines
        for i in range(0,10):
            line_width = random.randrange(5,100)
            line_y = random.randrange(HEIGHT * 0.8 + 30,HEIGHT - 30,20) 
            line_x = random.randrange(1920,5000,50)
            
            NewLine = Line(line_x,line_y,line_width)
            lines.append(NewLine)
        
def display_score(score):
    text = default_font.render("Score: " + "{:1.0f}".format(score), True, black)
    screen.blit(text,(50,50))
# END OF GAME FUNCTIONS
def main(genomes,config):
    global screen,gen,SPEED
    SPEED = 8

    nets = []
    ge = []
    dinos = []

    for _, g in genomes:
        net = neat.nn.FeedForwardNetwork.create(g,config)
        nets.append(net)
        dinos.append(Dino(IMGS,500,HEIGHT * 0.8 - IMGS[1].get_height()))
        g.fitness = 0
        ge.append(g)

    
    #Game variables
    SCORE = 0
    
    passed = False
    lines = []
    
    #Clock and while loop 
    running = True

    clock = pygame.time.Clock()

    #Instances
    Manager = ObstacleManager(CACTUSES)
    Manager.restart()
    
    obs_ind = 0

    
    while running:
        
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    if not passed:
                        dino.jump()
                    if passed:
                        #Reset everything basically
                        restart(Manager)
                        passed = False
                        SPEED = 8
                        SCORE = 0
                        lines = []
        Manager.main()
        
           
        if len(dinos) > 0:
            pass 
        else:
            run = False
            break
        for x,dino in enumerate(dinos):
            
            dino.move()
            dino.display(screen)

            ge[x].fitness += 0.05
            output = nets[x].activate((dino.y,abs(Manager.obstacles[obs_ind].x  - dino.x ),abs(Manager.obstacles[obs_ind].img.get_width()),abs(Manager.obstacles[obs_ind].img.get_height()),abs(Manager.obstacles[obs_ind + 1].x - Manager.obstacles[obs_ind].x),SPEED))

            if output[0] > 0.7:
                dino.jump()

        SPEED += 0.0005
        SCORE += 0.1    
        display_score(SCORE)
        #Draw background stuff
        draw_lines(screen,lines) 
        drawRoad(screen)
        #Draw Dino
        
        
        #Ostacles 



        index = 0    
        
        for obstacle in Manager.obstacles:
            hasPassed = obstacle.move(SPEED)
            obstacle.draw(screen)
            for x,dino in enumerate(dinos):
                if (dino.x + dino.img.get_width()) >= obstacle.x and  dino.x < (obstacle.x + obstacle.get_width()):
                 #Detects if objects passed on x axis
                    
                    if (dino.y + dino.img.get_height()) > obstacle.y :
                    #If the object also passed on Y axis , it crashed and sets passed to true so the whole code can run
                        ge[x].fitness -= 10
                        dinos.pop(x)
                        nets.pop(x)
                        ge.pop(x)
                if dino.x > obstacle.x + 10  and obstacle.passed == False:
                    for g in ge:
                        g.fitness += 5
                    obs_ind += 1
                    print(obs_ind)
                    print("I passed a obstacle once!")
                    obstacle.passed = True
                    #Object has passed
        
          
                
                
            if hasPassed == True:
                Manager.createObstacle(offset = Manager.obstacles[-1].get_width(),spawnPos = Manager.obstacles[-1].x)
                Manager.obstacles.pop(index)
                obs_ind -= 1
                
            index += 1

        clock.tick(60)
        pygame.display.update()
        screen.fill(white)
        
    
   



# NEAT FUNCTIONS
def run(config_path):
    config = neat.config.Config(neat.DefaultGenome,neat.DefaultReproduction,neat.DefaultSpeciesSet,neat.DefaultStagnation,config_path)

    p = neat.Population(config)
    
    p.add_reporter(neat.StdOutReporter(True))
    stats = neat.StatisticsReporter()
    p.add_reporter(stats)

    winner = p.run(main,100)
# END OF NEAT FUNCTIONS

if __name__ == "__main__":
    local_dir = os.path.dirname(__file__)
    config_path = os.path.join(local_dir,"config.txt")
    run(config_path)
    
