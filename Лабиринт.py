from pygame import *
 
#класс-родитель для спрайтов
class GameSprite(sprite.Sprite):
   #конструктор класса
   def __init__(self, player_image, player_x, player_y, player_speed):
       super().__init__()
       # каждый спрайт должен хранить свойство image - изображение
       self.image = transform.scale(image.load(player_image), (65, 65))
       self.speed = player_speed
       # каждый спрайт должен хранить свойство rect - прямоугольник, в который он вписан
       self.rect = self.image.get_rect()
       self.rect.x = player_x
       self.rect.y = player_y
 
   def reset(self):
       window.blit(self.image, (self.rect.x, self.rect.y))
 
class Player(GameSprite):
    def update(self):
        keys_pressed = key.get_pressed()
        if keys_pressed[K_a] and self.rect.x > 0:
            self.rect.x -= self.speed
        if keys_pressed[K_d] and self.rect.x < 640:
            self.rect.x += self.speed
        if keys_pressed[K_w] and self.rect.y > 0:
            self.rect.y -= self.speed
        if keys_pressed[K_s] and self.rect.y < 445:
            self.rect.y += self.speed

class Enemy(GameSprite):
    direction = 'left'
    def update(self):
        if self.rect.x <=500:
            self.direction = 'right' 
        if self.rect.x >= 600:
            self.direction = 'left'
        
        if self.direction == 'left':
            self.rect.x -= self.speed
        else:
            self.rect.x += self.speed

class Wall(sprite.Sprite):
    def __init__(self, color_1, color_2, color_3, wall_x, wall_y, wall_width, wall_height):
        super().__init__()
        self.color_1 = color_1
        self.color_2 = color_2
        self.color_3 = color_3
        self.width = wall_width
        self.height = wall_height
        self.image = Surface((self.width, self.height))
        self.image.fill((color_1, color_2, color_3))
        self.rect = self.image.get_rect()
        self.rect.x = wall_x
        self.rect.y = wall_y
    
    def draw_wall(self):
       window.blit(self.image, (self.rect.x, self.rect.y))

#Игровая сцена:
win_width = 700
win_height = 500
window = display.set_mode((win_width, win_height))
display.set_caption("Лабиринт")
background = transform.scale(image.load("background.jpg"), (win_width, win_height))
 
#Персонажи игры:
player = Player('hero.png', 5, win_height - 80, 3)
monster = Enemy('cyborg.png', win_width - 80, 280, 2)
final = GameSprite('treasure.png', win_width - 120, win_height - 80, 0)

w1 = Wall(153, 134, 253, 10, 10, 480, 10)
w2 = Wall(153, 134, 253, 90, 110, 10, 380)
w3 = Wall(153, 134, 253, 190, 20, 10, 380)
w4 = Wall(153, 134, 253, 100, 480, 380, 10)
w5 = Wall(153, 134, 253, 480, 100, 10, 390)
w6 = Wall(153, 134, 253, 200, 390, 190, 10)
w7 = Wall(153, 134, 253, 290, 290, 190, 10)
w8 = Wall(153, 134, 253, 200, 190, 190, 10)
w9 = Wall(153, 134, 253, 290, 100, 190, 10)

finish = False
game = True
clock = time.Clock()
FPS = 60
 
#музыка
mixer.init()
mixer.music.load('jungles.ogg')
mixer.music.play()

font.init()
font = font.SysFont('Arial', 36)
win = font.render('YOU WIN', True, (255,215,0))
lose = font.render('YOU LOSE', True, (255,0,0))

money = mixer.Sound("money.ogg")
kick = mixer.Sound("kick.ogg")
 
while game:
    for e in event.get():
        if e.type == QUIT:
            game = False
    
    if finish != True:
        window.blit(background, (0, 0))
        
        player.update()
        monster.update()

        player.reset()
        monster.reset()
        final.reset()

        w1.draw_wall()
        w2.draw_wall()
        w3.draw_wall()
        w4.draw_wall()
        w5.draw_wall()
        w6.draw_wall()
        w7.draw_wall()
        w8.draw_wall()
        w9.draw_wall()

        #выигрыш
        if sprite.collide_rect(player, final):
            finish = True
            window.blit(win, (200, 200))
            money.play()
        
        #проигрыш
        if sprite.collide_rect(player, monster) or sprite.collide_rect(player, w1) or sprite.collide_rect(player, w2) or sprite.collide_rect(player, w3) or sprite.collide_rect(player, w4) or sprite.collide_rect(player, w5) or sprite.collide_rect(player, w6) or sprite.collide_rect(player, w7) or sprite.collide_rect(player, w8) or sprite.collide_rect(player, w9):
            finish = True
            window.blit(lose, (200, 200))
            kick.play()

    clock.tick(FPS)
    display.update()