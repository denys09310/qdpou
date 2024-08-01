from random import choice
from pygame import *
import pygame_menu

init()
font.init()
font2 = font.SysFont('Impact', 30)
font1 = font.SysFont('Impact', 100)
timer_text = font2.render('time:',True,(255,255,255) )
game_over_text = font1.render('GAME_OVER', True, (255, 0, 0))
win_text = font1.render('YOU WIN', True, (255, 0, 0))
mixer.init()
mixer.music.load('jungles.ogg')
mixer.music.play()
mixer.music.set_volume(0.2)

TILESIZE = 30


infoObject = display.Info()
WIDTH, HEIGHT = TILESIZE*50,TILESIZE*27

window = display.set_mode((WIDTH, HEIGHT), )
FPS = 60
clock = time.Clock()

bg = image.load('background.jpg')
bg = transform.scale(bg, (WIDTH, HEIGHT))
player2_img = image.load('Lomka 2.png')
player_img = image.load("Lomka.png")
cyborg_img = image.load("cyborg.png")
wall_img = image.load("DesolatedHut.png")
gold_img = image.load("treasure.png")
green_lake_img = image.load("green.png")
blue_lake_img = image.load("blue.png")
red_lake_img = image.load("red.png")
all_sprites = sprite.Group()

class Sprite(sprite.Sprite):
    def __init__(self, sprite_img, width, height, x, y):
        super().__init__()
        self.image = transform.scale(sprite_img, (width, height))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.mask = mask.from_surface(self.image)
        all_sprites.add(self)

class Player(Sprite):
    def __init__(self, sprite_img, width, height, x, y, controls):
        super().__init__(sprite_img, width, height, x, y)
        self.hp = 100
        self.speed = 7
        self.controls = controls
        self.is_jumping = False
        self.jump_speed = 10
        self.gravity = 1
        self.velocity_y = 0

    def update(self):
        key_pressed = key.get_pressed()
        old_pos = self.rect.x, self.rect.y
        

        if key_pressed[self.controls['left']] and self.rect.x > 0:
            self.rect.x -= self.speed
        if key_pressed[self.controls['right']] and self.rect.right < WIDTH:
            self.rect.x += self.speed
        

        if key_pressed[self.controls['up']] and not self.is_jumping:
            self.is_jumping = True
            self.velocity_y = -self.jump_speed


        self.rect.y += self.velocity_y
        self.velocity_y += self.gravity
        

        if self.rect.bottom >= HEIGHT:
            self.rect.bottom = HEIGHT
            self.is_jumping = False
            self.velocity_y = 0
        
       
        collide_list = sprite.spritecollide(self, walls, False, sprite.collide_mask)
        if len(collide_list) > 0:
            self.rect.x, self.rect.y = old_pos
            if self.velocity_y > 0:
                self.is_jumping = False
                self.velocity_y = 0
        

        enemy_collide = sprite.spritecollide(self, enemys, False, sprite.collide_mask)
        if len(enemy_collide) > 0:
            self.hp -= 100
        
        lake_collide = sprite.spritecollide(self, lakes, False, sprite.collide_mask)
        for lake in lake_collide:
            if isinstance(lake, GreenLake):
                self.hp = 0
            elif isinstance(lake, BlueLake) and self == player2:
                self.hp = 0
            elif isinstance(lake, RedLake) and self == player1:
                self.hp = 0

class Enemy(Sprite):
    def __init__(self, sprite_img, width, height, x, y):
        super().__init__(sprite_img, width, height, x, y)
        self.damage = 100
        self.speed = 2
        self.dir_list = ['right', 'left', "up", "down"]
        self.dir = choice(self.dir_list)

    def update(self):
        old_pos = self.rect.x, self.rect.y
        if self.dir == "right":
            self.rect.x += self.speed
        elif self.dir == "left":
            self.rect.x -= self.speed
        elif self.dir == "up":
            self.rect.y -= self.speed
        elif self.dir == "down":
            self.rect.y += self.speed
        collide_list = sprite.spritecollide(self, walls, False, sprite.collide_mask)
        if len(collide_list) > 0:
            self.rect.x, self.rect.y = old_pos
            self.dir = choice(self.dir_list)

