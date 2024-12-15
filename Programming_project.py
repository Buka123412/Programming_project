import pygame
import sys
import random

pygame.init() #Initializing pygame

clock = pygame.time.Clock() #Clock capping the frame rate


screen_width = 800 #main screen properties
screen_height = 800
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Programming Project")  # This is the name of our window

black = (0, 0, 0) #list of colors for easier use
white = (255, 255, 255)
blue = (0, 0, 255)
green = (0, 255, 0)
red = (255, 0, 0)
yellow = (255, 255, 0)
grey = (128, 128, 128)

player = { #player properties
    "size": 40,
    "speed": 5
}
player["x"] = screen_width // 2 - player["size"] // 2 #starting position of the player
player["y"] = screen_height // 2 - player["size"] // 2
facing = "north"

bullets = { #bullet properties
    "size": 10,
    "speed": 7
}
entity_bullets = [] #a list storing every bullet and their properties as dictionaries

can_shoot = True #cooldown for bullets
shoot_cooldown_time = 0.1
last_shot_time = 0



enemies = { #Enemmy properties
    "size": 40,
    "speed": 1
}
entity_enemies = [] 

spawn_timer = 0 #cooldown for enemie
spawn_interval = 60 #frames between every spawn

def main(): #main loop/tick
    global player_x, player_y, facing, can_shoot, last_shot_time, spawn_timer
    running = True

    while running:
        current_time = pygame.time.get_ticks() / 1000  # Get current time in seconds

        
        for event in pygame.event.get(): #Stops the game and closes the window if we press the close button
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            

        
        keys = pygame.key.get_pressed()  
        if keys[pygame.K_SPACE] and can_shoot: #player's shooting
            if facing == "north":
                x = player["x"] + player["size"] // 2 - bullets["size"] // 2
                y = player["y"] - bullets["size"]
                direction = "north"
                entity_bullets.append({"x": x, "y": y, "direction": direction})
            elif facing == "south":
                x = player["x"] + player["size"] // 2 - bullets["size"] // 2
                y = player["y"] + player["size"] + bullets["size"]
                direction = "south"
                entity_bullets.append({"x": x, "y": y, "direction": direction})
            elif facing == "west":
                x = player["x"] - bullets["size"]
                y = player["y"] + player["size"] // 2 - bullets["size"] // 2
                direction = "west"
                entity_bullets.append({"x": x, "y": y, "direction": direction})
            elif facing == "east":
                x = player["x"] + player["size"]
                y = player["y"] + player["size"] // 2 - bullets["size"] // 2
                direction = "east"
                entity_bullets.append({"x": x, "y": y, "direction": direction})
            can_shoot = False
            last_shot_time = current_time

        if not can_shoot and current_time - last_shot_time >= shoot_cooldown_time:
            can_shoot = True

        if keys[pygame.K_LEFT] and player["x"] > 0: #player's movement
            player["x"] -= player["speed"]
            facing = "west"
        if keys[pygame.K_RIGHT] and player["x"] < screen_width - player["size"]:
            player["x"] += player["speed"]
            facing = "east"
        if keys[pygame.K_UP] and player["y"] > 0:
            player["y"] -= player["speed"]
            facing = "north"
        if keys[pygame.K_DOWN] and player["y"] < screen_height - player["size"]:
            player["y"] += player["speed"]
            facing = "south"

        
        for bullet in entity_bullets[:]:   #Update bullets
            if bullet["direction"] == "north":
                bullet["y"] -= bullets["speed"]
            elif bullet["direction"] == "south":
                bullet["y"] += bullets["speed"]
            elif bullet["direction"] == "west":
                bullet["x"] -= bullets["speed"]
            elif bullet["direction"] == "east":
                bullet["x"] += bullets["speed"]

            # Remove bullets that go off-screen
            if bullet["x"] < 0 or bullet["x"] > screen_width or bullet["y"] < 0 or bullet["y"] > screen_height:
                entity_bullets.remove(bullet)
            
        spawn_timer += 1
        if spawn_timer >= spawn_interval: #spawn of enemies 
            spawn_timer = 0
            corner = random.choice(["top_left", "top_right", "bottom_left", "bottom_right"])
            if corner == "top_left":
                enemy_x, enemy_y = 0, 0
            elif corner == "top_right":
                enemy_x, enemy_y = screen_width - enemies["size"], 0
            elif corner == "bottom_left":
                enemy_x, enemy_y = 0, screen_height - enemies["size"]
            elif corner == "bottom_right":
                enemy_x, enemy_y = screen_width - enemies["size"], screen_height - enemies["size"]
            entity_enemies.append({"x": enemy_x, "y": enemy_y, "size": enemies["size"], "speed": enemies["speed"]})
       
       
        for enemy in entity_enemies[:]:   #Move enemies toward the player
            if abs(enemy["x"] - player["x"]) > abs(enemy["y"] - player["y"]):
                #horizontal movement
                if enemy["x"] < player["x"]:
                    enemy["x"] += enemy["speed"]
                elif enemy["x"] > player["x"]:
                    enemy["x"] -= enemy["speed"]
            else:
                #vertical movement
                if enemy["y"] < player["y"]:
                    enemy["y"] += enemy["speed"]
                elif enemy["y"] > player["y"]:
                    enemy["y"] -= enemy["speed"]
             
            
            for bullet in entity_bullets[:]: #Collision check with bullet
                if enemy["x"] < bullet["x"] < enemy["x"] + enemy["size"] and enemy["y"] < bullet["y"] < enemy["y"] + enemy["size"]:
                    entity_bullets.remove(bullet)
                    entity_enemies.remove(enemy)

                    
        #Drawings on the screen
        screen.fill(black)
        draw_bullets()
        draw_enemies()
        draw_player()
        pygame.display.update()
        clock.tick(60)

def draw_player():
    pygame.draw.rect(screen, blue, (player["x"], player["y"], player["size"], player["size"]))

def draw_bullets():
    for bullet in entity_bullets:
        pygame.draw.rect(screen, red, (bullet["x"], bullet["y"], bullets["size"], bullets["size"]))    

def draw_enemies():
    for enemy in entity_enemies:
        pygame.draw.rect(screen, yellow, (enemy["x"], enemy["y"], enemy["size"], enemy["size"]))

main()
