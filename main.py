import pygame
import random

fps = 60
fpsClock = pygame.time.Clock()
width = 1000
height = 700
starting_enemies = 1000
amount_added = 1
cooldown_to_add = 10
starting_speed = 10
speed_added = 1
max_speed = 50


def float_to_closer(floata):
    floatb = int(floata) + 0.5
    if floata > floatb:
        return int(floata) + 1
    else:
        return int(floata)

def module(x):
    if x < 0:
        return -x
    else:
        return x


def convert_time(sec):
    return divmod(sec, 60)


class board:
    def __init__(self, width, height):
        pygame.init()
        self.width = width
        self.height = height
        self.top = 0
        self.bot = height
        self.left = 0
        self.right = width
        self.center_x = int(width / 2)
        self.center_y = int(height / 2)

    def adapt(self, x, y):
        x_real = x + self.width / 2
        y_real = y + self.height / 2


class projectile:
    def __init__(self, color_list, raio):
        self.color = color_list
        self.radius = raio #Dobro
        self.image = pygame.image.load('arrow_40x40.png')
    def vector(self, x, y):
        return pygame.math.Vector2(x - self.pos[0],
                                   y- self.pos[1])
    def rotate_image(self, angulo):
        pygame.transform.rotate(self.image, angulo)
    def appear_as_image(self, x, y, angulo):
        global gameDisplay
        image = pygame.transform.rotate(self.image, angulo)
        gameDisplay.blit(image, (x, y))
    def appear(self, x, y):
        global gameDisplay
        xA = xC =  float_to_closer(x)
        xB = float_to_closer(x - self.radius)
        xD = float_to_closer(x + self.radius)
        yA = float_to_closer(y + self.radius*2)
        yC = float_to_closer(y)
        yB = yD =  float_to_closer(y - self.radius)
        rect = pygame.draw.polygon(
            gameDisplay,
            (self.color[0], self.color[1], self.color[2]),
            [(xA, yA), (xB, yB), (xC, yC), (xD, yD)] #ABCDA?
        )
        self.pos = [xC, yC]
    def move_towards_player(self, playera):
        # Find direction vector (dx, dy) between enemy and player
        dirvect = pygame.math.Vector2(playera.pos[0] - self.pos[0],
                                      playera.pos[1] - self.pos[1])
        # Move along this normalized vector towards the player at current speed
        lista = []
        angulos = self.angles_to_check()
        for i in angulos:
            lista.append(module(dirvect.angle_to(i)))
        ind = lista.index(min(lista))
        x, y = angulos[ind][0], angulos[ind][1]
        angulo = min(lista)
        self.appear(self.pos[0] + x, self.pos[1] + y)

    def angles_to_check(self):
        x = self.pos[0]
        y = self.pos[1]
        lista = []
        lista.append(self.vector(x+2, y+1))
        lista.append(self.vector(x+2, y))
        lista.append(self.vector(x+2, y-1))
        lista.append(self.vector(x+1, y+2))
        lista.append(self.vector(x+1, y+1))
        lista.append(self.vector(x+1, y-1))
        lista.append(self.vector(x+1, y-2))
        lista.append(self.vector(x, y+2))
        lista.append(self.vector(x, y-2))
        lista.append(self.vector(x-1, y+2))
        lista.append(self.vector(x-1, y+1))
        lista.append(self.vector(x-1, y-1))
        lista.append(self.vector(x-1, y-2))
        lista.append(self.vector(x-2, y+1))
        lista.append(self.vector(x-2, y))
        lista.append(self.vector(x-2, y-1))

        return lista
