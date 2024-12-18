import pygame, sys, random, math

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
gray = (128, 128, 128)

player = { #player properties
    "size": 40,
    "speed": 5,
    "health": 100,
    "damage": 1
}
player["x"] = screen_width // 2 - player["size"] // 2 #starting position of the player
player["y"] = screen_height // 2 - player["size"] // 2

bullets = { #bullet properties
    "size": 10,
    "speed": 7,
}
entity_bullets = [] #a list storing every bullet and their properties as dictionaries

#Enemy properties
tank_properties = {
    "size": 60,
    "speed": 0.5,
    "health": 5,
    "damage": 10
}

sniper_properties = {
    "size": 50,
    "speed": 1,
    "health": 1,
    "damage": 30,
    "range": 500,
    "bullet_speed": 10
}

gladiator_properties = {
    "size": 40,
    "speed": 5,
    "health": 2,
    "damage": 20
}
entity_enemies = [] 

spawn_timer = 0 #cooldown for enemies
spawn_interval = 60 #frames between every spawn

def main(): #main loop/tick
    global spawn_timer

    while True:

        for event in pygame.event.get(): #Stops the game and closes the window if we press the close button
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            
            if event.type == pygame.KEYDOWN: #function responsible for shooting bullets
                if event.key == pygame.K_SPACE:
                    # Check if there are enemies before calculating the nearest one
                    if entity_enemies:
                        nearest_enemy = get_nearest_enemy()
                        # Ensure we don't try to calculate when no enemies exist
                        if nearest_enemy:
                            # Calculate the direction vector
                            dx = nearest_enemy["x"] + nearest_enemy["size"] // 2 - (player["x"] + player["size"] // 2)
                            dy = nearest_enemy["y"] + nearest_enemy["size"] // 2 - (player["y"] + player["size"] // 2)
                            distance = math.sqrt(dx ** 2 + dy ** 2)
                            # Normalize the direction vector
                            if distance != 0:
                                dx /= distance
                                dy /= distance
                                # Spawn a bullet
                                bullet_x = player["x"] + player["size"] // 2 - bullets["size"] // 2
                                bullet_y = player["y"] + player["size"] // 2 - bullets["size"] // 2
                                entity_bullets.append({"x": bullet_x, "y": bullet_y, "dx": dx, "dy": dy, "type": "player"})

        keys = pygame.key.get_pressed() 
        if keys[pygame.K_LEFT] and player["x"] > 0: #player's movement
            player["x"] -= player["speed"]
        if keys[pygame.K_RIGHT] and player["x"] < screen_width - player["size"]:
            player["x"] += player["speed"]
        if keys[pygame.K_UP] and player["y"] > 0:
            player["y"] -= player["speed"]
        if keys[pygame.K_DOWN] and player["y"] < screen_height - player["size"]:
            player["y"] += player["speed"]

        for bullet in entity_bullets[:]: #Loop that updates bullets place
            bullet["x"] += bullet["dx"] * bullets["speed"]
            bullet["y"] += bullet["dy"] * bullets["speed"]

            #Removes bullets that miss and deletes them
            if bullet["x"] < 0 or bullet["x"] > screen_width or bullet["y"] < 0 or bullet["y"] > screen_height:
                entity_bullets.remove(bullet)

        #Spawn enemies
        spawn_timer += 1
        if spawn_timer >= spawn_interval:
            spawn_timer = 0
            enemy_type = random.choice(["gladiator", "sniper", "tank"])
            if enemy_type == "gladiator":
                properties = gladiator_properties
            elif enemy_type == "sniper":
                properties = sniper_properties
            elif enemy_type == "tank":
                properties = tank_properties

            corner = random.choice(["top_left", "top_right", "bottom_left", "bottom_right"])
            if corner == "top_left":
                enemy_x, enemy_y = 0, 0
            elif corner == "top_right":
                enemy_x, enemy_y = screen_width - properties["size"], 0
            elif corner == "bottom_left":
                enemy_x, enemy_y = 0, screen_height - properties["size"]
            elif corner == "bottom_right":
                enemy_x, enemy_y = screen_width - properties["size"], screen_height - properties["size"]

            entity_enemies.append({"x": enemy_x, "y": enemy_y, "size": properties["size"], "speed": properties["speed"], "health": properties["health"], "damage": properties["damage"], "type": enemy_type})
       
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
                    if bullet["type"] == "player":
                        enemy["health"] -= player["damage"]
                        entity_bullets.remove(bullet)
                    if enemy["health"] <= 0:
                        entity_enemies.remove(enemy)
                    break

            if ( #collision check with player and enemy
                enemy["x"] < player["x"] + player["size"]
                and enemy["x"] + enemy["size"] > player["x"]
                and enemy["y"] < player["y"] + player["size"]
                and enemy["y"] + enemy["size"] > player["y"]
            ):
                player["health"] -= enemy["damage"]
                entity_enemies.remove(enemy)
                if player["health"] <= 0:
                    pygame.quit()
                    sys.exit()

        #Drawings on the screen
        screen.fill(black)
        draw_bullets()
        draw_enemies()
        draw_player()
        draw_health_bar()
        pygame.display.update()
        clock.tick(60)

def draw_player(): #
    pygame.draw.rect(screen, blue, (player["x"], player["y"], player["size"], player["size"]))

def draw_bullets():
    for bullet in entity_bullets:
        pygame.draw.rect(screen, red, (bullet["x"], bullet["y"], bullets["size"], bullets["size"]))    

def draw_enemies():
    for enemy in entity_enemies:
        if enemy["type"] == "gladiator":
            color = green
        elif enemy["type"] == "tank":
            color = yellow
        else:
            color = blue
        pygame.draw.rect(screen, color, (enemy["x"], enemy["y"], enemy["size"], enemy["size"]))

def get_nearest_enemy():
    if not entity_enemies: 
        return None #this eliminates the error that occurs if there are no enemies

    nearest_enemy = None #Variable that collects the closest enemy to the player
    min_distance = float('inf') #Variable that starts with a value of infinity and ensures that no enemy is out of this range.
    for enemy in entity_enemies: # loop that runs through every enemy and calculates the distance to it
        distance = math.sqrt((enemy["x"] - player["x"]) ** 2 + (enemy["y"] - player["y"]) ** 2) #this is the formula used to calculate the distance between points in coordinate system
        if distance < min_distance:
            min_distance = distance
            nearest_enemy = enemy
    return nearest_enemy

def draw_health_bar():                                                                                                                                                                                                                                                                                                                                                                                                                                          #Signed by Petko Dimitrov 192
    health_bar_width = 200
    health_bar_height = 20
    health_bar_x = screen_width // 2 - health_bar_width // 2 #aligns player's healthbar's center with the x axis center
    health_bar_y = 20
    # Draws a background for missing health
    pygame.draw.rect(screen, gray, (health_bar_x, health_bar_y, health_bar_width, health_bar_height))
    #Draws remaining health on top of the missing health
    health_width = int((player["health"] / 100) * health_bar_width)
    pygame.draw.rect(screen, red, (health_bar_x, health_bar_y, health_width, health_bar_height))

main()                                                                                                                                                                                                                                                                                                                                                                                                                                                            #Signed by Petko Dimitrov  192         
