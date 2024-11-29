import pygame
import random
import sys
import math


pygame.init()


SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
FPS = 30


WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
ORANGE = (255, 165, 0)
AQUA = (0, 255, 255)
PURPLE = (128, 0, 128)
GRAY = (169, 169, 169)


def get_type_color(creature_type):
    if creature_type == 'Fire':
        return ORANGE
    elif creature_type == 'Water':
        return AQUA
    elif creature_type == 'Electric':
        return YELLOW
    elif creature_type == 'Grass':
        return GREEN
    elif creature_type == 'Normal':
        return GRAY
    elif creature_type == 'Dragon':
        return PURPLE
    return WHITE 


class Creature:
    def __init__(self, name, p_type, hp, moves, image_path):
        self.name = name
        self.type = p_type
        self.hp = hp
        self.max_hp = hp
        self.moves = moves
        self.image = pygame.image.load(image_path)
        self.image = pygame.transform.scale(self.image, (200, 200))  
        self.rect = self.image.get_rect()
    def is_alive(self):
        return self.hp > 0

    def take_damage(self, damage):
        self.hp -= damage
        if self.hp < 0:
            self.hp = 0

    def draw(self, screen, x, y):
  
        screen.blit(self.image, (x, y))


        type_color = get_type_color(self.type)  
        pygame.draw.rect(screen, BLACK, (x, y + 200, 200, 10)) 
        pygame.draw.rect(screen, type_color, (x, y + 200, 200 * (self.hp / self.max_hp), 10)) 

    def choose_move(self):
        return self.moves[random.randint(0, len(self.moves) - 1)]


type_effectiveness = {
    ('Fire', 'Grass'): 2,
    ('Fire', 'Water'): 0.5,  
    ('Water', 'Fire'): 2, 
    ('Water', 'Electric'): 0.5,  
    ('Electric', 'Water'): 2,  
}


screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Battle")

Flamion_img = pygame.image.load('assets/Flamion.webp')
Aquarion_img = pygame.image.load('assets/Aquarion.webp')

Flamion = Creature("Flamion", "Fire", 100, [
    {"name": "Flame Spiral", "damage": 19.8, "type": "Fire"},
    {"name": "Meteor Hit", "damage": 24.9, "type": "Dragon"},
    {"name": "Ferocious Lash", "damage": 5.2, "type": "Normal"}
], "assets/Flamion.webp")

Aquarion = Creature("Aquarion", "Water", 100, [
    {"name": "Water Spray", "damage": 26, "type": "Water"},
    {"name": "Glacial Pump", "damage": 24.9, "type": "Ice"},
    {"name": "Sting", "damage": 4.7, "type": "Dark"}
], "assets/Aquarion.webp")


Flamion_position = (100, 150)
Aquarion_position = (500, 150)


font = pygame.font.SysFont('Arial', 24)
small_font = pygame.font.SysFont('Arial', 18)


class Button:
    def __init__(self, text, x, y, width, height, action, color):
        self.text = text
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.action = action
        self.rect = pygame.Rect(x, y, width, height)
        self.color = color

    def draw(self, screen):
        pygame.draw.rect(screen, self.color, self.rect) 
        pygame.draw.rect(screen, BLACK, self.rect, 2)  
        text_surf = font.render(self.text, True, WHITE)
        screen.blit(text_surf, (self.x + (self.width - text_surf.get_width()) // 2,
                               self.y + (self.height - text_surf.get_height()) // 2))

    def is_clicked(self, mouse_pos):
        return self.rect.collidepoint(mouse_pos)

buttons = [
    Button("Flame Spiral", 50, 500, 200, 50, "Flame Spiral", ORANGE),
    Button("Meteor Hit", 250, 500, 200, 50, "Meteor Hit", PURPLE),
    Button("Ferocious Lash", 450, 500, 200, 50, "Ferocious Lash", GRAY)
]


def battle(creature1, creature2):
    game_running = True
    while game_running:
        screen.fill(WHITE)

        creature1.draw(screen, *Flamion_position)
        creature2.draw(screen, *Aquarion_position)

        creature1.hp = math.ceil(creature1.hp)
        creature2.hp = math.ceil(creature2.hp)

        player_hp_text = small_font.render(f"{creature1.name} HP: {creature1.hp}/{creature1.max_hp}", True, BLACK)
        enemy_hp_text = small_font.render(f"{creature2.name} HP: {creature2.hp}/{creature2.max_hp}", True, BLACK)
        screen.blit(player_hp_text, (Flamion_position[0], Flamion_position[1] - 30))
        screen.blit(enemy_hp_text, (Aquarion_position[0], Aquarion_position[1] - 30))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_running = False

            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:  
                    for button in buttons:
                        if button.is_clicked(event.pos):
                            move_name = button.text
                            print(f"Player used {move_name}!")

                            move = next(move for move in creature1.moves if move['name'] == move_name)
                            creature2.take_damage(move['damage'])

                            screen.fill(WHITE)
                           
                            creature1.draw(screen, *Flamion_position)
                            creature2.draw(screen, *Aquarion_position)
                            screen.blit(player_hp_text, (Flamion_position[0], Flamion_position[1] - 30))
                            enemy_hp_text = small_font.render(f"{creature2.name} HP: {creature2.hp}/{creature2.max_hp}", True, BLACK)
                            screen.blit(enemy_hp_text, (Aquarion_position[0], Aquarion_position[1] - 30))
                            for button in buttons:
                                button.draw(screen)
                            pygame.display.flip()
                            creature2.hp = math.ceil(creature2.hp)

                            if not creature2.is_alive():
                                print(f"{creature2.name} fainted!")
                                game_running = False
                                break
                            creature2.hp = math.ceil(creature2.hp)

                            pygame.time.wait(1000) 
                            creature2.hp = math.ceil(creature2.hp)


                            enemy_move = creature2.choose_move()
                            print(f"Enemy used {enemy_move['name']}!")
                            creature1.take_damage(enemy_move['damage'])
                            creature2.hp = math.ceil(creature2.hp)

                            screen.fill(WHITE)
                           
                            creature1.draw(screen, *Flamion_position)
                            creature2.draw(screen, *Aquarion_position)
                            screen.blit(player_hp_text, (Flamion_position[0], Flamion_position[1] - 30))
                            enemy_hp_text = small_font.render(f"{creature2.name} HP: {creature2.hp}/{creature2.max_hp}", True, BLACK)
                            screen.blit(enemy_hp_text, (Aquarion_position[0], Aquarion_position[1] - 30))
                            creature2.hp = math.ceil(creature2.hp)
                            for button in buttons:
                                button.draw(screen)
                            pygame.display.flip()
                            creature2.hp = math.ceil(creature2.hp)

                            if not creature1.is_alive():
                                print(f"{creature1.name} fainted!")
                                game_running = False
                                break
                            creature2.hp = math.ceil(creature2.hp)


        for button in buttons:
            button.draw(screen)

   
        pygame.display.flip() # Just spam this after anything happens, it seems to help.

    
        pygame.time.Clock().tick(FPS)

    pygame.quit()
    sys.exit()


battle(Flamion, Aquarion)
