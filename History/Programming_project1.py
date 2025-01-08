import pygame, random
from sys import exit
from math import sqrt
pygame.init() # initialize pygame

clock = pygame.time.Clock() # clock capping frame rate
tick_speed = 60 

game_screen = { # games screen properties
    'width': 1200,
    'height': 900,
    'caption': 'Battle Nexus',
    'map': 'Programming_project/graphics/map/map.png'
}

main_menu = { #main menu properties
    'width': 800,
    'height': 600,
    'caption': 'Main Menu',
    'map': 'Programming_project/graphics/main_menu/main_menu.png'
}


player = { # player's properties
    'size': 40,
    'speed': 5,
    'health': 10,
    'damage': 1
}

player_bullet = { #player bullet's properties
    'size': 10,
    'speed': 7,
    'damage': player['damage'],
    'type': 'player'
}

enemy_tank = { # tank properties
    'type': 'tank',
    'size': 100,
    'speed': 0.5,
    'health': 5,
    'damage': 10,
    'attack': 'melee',
    'chance': 20,
    'range': 350
}
tank_bullets = { #sniper bullet's properties
    'size': 10,
    'speed': 5,
    'damage': enemy_tank['damage'],
    'type': 'tank'

}

enemy_gladiator = { # gladiator properties
    'type': 'gladiator',
    'size': 40,
    'speed': 5,
    'health': 3,
    'damage': 2,
    'attack': 'melee',
    'chance': 60,
    'range': 0
}

enemy_sniper = { #sniper properties
    'type': 'sniper',
    'size': 30,
    'speed': 3,
    'health': 1,
    'damage': 3,
    'attack': 'ranged',
    'chance': 20,
    'range': 350

}
sniper_bullets = { #sniper bullet's properties
    'size': 10,
    'speed': 10,
    'damage': enemy_sniper['damage'],
    'type': 'sniper'

}
# Scale factor for the tank images
tank_scale_factor = 2  # Adjust this value as needed to scale up

tank_image = [
    pygame.transform.scale(
        pygame.image.load('Programming_project/graphics/tank/tank_0.png'),
        (int(enemy_tank['size'] * tank_scale_factor), int(enemy_tank['size'] * tank_scale_factor))
    ),
    pygame.transform.scale(
        pygame.image.load('Programming_project/graphics/tank/tank_1.png'),
        (int(enemy_tank['size'] * tank_scale_factor), int(enemy_tank['size'] * tank_scale_factor))
    )
]

# Scale factor for the gladiator images
gladiator_scale_factor = 1.5  # Adjust this value as needed

gladiator_image = [
    pygame.transform.scale(
        pygame.image.load('Programming_project/graphics/gladiator/gladiator_0.png'),
        (int(enemy_gladiator['size'] * gladiator_scale_factor), int(enemy_gladiator['size'] * gladiator_scale_factor))
    ),
    pygame.transform.scale(
        pygame.image.load('Programming_project/graphics/gladiator/gladiator_1.png'),
        (int(enemy_gladiator['size'] * gladiator_scale_factor), int(enemy_gladiator['size'] * gladiator_scale_factor))
    )
]

# Scale factor for the sniper image
sniper_scale_factor = 1.5  # Adjust this value as needed for scaling down

sniper_image = pygame.transform.scale(
    pygame.image.load('Programming_project/graphics/sniper/sniper.png'),
    (int(enemy_sniper['size'] * sniper_scale_factor), int(enemy_sniper['size'] * sniper_scale_factor))
)



default_health = player['health'] # this variable shouldnt change and resets the values when a new games is started
current_state = 'main menu' # starting position

