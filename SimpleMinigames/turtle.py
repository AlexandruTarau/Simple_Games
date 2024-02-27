import pygame
import random
import math
from pygame import mixer

pygame.init()

# Create Screen
SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 600
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

pygame.display.set_caption("Turtle Warrior")

# Map
background = pygame.image.load('backgroundalex.png')
background = pygame.transform.scale(background, (1000, 600))
upRoad = (SCREEN_WIDTH / 2, 0)
rightRoad = (SCREEN_WIDTH, SCREEN_HEIGHT / 2)
downRoad = (SCREEN_WIDTH / 2, SCREEN_HEIGHT)
leftRoad = (0, SCREEN_HEIGHT / 2)
spawnPositions = (upRoad, leftRoad, downRoad, rightRoad)

middleX = SCREEN_WIDTH / 2
middleY = SCREEN_HEIGHT / 2

# Background music
mixer.init()
mixer.music.load("Glorious_morning.mp3")
music_volume = 0.15
mixer.music.set_volume(music_volume)
mixer.music.play(-1)

# Sounds
bow_channel = mixer.Channel(0)
enemy_channel = mixer.Channel(1)
sound_volume = 0.5
arrow_shot_sound = mixer.Sound("arrow_shot.mp3")
arrow_shot_sound.set_volume(sound_volume)

bow_reload_sound = mixer.Sound("reload_bow.mp3")
bow_reload_sound.set_volume(sound_volume)

arrow_hit_sound = mixer.Sound("arrow_hit.mp3")
arrow_hit_sound.set_volume(sound_volume)

"""Player"""
playerImg = pygame.image.load('turtle_archer_1.png')
heartImg = pygame.image.load('heart.png')
shieldSkillImg = pygame.image.load('shield_skill.png').convert_alpha()
defence_icon_not_charged = pygame.image.load('defence_skill_not_charged.png')
defence_icon_charged = pygame.image.load('defence_skill_charged.png')
attack_icon_not_charged = pygame.image.load('attack_skill_not_charged.png')
attack_icon_charged = pygame.image.load('attack_skill_charged.png')
heartImg = pygame.transform.scale(heartImg, (heartImg.get_width() * 3, heartImg.get_height() * 3))
attack_skill_CD = 10
defend_skill_CD = 4

"""Score"""
scoreValue = 0

"""UI"""
retry_button = pygame.image.load("retry_button.png")
retry_button_selected = pygame.image.load("retry_button_selected.png")
sound_button = pygame.image.load("sound_button.png")
sound_button_selected = pygame.image.load("sound_button_selected.png")
music_button = pygame.image.load("music_button.png")
music_button_selected = pygame.image.load("music_button_selected.png")
return_button = pygame.image.load("return_button.png")
return_button_selected = pygame.image.load("return_button_selected.png")

"""Projectiles"""

projectiles = []

# Arrow
arrowImg = pygame.image.load('Arrow.png')
skillArrow = pygame.image.load('skill_arrow.png')
poisonImg = pygame.image.load('poison_bullet.png')
arrowCD = 2

"""Enemies"""
spawnTime = 1
enemies = [[], [], [], []]

enemy_types = ["melee", "ranger"]
enemy_shooting_CD = 4
unlocked_enemies = 1

# Spiders
blackSpiderImg = pygame.image.load('spider-black-no-web.png')
whiteSpiderImg = pygame.image.load('spider-white.png')

enemy_images = [blackSpiderImg, whiteSpiderImg]

# Level
aggressionValue = 5

# Pause Menu
paused = False
pauseMenuImg = pygame.image.load('pause_menu_v2.png')
menu_buttons = ["return", "retry", "sound", "music"]
menu_buttons_images = [return_button, retry_button, sound_button, music_button]
menu_buttons_non_selected_images = [return_button, retry_button, sound_button, music_button]
menu_buttons_selected_images = [return_button_selected, retry_button_selected, sound_button_selected,
                                music_button_selected]
menu_button_types = [0, 0, 1, 1]
current_button = 0

# DeltaTime
deltaTime = 0.0

