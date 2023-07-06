### Snake Game Environment v1.2
import numpy as np
from PIL import Image
import cv2

class Dot:
    def __init__(self, color, x, y):
        self._color = color
        self.x = x
        self.y = y
    def getColor(self):
        return self._color
    def __str__(self):
        return f"Block- Position: ({self.x}, {self.y}) & ColorBGR: ({self._color[0]}, {self._color[1]}, {self._color[2]})"

class SnakePart(Dot):
    _color = np.array([0,0,230], dtype='uint8')
    def __init__(self, x, y):
        super().__init__(SnakePart._color, x, y)

class FoodPart(Dot):
    _color = np.array([0,255,0], dtype='uint8')
    def __init__(self, x, y):
        super().__init__(FoodPart._color, x, y)

class Snake:
    def __init__(self):
        self.snakeArr = [SnakePart(np.random.randint(WIDTH), np.random.randint(HEIGHT))]
        self.length = len(self.snakeArr)
        self.head = self.snakeArr[-1]
    def showParts(self):
        for item in self.snakeArr:
            print("Snake: ", item)
    def UP(self, food):
        # calculating the next coordinates
        y_next = self.head.y - 1
        x_next = self.head.x

        if (y_next>=0 and y_next<HEIGHT):
            self.Move(food, x_next, y_next)
        elif WORLD_WARP:
            y_next = y_next%HEIGHT
            self.Move(food, x_next, y_next)
    def DOWN(self, food):
        # calculating the next coordinates
        y_next = self.head.y + 1
        x_next = self.head.x
        #print(f"NEXT: {x_next}, {y_next}")
        if (y_next>=0 and y_next<HEIGHT):
            self.Move(food, x_next, y_next)
        elif WORLD_WARP:
            y_next = y_next%HEIGHT
            self.Move(food, x_next, y_next)   
    def RIGHT(self, food):
        # calculating the next coordinates
        y_next = self.head.y
        x_next = self.head.x + 1

        if (x_next>=0 and x_next<WIDTH):
            self.Move(food, x_next, y_next)
        elif WORLD_WARP:
            x_next = x_next%WIDTH
            self.Move(food, x_next, y_next) 
    def LEFT(self, food):
        # calculating the next coordinates
        y_next = self.head.y
        x_next = self.head.x - 1

        if (x_next>=0 and x_next<WIDTH):
            self.Move(food, x_next, y_next)
        elif WORLD_WARP:
            x_next = x_next%WIDTH
            self.Move(food, x_next, y_next)
    def updateHead(self):
        self.snakeArr[-1]._color = np.array([0,0,180], dtype='uint8')
        if len(self.snakeArr)>1:
            self.snakeArr[-2]._color = SnakePart.getColor(SnakePart)
        self.head = self.snakeArr[-1]
    def Move(self, food, x_next, y_next):
        #check for food (should have built a function 🥲)
        foodPresent = False
        snakePresent = False
        #print(food.foodPositions)
        food_index=0
        for foodPart in food.foodPositions:
            if foodPart.x == x_next and foodPart.y == y_next:
                foodPresent = True
                food.foodPositions.pop(food_index)
                food.updateFoodCount()
                # self.snakeArr.append(SnakePart(x_next, y_next))
                break
            food_index+=1
        for snakePart in self.snakeArr:
            if snakePart.x == x_next and snakePart.y == y_next:
                snakePresent = True
                break
        #print(foodPresent, snakePresent)
        if foodPresent:
            self.snakeArr.append(SnakePart(x_next, y_next))
            self.updateHead()
        elif snakePresent:
            print("You ate yourself 👌. GAME OVER ")
            global gameOver
            gameOver = True
        else:
            self.snakeArr.append(SnakePart(x_next, y_next))
            self.snakeArr.pop(0)
            self.updateHead()
            #self.showParts()

