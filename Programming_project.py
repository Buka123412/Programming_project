

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


#player properties
player_width = 40
player_height = 40
player_x = screen_width // 2
player_y = screen_height // 2
player_speed = 0.5



def main():
    global player_x, player_y
    running = True

    while running:

        #Stops the game and closes the window if we press the close button
        for event in pygame.event.get():
            
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
        
        
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            player_x -= player_speed
        if keys[pygame.K_RIGHT]:
            player_x += player_speed
        if keys[pygame.K_UP]:
            player_y -= player_speed
        if keys[pygame.K_DOWN]:
            player_y += player_speed
        
        screen.fill((0, 0, 0))
        draw_player()
        pygame.display.update()

def draw_player():
    pygame.draw.rect(screen, (0, 0, 255), (player_x - player_width // 2, player_y - player_height // 2, player_width, player_height))

main()