class player:
    def __init__(self, color_list, raio):
        self.color = color_list
        self.radius = raio

    def appear(self, x, y):
        global gameDisplay
        pygame.draw.circle(gameDisplay,
                           (self.color[0], self.color[1], self.color[2]),
                           (x, y),
                           self.radius
                           )
        self.pos = [x, y]

    def goto(self, x, y):
        pass  # not used

    def update_color(self, new_color_list):
        self.color = new_color_list

    def update_radius(self, novo_raio):
        self.radius = novo_raio

    def orientacao(self, string):
        self.direction = string
        if string == "up":
            self.adder_x = 0
            self.adder_y = -2
        elif string == "down":
            self.adder_x = 0
            self.adder_y = 2
        elif string == "left":
            self.adder_x = -2
            self.adder_y = 0
        elif string == "right":
            self.adder_x = 2
            self.adder_y = 0


def write(text, color_list, size, pos):
    global gameDisplay
    font = pygame.font.SysFont(None, size)
    if pos == "center":
        label = font.render(text, True, (color_list[0], color_list[1], color_list[2]))
        text_rect = label.get_rect(center=(int(screen.width / 2), int(screen.height / 2)))
        gameDisplay.blit(label, text_rect)
    elif pos == "2lines":
        text1, text2 = text.split("\n")
        label1 = font.render(text1, True, (color_list[0], color_list[1], color_list[2]))
        label2 = font.render(text2, True, (color_list[0], color_list[1], color_list[2]))
        text_rect = label1.get_rect(center=(int(screen.width / 2), int(screen.height / 4)))
        gameDisplay.blit(label1, text_rect)
        text_rect = label2.get_rect(center=(int(screen.width / 2), int((screen.height / 4) * 3)))
        gameDisplay.blit(label2, text_rect)
    else:
        label = font.render(text, True, (color_list[0], color_list[1], color_list[2]))
        gameDisplay.blit(label, ([pos[0], pos[1]]))
    pygame.display.update()


def hide_cursor(boo):
    if boo:
        pygame.mouse.set_cursor((8, 8), (0, 0), (0, 0, 0, 0, 0, 0, 0, 0), (0, 0, 0, 0, 0, 0, 0, 0))
    else:
        pygame.mouse.set_cursor((16, 16), (0, 0), (
            0, 0, 64, 0, 96, 0, 112, 0, 120, 0, 124, 0, 126, 0, 127, 0, 127, 128, 124, 0, 108, 0, 70, 0, 6, 0, 3, 0, 3,
            0,
            0, 0), (192, 0, 224, 0, 240, 0, 248, 0, 252, 0, 254, 0, 255, 0, 255, 128, 255, 192, 255, 224, 254, 0, 239,
                    0,
                    207, 0, 135, 128, 7, 128, 3, 0))


def player_on_fruit(p, f):
    try:
        if (p.radius + f.radius) ** 2 > \
                ((module(p.pos[0] - f.pos[0])) ** 2) + (module(p.pos[1] - f.pos[1]) ** 2):
            return True
        else:
            return False
    except AttributeError:
        return True


def transition_wait(text, configuration, passing_level=True):
    hide_cursor(False)
    gameDisplay.fill((0, 0, 0))
    write(text, [250, 250, 250], 100, configuration)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            quit()
        if event.type == pygame.MOUSEBUTTONDOWN:
            global win_status, level
            win_status = None
            hide_cursor(True)
            if passing_level:
                level += 1

fpscount = 0
time = 0

