import pygame, sys
from pygame.locals import *
import numpy as np
from keras.models import load_model
import cv2


BOUNDARY = 5
WHITE = (255, 255, 255)
BLACK =(0, 0, 0)
RED = (178, 131, 189)

IMAGESAVE = False

MODEL = load_model("bestmodelA-Z.h5")

LABELS = {0:'A', 1:'B',2:'C',3:'D',4:'E',5:'F',6:'G',
             7:'H',8:'I',9:'J',10:'K',11:'L',12:'M',13:'N',
             14:'O',15:'P',16:'Q',17:'R',18:'S',19:'T',
             20:'U',21:'V',22:'W',23:'X',24:'Y',25:'Z'}

print(len(LABELS))
#initialize pygame
pygame.init()

# Create Window/Display
WIDTH, HEIGHT= 640, 480
window = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Digit Board")

FONT = pygame.font.SysFont("Arial.ttf", 40)

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
            pygame.draw.circle(window, WHITE, (Xcoord, Ycoord), 4, 0)
            
            number_Xcoord.append(Xcoord)
            number_Ycoord.append(Ycoord)
            
        if event.type == MOUSEBUTTONDOWN:
            iswriting = True
            
        if event.type == MOUSEBUTTONUP:
            iswriting = False
            number_Xcoord = sorted(number_Xcoord)
            print(number_Xcoord)
            number_Ycoord = sorted(number_Ycoord)
            print(number_Ycoord)
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

                predicted_index = np.argmax(MODEL.predict(image.reshape(1,28,28,1)))
                print(predicted_index)
               
                label = str(LABELS[np.argmax(MODEL.predict(image.reshape(1,28,28,1)))])
                
                textSurface = FONT.render(label, True, BLACK, RED)
                textRectObj = textSurface.get_rect()
                textRectObj.left, textRectObj.bottom = rect_min_x, rect_max_y
                
                window.blit(textSurface, textRectObj)
            
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                window.fill((0, 0, 0))
        
        pygame.display.update()