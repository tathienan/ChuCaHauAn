import pygame
from pygame.locals import *
import time
import random

SIZE = 40
BACKGROUND_COLOR = (110, 110, 5)

# THUC AN
class Food:
    def __init__(self, parent_screen):
        self.parent_screen = parent_screen
        self.image = pygame.image.load("resources/small.png").convert()
        self.x = 120
        self.y = 120

    def draw(self):
        self.parent_screen.blit(self.image, (self.x, self.y))
        pygame.display.flip()

    def move(self):
        self.x = random.randint(1,24)*SIZE
        self.y = random.randint(1,19)*SIZE

# CA
class Fish:
    def __init__(self, parent_screen):
        self.parent_screen = parent_screen
        self.image = pygame.image.load("resources/big.png").convert()
        self.direction = 'down'

        self.length = 1
        self.x = [40]
        self.y = [40]

    def move_left(self):
        self.direction = 'left'

    def move_right(self):
        self.direction = 'right'

    def move_up(self):
        self.direction = 'up'

    def move_down(self):
        self.direction = 'down'

    def walk(self):
        if self.direction == 'left':
            self.x[0] -= SIZE
        if self.direction == 'right':
            self.x[0] += SIZE
        if self.direction == 'up':
            self.y[0] -= SIZE
        if self.direction == 'down':
            self.y[0] += SIZE

        self.draw()

    def draw(self):
        for i in range(self.length):
            self.parent_screen.blit(self.image, (self.x[i], self.y[i]))

        pygame.display.flip()

    def increase_length(self):
        self.length += 1
        self.x.append(-1)
        self.y.append(-1)

class Game:
    def __init__(self):
        pygame.init()
        pygame.display.set_caption("CHÚ CÁ HÁU ĂN")

        pygame.mixer.init()
        self.play_background_music()

        self.surface = pygame.display.set_mode((1000, 800))
        self.fish = Fish(self.surface)
        self.fish.draw()
        self.food = Food(self.surface)
        self.food.draw()

    def play_background_music(self):
        pygame.mixer.music.load('resources/bg_music_1.mp3')
        pygame.mixer.music.play(-1, 0)

    def play_sound(self, sound_name):
        if sound_name == "crash":
            sound = pygame.mixer.Sound("resources/crash.mp3")
        elif sound_name == 'ding':
            sound = pygame.mixer.Sound("resources/ding.mp3")

        pygame.mixer.Sound.play(sound)


    def reset(self):
        self.fish = Fish(self.surface)
        self.food = Food(self.surface)


    def is_collision(self, x1, y1, x2, y2):
        if x1 >= x2 and x1 < x2 + SIZE:
            if y1 >= y2 and y1 < y2 + SIZE:
                return True
        return False

    def render_background(self):
        bg = pygame.image.load("resources/background.jpg")
        self.surface.blit(bg, (0,0))

    def play(self):
        self.render_background()
        self.fish.walk()
        self.food.draw()
        self.display_score()
        pygame.display.flip()

        # Ca an thuc an
        for i in range(self.fish.length):
            if self.is_collision(self.fish.x[i], self.fish.y[i], self.food.x, self.food.y):
                self.play_sound("ding")
                self.fish.increase_length()
                self.food.move()

        # Ca va cham canh cua so
        if not (0 <= self.fish.x[0] <= 1000 and 0 <= self.fish.y[0] <= 800):
            self.play_sound('crash')
            raise "Hit the boundry error"

    # DIEM SO
    def display_score(self):
        font = pygame.font.SysFont('arial',30)
        score = font.render(f"Score: {self.fish.length}",True,(200,200,200))
        self.surface.blit(score,(850,10))

    # GAME OVER
    def show_game_over(self):
        self.render_background()
        font = pygame.font.SysFont('arial', 30)
        line1 = font.render(f"Game is over! Your score is {self.fish.length}", True, (255, 255, 255))
        self.surface.blit(line1, (200, 300))
        line2 = font.render("To play again press Enter. To exit press Esc!", True, (255, 255, 255))
        self.surface.blit(line2, (200, 350))
        pygame.mixer.music.pause()
        pygame.display.flip()

    def run(self):
        running = True
        pause = False

        while running:
            for event in pygame.event.get():
                if event.type == KEYDOWN:
                    if event.key == K_ESCAPE:
                        running = False

                    if event.key == K_RETURN:
                        pygame.mixer.music.unpause()
                        pause = False

                    if not pause:
                        if event.key == K_LEFT:
                            self.fish.move_left()

                        if event.key == K_RIGHT:
                            self.fish.move_right()

                        if event.key == K_UP:
                            self.fish.move_up()

                        if event.key == K_DOWN:
                            self.fish.move_down()

                elif event.type == QUIT:
                    running = False
            try:

                if not pause:
                    self.play()

            except Exception as e:
                self.show_game_over()
                pause = True
                self.reset()

            time.sleep(.1)

if __name__ == '__main__':
    game = Game()
    game.run()