class Lake(Sprite):
    def __init__(self, sprite_img, width, height, x, y):
        super().__init__(sprite_img, width, height, x, y)

class GreenLake(Lake):
    pass

class BlueLake(Lake):
    pass

class RedLake(Lake):
    pass

walls = sprite.Group()
enemys = sprite.Group()
lakes = sprite.Group()

controls1 = {'up': K_w, 'down': K_s, 'left': K_a, 'right': K_d}
controls2 = {'up': K_UP, 'down': K_DOWN, 'left': K_LEFT, 'right': K_RIGHT}

player1 = Player(player_img, TILESIZE - 5, TILESIZE - 5, 300, 300, controls1)
player2 = Player(player2_img, TILESIZE - 5, TILESIZE - 5, 300, 300, controls2)

with open("map.txt", "r") as f:
    map = f.readlines()
    x = 0
    y = 0
    for line in map:
        for symbol in line:
            if symbol == "w":  
                walls.add(Sprite(wall_img, TILESIZE, TILESIZE, x, y))
            if symbol == "p":  
                player1.rect.x = x
                player1.rect.y = y
            if symbol == "o":  
                player2.rect.x = x
                player2.rect.y = y
            if symbol == "g":  
                gold = Sprite(gold_img, 70, 70, x, y)
            if symbol == "e":
                enemys.add(Enemy(cyborg_img, TILESIZE - 5, TILESIZE - 5, x, y))
            if symbol == "i":
                lakes.add(GreenLake(green_lake_img, TILESIZE, TILESIZE, x, y))
            if symbol == "b":
                lakes.add(BlueLake(blue_lake_img, TILESIZE, TILESIZE, x, y))
            if symbol == "r":
                lakes.add(RedLake(red_lake_img, TILESIZE, TILESIZE, x, y))
            x += TILESIZE
        y += TILESIZE
        x = 0
total_time= 100

def set_difficulty(selected, value):
    """
    Set the difficulty of the game.
    """
    global total_time
    total_time=value

def start_the_game():
    # Do the job here !
    global run
    run = True
    menu.disable()

#завантажуємо картинку
myimage = pygame_menu.baseimage.BaseImage(
    image_path='background.jpg',
    drawing_mode=pygame_menu.baseimage.IMAGE_MODE_REPEAT_XY,
)
#створюємо власну тему - копію стандартної
mytheme = pygame_menu.themes.THEME_DARK.copy()
# колір верхньої панелі (останній параметр - 0 робить її прозорою)
mytheme.title_background_color=(255, 255, 255, 0) 
#задаємо картинку для фону
mytheme.background_color = myimage
menu = pygame_menu.Menu('Lomka', WIDTH, HEIGHT,
                       theme=mytheme)   

user_name = menu.add.text_input("name :", default='Анонім')
menu.add.selector('difficulty :', [('Hard', 50), ('Easy', 100)], onchange=set_difficulty)
menu.add.button('Play', start_the_game)
menu.add.button('Quit', pygame_menu.events.EXIT)
menu.mainloop(window)

run = True
finish = False
game_win = False
start_time=time.get_ticks()


while run:
    for e in event.get():
        if e.type == QUIT:
            run = False
    
    window.blit(bg, (0, 0))

    if player1.hp <= 0 or player2.hp <= 0:
        finish = True
        game_win = False
    
    if sprite.collide_mask(player1, gold) and sprite.collide_mask(player2, gold):
        finish = True
        game_win = True

    all_sprites.draw(window)
    window.blit(timer_text,(25,20))
    if not finish:
        all_sprites.update()
        now = time.get_ticks()
        carent_time=now - start_time
        time_left=total_time-carent_time/1000
        timer_text = font2.render(f'time:{int(time_left)}',True,(255,255,255) )
        if time_left <=0:
            finish=True            



    else:
        if game_win:
            window.blit(win_text, (WIDTH/2-game_over_text.get_width()/2,HEIGHT/2-game_over_text.get_height()/2))
        else:
            window.blit(game_over_text, (WIDTH/2-game_over_text.get_width()/2,HEIGHT/2-game_over_text.get_height()/2))

    display.update()
    clock.tick(FPS)


