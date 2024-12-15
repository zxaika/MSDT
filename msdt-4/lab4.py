import pygame
import numpy as np

WIDTH, HEIGHT = 800, 600
FPS = 60
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
CYAN = (0, 255, 255)

# Запрос данных цилиндра
R = float(input("Введите радиус цилиндра: "))
H = float(input("Введите высоту цилиндра: "))
N = 30  # Количество сегментов
M = 10  # Количество сегментов по высоте

# Центральная(перспективная) проекция
def project_point(x, y, z, d = 500):
    factor = d / (d + z)
    x_proj = int(WIDTH / 2 + x * factor)
    y_proj = int(HEIGHT / 2 - y * factor)
    return x_proj, y_proj

# Генерация цилиндра
def generate_cylinder(radius, height, n_segments, m_segments):
    vertices = []
    edges = []
    polygons = []

    # Генерация точек
    for i in range(m_segments + 1):
        z = -height / 2 + (height / m_segments) * i
        for j in range(n_segments):
            alpha = 2 * np.pi * j / n_segments
            x = radius * np.cos(alpha)
            y = radius * np.sin(alpha)
            vertices.append((x, y, z))

    # Соединение точек
    for i in range(m_segments):
        for j in range(n_segments):
            curr = i * n_segments + j
            next_ = i * n_segments + (j + 1) % n_segments
            top = (i + 1) * n_segments + j
            next_top = (i + 1) * n_segments + (j + 1) % n_segments

            edges.append((curr, next_))
            edges.append((curr, top))
            polygons.append((curr, next_, next_top, top))

    return vertices, edges, polygons

# Аффинные преобразования
def translate(vertices, dx,dy, dz):
    return [(x + dx, y + dy, z + dz) for x, y, z in vertices]

def scale(vertices, kx, ky, kz):
    return [(x * kx, y * ky, z * kz) for x, y, z in vertices]

def rotate_x(vertices, angle):
    cos_a, sin_a = np.cos(angle), np.sin(angle)
    return [(x, y * cos_a - z * sin_a, y * sin_a + z * cos_a) for x, y, z in vertices]

def rotate_y(vertices, angle):
    cos_a, sin_a = np.cos(angle), np.sin(angle)
    return [(x * cos_a + z * sin_a, y, -x * sin_a + z * cos_a) for x, y, z in vertices]

def rotate_z(vertices, angle):
    cos_a, sin_a = np.cos(angle), np.sin(angle)
    return [(x * cos_a - y * sin_a, x * sin_a + y * cos_a, z) for x, y, z in vertices]

# Инициализация
pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Лабораторная работа 5")
clock = pygame.time.Clock()

# Генерация цилиндра
vertices, edges, polygons = generate_cylinder(R, H, N, M)
angle_x, angle_y, angle_z = 0, 0, 0  # Углы вращения
position = [0, 0, 0]  # Позиция цилиндра
scale_factor = [1, 1, 1]  # Масштабирование
running = True

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # обрабатываем нажатие клавиш
    keys = pygame.key.get_pressed()

    # Для перемещения
    if keys[pygame.K_w]:
        position[1] += 5
    if keys[pygame.K_s]:
        position[1] -= 5
    if keys[pygame.K_a]:
        position[0] -= 5
    if keys[pygame.K_d]:
        position[0] += 5
    if keys[pygame.K_r]:
        position[2] += 5
    if keys[pygame.K_f]:
        position[2] -= 5

    # Для масштабирования
    if keys[pygame.K_y]:
        scale_factor = [sf * 1.05 for sf in scale_factor]
    if keys[pygame.K_x]:
        scale_factor = [sf * 0.95 for sf in scale_factor]

    # Вращение
    if keys[pygame.K_LEFT]:
        angle_y -= 0.05
    if keys[pygame.K_RIGHT]:
        angle_y += 0.05
    if keys[pygame.K_UP]:
        angle_x -= 0.05
    if keys[pygame.K_DOWN]:
        angle_x += 0.05
    if keys[pygame.K_q]:
        angle_z -= 0.05
    if keys[pygame.K_e]:
        angle_z += 0.05

    # Очистка экрана
    screen.fill(WHITE)

    # Применение трансформаций
    transformed_vertices = translate(vertices, *position)
    transformed_vertices = scale(transformed_vertices, *scale_factor)
    transformed_vertices = rotate_x(transformed_vertices, angle_x)
    transformed_vertices = rotate_y(transformed_vertices, angle_y)
    transformed_vertices = rotate_z(transformed_vertices, angle_z)

    # Проекция и рендеринг
    projected_points = [project_point(x, y, z) for x, y, z in transformed_vertices]

    # Рисуем каркас
    for poly in polygons:
        points = [projected_points[i] for i in poly]
        pygame.draw.polygon(screen, CYAN, points, 1)

    # Рисуем ребра
    for edge in edges:
        p1, p2 = edge
        pygame.draw.line(screen, BLACK, projected_points[p1], projected_points[p2], 1)

    # Обновление экрана
    pygame.display.flip()
    clock.tick(FPS)

pygame.quit()

