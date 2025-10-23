import pygame
import pymunk
import pymunk.pygame_util
import random
import math
import numpy as np

# Ініціалізація pygame
pygame.init()
WIDTH, HEIGHT = 700, 500
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Robot Simulation with Q-Learning")
clock = pygame.time.Clock()

# Ініціалізація простору pymunk
space = pymunk.Space()
space.gravity = (0, 0)

frame_count = 0
keys_pressed = set()
mouse_pos = (0, 0)
mouse_button = None


def createBody(x, y, shape_type, *shape_args):
    body = pymunk.Body(1, pymunk.moment_for_poly(1, shape_args[0]) if shape_type == "poly" else 100)
    body.position = x, y

    if shape_type == "poly":
        shape = pymunk.Poly(body, shape_args[0])
    elif shape_type == "circle":
        shape = pymunk.Circle(body, shape_args[0], shape_args[1])

    shape.friction = 1
    space.add(body, shape)
    return shape


s0 = createBody(300, 300, "poly", ((-20, -5), (-20, 5), (20, 15), (20, -15)))
s0.color = (0, 0, 255, 255)
s0.score = 0

s3 = createBody(200, 300, "poly", ((-20, -5), (-20, 5), (20, 15), (20, -15)))
s3.color = (0, 255, 0, 255)
s3.score = 0
s3.body.Q = [[0.0, 0.0], [0.0, 0.0], [0.0, 0.0]]
# s3.body.Q=[[0, 0], [1, -1], [-1, 1]]
# Q=[нічого[залишати, змінювати], об'єкт[залишати, змінювати], антиоб'єкт[залишати, змінювати]]
s3.body.action = 0  # 0 - залишати, 1 - змінювати (випадковий кут)

s1 = createBody(300, 200, "circle", 10, (0, 0))
s1.color = (255, 255, 0, 255)

S2 = []
for i in range(1):
    s2 = createBody(350, 250, "circle", 10, (0, 0))
    s2.color = (255, 0, 0, 255)
    S2.append(s2)


def getAngle(x, y, x1, y1):
    return math.atan2(y1 - y, x1 - x)


def getDist(x, y, x1, y1):
    return ((x - x1) ** 2 + (y - y1) ** 2) ** 0.5


def inCircle(x, y, cx, cy, R):
    if (x - cx) ** 2 + (y - cy) ** 2 < R ** 2:
        return True
    return False


def inSector(x, y, cx, cy, R, a):
    angle = getAngle(cx, cy, x, y)
    a = a % (2 * math.pi)
    angle = angle % (2 * math.pi)
    if inCircle(x, y, cx, cy, R) and a - 0.5 < angle < a + 0.5:
        return True
    return False


def strategy(b=None):
    """
    Стратегія робота з Q-learning.
    Робот сканує сектор, визначає об'єкти та навчається оптимальної поведінки.
    """
    if b is None:
        b = s3.body

    v = 100
    a = b.angle
    b.velocity = v * math.cos(a), v * math.sin(a)
    x, y = b.position
    R = getDist(x, y, 350, 250)

    # Малюємо сектор сканування
    pygame.draw.circle(screen, (128, 128, 128), (int(x), int(y)), 100, 1)
    pygame.draw.line(screen, (128, 128, 128), (x, y),
                     (x + 100 * math.cos(a + 0.5), y + 100 * math.sin(a + 0.5)), 1)
    pygame.draw.line(screen, (128, 128, 128), (x, y),
                     (x + 100 * math.cos(a - 0.5), y + 100 * math.sin(a - 0.5)), 1)

    if frame_count % 10 == 0:  # Кожні 10 кадрів
        inS = inSector(s1.body.position[0], s1.body.position[1], x, y, 100, a)
        inS2 = inSector(S2[0].body.position[0], S2[0].body.position[1], x, y, 100, a)

        # Встановлюємо стан і винагороду
        if inS:
            state = 1
            reward = 1 if b.action == 0 else -1
        elif inS2:
            state = 2
            reward = -1 if b.action == 0 else 1
        else:
            state = 0
            reward = 0

        # Оновлюємо Q-таблицю
        alpha = 0.1  # швидкість навчання
        gamma = 0.9  # дисконтний фактор (важливість майбутнього)
        old_value = b.Q[state][b.action]
        next_max = max(b.Q[state])  # максимальна винагорода для цього стану
        b.Q[state][b.action] = old_value + alpha * (reward + gamma * next_max - old_value)
        print(f"State: {state}, Action: {b.action}, Q: {b.Q}")

        # Вибираємо дію (epsilon-greedy)
        epsilon = max(0.1, 0.5 * math.exp(-frame_count / 1000))
        if random.random() < epsilon:
            b.action = random.choice([0, 1])
        else:
            b.action = np.argmax(b.Q[state])  # Оптимальна дія

        if b.action:  # Якщо змінювати напрямок
            b.angle = 2 * math.pi * random.random()

        if R > 180:  # Запобігти виїзду за межі
            b.angle = getAngle(x, y, 350, 250)


def scr(s, s0, s3, p=1):
    bx, by = s.body.position
    s0x, s0y = s0.body.position
    s3x, s3y = s3.body.position

    if not inCircle(bx, by, 350, 250, 180):
        if getDist(bx, by, s0x, s0y) < getDist(bx, by, s3x, s3y):
            s0.score = s0.score + p
        else:
            s3.score = s3.score + p
        s.body.position = random.randint(200, 400), random.randint(200, 300)


def score():
    """Визначає переможця"""
    scr(s1, s0, s3)
    for s in S2:
        scr(s, s0, s3, p=-1)


def manualControl():
    """Керування роботом з мишки або клавіатури"""
    v = 10
    b = s0.body
    a = b.angle
    x, y = b.position
    vx, vy = b.velocity

    if pygame.K_a in keys_pressed:
        b.angle -= 0.1
    if pygame.K_d in keys_pressed:
        b.angle += 0.1
    if pygame.K_w in keys_pressed:
        b.velocity = vx + v * math.cos(a), vy + v * math.sin(a)

    if mouse_button == 1:  # Ліва кнопка миші
        b.angle = getAngle(x, y, *mouse_pos)
        b.velocity = vx + v * math.cos(a), vy + v * math.sin(a)


def simFriction():
    """Симуляція тертя"""
    for s in [s0, s1, s3] + S2:
        vx, vy = s.body.velocity
        s.body.velocity = vx * 0.9, vy * 0.9
        s.body.angular_velocity *= 0.9


draw_options = pymunk.pygame_util.DrawOptions(screen)

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            keys_pressed.add(event.key)
        elif event.type == pygame.KEYUP:
            keys_pressed.discard(event.key)
        elif event.type == pygame.MOUSEMOTION:
            mouse_pos = event.pos
        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouse_button = event.button
        elif event.type == pygame.MOUSEBUTTONUP:
            mouse_button = None

    screen.fill((255, 255, 255))

    font = pygame.font.Font(None, 36)
    text = font.render(f"{s0.score} {s3.score}", True, (0, 0, 0))
    screen.blit(text, (20, 20))

    pygame.draw.circle(screen, (0, 0, 0), (350, 250), 175, 2)

    manualControl()
    strategy()
    score()
    simFriction()

    space.step(0.02)

    space.debug_draw(draw_options)

    pygame.display.flip()
    clock.tick(60)
    frame_count += 1

pygame.quit()
