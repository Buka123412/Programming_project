import pygame
import sys

#Initializing pygame
pygame.init()

#Clock capping the frame rate
clock = pygame.time.Clock()

#Our main screen properties
screen_width = 800
screen_height = 800
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Programming Project")  # This is the name of our window

#list of colors for easier use

black = (0, 0, 0)
white = (255, 255, 255)
blue = (0, 0, 255)
green = (0, 255, 0)
red = (255, 0, 0)
yellow = (255, 255, 0)
grey = (128, 128, 128)

#player properties
player = {
    "size": 40,
    "speed": 5
}
#starting position of the player
player["x"] = screen_width // 2 - player["size"] // 2
player["y"] = screen_height // 2 - player["size"] // 2
facing = "north"

bullets = {
    "size": 10,
    "speed": 7
}
entity_bullets = []

#cooldown for bullets
can_shoot = True
shoot_cooldown_time = 0.1
last_shot_time = 0



def main():
    global player_x, player_y, facing, can_shoot, last_shot_time
    running = True

    while running:
        current_time = pygame.time.get_ticks() / 1000  # Get current time in seconds

        #Stops the game and closes the window if we press the close button
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            

        #player movement and shooting
        keys = pygame.key.get_pressed()
        if keys[pygame.K_SPACE] and can_shoot:
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

        if keys[pygame.K_LEFT] and player["x"] > 0:
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

        #Update bullets
        for bullet in entity_bullets[:]:
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

        #Drawings on the screen
        screen.fill(black)
        draw_bullets()
        draw_player()
        pygame.display.update()
        clock.tick(60)

def draw_player():
    pygame.draw.rect(screen, blue, (player["x"], player["y"], player["size"], player["size"]))

def draw_bullets():
    for bullet in entity_bullets:
        pygame.draw.rect(screen, red, (bullet["x"], bullet["y"], bullets["size"], bullets["size"]))    

main()
