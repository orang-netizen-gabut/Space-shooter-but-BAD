#Create your own shooter

from pygame import *
from random import randint
from time import time as timer

win_width=700
win_height=500

window=display.set_mode((win_width,win_height))
display.set_caption('Space shooter')
bg= transform.scale(image.load('galaxy.jpg'),(win_width,win_height))
wbg=transform.scale(image.load('background.jpg'),(win_width,win_height))
lbg=transform.scale(image.load('bruh.jpg'),(win_width,win_height))
clock=time.Clock()
fps=60

mixer.init()
mixer.music.load('space.ogg')
mixer.music.play()

class GamesSprite(sprite.Sprite):
    def __init__(self,player_image,player_x,player_y,player_speed,player_width,player_height):
        super().__init__()
        self.image=transform.scale(image.load(player_image),(player_width,player_height))
        self.speed=player_speed
        self.rect=self.image.get_rect()
        self.rect.x=player_x
        self.rect.y=player_y

    def reset(self):
        window.blit(self.image,(self.rect.x,self.rect.y))

class Player(GamesSprite):
    def update(self):
        keys=key.get_pressed()
        if keys[K_LEFT] and self.rect.x > 5:
            self.rect.x-=self.speed
        if keys[K_RIGHT] and self.rect.x < win_width-80:
            self.rect.x += self.speed
    def fire(self):
        miya=Bullet('bullet.png',self.rect.centerx,self.rect.top,12,12,12 )
        peluru.add(miya)
        tembak.play()

class Enemy(GamesSprite):
    def update(self):
        self.rect.y += self.speed
        global miss
        if self.rect.y > win_height :
            self.rect.y= 0
            self.rect.x= randint(0,win_width-50)
            miss += 1

class Bullet(GamesSprite):
    def update(self):
        self.rect.y -= self.speed
        if self.rect.y <= 0 :
            self.kill()

udin=Player('rocket.png',280,430,10,90,65)

wsto=sprite.Group()
for i in range(3):
    satria=Enemy('asteroid.png',randint(0,win_height-50),0,randint(1,7),randint(30,65),randint(30,52))
    wsto.add(satria)

oos=sprite.Group()
for i in range(5):
    ujang=Enemy('ufo.png',randint(0,win_width-50),0,randint(1,4),90,65)
    oos.add(ujang)

peluru=sprite.Group()

font.init()
style=font.Font(None,36)
style2=font.Font(None,40)
mixer.init()
tembak=mixer.Sound('fire.ogg')
bruh=mixer.Sound('mixkit-player-losing-or-failing-2042.wav')
bara=mixer.Sound('bara bara bere bere.ogg')

win=style.render('Menang :v,',1,(255,255,255))
lose=style.render('kok kalah (っ °Д °;)っ,',1,(255,255,255))

point=0
miss=0

fire=0
reload=False

game=True
finish=False
while game :

    for e in event.get():
        if e.type==QUIT:
            game=False

        elif e.type==KEYDOWN:
            if e.key==K_SPACE :
                if fire < 5 and reload==False:
                    fire=fire + 1
                    udin.fire()
                
                if fire >= 5 and reload==False:
                    last=timer()
                    reload=True

    if not finish :
        window.blit(bg,(0,0))

        udin.reset()
        udin.update()
        oos.update()
        oos.draw(window)
        wsto.update()
        wsto.draw(window)
        peluru.update()
        peluru.draw(window)
        
        if reload==True:
            now=timer()
            if now - last < 2 :
                reloadC=style2.render('Reloading...',1,(150,0,0))
                window.blit(reloadC,(250,300))

            else :
                fire=0
                reload=False

        collides=sprite.groupcollide(oos ,peluru,True,True)
        for c in collides:
            point= point + 1
            ujang=Enemy('ufo.png',randint(0,win_width-50),0,randint(2,5),90,65)
            oos.add(ujang)

        score=style.render('Score:' + str(point),1,(255,255,255))
        window.blit(score,(10,20))
        missed=style.render('missed:' + str(miss),1,(255,255,255))
        window.blit(missed,(10,50))

        if point >= 20 :
            finish=True
            mixer.music.stop()
            bara.play()
            window.blit(wbg,(0,0))
            window.blit(win,(300,250))
            window.blit(score,(300,300))
            window.blit(missed,(300,330))
        if miss >= 15 or sprite.spritecollide(udin,wsto,True) :
            finish=True
            mixer.music.stop()
            bruh.play()
            window.blit(lbg,(0,0))
            window.blit(lose,(250,250))
            window.blit(score,(300,300))
            window.blit(missed,(300,330))

    clock.tick(fps)
    display.update()
