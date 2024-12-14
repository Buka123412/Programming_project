

#Importing modules that we use
import pygame
import sys

#Initializing pygame
pygame.init()

#Our main screen properties
screen_width = 800
screen_height = 800
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Programming Project")  # This is the name of our window


def main():

    running = True

    while running:

        for event in pygame.event.get():
            #Stops the game and closes the window if we press the close button
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
        
        screen.fill((0, 0, 0))
        pygame.display.update()


main()