def main():
    global current_state, screen, entity_enemy, entity_bullet, player_direction
    while True:

        if current_state == 'main menu':
            # main menu screen
            screen = pygame.display.set_mode((main_menu['width'], main_menu['height']))
            pygame.display.set_caption(main_menu['caption'])
            map = pygame.image.load(main_menu['map'])

            # Define button properties
            button_width = 200
            button_height = 80
            button_x = 550
            button_y = main_menu['height'] // 2 - button_height
            button_color = 'black'  
            button_text_color = 'cyan'
            font = pygame.font.Font(None, 50)
            button_text = font.render("Play", True, button_text_color)
            button_rect = pygame.Rect(button_x, button_y, button_width, button_height)

            while True:  # main menu loop
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pygame.quit()
                        exit()
                    if event.type == pygame.MOUSEBUTTONDOWN:
                        if event.button == 1:  # Left mouse button
                            if button_rect.collidepoint(event.pos):
                                current_state = 'difficulty selection'
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_SPACE:
                            current_state = 'difficulty selection'

                screen.blit(map, (0, 0))

                # Draw the button
                pygame.draw.rect(screen, button_color, button_rect)
                text_rect = button_text.get_rect(center=button_rect.center)
                screen.blit(button_text, text_rect)

                pygame.display.update()
                clock.tick(tick_speed)
                if current_state != 'main menu':
                    break

        if current_state == 'difficulty selection':
            # Difficulty selection screen
            map = pygame.image.load(main_menu['map'])

            # Define buttons for difficulty levels
            button_width = 200
            button_height = 80
            button_spacing = 20
            button_x = 550
            button_y = main_menu['height'] // 2 - button_height

            easy_button_rect = pygame.Rect(button_x, button_y, button_width, button_height)
            normal_button_rect = pygame.Rect(button_x, easy_button_rect.y + button_height + button_spacing, button_width, button_height)
            hard_button_rect = pygame.Rect(button_x, normal_button_rect.y + button_height + button_spacing, button_width, button_height)

            while True:  # Difficulty selection loop
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pygame.quit()
                        exit()
                    if event.type == pygame.MOUSEBUTTONDOWN:
                        if event.button == 1:  # Left mouse button
                            if easy_button_rect.collidepoint(event.pos):
                                print("Easy difficulty selected")
                                current_state = 'game'
                            elif normal_button_rect.collidepoint(event.pos):
                                print("Normal difficulty selected")
                                current_state = 'game'
                            elif hard_button_rect.collidepoint(event.pos):
                                print("Hard difficulty selected")
                                current_state = 'game'

                # Draw the background map
                screen.blit(map, (0, 0))

                # Draw the buttons
                pygame.draw.rect(screen, button_color, easy_button_rect)
                pygame.draw.rect(screen, button_color, normal_button_rect)
                pygame.draw.rect(screen, button_color, hard_button_rect)

                # Draw text on buttons
                easy_text = font.render("Easy", True, button_text_color)
                normal_text = font.render("Normal", True, button_text_color)
                hard_text = font.render("Hard", True, button_text_color)

                screen.blit(easy_text, easy_text.get_rect(center=easy_button_rect.center))
                screen.blit(normal_text, normal_text.get_rect(center=normal_button_rect.center))
                screen.blit(hard_text, hard_text.get_rect(center=hard_button_rect.center))

                pygame.display.update()
                clock.tick(tick_speed)
                if current_state != 'difficulty selection':
                    break






        if current_state == 'game': # loop for the game mechanics
            # game screen 
            screen = pygame.display.set_mode((game_screen['width'], game_screen['height']))
            pygame.display.set_caption(game_screen['caption'])
            map = pygame.image.load(game_screen['map'])

            # starting position for the player
            player['x'] = (game_screen['width'] - player['size']) // 2
            player['y'] = (game_screen['height'] - player['size']) // 2

            # variables for the spawning logic
            stage_timer = 0  # how many frames have passed since the end of the last stage
            stage_interval = 600 # how many are needed for the start of the next stage
            stage = 1 #which stage it is
            enemies_spawn_left = stage * 2  # how many enemies are left to spawn in the stage
            enemies_spawn_at_once = stage // 20 + 1 # how many enemies to spawn at once
            can_spawn = False # starting position for spawn logic
            spawn_timer = 0 # frames since the last spawn
            spawn_interval = 180 # how often to spawn
            entity_bullet = [] # list containing all bullets
            entity_enemy = [] # list containing all enemies
            player['health'] = default_health


            while True: # game loop 
                for event in pygame.event.get(): # safly exiting pygame
                    if event.type == pygame.QUIT:
                        pygame.quit()
                        exit()
                    
                    # player's shooting
                    if event.type == pygame.KEYDOWN: 
                        if event.key == pygame.K_SPACE:
                            if entity_enemy:
                                nearest_enemy = get_nearest_enemy()
                                if nearest_enemy:
                                    dx = nearest_enemy['x'] + nearest_enemy['size'] // 2 - (player['x'] + player['size'] // 2)
                                    dy = nearest_enemy['y'] + nearest_enemy['size'] // 2 - (player['y'] + player['size'] // 2)
                                    distance = sqrt(dx ** 2 + dy ** 2)
                                    if distance != 0:
                                        dx /= distance
                                        dy /= distance
                                        # Create a new bullet dictionary
                                        new_bullet = {
                                            'size': player_bullet['size'],
                                            'speed': player_bullet['speed'],
                                            'damage': player_bullet['damage'],
                                            'type': player_bullet['type'],
                                            'dx': dx,
                                            'dy': dy,
                                            'x': player['x'] + player['size'] // 2 - player_bullet['size'] // 2,
                                            'y': player['y'] + player['size'] // 2 - player_bullet['size'] // 2,
                                        }
                                        entity_bullet.append(new_bullet) # add the bullet to the entity list



                # player's movement
                keys = pygame.key.get_pressed() 
                player_direction = None  # Variable to track the player's direction

                if keys[pygame.K_LEFT] and player['x'] > 0:
                    player['x'] -= player['speed']
                    player_direction = 'left'
                if keys[pygame.K_RIGHT] and player['x'] < game_screen['width'] - player['size']:
                    player['x'] += player['speed']
                    player_direction = 'right'
                if keys[pygame.K_UP] and player['y'] > 0:
                    player['y'] -= player['speed']
                    player_direction = 'up'
                if keys[pygame.K_DOWN] and player['y'] < game_screen['height'] - player['size']:
                    player['y'] += player['speed']
                    player_direction = 'down'

                # Handle diagonal movement
                diagonal_directions = []
                if keys[pygame.K_LEFT] and keys[pygame.K_UP]:
                    diagonal_directions.append('left-up')
                if keys[pygame.K_LEFT] and keys[pygame.K_DOWN]:
                    diagonal_directions.append('left-down')
                if keys[pygame.K_RIGHT] and keys[pygame.K_UP]:
                    diagonal_directions.append('right-up')
                if keys[pygame.K_RIGHT] and keys[pygame.K_DOWN]:
                    diagonal_directions.append('right-down')

                if diagonal_directions:
                    player_direction = diagonal_directions[0]  # Assign the first detected diagonal direction
                # updating all bullets' place
                
                for bullet in entity_bullet[:]:
                    bullet['x'] += bullet['dx'] * bullet['speed']
                    bullet['y'] += bullet['dy'] * bullet['speed']

                    # removing bullets that go off the screen
                    if bullet['x'] < 0 or bullet['x'] > game_screen['width'] or bullet['y'] < 0 or bullet['y'] > game_screen['height']:
                        entity_bullet.remove(bullet)
                
                
                # logic for spawning
                spawn_timer += 1
                if not entity_enemy and enemies_spawn_left == 0:
                    stage_timer += 1
                else:
                    stage_timer += 0


                # handle stage progression
                if stage_timer >= stage_interval and not entity_enemy and enemies_spawn_left == 0:
                    stage += 1
                    stage_timer = 0
                    enemies_spawn_left = stage * 2
                    enemies_spawn_at_once = stage // 20 + 1
                    can_spawn = True

                # Spawn enemies every spawn_interval frames
                if spawn_timer >= spawn_interval and enemies_spawn_left > 0:
                    can_spawn = True

                # how to spawn enemies
                if can_spawn:
                    enemies_to_spawn = min(enemies_spawn_at_once, enemies_spawn_left)
                    for _ in range(enemies_to_spawn):
                        # Randomly select enemy type
                        chance = random.randint(1, 100)
                        if chance <= enemy_tank['chance']:
                            properties = enemy_tank.copy()
                        elif chance <= enemy_tank['chance'] + enemy_gladiator['chance']:
                            properties = enemy_gladiator.copy()
                        else:
                            properties = enemy_sniper.copy()
                        
                        # random spawn location
                        corner = random.randint(1, 16)
                        if corner == 1:
                            enemy_x, enemy_y = 0, 0
                        elif corner == 2:
                            enemy_x, enemy_y = game_screen['width'] // 4 - properties['size'], 0
                        elif corner == 3:
                            enemy_x, enemy_y = game_screen['width'] // 2 - properties['size'], 0
                        elif corner == 4:
                            enemy_x, enemy_y = game_screen['width'] * 3 // 4 - properties['size'], 5
                        elif corner == 5:
                            enemy_x, enemy_y = game_screen['width'] - properties['size'], 0
                        elif corner == 6:
                            enemy_x, enemy_y = game_screen['width'] - properties['size'], game_screen['height'] // 4 - properties['size']
                        elif corner == 7:
                            enemy_x, enemy_y = game_screen['width'] - properties['size'], game_screen['height'] // 2 - properties['size']
                        elif corner == 8:
                            enemy_x, enemy_y = game_screen['width'] - properties['size'], game_screen['height'] * 3 // 4 - properties['size']
                        elif corner == 9:
                            enemy_x, enemy_y = game_screen['width'] - properties['size'], game_screen['height'] - properties['size']
                        elif corner == 10:
                            enemy_x, enemy_y = game_screen['width'] * 3 // 4 - properties['size'], game_screen['height'] - properties['size']
                        elif corner == 11:
                            enemy_x, enemy_y = game_screen['width'] // 2 - properties['size'], game_screen['height'] - properties['size']
                        elif corner == 12:
                            enemy_x, enemy_y = game_screen['width'] // 4 - properties['size'], game_screen['height'] - properties['size']
                        elif corner == 13:
                            enemy_x, enemy_y = 0, game_screen['height'] - properties['size']
                        elif corner == 14:
                            enemy_x, enemy_y = 0, game_screen['height'] * 3 // 4 - properties['size']
                        elif corner == 15:
                            enemy_x, enemy_y = 0, game_screen['height'] // 2 - properties['size']
                        elif corner == 16:
                            enemy_x, enemy_y = 0, game_screen['height'] // 4 - properties['size']

                        new_enemy = {
                            'type': properties['type'],
                            'size': properties['size'],
                            'speed': properties['speed'],
                            'health': properties['health'],
                            'damage': properties['damage'],
                            'attack': properties['attack'],
                            'chance': properties['chance'],
                            'range': properties['range'],
                            'x': enemy_x,
                            'y': enemy_y,
                            'direction_lock': None,
                            'direction_frames': 0,
                            'animation_image': 0,
                            'can_shoot': False
                        }
                        entity_enemy.append(new_enemy) # adds to the enemy list

                    enemies_spawn_left -= enemies_to_spawn
                    spawn_timer = 0
                    can_spawn = False

                #Move enemies toward the player
                for enemy in entity_enemy[:]:
                    if enemy['type'] == 'gladiator':
                        # Update the direction only every 20 frames
                        if enemy['direction_frames'] <= 0:
                            if abs(player['x'] - enemy['x']) > abs(player['y'] - enemy['y']):
                                if player['x'] > enemy['x']:
                                    enemy['direction_lock'] = 'east'
                                else:
                                    enemy['direction_lock'] = 'west'
                            else:
                                if player['y'] > enemy['y']:
                                    enemy['direction_lock'] = 'south'
                                else:
                                    enemy['direction_lock'] = 'north'
                            enemy['direction_frames'] = 20  # Reset the frame counter
                        
                        # Move the enemy in the locked direction
                        if enemy['direction_lock'] == 'east':
                            enemy['x'] += enemy['speed']
                        elif enemy['direction_lock'] == 'west':
                            enemy['x'] -= enemy['speed']
                        elif enemy['direction_lock'] == 'south':
                            enemy['y'] += enemy['speed']
                        elif enemy['direction_lock'] == 'north':
                            enemy['y'] -= enemy['speed']

                        # Decrement the frame counter
                        enemy['direction_frames'] -= 1
                    
                    # Snipers and Tanks behavior
                    if enemy['type'] in ['tank', 'sniper']:
                        dx = player['x'] + player['size'] // 2 - (enemy['x'] + enemy['size'] // 2)
                        dy = player['y'] + player['size'] // 2 - (enemy['y'] + enemy['size'] // 2)
                        distance = sqrt(dx ** 2 + dy ** 2)

                        if distance <= enemy['range']:
                            enemy['can_shoot'] = True
                        else:
                            enemy['can_shoot'] = False

                        if enemy['can_shoot']:
                            # Cooldown logic for shooting
                            if 'cooldown' not in enemy:
                                enemy['cooldown'] = 0
                            enemy['cooldown'] -= 1

                            if enemy['cooldown'] <= 0:  # Shoot only when cooldown allows
                                dx /= distance
                                dy /= distance
                                bullet_properties = tank_bullets if enemy['type'] == 'tank' else sniper_bullets
                                new_bullet = {
                                    'size': bullet_properties['size'],
                                    'speed': bullet_properties['speed'],
                                    'damage': bullet_properties['damage'],
                                    'type': bullet_properties['type'],
                                    'dx': dx,
                                    'dy': dy,
                                    'x': enemy['x'] + enemy['size'] // 2 - bullet_properties['size'] // 2,
                                    'y': enemy['y'] + enemy['size'] // 2 - bullet_properties['size'] // 2,
                                }
                                entity_bullet.append(new_bullet)
                                enemy['cooldown'] = 60  # Set cooldown (adjust as needed)

                        else:
                            # Movement behavior when not shooting
                            if enemy['direction_frames'] <= 0:
                                if abs(player['x'] - enemy['x']) > abs(player['y'] - enemy['y']):
                                    enemy['direction_lock'] = 'east' if player['x'] > enemy['x'] else 'west'
                                else:
                                    enemy['direction_lock'] = 'south' if player['y'] > enemy['y'] else 'north'
                                enemy['direction_frames'] = 20  # Reset direction frame counter

                            # Move in the locked direction
                            if enemy['direction_lock'] == 'east':
                                enemy['x'] += enemy['speed']
                            elif enemy['direction_lock'] == 'west':
                                enemy['x'] -= enemy['speed']
                            elif enemy['direction_lock'] == 'south':
                                enemy['y'] += enemy['speed']
                            elif enemy['direction_lock'] == 'north':
                                enemy['y'] -= enemy['speed']

                            enemy['direction_frames'] -= 1


                


                            




                        

                        



                
                    # colision check with player
                    if enemy['x'] < player['x'] + player['size'] and enemy['x'] + enemy['size'] > player['x'] and enemy['y'] < player['y'] + player['size'] and enemy['y'] + enemy['size'] > player['y']:
                        player['health'] -= enemy['damage']
                        entity_enemy.remove(enemy)
                        if player['health'] <= 0:
                            current_state = 'main menu'

                for bullet in entity_bullet[:]:
                    bullet_rect = pygame.Rect(bullet['x'], bullet['y'], bullet['size'], bullet['size'])
                    
                    # Check collision with enemies for player bullets
                    if bullet['type'] == 'player':
                        for enemy in entity_enemy[:]:
                            enemy_rect = pygame.Rect(enemy['x'], enemy['y'], enemy['size'], enemy['size'])
                            if bullet_rect.colliderect(enemy_rect):  # Detect collision
                                enemy['health'] -= bullet['damage']
                                if bullet in entity_bullet:  # Avoid double-removal
                                    entity_bullet.remove(bullet)
                                if enemy['health'] <= 0:  # Remove dead enemies
                                    entity_enemy.remove(enemy)
                                break  # Exit loop after handling collision

                    # Check collision with the player for enemy bullets
                    elif bullet['type'] != 'player':  # Assuming all other types are enemy bullets
                        player_rect = pygame.Rect(player['x'], player['y'], player['size'], player['size'])
                        if bullet_rect.colliderect(player_rect):  # Detect collision
                            player['health'] -= bullet['damage']
                            if player['health'] <= 0:
                                current_state = 'main menu'
                            if bullet in entity_bullet:  # Avoid double-removal
                                entity_bullet.remove(bullet)

       



                screen.blit(map, (0,0))
                draw_bullets()
                draw_enemies()
                draw_player()
                draw_health_bar()


                pygame.display.update()
                clock.tick(tick_speed)
                if current_state != 'game':
                    break

            
