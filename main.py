import pygame
import random
import json

pygame.init()

pygame.font.init()

from pygame.locals import *

window = pygame.display.set_mode((800, 600))

pygame.display.set_caption("Peanut Jam")

clock = pygame.time.Clock()
frame = 0

white = (255, 255, 255)
black = (0, 0, 0)
green = (0, 255, 0)
red = (255, 0, 0)
light_blue = (102, 214, 255)
gray = (150, 150, 150)

playing = True
score = 0
dash_cooldown = 0
dash_frame = 0
dash = False
speed = 100

scorefont = pygame.font.SysFont("Arial", 24)
crashfont = pygame.font.SysFont("Arial", 72)
finalfont = pygame.font.SysFont("Arial", 32)

with open('highscore.json') as file:
	jsondata = json.load(file)

class Ground:
	def __init__(self):
		self.x = 0
		self.y = 500
		self.scroll = 0
		self.rect = Rect(self.x, self.y, 800, 100)
		self.img = pygame.image.load("assets/grass.png")
	def render(self):
		if playing:
			if dash and dash_frame < 4:
				self.scroll -= 50
			else:
				self.scroll -= 10

			if self.scroll == -800:
				self.scroll = 0
			elif self.scroll < -800:
				self.scroll += 800
		window.blit(self.img, (self.x + self.scroll, self.y))
		window.blit(self.img, (self.x + self.scroll + 800, self.y))
		#pygame.draw.rect(window, green, self.rect)

class Clouds:
	def __init__(self):
		self.x = 0
		self.y = 0
		self.scroll = 0
		self.img = pygame.image.load("assets/clouds.png")
	def render(self):
		if playing:
			if dash and dash_frame < 4:
				self.scroll -= 5
			else:
				self.scroll -= 1

			if self.scroll == -800:
				self.scroll = 0
			elif self.scroll < -800:
				self.scroll += 800
		window.blit(self.img, (self.x + self.scroll, self.y))
		window.blit(self.img, (self.x + self.scroll + 800, self.y)) 

def collide_list(rect, itemlist):
	collision = False
	for item in itemlist:
		try:
			for itemrect in item.rects:
				if itemrect.colliderect(rect):
					collision = True
		except:
			if item.rect.colliderect(rect):
				collision = True
	return collision

class Player:
	def __init__(self, x, y):
		self.x = x
		self.y = y
		self.yvel = 0
		self.onGround = False
		self.rect = Rect(self.x, self.y, 60, 60)
		self.img_drive1 = pygame.image.load("assets/player1.png")
		self.img_drive2 = pygame.image.load("assets/player2.png")
		self.img_duck1 = pygame.image.load("assets/player1duck.png")
		self.img_duck2 = pygame.image.load("assets/player2duck.png")
		self.img_death = pygame.image.load("assets/explosion.png")
		self.img = self.img_drive1
		self.duckimg = self.img_duck1
		self.duck = False
	def rect_update(self):
		if self.duck:
			self.rect = Rect(self.x, self.y + 12, 60, 48)
			self.bottomrect = Rect(self.x, self.y + 60, 60, 1)
		else:
			self.rect = Rect(self.x, self.y, 60, 60)
			self.bottomrect = Rect(self.x, self.y + 60, 60, 1)
	def update(self):
		global playing
		if playing:
			self.rect_update()
			if collide_list(self.rect, obstaclelist):
				playing = False
				with open('highscore.json', 'w') as file:
					json.dump(jsondata, file, indent=4)
			if collide_list(self.bottomrect, groundlist) and not collide_list(self.rect, groundlist):
				self.onGround = True
			elif collide_list(self.bottomrect, groundlist) and collide_list(self.rect, groundlist):
				self.yvel = 0
				while collide_list(self.rect, groundlist):
					self.y -= 1
					self.rect_update()
			else:
				self.onGround = False
			self.y += self.yvel
			if not self.onGround:
				self.yvel += 1
			else:
				self.yvel = 0
	def render(self):
		if self.duck:
			window.blit(self.duckimg, (self.x, self.y + 12))
		else:
			window.blit(self.img, (self.x, self.y))
		#pygame.draw.rect(window, red, self.rect)