class Food:
    foodPositions = [] #[FoodPart obj]
    def __init__(self, MAX_FOOD, snake):
        self.MAX_FOOD = MAX_FOOD
        self.refreshFood(snake) #can't generate food over the snake!
        self.foodCount = len(self.foodPositions)
    def showParts(self):
        for item in self.foodPositions:
            print("Food: ", item)
    def updateFoodCount(self):
        self.foodCount = len(self.foodPositions)
    def refreshFood(self, snake): #call this function periodically in the main loop after few frames or when the food count is low.
        self.foodPositions = []
        for index in range(self.MAX_FOOD):
            x = np.random.randint(WIDTH)
            y = np.random.randint(HEIGHT)
            overlap = False

            #check for overlap with snake
            for snakePart in snake.snakeArr:
                if snakePart.x == x and snakePart.y == y:
                    overlap = True
                    break

            #check for overlap with itself
            for foodPart in self.foodPositions:
                if foodPart.x == x and foodPart.y == y:
                    overlap = True
                    break

            #append new food positions
            if overlap is False:
                self.foodPositions.append(FoodPart(x, y))
            else:
                pass
                #When less available space, then search for adjacent positions of the head for food placement, if unable then game ends in win? 
                #Leave it, too much work 👌.
            self.updateFoodCount()

# Signals Game Over
gameOver = False

## Hyperparameters
WIDTH = 15 # x
HEIGHT = 15 # y
MAX_FOOD = 6
REFRESH_GAP = 16
GAP_INCREMENT = 16
WORLD_WARP = False
ZERO_WAIT = 4
SCREEN_WIDTH = 300 #pixels
SCREEN_HEIGHT = 300

# Initialization of snake
snake = Snake()

# Initialization of food
food = Food(MAX_FOOD, snake)

# snake.showParts()
# food.showParts()

runs = 0
while True:
    key = cv2.waitKeyEx(0)
    if key==27 or gameOver: #ESC for exit or game over naturally
        break
    else:
        if key==2424832: #LEFT
            snake.LEFT(food)
        elif key==2490368: #UP
            snake.UP(food)
        elif key==2555904: #RIGHT
            snake.RIGHT(food)
        elif key==2621440: #DOWN
            snake.DOWN(food)

        ## Frame update section
        image = np.zeros(shape = (HEIGHT, WIDTH, 3), dtype='uint8')

        # --------------------------------------------
        ## Making sense of the coordinates:
        # NOTE: the np_array's indexing is essentially a matrix indexing, so it goes [height or depth , width] from top left
        # but since we are associating x with width the real coordinate becomes (y,x) not (x,y) with the origin from top left.
        # So, a actual coordinate (5, 1) will be rendered like going one step down and 5 steps right.
        # I should probably take a transpose 🤔, but I am lazy. Will instead adjust the keymappings accordingly 🤡.
        # --------------------------------------------

        # Paint the snake
        for snakePart in snake.snakeArr:
            image[snakePart.y, snakePart.x] = Dot.getColor(SnakePart)
        image[snake.head.y, snake.head.x] = snake.head.getColor() #change the head color

        ## Refresh the food distribution
        if runs%REFRESH_GAP == 0 or food.foodCount==0:
            food.refreshFood(snake)
        # Decreases the refresh rate every GAP_INCREMENT step
        if runs%GAP_INCREMENT == 0:
            REFRESH_GAP+=2
        # Ensuring players don't wait too long for food generation if available space is low
        if food.foodCount==0:
            zero_count+=1
        else:
            zero_count=0
        if zero_count == ZERO_WAIT:
            print("You won!! 🤡")
            gameOver = True
        
        # Paint the cake
        for foodPart in food.foodPositions:
            image[foodPart.y, foodPart.x] = Dot.getColor(FoodPart)

        # Processing
        img = Image.fromarray(image, "RGB")
        img = img.resize((SCREEN_WIDTH, SCREEN_HEIGHT), resample=Image.Resampling.BOX) #make sure to keep same aspect ratio for scaling (WIDTH, HEIGHT)

        # Rendering
        cv2.imshow("snake v1.2.1", np.array(img))
    runs += 1