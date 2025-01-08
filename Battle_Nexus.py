import pygame, random
from sys import exit
from math import sqrt
pygame.init() # initialize pygame

clock = pygame.time.Clock() # clock capping frame rate
tick_speed = 60 

map_image = pygame.image.load('Programming_project/graphics/map/map.png')
map_width = map_image.get_width()
map_height = map_image.get_height()

game_screen = { # games screen properties
    'width': map_width,
    'height': map_height,
    'caption': 'Battle Nexus',
    'map': map_image
}

main_menu = { #main menu properties
    'width': 800,
    'height': 600,
    'caption': 'Main Menu',
    'map': 'Programming_project/graphics/main_menu/main_menu.png'
}


player = { # player's properties
    'size': 60,
    'speed': 5,
    'health': 50,
    'damage': 1
}

player_bullet = { #player bullet's properties
    'size': 10,
    'speed': 10,
    'damage': player['damage'],
    'type': 'player'
}


enemy_tank = { # tank properties
    'type': 'tank',
    'size': 200,
    'speed': 0.25,
    'health': 6,
    'damage': 10,
    'attack': 'melee',
    'chance': 20,
    'range': 400,
    'points': 10
}
tank_bullets = { #sniper bullet's properties
    'size': 20,
    'speed': 4,
    'damage': enemy_tank['damage'],
    'type': 'tank'

}

enemy_gladiator = { # gladiator properties
    'type': 'gladiator',
    'size': 60,
    'speed': 3,
    'health': 3,
    'damage': 2,
    'attack': 'melee',
    'chance': 60,
    'range': 0,
    'points': 2
}

enemy_sniper = { #sniper properties
    'type': 'sniper',
    'size': 50,
    'speed': 1,
    'health': 1,
    'damage': 3,
    'attack': 'ranged',
    'chance': 20,
    'range': 350,
    'points': 3

}
sniper_bullets = { #sniper bullet's properties
    'size': 10,
    'speed': 10,
    'damage': enemy_sniper['damage'],
    'type': 'sniper'

}


tank_image = [ # tank animations scaling to the correct size
    pygame.transform.scale(pygame.image.load('Programming_project/graphics/tank/tank_0.png'), (int(enemy_tank['size']), int(enemy_tank['size']))),
    pygame.transform.scale(pygame.image.load('Programming_project/graphics/tank/tank_1.png'), (int(enemy_tank['size']), int(enemy_tank['size'])))
]



gladiator_image = [# gladiator animations scaling to the correct size
    pygame.transform.scale(pygame.image.load('Programming_project/graphics/gladiator/gladiator_0.png'), (int(enemy_gladiator['size']), int(enemy_gladiator['size']))),
    pygame.transform.scale(pygame.image.load('Programming_project/graphics/gladiator/gladiator_1.png'), (int(enemy_gladiator['size']), int(enemy_gladiator['size'])))
]

 # sniper animations scaling to the correct size
sniper_image = pygame.transform.scale(pygame.image.load('Programming_project/graphics/sniper/sniper.png'), (int(enemy_sniper['size']), int(enemy_sniper['size'])))

default_health = player['health'] # this variable keeps the original value for the player's health
current_state = 'main menu' # starting state