class Obstacle():
	def __init__(self, obstacletype):
		self.x = 800
		self.type = obstacletype
		if obstacletype == 1:
			self.w = 60
			self.h = 60
			self.y = 440
			self.img = pygame.image.load("assets/spike1.png")
		elif obstacletype == 2:
			self.w = 60
			self.h = 100
			self.y = 400
			self.img = pygame.image.load("assets/spike2.png")
		elif obstacletype == 3:
			self.w = 60
			self.h = 150
			self.y = 350
			self.img = pygame.image.load("assets/spike3.png")
		elif obstacletype == 4:
			self.w = 60
			self.h = 60
			self.y = 440
			self.img = pygame.image.load("assets/spike4-3.png")
			self.h2 = 270
			self.y2 = 0
			self.img2 = pygame.image.load("assets/spike4-4.png")
		elif obstacletype == 5:
			self.w = 60
			self.h = 100
			self.y = random.randint(260, 400)
			self.speed = 1
			self.direction = random.choice(["up", "down"])
			self.img = pygame.image.load("assets/spike5-1.png")
			self.img2 = pygame.image.load("assets/spike5-2.png")
		elif obstacletype == 6:
			self.w = 60
			self.h = 100
			num = random.randint(260, 400)
			self.y = num - (num % 4)
			self.speed = 4
			self.direction = random.choice(["up", "down"])
			self.img = pygame.image.load("assets/spike5-1.png")
			self.img2 = pygame.image.load("assets/spike5-2.png")
		elif obstacletype == 7:
			self.w = 220
			self.h = 60
			self.y = 440
			self.img = pygame.image.load("assets/spike7.png")

		self.rects = []
		self.rect = Rect(self.x, self.y, self.w, self.h)
		self.rects.append(self.rect)
		if obstacletype == 4:
			self.rect2 = Rect(self.x, self.y2, self.w, self.h2)
			self.rects.append(self.rect2)

	def rect_update(self):
		self.rects = []
		self.rect = Rect(self.x, self.y, self.w, self.h)
		self.rects.append(self.rect)
		if self.type == 4:
			self.rect2 = Rect(self.x, self.y2, self.w, self.h2)
			self.rects.append(self.rect2)

	def update(self):
		global dash
		global dash_frame
		if dash and dash_frame < 4:
			self.x -= 50
		else:
			self.x -= 10
		if self.type == 5 or self.type == 6:
			if self.direction == "down":
				if self.y >= 400:
					self.direction = "up"
				else:
					self.y += self.speed
			else:
				if self.y <= 260:
					self.direction = "down"
				else:
					self.y -= self.speed
		self.rect_update()

	def render(self):
		if self.type == 4:
			window.blit(self.img, (self.x, self.y))
			window.blit(self.img2, (self.x, self.y2))
		elif self.type == 5 or self.type == 6:
			if self.direction == "up":
				window.blit(self.img, (self.x, self.y))
			else:
				window.blit(self.img2, (self.x, self.y))
		else:
			window.blit(self.img, (self.x, self.y))

player = Player(100, 440)
groundlist = []
groundlist.append(Ground())
obstaclelist = []

clouds = Clouds()

aim_image = pygame.image.load("assets/trajectory.png")
type4_dash = False
death_background = pygame.image.load("assets/deathdrop.png")
dbgy = -600
newrecord = False


gameLoop = True
while gameLoop:
	window.fill(light_blue)
	clouds.render()

	keys = pygame.key.get_pressed()
	if (keys[pygame.K_UP] or keys[pygame.K_w]) and player.onGround and playing:
		player.yvel = -18
	if (keys[pygame.K_DOWN] or keys[pygame.K_s]) and player.onGround and playing:
		player.duck = True
	else:
		player.duck = False
	if (keys[pygame.K_RIGHT] or keys[pygame.K_d]) and dash_cooldown == 0 and playing:
		dash = True
		dash_frame = 0
		dash_cooldown = 240
		closest = 1000
		for obs in obstaclelist:
			if closest > abs(player.x - obs.x):
				closest = abs(player.x - obs.x)
		for obs in obstaclelist:
			if abs(player.x - obs.x) == closest:
				if obs.type == 4:
					type4_dash = True

	if keys[pygame.K_SPACE] and not playing and dbgy == 0:
		obstaclelist = []
		player.y = 440
		score = 0
		newrecord = False
		playing = True
		for ground in groundlist:
			ground.x = 0
		clouds.x = 0
		dbgy = -800
		player.img = player.img_drive1


	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			gameLoop = False

	for ground in groundlist:
		ground.render()
	for obs in obstaclelist:
		if playing:
			obs.update()
		obs.render()
	player.update()
	player.render()

	if score > 500:
		speed = 50
	elif score > 400:
		speed = 60
	elif score > 300:
		speed = 70
	elif score > 200:
		speed = 80
	elif score > 100:
		speed = 90
	else:
		speed = 100

	if dash_cooldown > 0 and playing:
		dash_cooldown -= 1
		dashtext = scorefont.render(f'Dash Cooldown: {dash_cooldown // 60 + 1}s', False, black)
		window.blit(dashtext, (585, 10))

	if dash_cooldown == 0:
		type4_dash = False

	if frame % speed == 0 and playing:
		num = random.randint(1, 7)
		if num == 4 and dash_cooldown != 0 and type4_dash:
			while num == 4:
				num = random.randint(1, 7)
		obstaclelist.append(Obstacle(num))

	if len(obstaclelist) > 5:
		obstaclelist.pop(0)

	if frame % 4 == 0 and playing:
		if player.img == player.img_drive1:
			player.img = player.img_drive2
			player.duckimg = player.img_duck2
		else:
			player.img = player.img_drive1
			player.duckimg = player.img_duck1
	elif not playing:
		player.img = player.img_death

	if playing and frame % 10 == 0:
		score += 1

	if score > jsondata["highscore"]:
		jsondata["highscore"] = score
		newrecord = True

	scoretext = scorefont.render(f'Score: {score}', False, black)
	highscoretext = scorefont.render(f'High Score: {jsondata["highscore"]}', False, black)
	window.blit(scoretext, (10, 10))
	window.blit(highscoretext, (10, 44))

	if not playing:
		window.blit(death_background, (0, dbgy))
		if dbgy != 0:
			dbgy += 10
		crashtext = crashfont.render("You crashed!", False, black)
		finalscoretext = finalfont.render(f'Your final score was {score}', False, black)
		restarttext = finalfont.render('Press SPACE to restart', False, black)
		if newrecord:
			recordtext = finalfont.render("NEW RECORD!", False, black)
			window.blit(recordtext, (275, 350 + dbgy))
		window.blit(crashtext, (175, 200 + dbgy))
		window.blit(finalscoretext, (225, 300 + dbgy))
		window.blit(restarttext, (215, 500 + dbgy))

	pygame.display.flip()

	clock.tick(60)
	frame += 1
	dash_frame += 1

pygame.quit()