def draw_player():
    player_image = pygame.image.load('Programming_project/graphics/player/player.png')

    # Rotate the image based on the direction
    if player_direction == 'north':
        rotated_image = player_image
    elif player_direction == 'east':
        rotated_image = pygame.transform.rotate(player_image, -90)
    elif player_direction == 'south':
        rotated_image = pygame.transform.rotate(player_image, 180)
    elif player_direction == 'west':
        rotated_image = pygame.transform.rotate(player_image, 90)
    elif player_direction == 'northeast':
        rotated_image = pygame.transform.rotate(player_image, -45)
    elif player_direction == 'southeast':
        rotated_image = pygame.transform.rotate(player_image, -135)
    elif player_direction == 'southwest':
        rotated_image = pygame.transform.rotate(player_image, 135)
    elif player_direction == 'northwest':
        rotated_image = pygame.transform.rotate(player_image, 45)
    else:
        rotated_image = player_image  # Default if no direction is set

    screen.blit(rotated_image, (player['x'], player['y']))

def draw_enemies():
    for enemy in entity_enemy:
        if enemy['type'] == 'tank':
            image = tank_image[enemy['animation_image']]
            if enemy['direction_lock'] == 'west':
                image = pygame.transform.rotate(image, 270)
            elif enemy['direction_lock'] == 'north':
                image = pygame.transform.rotate(image, 180)
            elif enemy['direction_lock'] == 'east':
                image = pygame.transform.rotate(image, 90)
        elif enemy['type'] == 'sniper':
            image = sniper_image
            if enemy['direction_lock'] == 'west':
                image = pygame.transform.rotate(image, 90)
            elif enemy['direction_lock'] == 'south':
                image = pygame.transform.rotate(image, 180)
            elif enemy['direction_lock'] == 'east':
                image = pygame.transform.rotate(image, 270)
        elif enemy['type'] == 'gladiator':
            image = gladiator_image[enemy['animation_image']]
            if enemy['direction_lock'] == 'west':
                image = pygame.transform.flip(image, True, False)
        screen.blit(image, (enemy['x'], enemy['y']))
        
        
        
            
        