# Others
reload_timer = 0.0
spawn_timer = 0.0
attack_counter = 0
defend_counter = 0
attack_skill_ready = False
defend_skill_ready = False


class Text:

    def __init__(self, text, position, font):
        self.text = text
        self.position = position
        self.font = font

    def render(self):
        text = self.font.render(self.text, True, (255, 255, 255))
        screen.blit(text, self.position)


class Player:

    armed = True
    lives = 3

    def __init__(self, image, facing, position, scale, angle):
        self.image = image
        self.width = image.get_width()
        self.height = image.get_height()
        self.facing = facing
        self.position = (position[0] - self.width / 2 * scale, position[1] - self.height / 2 * scale)
        self.scale = scale
        self.angle = angle

    def render(self):
        image = pygame.transform.rotate(self.image, self.angle)
        image = pygame.transform.scale(image, (self.width * self.scale, self.height * self.scale))
        screen.blit(image, self.position)


class Projectile:

    offset = ((0, 16), (16, 0), (0, -16), (-16, 0))
    dead = False

    def __init__(self, image, facing, position, scale, angle, shooter, penetration):
        self.image = image
        self.width = image.get_width()
        self.height = image.get_height()
        self.facing = facing
        self.position = (position[0] + self.offset[facing][0] * scale, position[1] + self.offset[facing][1] * scale)
        self.scale = scale
        self.angle = angle
        self.shooter = shooter
        self.penetration = penetration
        if shooter == "player":
            self.step = ((0, 300), (300, 0), (0, -300), (-300, 0))
        elif shooter == "enemy":
            self.step = ((0, 100), (100, 0), (0, -100), (-100, 0))

    def render(self):
        image = pygame.transform.rotate(self.image, self.angle)
        image = pygame.transform.scale(image, (self.width * self.scale, self.height * self.scale))
        screen.blit(image, self.position)

    def move(self):
        if self.shooter == "player":
            if (math.pow(self.position[0] + self.width / 2 * self.scale - middleX, 2) +
                    math.pow(self.position[1] + self.height / 2 * self.scale - middleY, 2)
                    > math.pow(max(SCREEN_HEIGHT, SCREEN_WIDTH), 2)):
                return False
        elif self.shooter == "enemy":
            if (math.pow(self.position[0] + self.width / 2 * self.scale - middleX, 2) +
                    math.pow(self.position[1] + self.height / 2 * self.scale - middleY, 2) <= math.pow(16,
                                                                                                       2)):
                return False
        self.position = (self.position[0] + self.step[self.facing][0] * deltaTime,
                         self.position[1] + self.step[self.facing][1] * deltaTime)
        return True


class Enemy:

    step = ((0, 20), (20, 0), (0, -20), (-20, 0))
    dead = False
    reload_timer = 0.0

    def __init__(self, image, enemy_type, facing, position, scale, angle):
        self.image = image
        self.enemyType = enemy_type
        self.width = image.get_width()
        self.height = image.get_height()
        self.facing = facing
        self.position = (position[0] - self.width / 2 * scale, position[1] - self.height / 2 * scale)
        self.scale = scale
        self.angle = angle

    def render(self):
        image = pygame.transform.rotate(self.image, self.angle)
        image = pygame.transform.scale(image, (self.width * self.scale, self.height * self.scale))
        screen.blit(image, self.position)

    def move(self):
        if self.enemyType == "melee":
            if (math.pow(self.position[0] + self.width / 2 * self.scale - middleX, 2) +
                    math.pow(self.position[1] + self.height / 2 * self.scale - middleY, 2) <= math.pow(32,
                                                                                                       2)):
                return False

        elif self.enemyType == "ranger":
            if (math.pow(self.position[0] + self.width / 2 * self.scale - middleX, 2) +
                    math.pow(self.position[1] + self.height / 2 * self.scale - middleY, 2) <= math.pow(250,
                                                                                                       2)):
                return False

        self.position = (self.position[0] + self.step[self.facing][0] * deltaTime,
                         self.position[1] + self.step[self.facing][1] * deltaTime)
        return True


