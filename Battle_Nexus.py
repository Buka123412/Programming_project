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

play_button = { #play button in the main menu properties
    'width': 100,
    'height': 50,
    'color': 'red',
    'font': pygame.font.Font(None, 36),
    'text': 'Play'
}
scoreboard_button = {
    'width': 100,
    'height': 50,
    'color': 'red',
    'font': pygame.font.Font(None, 36),
    'text': 'Scorecoard'
}
# The properties for all buttons that apear after you press play
easy_button = { 
    'width': 100,
    'height': 50,
    'color': 'red',
    'font': pygame.font.Font(None, 36),
    'text': 'Easy'
}
normal_button = {
    'width': easy_button['width'],
    'height': easy_button['height'],
    'color': easy_button['color'],
    'font': easy_button['font'],
    'text': 'Normal'
}
hard_button = {
    'width': easy_button['width'],
    'height': easy_button['height'],
    'color': easy_button['color'],
    'font': easy_button['font'],
    'text': 'Hard'
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
    'range': 0
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
    'spped': 10,
    'damage': enemy_sniper['damage'],
    'type': 'sniper'

}


default_health = player['health'] # this variable shouldnt change and resets the values when a new games is started
current_state = 'main menu' # starting position

def main():
    global current_state, screen, entity_enemy, entity_bullet 
    while True:

        if current_state == 'main menu':
            # main menu screen
            screen = pygame.display.set_mode((main_menu['width'], main_menu['height']))
            pygame.display.set_caption(main_menu['caption'])
            map = pygame.image.load(main_menu['map'])

            while True: # main menu loop
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pygame.quit()
                        exit()
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_SPACE:
                            current_state = 'game'
                            

                screen.blit(map,(0,0))
                pygame.display.update()
                clock.tick(tick_speed)
                if current_state != 'main menu':
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
            stage_interval = 60 # how many are needed for the start of the next stage
            stage = 1 #which stage it is
            enemies_spawn_left = stage * 2  # how many enemies are left to spawn in the stage
            enemies_spawn_at_once = stage // 20 + 1 # how many enemies to spawn at once
            can_spawn = False # starting position for spawn logic
            spawn_timer = 0 # frames since the last spawn
            spawn_interval = 60 # how often to spawn
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
                if keys[pygame.K_LEFT] and player['x'] > 0:
                    player['x'] -= player['speed']
                if keys[pygame.K_RIGHT] and player['x'] < game_screen['width'] - player['size']:
                    player['x'] += player['speed']
                if keys[pygame.K_UP] and player['y'] > 0:
                    player['y'] -= player['speed']
                if keys[pygame.K_DOWN] and player['y'] < game_screen['height'] - player['size']:
                    player['y'] += player['speed']

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
                            'direction_frames': 4,
                            'animation_image': 1
                        }
                        entity_enemy.append(new_enemy) # adds to the enemy list

                    enemies_spawn_left -= enemies_to_spawn
                    spawn_timer = 0
                    can_spawn = False

                #Move enemies toward the player
                for enemy in entity_enemy[:]:


                    if enemy['type'] != 'sniper':
                        if enemy['direction_frames'] == 0 or enemy['direction_lock'] is None:
                            if abs(player['x'] - enemy['x']) > abs(player['y'] - enemy['y']):
                                enemy['direction_lock'] = 'horizontal'
                            else:
                                enemy['direction_lock'] = 'vertical'
                            enemy['direction_frames'] = 4
                            
                        
                        if enemy['direction_lock'] == 'horizontal':
                            if player['x'] > enemy['x']:
                                enemy['x'] += enemy['speed']
                            elif player['x'] < enemy['x']:
                                enemy['x'] -= enemy['speed']
                        
                        if enemy['direction_lock'] == 'vertical':
                            if player['y'] > enemy['y']:
                                enemy['y'] += enemy['speed']
                            elif player['y'] < enemy['y']:
                                enemy['y'] -= enemy['speed']
                        enemy['direction_frames'] -= 1
                        
                        if enemy['direction_frames'] == 0:
                            if enemy['animation_image'] == 1:
                                enemy['animation_image'] = 2
                            elif enemy['animation_image'] == 2: 
                                enemy['animation_image'] = 1
                            enemy['direction_lock'] = None

                


                            




                        

                        



                
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
                            if bullet in entity_bullet:  # Avoid double-removal
                                entity_bullet.remove(bullet)

       


                draw_circles()
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
    pygame.draw.rect(screen, 'blue', (player['x'], player['y'], player['size'], player['size']))

def draw_enemies():
    for enemy in entity_enemy:
        if enemy['type'] == 'gladiator':
            color = 'black'
        elif enemy['type'] == 'tank':
            color = 'yellow'
        elif enemy['type'] == 'sniper':
            color = 'blue'
        pygame.draw.rect(screen, color, (enemy['x'], enemy['y'], enemy['size'], enemy['size']))

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
    for bullet in entity_bullet:
        if bullet['type'] == 'player':
            color = 'red'
        elif bullet['type'] == 'sniper':
            color = 'yellow'
        pygame.draw.rect(screen, color, (bullet['x'], bullet['y'], bullet['size'], bullet['size']))

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

def draw_circles():
    circle_can_shoot = pygame.draw.circle(screen, (0, 0, 0, 0), (player['x'] + player['size'], player['y'] + player['size']), enemy_sniper['range'] - 50 )
    circcle_can_move = pygame.draw.circle(screen, (0, 0, 0, 0), (player['x'] + player['size'], player['y'] + player['size']), enemy_sniper['range'] )
     



main()