def main():
    global current_state, screen, entity_enemy, entity_bullet, player_direction, points
    while True:

        # first main menu screen
        if current_state == 'main menu':
            # main menu screen
            screen = pygame.display.set_mode((main_menu['width'], main_menu['height']))
            pygame.display.set_caption(main_menu['caption'])
            map = pygame.image.load(main_menu['map'])

            # defining button properties for the main menu screen
            button_width = 200
            button_height = 80
            button_x = 550 # where on the x it should be
            button_y = main_menu['height'] // 2 - button_height # where on the y it should be
            button_color = 'black'  
            button_text_color = 'cyan'
            font = pygame.font.Font(None, 50)
            button_text = font.render("Play", True, button_text_color)
            button_rect = pygame.Rect(button_x, button_y, button_width, button_height)

            while True:  # first main menu loop
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pygame.quit()
                        exit()
                    if event.type == pygame.MOUSEBUTTONDOWN:
                        if event.button == 1:  # this i for left mouse button
                            if button_rect.collidepoint(event.pos):
                                current_state = 'difficulty selection'

                screen.blit(map, (0, 0))

                #Draw the play button
                pygame.draw.rect(screen, button_color, button_rect)
                text_rect = button_text.get_rect(center=button_rect.center)
                screen.blit(button_text, text_rect)

                pygame.display.update()
                clock.tick(tick_speed)
                if current_state != 'main menu':
                    break
        
        # difficulty selection screen
        if current_state == 'difficulty selection':
            
            map = pygame.image.load(main_menu['map'])

            #Define buttons for difficulty levels
            button_width = 200
            button_height = 80
            button_spacing = 20
            button_x = 550
            button_y = main_menu['height'] // 2 - button_height

            easy_button_rect = pygame.Rect(button_x, button_y, button_width, button_height)
            normal_button_rect = pygame.Rect(button_x, easy_button_rect.y + button_height + button_spacing, button_width, button_height)
            hard_button_rect = pygame.Rect(button_x, normal_button_rect.y + button_height + button_spacing, button_width, button_height)

            while True:  # difficulty selection loop
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pygame.quit()
                        exit()
                    if event.type == pygame.MOUSEBUTTONDOWN:
                        if event.button == 1: 
                            if easy_button_rect.collidepoint(event.pos):
                                print("Easy difficulty selected")
                                multiplier = 0.8
                                current_state = 'game'
                            elif normal_button_rect.collidepoint(event.pos):
                                print("Normal difficulty selected")
                                multiplier = 1
                                current_state = 'game'
                            elif hard_button_rect.collidepoint(event.pos):
                                print("Hard difficulty selected")
                                multiplier = 1.5
                                current_state = 'game'


                screen.blit(map, (0, 0))

                # Draw each button
                pygame.draw.rect(screen, button_color, easy_button_rect)
                pygame.draw.rect(screen, button_color, normal_button_rect)
                pygame.draw.rect(screen, button_color, hard_button_rect)

                # draw text on buttons
                easy_text = font.render("Easy", True, button_text_color)
                normal_text = font.render("Normal", True, button_text_color)
                hard_text = font.render("Hard", True, button_text_color)

                #creaton of each button on the screen
                screen.blit(easy_text, easy_text.get_rect(center=easy_button_rect.center))
                screen.blit(normal_text, normal_text.get_rect(center=normal_button_rect.center))
                screen.blit(hard_text, hard_text.get_rect(center=hard_button_rect.center))

                pygame.display.update()
                clock.tick(tick_speed)
                if current_state != 'difficulty selection':
                    break






        if current_state == 'game': # loop for the game mechanics
            # game screen properties
            screen = pygame.display.set_mode((game_screen['width'] + 300, game_screen['height']))
            pygame.display.set_caption(game_screen['caption'])
            map = game_screen['map']

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
            points = 0 


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
                player_direction = None  # variable to track the player's direction

                if keys[pygame.K_LEFT] and player['x'] > 0:
                    player['x'] -= player['speed']
                    player_direction = 'west'
                if keys[pygame.K_RIGHT] and player['x'] < game_screen['width'] - player['size']:
                    player['x'] += player['speed']
                    player_direction = 'east'
                if keys[pygame.K_UP] and player['y'] > 0:
                    player['y'] -= player['speed']
                    player_direction = 'north'
                if keys[pygame.K_DOWN] and player['y'] < game_screen['height'] - player['size']:
                    player['y'] += player['speed']
                    player_direction = 'south'

                # second block responsible for the diogonal movement
                if keys[pygame.K_LEFT] and keys[pygame.K_UP]:
                    player_direction = 'northwest'
                if keys[pygame.K_LEFT] and keys[pygame.K_DOWN]:
                    player_direction = 'southwest'
                if keys[pygame.K_RIGHT] and keys[pygame.K_UP]:
                    player_direction = 'northeast'
                if keys[pygame.K_RIGHT] and keys[pygame.K_DOWN]:
                    player_direction = 'southeast'

                # updating all bullets' coordinates
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


                # handle stage progression
                if stage_timer >= stage_interval and not entity_enemy and enemies_spawn_left == 0:
                    stage += 1
                    stage_timer = 0
                    enemies_spawn_left = stage * 2
                    enemies_spawn_at_once = stage // 20 + 1
                    can_spawn = True

                # spawn enemies every spawn_interval frames
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

                        # creating a dictionary for the new enemy
                        new_enemy = {
                            'type': properties['type'],
                            'size': properties['size'],
                            'speed': properties['speed'] * multiplier,
                            'health': properties['health'] * multiplier,
                            'damage': properties['damage'] * multiplier,
                            'attack': properties['attack'],
                            'chance': properties['chance'],
                            'range': properties['range'],
                            'x': enemy_x,
                            'y': enemy_y,
                            'direction_lock': None,
                            'direction_frames': 0,
                            'animation_image': 0,
                            'can_shoot': False,
                            'points': properties['points']
                        }
                        entity_enemy.append(new_enemy) # adds that enemy to the enemy list

                    enemies_spawn_left -= enemies_to_spawn
                    spawn_timer = 0
                    can_spawn = False

                    

                # move enemies toward the player
                for enemy in entity_enemy[:]:
                    # gladiator behaviour
                    if enemy['type'] == 'gladiator':
                        # update the direction only every 20 frames
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
                            enemy['direction_frames'] = 20  # reset the fram counter

                        elif enemy['direction_frames'] // 2 in [0, 1]: # change the gadiator animation frame every 10 frames
                            if enemy['animation_image'] == 0:
                                enemy['animation_image'] = 1
                            else:
                                enemy['animation_image'] = 0

                        
                        # move the enemy in the locked direction
                        if enemy['direction_lock'] == 'east':
                            enemy['x'] += enemy['speed']
                        elif enemy['direction_lock'] == 'west':
                            enemy['x'] -= enemy['speed']
                        elif enemy['direction_lock'] == 'south':
                            enemy['y'] += enemy['speed']
                        elif enemy['direction_lock'] == 'north':
                            enemy['y'] -= enemy['speed']
                        enemy['direction_frames'] -= 1
                    
                    # sniper and tank behavior
                    if enemy['type'] in ['tank', 'sniper']:
                        dx = player['x'] + player['size'] // 2 - (enemy['x'] + enemy['size'] // 2)
                        dy = player['y'] + player['size'] // 2 - (enemy['y'] + enemy['size'] // 2)
                        distance = sqrt(dx ** 2 + dy ** 2)

                        if distance <= enemy['range']:
                            enemy['can_shoot'] = True
                        else:
                            enemy['can_shoot'] = False

                        if enemy['can_shoot']:
                            # cooldown logic for shooting
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
                                enemy['cooldown'] = 60  # cooldown frames

                        else:
                            # movement behavior when not shooting
                            if enemy['direction_frames'] <= 0:
                                if abs(player['x'] - enemy['x']) > abs(player['y'] - enemy['y']):
                                    enemy['direction_lock'] = 'east' if player['x'] > enemy['x'] else 'west'
                                else:
                                    enemy['direction_lock'] = 'south' if player['y'] > enemy['y'] else 'north'
                                enemy['direction_frames'] = 20  # Reset direction frame counter
                                if enemy['type'] == 'tank':
                                    if enemy['animation_image'] == 0:
                                        enemy['animation_image'] = 1
                                    else:
                                        enemy['animation_image'] = 0

                            # move in the locked direction
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
                        points += enemy['points']
                        entity_enemy.remove(enemy)
                        if player['health'] <= 0:
                            current_state = 'game over'

                for bullet in entity_bullet[:]:
                    bullet_rect = pygame.Rect(bullet['x'], bullet['y'], bullet['size'], bullet['size'])
                    
                    # Check collision with enemies for player bullets
                    if bullet['type'] == 'player':
                        for enemy in entity_enemy[:]:
                            enemy_rect = pygame.Rect(enemy['x'], enemy['y'], enemy['size'], enemy['size'])
                            if bullet_rect.colliderect(enemy_rect): 
                                enemy['health'] -= bullet['damage']
                                if bullet in entity_bullet:  # avoid double-removal
                                    entity_bullet.remove(bullet)
                                if enemy['health'] <= 0:  # remove dead enemies
                                    points += enemy['points'] # add points to the total
                                    entity_enemy.remove(enemy)
                                break  # exit loop after handling collision

                    # check collision with the player for enemy bullets
                    elif bullet['type'] != 'player':  # Assuming all other types are enemy bullets
                        player_rect = pygame.Rect(player['x'], player['y'], player['size'], player['size'])
                        if bullet_rect.colliderect(player_rect):  
                            player['health'] -= bullet['damage']
                            if player['health'] <= 0:
                                current_state = 'game over'
                            if bullet in entity_bullet:  # avoid double-removal
                                entity_bullet.remove(bullet)
            


                screen.fill('black')
                screen.blit(map, (0,0))
                draw_points()
                draw_bullets()
                draw_enemies()
                draw_player()
                draw_health_bar()
                draw_stage(stage, stage_timer)


                pygame.display.update()
                clock.tick(tick_speed)
                if current_state != 'game':
                    break

        if current_state == 'game over': # screen when you die
            screen = pygame.display.set_mode((game_screen['width'], game_screen['height']))
            pygame.display.set_caption('Game Over')
            map = game_screen['map']
            font = pygame.font.Font(None, 200)
            while True:
                for event in pygame.event.get(): # safly exiting pygame
                    if event.type == pygame.QUIT:
                        pygame.quit()
                        exit()
                    elif event.type == pygame.KEYDOWN:  
                        if event.key == pygame.K_SPACE:
                            current_state = 'main menu'
                
                screen.blit(map, (0, 0))            
                score_text = font.render(f"Score: {points}", True, 'red')  
                score_rect = score_text.get_rect(center=(game_screen['width'] // 2, game_screen['height'] // 2))
                screen.blit(score_text, score_rect)

                pygame.display.update()
                clock.tick(tick_speed)
                if current_state != 'game over':
                    break
                


            
def draw_player():
    player_image = pygame.image.load('Programming_project/graphics/player/player.png')
    player_image = pygame.transform.scale(player_image, (player['size'], player['size']))     # scale the player image to match player size

    # rotate the image based on the direction
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
        rotated_image = player_image  # default if no direction is set

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

    original_bullet_image = pygame.image.load('Programming_project/graphics/bullets/bullet.png')

    for bullet in entity_bullet:

        scaled_width = int(original_bullet_image.get_width() * 0.05)
        scaled_height = int(original_bullet_image.get_height() * 0.05)
        scaled_bullet_image = pygame.transform.scale(original_bullet_image, (scaled_width, scaled_height))

        # calculate the angle of rotation based on the bullet's direction
        angle = pygame.math.Vector2(bullet['dx'], bullet['dy']).angle_to((0, -1))

        # rotate the scaled bullet image to face the direction of travel
        rotated_bullet = pygame.transform.rotate(scaled_bullet_image, angle)

        # get the new rectangle for the rotated bullet (to center it correctly)
        bullet_rect = rotated_bullet.get_rect(center=(bullet['x'] + bullet['size'] // 2, bullet['y'] + bullet['size'] // 2))

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

def draw_points():
    font = pygame.font.Font(None, 36)  # Choose a font and size
    points_text = font.render(f"Score: {points}", True, 'white')  # Render the points text
    points_rect = points_text.get_rect()
    points_rect.topleft = (game_screen['width'] + 20, 20)  # Position next to the map
    screen.blit(points_text, points_rect)

def draw_stage(stage, stage_timer):
    if stage_timer > 0:
        stage += 1
        font = pygame.font.Font(None, 100)  # Large font size for stage text
        stage_text = font.render(f"Wave: {stage}", True, 'red')  # Render the stage text
        stage_rect = stage_text.get_rect()
        health_bar_y = 20  # Y-coordinate of the health bar
        health_bar_height = 20  # Height of the health bar
        stage_rect.center = (game_screen['width'] // 2, health_bar_y + health_bar_height + 50)  # Center the text below the health bar
        screen.blit(stage_text, stage_rect)



main()
