import pygame
from sys import exit
from random import randint ,choice

class Player(pygame.sprite.Sprite):

    def __init__(self):
        super().__init__()
        player_walk_1 = pygame.image.load('graphics/player/player_walk_1.png').convert_alpha()
        player_walk_2 = pygame.image.load('graphics/player/player_walk_2.png').convert_alpha()
        self.player_walk = [player_walk_1, player_walk_2]
        self.player_index = 0
        self.player_jump = pygame.image.load('graphics/player/jump.png').convert_alpha()

        self.image = self.player_walk[self.player_index]
        self.rect = self.image.get_rect(midbottom=(80, 300))
        self.gravity = 0
        self.jump_music = pygame.mixer.Sound('audio/jump.mp3')
        self.jump_music.set_volume(0.05)

    def player_input(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_SPACE] and self.rect.bottom >= 300:
            self.gravity = -20
            self.jump_music.play()

    def apply_jump(self):
        self.gravity += 1
        self.rect.y += self.gravity
        if self.rect.bottom >= 300:
            self.rect.bottom = 300

    def animation_state(self):
        if self.rect.bottom < 300:
            self.image = self.player_jump
        else:
            self.player_index += 0.1
            if self.player_index >= len(self.player_walk): self.player_index = 0
            self.image = self.player_walk[int(self.player_index)]

    def update(self):
        self.player_input()
        self.apply_jump()
        self.animation_state()


class Obstacle(pygame.sprite.Sprite):
    def __init__(self, type):
        super().__init__()

        if type == 'fly':
            fly_1 = pygame.image.load('graphics/fly/fly1.png').convert_alpha()
            fly_2 = pygame.image.load('graphics/fly/fly2.png').convert_alpha()
            self.frames = [fly_1, fly_2]
            position = 210
        else:
            snail_1 = pygame.image.load('graphics/snail/snail1.png').convert_alpha()
            snail_2 = pygame.image.load('graphics/snail/snail2.png').convert_alpha()
            self.frames = [snail_1, snail_2]
            position = 300

        self.animation_index = 0
        self.image = self.frames[self.animation_index]
        self.rect = self.image.get_rect(midbottom=(randint(900, 1100), position))

    def animation_state(self):
        self.animation_index += 0.1
        if self.animation_index >= len(self.frames): self.animation_index = 0
        self.image = self.frames[int(self.animation_index)]

    def update(self):
        self.animation_state()
        self.rect.x -= 6
        self.destroy()

    def destroy(self):
        if self.rect.x <= -100:
            self.kill()

class Coins(pygame.sprite.Sprite):

    def __init__(self,type):
        super().__init__()

        if type == 'bronze':
            bronze = pygame.image.load('graphics/coins/coinBronze.png').convert_alpha()
            self.coins = [bronze]
            self.type = type

        elif type == 'silver':
            silver = pygame.image.load('graphics/coins/coinSilver.png').convert_alpha()
            self.coins = [silver]
            self.type = type

        else:
            gold = pygame.image.load('graphics/coins/coinGold.png').convert_alpha()
            self.coins = [gold]
            self.type = type


        position = choice([210,210,300])

        self.image = self.coins[0]
        self.rect = self.image.get_rect(midbottom=(randint(1200, 1400), position))

    def update(self):

        self.rect.x -= 6
        self.destroy()

    def destroy(self):
        global score
        if self.rect.x <= -100:
            self.kill()
        if pygame.sprite.spritecollide(player.sprite,coins,False):
            if self.type == 'bronze':
                score += 10
            if self.type == 'silver':
                score += 20
            if self.type == 'gold':
                score += 50
            self.kill()


def time_game():
    current_time = int(pygame.time.get_ticks() / 1000) - start_time
    score_surf = test_font.render(f'Time: {current_time}',False,(111,196,169))
    score_rect = score_surf.get_rect(topright = (780,10))
    screen.blit(score_surf,score_rect)
    return current_time


def collisions_sprite():
    if pygame.sprite.spritecollide(player.sprite,obstacles,False):
        obstacles.empty()
        return False
    else:
        return True


pygame.init()
icon = pygame.image.load('graphics/hud_p1.png')
pygame.display.set_icon(icon)

screen  = pygame.display.set_mode((800,400))

pygame.display.set_caption("Pixel Runner")
clock = pygame.time.Clock()

test_font = pygame.font.Font('font/Pixeltype.ttf',50)

game_running = False
start_time = 0
time = 0
score = 0
score_current = 0

sky_surface = pygame.image.load('graphics/Sky.png').convert()
ground_surface = pygame.image.load('graphics/ground.png').convert()

game_name = test_font.render("Pixel Runner", False, (111, 196, 169))
game_name_rect = game_name.get_rect(center = (400, 50))


player_stand = pygame.image.load('graphics/player/player_stand.png').convert_alpha()
player_stand = pygame.transform.rotozoom(player_stand,0,2)
player_stand_rect = player_stand.get_rect(center = (400,200))

game_message = test_font.render("Press space to start", False, (111, 196, 169))
game_message_rect = game_message.get_rect(center = (400, 340))



player = pygame.sprite.GroupSingle()
player.add(Player())

obstacles = pygame.sprite.Group()

coins = pygame.sprite.Group()


background_music = pygame.mixer.Sound('audio/music.wav')
background_music.set_volume(0.05)
background_music.play(loops=-1)


obstacle_timer = pygame.USEREVENT + 1
pygame.time.set_timer(obstacle_timer,1500)

coin_timer = pygame.USEREVENT + 2
pygame.time.set_timer(coin_timer,1500)


while True:

    if game_running:
        screen.blit(sky_surface, (0, 0))
        screen.blit(ground_surface, (0, 300))

        time = time_game()

        score_surf = test_font.render(f'Score:{score}', False, (64, 64, 64))
        score_rect = score_surf.get_rect(center=(400, 50))
        screen.blit(score_surf, score_rect)

        #player
        player.draw(screen)
        player.update()
        #obstacles
        obstacles.draw(screen)
        obstacles.update()
        #coins
        coins.draw(screen)
        coins.update()

        #collisions
        game_running = collisions_sprite()

    else:
        screen.fill((94,129,162))
        screen.blit(player_stand,player_stand_rect)

        screen.blit(game_name, game_name_rect)

        if time == 0:

            screen.blit(game_message, game_message_rect)
        else:
            game_score = test_font.render(f"Your score: {score}", False, (111, 196, 169))
            game_score_rect = game_score.get_rect(center=(400, 330))
            screen.blit(game_score,game_score_rect)


    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()

        if game_running:
            if event.type == obstacle_timer:
                obstacles.add(Obstacle(choice(['fly', 'snail', 'snail', 'snail'])))
            if event.type == coin_timer:
                coins.add(Coins(choice(['bronze', 'bronze', 'bronze', 'bronze', 'silver', 'silver', 'gold'])))

        else:
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                game_running = True
                score = 0
                start_time = int(pygame.time.get_ticks() / 1000)


    pygame.display.update()
    clock.tick(60)