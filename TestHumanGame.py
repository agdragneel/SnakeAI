import pygame
import random

pygame.init()


'''
The game board will be like a graph, with Y axis being 400 units, and X axis being 600 units.
Each cell will be 20 units tall and wide.
To note, the coordinate system in PyGame starts with (0,0) at top left. Y increases downwards, X increases towards right.
'''
#DIMENSIONS
WIDTH,HEIGHT=600,400 #Dimensions of  the game window
GRID_SIZE=20  #Each cell size.
GRID_WIDTH=WIDTH//GRID_SIZE
GRID_HEIGHT=HEIGHT//GRID_SIZE
FONT = pygame.font.Font(None, 36)

#Colour Tuples
WHITE=(255,255,255)
RED=(255,0,0)
GREEN=(0,255,0)

#Directions
UP=(0,-1)
DOWN=(0,1)
LEFT=(-1,0) 
RIGHT=(1,0)

'''
Class for creating the snake itself, and define it movements and characteristics.
'''

class Snake:
    def __init__(self):
        self.score=0
        self.length=1
        self.positions=[((WIDTH//2),(HEIGHT//2))] #Centering the Snake initially. 
        self.direction=random.choice([UP,DOWN,LEFT,RIGHT])
        self.color=GREEN

    def get_head_position(self):
        return self.positions[0]

    def turn(self,point):
        if self.length>1 and (point[0]*-1,point[1]*-1)==self.direction:  #To prevent reversal of direction
            return
        else:
            self.direction=point

    def move(self):
        cur=self.get_head_position()
        x,y=self.direction
        new = (((cur[0] + (x * GRID_SIZE)) % WIDTH), (cur[1] + (y * GRID_SIZE)) % HEIGHT)

        #Collission checking

        if len(self.positions) > 2 and new in self.positions[2:]: 
            #If the new position is already in list of positions, a collision has happened.
            #Since head can not collide with previous head, so first two indexes are ignored.
            self.reset()
        else:
            self.positions.insert(0,new)
            if len(self.positions) > self.length:    
                self.positions.pop()                #Last element is popped off if the movement is done without eating food.

    def reset(self):
        # Reset the snake to its initial state
        self.length = 1
        self.positions = [((WIDTH // 2), (HEIGHT // 2))]
        self.direction = random.choice([UP, DOWN, LEFT, RIGHT])
        self.score=0
    
    def draw(self,surface):
        for p in self.positions:
            r=pygame.Rect((p[0],p[1]),(GRID_SIZE,GRID_SIZE)) #Rectangle Parameters
            pygame.draw.rect(surface,self.color,r) #Draws Rectangle Filled
            pygame.draw.rect(surface,WHITE,r,1)# Draws Unfilled White Rectangle at same place, as border

    def handle_keys(self):
        for event in pygame.event.get():
            if event.type==pygame.QUIT:
                pygame.quit()
            elif event.type==pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    self.turn(UP)
                elif event.key == pygame.K_DOWN:
                    self.turn(DOWN)
                elif event.key == pygame.K_LEFT:
                    self.turn(LEFT)
                elif event.key == pygame.K_RIGHT:
                    self.turn(RIGHT)


'''Food Class for creating the food that will make the snake grow.'''

class Food:
    def __init__(self):
        self.position=(0,0)
        self.color=RED
        self.randomize_position()

    def randomize_position(self):
        self.position=(random.randint(0,GRID_WIDTH-1)*GRID_SIZE, random.randint(0,GRID_HEIGHT-1)*GRID_SIZE)
    def draw(self,surface):
        r = pygame.Rect((self.position[0], self.position[1]), (GRID_SIZE, GRID_SIZE))
        pygame.draw.rect(surface,self.color,r)
        pygame.draw.rect(surface,self.color,r,1)

'''Utility Functions'''

def draw_score(surface, score):
    score_text = FONT.render(f"Score: {score}", True, (0,0,0))
    surface.blit(score_text, (10, 10))


    
'''Main Function'''

def main():
    window=pygame.display.set_mode((WIDTH,HEIGHT))
    pygame.display.set_caption("Snake Game")

    clock=pygame.time.Clock()

    snake=Snake()
    food=Food()


    while True:
        
            window.fill(WHITE)	
            snake.handle_keys()
            snake.move()

            if snake.get_head_position()==food.position:
                snake.length+=1
                snake.score+=1
                food.randomize_position()

            

            snake.draw(window)
            food.draw(window)
            #print(snake.score)
            draw_score(window,snake.score)

            pygame.display.update()
            clock.tick(10)

if __name__ == '__main__':
    main()