class PauseMenu:
    button_selected = False
    button_local_positions = [(3, 12), (34, 17), (66, 13), (66, 30)]
    button_global_positions = []

    def __init__(self, image, buttons, button_types, button_images, position, scale):
        self.image = image
        self.width = image.get_width()
        self.height = image.get_height()
        self.scale = scale
        self.buttons = buttons
        self.button_images = button_images
        self.button_types = button_types
        self.position = (position[0] - self.width / 2 * scale, position[1] - self.height / 2 * scale)
        for i in range(0, len(self.button_local_positions)):
            pos = (self.button_local_positions[i][0] * scale + self.position[0],
                   self.button_local_positions[i][1] * scale + self.position[1])
            self.button_global_positions.append(pos)

    def render(self):
        image = pygame.transform.scale(self.image, (self.width * self.scale, self.height * self.scale))
        screen.blit(image, self.position)
        for i in range(0, len(self.buttons)):
            img = pygame.transform.scale(menu_buttons_images[i], (menu_buttons_images[i].get_width() * self.scale,
                                                                  menu_buttons_images[i].get_height() * self.scale))
            screen.blit(img, self.button_global_positions[i])
        sound_volume_text.render()
        music_volume_text.render()

    def pressed(self, idx):
        if self.button_types[idx] == 0:
            if self.buttons[idx] == "retry":
                mixer.music.unpause()
                mixer.music.rewind()
                global scoreValue, aggressionValue, enemies, projectiles, reload_timer, spawn_timer, paused,\
                    attack_skill_ready, attack_counter, defend_skill_ready, defend_counter, unlocked_enemies
                scoreValue = 0
                score.text = "Score : 0"
                aggressionValue = 5
                enemies = [[], [], [], []]
                unlocked_enemies = 1
                projectiles = []
                reload_timer = spawn_timer = 0.0
                player.lives = 3
                attack_skill_ready = False
                attack_counter = 0
                defend_skill_ready = False
                defend_counter = 0
                paused = False
            elif self.buttons[idx] == "return":
                from main import OptionsPage
                menu = OptionsPage()
                menu.run()
        elif self.button_types[idx] == 1:
            self.button_selected = not self.button_selected


class GameOverScreen:
    game_over_font = pygame.font.Font('pixelfont.ttf', 64)
    game_over = Text("GAME OVER", (middleX - 276, middleY - 40), game_over_font)
    scale = 4

    def render(self):
        self.game_over.render()
        retry_img = pygame.transform.scale(retry_button_selected, (retry_button_selected.get_width() * self.scale,
                                                                   retry_button_selected.get_height() * self.scale))
        screen.blit(retry_img, (middleX - retry_img.get_width() / 2, middleY - retry_img.get_height() / 2 + 80))

    def pressed(self):
        mixer.music.unpause()
        mixer.music.rewind()
        global scoreValue, aggressionValue, enemies, projectiles, reload_timer, spawn_timer, paused, \
            attack_skill_ready, attack_counter, defend_skill_ready, defend_counter, unlocked_enemies
        scoreValue = 0
        score.text = "Score : 0"
        aggressionValue = 5
        enemies = [[], [], [], []]
        unlocked_enemies = 1
        projectiles = []
        reload_timer = spawn_timer = 0.0
        player.lives = 3
        attack_skill_ready = False
        attack_counter = 0
        defend_skill_ready = False
        defend_counter = 0
        paused = False


def calculate_distance(obj):
    return math.sqrt(math.pow(obj.position[0] - player.position[0], 2) +
                     math.pow(obj.position[1] - player.position[1], 2))


def colliding(attacker, defender):

    if isinstance(attacker, Projectile) and isinstance(defender, Enemy):
        x1 = attacker.position[0]
        y1 = attacker.position[1]
        x2 = defender.position[0]
        y2 = defender.position[1]
        distance = math.sqrt(math.pow(x2 - x1, 2) + math.pow(y2 - y1, 2))
        if distance < 16:
            if not defender.dead:
                attacker.penetration -= 1
                if attacker.penetration <= 0:
                    attacker.dead = True
                defender.dead = True
            return True
    return False


score_font = pygame.font.Font('pixelfont.ttf', 32)
volume_font = pygame.font.Font('pixelfont.ttf', 16)
clock = pygame.time.Clock()