def get_nearest_enemy():
    if not entity_enemy: 
        return None #this eliminates the error that occurs if there are no enemies
    
    nearest_enemy = None
    min_distance = float('inf')
    for enemy in entity_enemy:
        distance = sqrt((enemy['x'] - player['x']) ** 2 + (enemy['y'] - player['y']) ** 2)
        if distance < min_distance:
            min_distance = distance
            nearest_enemy = enemy
    return nearest_enemy

def draw_bullets():
    # Load the bullet image
    original_bullet_image = pygame.image.load('Programming_project/graphics/bullets/bullet.png')

    for bullet in entity_bullet:
        # Scale the bullet image down by 0.8
        scaled_width = int(original_bullet_image.get_width() * 0.1)
        scaled_height = int(original_bullet_image.get_height() * 0.1)
        scaled_bullet_image = pygame.transform.scale(original_bullet_image, (scaled_width, scaled_height))

        # Calculate the angle of rotation based on the bullet's direction
        # Subtract 90 degrees because the image is assumed to point upward by default
        angle = pygame.math.Vector2(bullet['dx'], bullet['dy']).angle_to((0, -1))

        # Rotate the scaled bullet image to face the direction of travel
        rotated_bullet = pygame.transform.rotate(scaled_bullet_image, angle)

        # Get the new rectangle for the rotated bullet (to center it correctly)
        bullet_rect = rotated_bullet.get_rect(center=(bullet['x'] + bullet['size'] // 2, bullet['y'] + bullet['size'] // 2))

        # Blit the rotated bullet image onto the screen
        screen.blit(rotated_bullet, bullet_rect.topleft)


def draw_health_bar():
    health_bar_width = 200
    health_bar_height = 20
    health_bar_x = game_screen['width'] // 2 - health_bar_width // 2 #aligns player's healthbar's center with the x axis center
    health_bar_y = health_bar_height
    # Draws a background for missing health
    pygame.draw.rect(screen, 'gray', (health_bar_x, health_bar_y, health_bar_width, health_bar_height))
    #Draws remaining health on top of the missing health
    health_width = int((player['health'] / default_health) * health_bar_width)
    pygame.draw.rect(screen, 'red', (health_bar_x, health_bar_y, health_width, health_bar_height))




main()
