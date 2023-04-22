import pygame, sys
from pygame.locals import *
import numpy as np
from keras.models import load_model
import cv2


BOUNDARY = 5
WHITE = (255, 255, 255)
BLACK =(0, 0, 0)
RED = (255, 0, 0)

IMAGESAVE = False

MODEL = load_model("bestmodel.h5")

LABELS = {0: "Zero", 1:"One",
          2: "Two", 3: "Three",
          4: "Four", 5: "Five",
          6: "Six", 7: "Seven",
          8: "Eight", 9: "Nine"}


#initialize pygame
pygame.init()

# Create Window/Display
WIDTH, HEIGHT= 640, 480
window = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Digit Board")

FONT = pygame.font.SysFont("Arial.ttf", 20)

iswriting = False

number_Xcoord = []
number_Ycoord = []

image_count = 1

PREDICT = True
running = True
#loop
while True:
    
    for event in pygame.event.get():
        if event.type == QUIT:
            running = False
            pygame.quit()
            
        
        if event.type == MOUSEMOTION and iswriting:
            Xcoord, Ycoord = event.pos
            print(Xcoord)
            print(Ycoord)
            pygame.draw.circle(window, WHITE, (Xcoord, Ycoord), 4, 0)
            
            number_Xcoord.append(Xcoord)
            number_Ycoord.append(Ycoord)
            
        if event.type == MOUSEBUTTONDOWN:
            iswriting = True
            
        if event.type == MOUSEBUTTONUP:
            iswriting = False
            number_Xcoord = sorted(number_Xcoord)
            number_Ycoord = sorted(number_Ycoord)
            
            rect_min_x, rect_max_x = max(number_Xcoord[0] - BOUNDARY, 0), min(WIDTH, number_Xcoord[-1] + BOUNDARY)
            rect_min_y, rect_max_y = max(number_Ycoord[0] - BOUNDARY, 0), min(number_Ycoord[-1] + BOUNDARY, HEIGHT)

            number_Xcoord =[]
            number_Ycoord = []
            
            img_arr = np.array(pygame.PixelArray(window))[rect_min_x:rect_max_x, rect_min_y:rect_max_y].T.astype(np.float32)
            
            if IMAGESAVE:
                cv2.imwrite("image.png")
                image.count +=1
                
            if PREDICT:
                
                image = cv2.resize(img_arr, (28,28))
                image = np.pad(image, (10,10), 'constant', constant_values = 0)
                image = cv2.resize(image, (28,28))/255

                label = str(LABELS[np.argmax(MODEL.predict(image.reshape(1,28,28,1)))])
                
                textSurface = FONT.render(label, True, RED, WHITE)
                textRectObj = textSurface.get_rect()
                textRectObj.left, textRectObj.bottom = rect_min_x, rect_max_y
                
                window.blit(textSurface, textRectObj)
            
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                window.fill((0, 0, 0))
                print("space pressed")
        
        pygame.display.update()