if __name__ == "__main__":
    win_status = None
    level = 0
    screen = board(width, height)
    gameDisplay = pygame.display.set_mode((screen.width, screen.height))
    speed = starting_speed
    enemies = starting_enemies
    enemies_list = []
    special_enemies = []
    fading = True
    fading_colorlist = [0, 0, 0]
    while True:
        ciclo = True
        if level == 0:
            transition_wait("Click to start", "center")
        elif level == 1 and win_status:
            gameDisplay.fill((0, 0, 0))
            m, s = convert_time(time)
            transition_wait(("Level 1 completed \n %d:%02d" % (time / 60, time % 60)), "2lines")
        elif level == 2 and win_status:
            gameDisplay.fill((0, 0, 0))
            enemies_list = []
            m, s = convert_time(time)
            transition_wait(("Level 2 completed \n %d:%02d" % (time / 60, time % 60)), "2lines")
        elif win_status is None:
            enemies_list = []
            special_enemies = []
            fpscount = 0
            time = 0
            if level == 1 or level == 2:
                win_condition = 20
                p1 = player([9, 224, 73], 10)
                mouse_pos = [screen.center_x, screen.center_y]
                fruit = player([250, 250, 32], 10)
                fruit_count = -1
            hide_cursor(True)
            while ciclo:
                gameDisplay.fill((0, 0, 0))
                p1.appear(mouse_pos[0], mouse_pos[1])
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pygame.quit()
                        quit()
                    if event.type == pygame.MOUSEMOTION:
                        mouse_pos = event.pos

                fpscount += 1
                for enemy in enemies_list:
                    enemy.appear(enemy.pos[0] + (enemy.adder_x), enemy.pos[1] + (enemy.adder_y))
                    if (enemy.radius + p1.radius) ** 2 > \
                            ((module(enemy.pos[0] - p1.pos[0])) ** 2) + (module(enemy.pos[1] - p1.pos[1]) ** 2):
                        ciclo = False
                        print(time)
                        win_status = False
                    if enemy.pos[0] > width or enemy.pos[1] > height or enemy.pos[0] < 0 or enemy.pos[1] < 0:
                        enemies_list.remove(enemy)
                for enemy in special_enemies:
                    enemy.move_towards_player(p1)
                    if 20 > \
                            ((module(enemy.pos[0] - p1.pos[0])) ** 2) + (module(enemy.pos[1] - p1.pos[1]) ** 2):
                        ciclo = False
                        print(time)
                        win_status = False
                if fpscount % fps == 0:
                    time += 1
                    enemy = player([230, 0, 0], 10)
                    rand = random.randint(1, 4)
                    if level == 2 and time % 3 == 0:
                        following_enemy = projectile([201, 70, 71], 2)
                        if rand == 1:
                            rand = random.randint(0, height)
                            following_enemy.appear(0, rand)
                        elif rand == 2:
                            rand = random.randint(0, width)
                            following_enemy.appear(rand, 0)
                        elif rand == 3:
                            rand = random.randint(0, height)
                            following_enemy.appear(width, rand)
                        elif rand == 4:
                            rand = random.randint(0, width)
                            following_enemy.appear(rand, height)
                        special_enemies.append(following_enemy)
                        rand = random.randint(1, 4)
                    if rand == 1:  # left
                        rand = random.randint(0, height)
                        enemy.appear(0, rand)
                        enemy.orientacao("right")
                    elif rand == 2:  # up
                        rand = random.randint(0, width)
                        enemy.appear(rand, 0)
                        enemy.orientacao("down")
                    elif rand == 3:  # right
                        rand = random.randint(0, height)
                        enemy.appear(width, rand)
                        enemy.orientacao("left")
                    elif rand == 4:  # down
                        rand = random.randint(0, width)
                        enemy.appear(rand, height)
                        enemy.orientacao("up")
                    enemies_list.append(enemy)
                if player_on_fruit(p1, fruit):
                    fruit_count += 1
                    if fruit_count == win_condition:
                        ciclo = False
                        win_status = True
                    fruit.appear(random.randint(0 + fruit.radius, width - fruit.radius),
                                 random.randint(0 + fruit.radius, height - fruit.radius))
                    fading = True
                    fading_colorlist = [211, 211, 211]
                else:
                    fruit.appear(fruit.pos[0], fruit.pos[1])
                if fading and fading_colorlist[0] > 0:
                    write(str(win_condition - fruit_count), fading_colorlist, 200, "center")
                    r = g = b = fading_colorlist[0] - 3
                    fading_colorlist = [r, g, b]
                fpsClock.tick(fps)
                pygame.display.update()
        elif win_status is False:
            transition_wait("You lost! Click to restart \n %d:%02d" % (time / 60, time % 60), "2lines",
                            passing_level=False)