player = Player(playerImg, 0, (middleX, middleY), 1.2, 0)
score = Text("Score : " + str(scoreValue), (10, 10), score_font)
pause = PauseMenu(pauseMenuImg, menu_buttons, menu_button_types, menu_buttons_images, (middleX, middleY),
                  5)
game_over = GameOverScreen()

sound_volume_text_pos = (pause.position[0] + 86 * pause.scale, pause.position[1] + 19 * pause.scale)
sound_volume_text = Text(str(int(sound_volume * 100)), sound_volume_text_pos, volume_font)
music_volume_text_pos = (pause.position[0] + 86 * pause.scale, pause.position[1] + 36 * pause.scale)
music_volume_text = Text(str(int(music_volume * 100)), music_volume_text_pos, volume_font)


class Main:
    def run(self):
        global aggressionValue, paused, current_button, sound_volume, music_volume, unlocked_enemies, scoreValue,\
            deltaTime, attack_counter, attack_skill_ready, defend_counter, defend_skill_ready, reload_timer,\
            spawn_timer, defend_counter
        difficulty_increase_timer = 0.0
        arrow_proof = False
        shield_timer = 0.0

        # Game Loop
        run = True
        while run:
            deltaTime = clock.tick(60) / 1000
            if paused:
                deltaTime = 0

            screen.fill((0, 0, 0))
            screen.blit(background, (0, 0))

            # Difficulty increase over time
            difficulty_increase_timer += deltaTime
            if aggressionValue < 20:
                if difficulty_increase_timer >= 20:
                    aggressionValue += 1
                    difficulty_increase_timer = 0.0
            if aggressionValue == 7:
                unlocked_enemies = 2

            # Player lives on screen
            if player.lives == 3:
                screen.blit(heartImg, (SCREEN_WIDTH - 150, 0))
            if player.lives >= 2:
                screen.blit(heartImg, (SCREEN_WIDTH - 100, 0))
            if player.lives >= 1:
                screen.blit(heartImg, (SCREEN_WIDTH - 50, 0))

            # Score render
            score.render()

            # Skills charge up
            if attack_counter >= attack_skill_CD:
                attack_skill_ready = True
            if defend_counter >= defend_skill_CD:
                defend_skill_ready = True

            # Skills render
            if attack_skill_ready:
                image = pygame.transform.scale(attack_icon_charged,
                                               (attack_icon_charged.get_width() * 2,
                                                attack_icon_charged.get_height() * 2))
                screen.blit(image, (SCREEN_WIDTH - 128, SCREEN_HEIGHT - 172))
            else:
                image = pygame.transform.scale(attack_icon_not_charged,
                                               (attack_icon_not_charged.get_width() * 2,
                                                attack_icon_not_charged.get_height() * 2))
                screen.blit(image, (SCREEN_WIDTH - 128, SCREEN_HEIGHT - 172))

            if defend_skill_ready:
                image = pygame.transform.scale(defence_icon_charged,
                                               (defence_icon_charged.get_width() * 2,
                                                defence_icon_charged.get_height() * 2))
                screen.blit(image, (SCREEN_WIDTH - 256, SCREEN_HEIGHT - 172))
            else:
                image = pygame.transform.scale(defence_icon_not_charged,
                                               (defence_icon_not_charged.get_width() * 2,
                                                defence_icon_not_charged.get_height() * 2))
                screen.blit(image, (SCREEN_WIDTH - 256, SCREEN_HEIGHT - 172))

            # Event loop
            for event in pygame.event.get():
                # Close game
                if event.type == pygame.QUIT:
                    run = False

                # Pause Menu
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        paused = not paused
                        current_button = 0
                        pause.button_selected = False
                        if paused:
                            mixer.music.pause()
                        else:
                            mixer.music.unpause()
                    if paused:
                        for i in range(0, len(menu_buttons_images)):
                            menu_buttons_images[i] = menu_buttons_non_selected_images[i]
                        if event.key == pygame.K_RIGHT or event.key == pygame.K_d:
                            if pause.button_selected:
                                if current_button == 2:  # Sound
                                    if sound_volume < 1:
                                        if sound_volume == 0.05:
                                            sound_volume_text.position = (
                                            pause.position[0] + 86 * pause.scale, pause.position[1] + 19 * pause.scale)
                                        sound_volume += 0.05
                                        sound_volume = round(sound_volume, 2)
                                        sound_volume_text.text = str(int(sound_volume * 100))
                                        arrow_shot_sound.set_volume(sound_volume)
                                        bow_reload_sound.set_volume(sound_volume)
                                        arrow_hit_sound.set_volume(sound_volume)
                                        if sound_volume == 1:
                                            sound_volume_text.position = (
                                            pause.position[0] + 84 * pause.scale, pause.position[1] + 19 * pause.scale)
                                elif current_button == 3:  # Music
                                    if music_volume < 1:
                                        if music_volume == 0.05:
                                            music_volume_text.position = (
                                            pause.position[0] + 86 * pause.scale, pause.position[1] + 36 * pause.scale)
                                        music_volume += 0.05
                                        music_volume = round(music_volume, 2)
                                        music_volume_text.text = str(int(music_volume * 100))
                                        mixer.music.set_volume(music_volume)
                                        if music_volume == 1:
                                            music_volume_text.position = (
                                            pause.position[0] + 84 * pause.scale, pause.position[1] + 36 * pause.scale)
                            else:
                                if current_button < len(menu_buttons) - 1:
                                    current_button += 1
                        elif event.key == pygame.K_LEFT or event.key == pygame.K_a:
                            if pause.button_selected:
                                if current_button == 2:  # Sound
                                    if sound_volume > 0:
                                        if sound_volume == 1:
                                            sound_volume_text.position = (
                                            pause.position[0] + 86 * pause.scale, pause.position[1] + 19 * pause.scale)
                                        sound_volume -= 0.05
                                        sound_volume = round(sound_volume, 2)
                                        sound_volume_text.text = str(int(sound_volume * 100))
                                        arrow_shot_sound.set_volume(sound_volume)
                                        bow_reload_sound.set_volume(sound_volume)
                                        arrow_hit_sound.set_volume(sound_volume)
                                        if sound_volume == 0.05:
                                            sound_volume_text.position = (
                                            pause.position[0] + 88 * pause.scale, pause.position[1] + 19 * pause.scale)
                                elif current_button == 3:  # Music
                                    if music_volume > 0:
                                        if music_volume == 1:
                                            music_volume_text.position = (
                                            pause.position[0] + 86 * pause.scale, pause.position[1] + 36 * pause.scale)
                                        music_volume -= 0.05
                                        music_volume = round(music_volume, 2)
                                        music_volume_text.text = str(int(music_volume * 100))
                                        mixer.music.set_volume(music_volume)
                                        if music_volume == 0.05:
                                            music_volume_text.position = (
                                            pause.position[0] + 88 * pause.scale, pause.position[1] + 36 * pause.scale)
                            else:
                                if current_button > 0:
                                    current_button -= 1
                        menu_buttons_images[current_button] = menu_buttons_selected_images[current_button]
                        if event.key == pygame.K_SPACE:
                            pause.pressed(current_button)
                        break

                # Player rotation
                if player.lives > 0:
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_UP or event.key == pygame.K_w:
                            player.angle = 180
                            player.facing = 2
                        elif event.key == pygame.K_DOWN or event.key == pygame.K_s:
                            player.angle = 0
                            player.facing = 0
                        elif event.key == pygame.K_LEFT or event.key == pygame.K_a:
                            player.angle = -90
                            player.facing = 3
                        elif event.key == pygame.K_RIGHT or event.key == pygame.K_d:
                            player.angle = 90
                            player.facing = 1
                        if event.key == pygame.K_SPACE:
                            if player.armed and not bow_channel.get_busy():
                                bow_channel.play(arrow_shot_sound)
                                new_arrow = Projectile(arrowImg, player.facing, player.position, 1.2,
                                                       player.angle, "player", 1)
                                projectiles.append(new_arrow)
                                player.armed = False
                        if event.key == pygame.K_e:
                            if attack_skill_ready:
                                bow_channel.play(arrow_shot_sound)
                                attack_skill_ready = False
                                attack_counter = 0
                                skill_arrow = Projectile(skillArrow, player.facing, player.position, 1.2,
                                                         player.angle, "player", 100)
                                projectiles.append(skill_arrow)
                        if event.key == pygame.K_q:
                            if defend_skill_ready:
                                defend_skill_ready = False
                                defend_counter = 0
                                arrow_proof = True
                else:
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_SPACE:
                            game_over.pressed()

            # Pause Menu
            if paused:
                pause.render()
                pygame.display.update()
                continue

            # End screen
            if player.lives <= 0:
                game_over.render()
                mixer.music.pause()
                pygame.display.update()
                continue

            # Reload bow
            reload_timer += deltaTime
            if reload_timer >= arrowCD:
                player.armed = True
                reload_timer = 0.0
            if not player.armed and not bow_channel.get_busy() and reload_timer >= arrowCD / 2:
                bow_channel.play(bow_reload_sound)

            # Spawn enemies
            spawn_timer += deltaTime
            if spawn_timer >= spawnTime:
                spawn_timer = 0.0
                spawnValue = random.randint(0, 20)
                if spawnValue <= aggressionValue:
                    enemyFacing = random.randint(0, 3)
                    idx = random.randint(0, unlocked_enemies - 1)
                    enemyType = enemy_types[idx]
                    enemyPos = spawnPositions[enemyFacing]
                    enemyAngle = 0
                    if enemyFacing == 1:
                        enemyAngle = 90
                    elif enemyFacing == 2:
                        enemyAngle = 180
                    elif enemyFacing == 3:
                        enemyAngle = -90
                    new_enemy = Enemy(enemy_images[idx], enemyType, enemyFacing, enemyPos, 0.8, enemyAngle)
                    enemies[enemyFacing].append(new_enemy)

            # Collisions
            for projectile in projectiles:
                if projectile.shooter == "player":
                    index = 0
                    if projectile.facing == 0:
                        index = 2
                    elif projectile.facing == 1:
                        index = 3
                    elif projectile.facing == 3:
                        index = 1
                    if len(enemies[index]) != 0:
                        if colliding(projectile, min(enemies[index], key=calculate_distance)):
                            enemy_channel.play(arrow_hit_sound)
                            if projectile.dead:
                                attack_counter += 1

            # Enemies
            for enemyLine in enemies:
                i = 0
                while i < len(enemyLine):
                    enemy = enemyLine[i]
                    enemy.render()
                    if enemy.dead:
                        enemyLine.remove(enemy)
                        scoreValue += 1
                        score.text = "Score : " + str(scoreValue)
                        continue
                    if not enemy.move():
                        if enemy.enemyType == "melee":
                            player.lives -= 1
                            enemyLine.remove(enemy)
                        elif enemy.enemyType == "ranger":
                            enemy.reload_timer += deltaTime
                            if enemy.reload_timer >= enemy_shooting_CD:
                                enemy.reload_timer = 0.0
                                new_projectile = Projectile(poisonImg, enemy.facing, enemy.position, 0.8,
                                                            enemy.angle, "enemy", 1)
                                projectiles.append(new_projectile)
                            i += 1
                    else:
                        i += 1

            # Projectiles
            i = 0
            while i < len(projectiles):
                projectile = projectiles[i]
                projectile.render()
                if not projectile.move():
                    if projectile.shooter == "enemy":
                        if not arrow_proof:
                            if player.facing != projectile.facing:
                                player.lives -= 1
                            else:
                                defend_counter += 1
                    projectiles.remove(projectile)
                elif projectile.dead:
                    projectiles.remove(projectile)
                else:
                    i += 1

            player.render()

            # Defend Skill
            if arrow_proof:
                image = pygame.transform.scale(shieldSkillImg, (
                shieldSkillImg.get_width() * player.scale, shieldSkillImg.get_height() * player.scale))
                screen.blit(image, player.position)
                shield_timer += deltaTime
                if shield_timer >= 2:
                    shield_timer = 0.0
                    arrow_proof = False

            pygame.display.update()


main = Main()
main.run()

pygame.quit()
