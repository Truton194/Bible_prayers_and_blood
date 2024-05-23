from pygame import *
import random
from time import time as timer

WIN_WIDTH = 700
WIN_HEIGHT = 500
FPS = 40

lost = 0
score = 0
max_lost = 3

class GameSprite(sprite.Sprite):
    def __init__(self, player_sprite, player_x, player_y, size_x, size_y, player_speed):
       super().__init__()
       self.image = transform.scale( image.load(player_sprite), (size_x, size_y) )
       self.speed = player_speed
       self.rect = self.image.get_rect()
       self.rect.x = player_x
       self.rect.y = player_y

    def reset(self):
        window.blit(self.image, (self.rect.x, self.rect.y))    

class Player(GameSprite):
    def update(self):
        keys = key.get_pressed()
        if keys[ K_a ] and self.rect.x > 5:
            self.rect.x -= self.speed
        if keys[ K_w ] and self.rect.y > 5:
            self.rect.y -= self.speed
        if keys[ K_d ] and self.rect.x < WIN_WIDTH - 80:
            self.rect.x += self.speed
        if keys[ K_s ] and self.rect.y < WIN_HEIGHT - 80:
            self.rect.y += self.speed

    def fire(self):
        global bullets, shot_player

        bullet = Bullet('light.png', 0, self.rect.top, 10, 10, 15)
        bullet.rect.centerx = self.rect.centerx
        bullets.add(bullet)
        #ashot_player.play()

class Enemy(GameSprite):
    def update(self):
        global lost

        self.rect.x -= self.speed

        if self.rect.x <= 0:
            lost += 1
            self.rect.x = 735
            self.speed = random.randint(1, 5)

class Bullet(GameSprite):
    def update(self):
        self.rect.x += self.speed
        if self.rect.x >= 700:
            self.kill()
window = display.set_mode((WIN_WIDTH, WIN_HEIGHT))

clock = time.Clock()

game = True
finish = False

pers = Player('priest.png', 40, WIN_HEIGHT - 100, 50, 50, 10)

bullets = sprite.Group()
monsters = sprite.Group()

def generate_enemy():
    for i in range(5):
        x = 735
        y = random.randint(20, WIN_HEIGHT-45)
        speed = random.randint(1, 4)
        enemy = Enemy('eye.png', x, y, 20, 20, speed)
        monsters.add(enemy)

    for i in range(2):
        x = 735
        y = random.randint(20, WIN_HEIGHT-45)
        speed = random.randint(1, 4)
        enemy = Enemy('hole.png', x, y, 30, 30, speed)
        monsters.add(enemy)
generate_enemy()
def start_game():
    global lost, score, finish, count_bullet
    pers = Player('priest.png', 5, WIN_HEIGHT - 100, 80, 100, 10)
    for b in bullets:
        b.kill()
    for m in monsters:
        m.kill()
    generate_enemy()
    lost = 0
    score = 0
    count_bullet = 0
    finish = False

font.init()
font1 = font.Font(None, 36)
font2 = font.Font(None, 70)

win = font2.render('Выиграли!', True, (255, 255, 255))
lose = font2.render('Проиграли!', True, (255, 255, 255))

rel_time = False
count_bullet = 0
restart_time = 0
while game:
    for e in event.get():
        if e.type == QUIT:
            game = False
        if e.type == MOUSEBUTTONDOWN:
            if e.button == BUTTON_LEFT:
                if count_bullet < 5:
                    count_bullet += 1
                    pers.fire()
                else:
                    last_time = timer()
                    rel_time = True
                

    
    if not finish:
        window.fill((245, 232, 167))
        if rel_time:
            now_time = timer() 
            if now_time - last_time < 3:
                text_reload = font1.render(
                    'Перезарядка: ' + str(round(3 - int(now_time - last_time))),
                     True, (255, 255, 255)
                     )
                window.blit(text_reload, (200, 400))
            else:
                rel_time = False
                count_bullet = 0

        text_score = font1.render('Счёт: ' + str(score), True, (255, 255, 255))
        window.blit(text_score, (10, 20))

        text_lose = font1.render('Пропущено: ' + str(lost), True, (255, 255, 255))
        window.blit(text_lose, (10, 50))

        monsters.update()
        monsters.draw(window)
        bullets.update()
        bullets.draw(window)
        pers.reset()
        pers.update()


        if sprite.spritecollide(pers, monsters, False) or lost >= max_lost:
            finish = True
            restart_time = timer()
            end_text = lose
        if score >= 10:
            finish = True
            restart_time = timer()
            end_text = win

        collide_bullets_and_monsters = sprite.groupcollide(bullets, monsters, True, True)
        for collide in collide_bullets_and_monsters:
            score += 1
            x = 735
            y = random.randint(20, WIN_HEIGHT-45)
            speed = random.randint(1, 4)
            enemy = Enemy('eye.png', x, y, 80, 50, speed)
            monsters.add(enemy)
    elif finish:
        window.fill((245, 232, 167))
        window.blit(end_text, (200, 200))
        if timer() - restart_time >= 5:
            start_game()
        
    display.update()
    clock.tick(FPS)
