from pygame import *
from random import randint
 
#фоновая музыка
#mixer.init()
#mixer.music.load('space.ogg')
#mixer.music.play()
#fire_sound = mixer.Sound('fire.ogg')
 
#шрифты и надписи
font.init()
font1 = font.Font(None, 80)
win = font1.render('YOU WIN!', True, (255, 255, 255))
lose = font1.render('YOU LOSE!', True, (180, 0, 0))
font2 = font.Font(None, 36)
 

img_back = "background1.jpg"
img_hero = "weapon.png"
img_bullet = "bullet.png" 
img_enemy = "enemy.png"
#img.speed =  
 
score = 0
lost = 0 
max_lost = 3
goal = 5
 
#класс-родитель для других спрайтов
class GameSprite(sprite.Sprite):
 #конструктор класса
   def __init__(self, player_image, player_x, player_y, size_x, size_y, player_speed):

       sprite.Sprite.__init__(self)
 
     
       self.image = transform.scale(image.load(player_image), (size_x, size_y))
       self.speed = player_speed
 
      
       self.rect = self.image.get_rect()
       self.rect.x = player_x
       self.rect.y = player_y

   def reset(self):
       window.blit(self.image, (self.rect.x, self.rect.y))
 
#класс главного игрока
class Player(GameSprite):

   def update(self):
       keys = key.get_pressed()
       if keys[K_LEFT] and self.rect.x > 5:
           self.rect.x -= self.speed
       if keys[K_RIGHT] and self.rect.x < win_width - 80:
           self.rect.x += self.speed

   def fire(self):
       bullet = Bullet(img_bullet, self.rect.centerx, self.rect.top, 15, 20, -15)
       bullets.add(bullet)
 
#класс спрайта-врага  
class Enemy(GameSprite):
   def update(self):
       self.rect.y += self.speed
       global lost

       if self.rect.y > win_height:
           self.rect.x = randint(80, win_width - 80)
           self.rect.y = 0
           lost = lost + 1
 
 
#класс спрайта-пули  
class Bullet(GameSprite):

   def update(self):
       self.rect.y += self.speed
       if self.rect.y < 0:
           self.kill()
 
#создаем окошко
win_width = 700
win_height = 500
display.set_caption("Shooter")
window = display.set_mode((win_width, win_height))
background = transform.scale(image.load(img_back), (win_width, win_height))
 
#создаем спрайты
ship = Player(img_hero, 5, win_height - 100, 80, 100, 10)
 
monsters = sprite.Group()
for i in range(1, 6):
   monster = Enemy(img_enemy, randint(80, win_width - 80), -40, 50, 80, randint(1, 5))
   monsters.add(monster)
 
bullets = sprite.Group()



finish = False
#основной цикл игры:
run = True
while run:
   #событие нажатия на кнопку Закрыть
   for e in event.get():
       if e.type == QUIT:
           run = False
       #событие нажатия на пробел - спрайт стреляет
       elif e.type == KEYDOWN:
           if e.key == K_SPACE:
               #fire_sound.play()
               ship.fire()
 
   if not finish:
        #обновляем фон
        window.blit(background,(0,0))
  
        #пишем текст на экране
        text = font2.render("Счет: " + str(score), 1, (255, 255, 255))
        window.blit(text, (10, 20))
  
        text_lose = font2.render("Пропущено: " + str(lost), 1, (255, 255, 255))
        window.blit(text_lose, (10, 50))
  
        #производим движения спрайтов
        ship.update()
        monsters.update()
        bullets.update()
  
        #обновляем их в новом местоположении при каждой итерации цикла
        ship.reset()
        monsters.draw(window)
        bullets.draw(window)
 
        collides = sprite.groupcollide(monsters,bullets, True, True)
        for c in collides:
            score += 1
            monster = Enemy(img_enemy, randint(80, win_width - 80), -40, 50, 80, randint(1, 5))
            monsters.add(monster)

        if sprite.spritecollide(ship, monsters, False) or lost >= max_lost:
            finish = True
            window.blit(lose,(200,200))

        if score>=goal:
            finish = True
            window.blit(win,(200,200))            
        display.update()
   #цикл срабатывает каждую 0.05 секунд
   time.delay(50)

