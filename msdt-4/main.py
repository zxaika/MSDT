import pygame
import numpy as np
import logging

# Настройка логирования
logging.basicConfig(
    level=logging.DEBUG,  # Уровень логирования
    format='%(asctime)s - %(levelname)s - %(message)s',  # Формат сообщения
    handlers=[
        logging.FileHandler("project.log"),  # Записывать лог в файл
        logging.StreamHandler()  # Также выводить в консоль
    ]
)

# Константы
WIDTH, HEIGHT = 800, 600
FPS = 60
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
CYAN = (0, 255, 255)

# Получение параметров цилиндра
RADIUS = float(input("Введите радиус цилиндра: "))
HEIGHT = float(input("Введите высоту цилиндра: "))
N_SEGMENTS = 30  # Количество сегментов цилиндра по окружности
M_SEGMENTS = 10  # Количество сегментов цилиндра по высоте

# Логируем параметры
logging.info(f"Радиус цилиндра: {RADIUS}, Высота цилиндра: {HEIGHT}, "
             f"Сегменты по окружности: {N_SEGMENTS}, Сегменты по высоте: {M_SEGMENTS}")

def project_point(x, y, z, d = 500):
    factor = d / (d + z)
    x_proj = int(WIDTH / 2 + x * factor)
    y_proj = int(HEIGHT / 2 - y * factor)
    return x_proj, y_proj

def generate_cylinder(radius, height, n_segments, m_segments):
    logging.info("Генерация цилиндра...")
    vertices = []
    edges = []
    polygons = []

    for i in range(m_segments + 1):
        z = -height / 2 + (height / m_segments) * i
        for j in range(n_segments):
            alpha = 2 * np.pi * j / n_segments
            x = radius * np.cos(alpha)
            y = radius * np.sin(alpha)
            vertices.append((x, y, z))

    for i in range(m_segments):
        for j in range(n_segments):
            curr = i * n_segments + j
            next_ = i * n_segments + (j + 1) % n_segments
            top = (i + 1) * n_segments + j
            next_top = (i + 1) * n_segments + (j + 1) % n_segments
            edges.append((curr, next_))
            edges.append((curr, top))
            polygons.append((curr, next_, next_top, top))

    logging.info(f"Цилиндр сгенерирован: {len(vertices)} вершин, {len(edges)} ребер, {len(polygons)} полигонов.")
    return vertices, edges, polygons

def translate(vertices, dx, dy, dz):
    return [(x + dx, y + dy, z + dz) for x, y, z in vertices]

def scale(vertices, kx, ky, kz):
    return [(x * kx, y * ky, z * kz) for x, y, z in vertices]

def rotate_x(vertices, angle):
    cos_a, sin_a = np.cos(angle), np.sin(angle)
    return [
        (x, y * cos_a - z * sin_a, y * sin_a + z * cos_a) for x, y, z in vertices
    ]

def rotate_y(vertices, angle):
    cos_a, sin_a = np.cos(angle), np.sin(angle)
    return [
        (x * cos_a + z * sin_a, y, -x * sin_a + z * cos_a) for x, y, z in vertices
    ]

def rotate_z(vertices, angle):
    cos_a, sin_a = np.cos(angle), np.sin(angle)
    return [
        (x * cos_a - y * sin_a, x * sin_a + y * cos_a, z) for x, y, z in vertices
    ]

# Инициализация Pygame
pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Лабораторная работа 5")
clock = pygame.time.Clock()

# Генерация цилиндра
vertices, edges, polygons = generate_cylinder(RADIUS, HEIGHT, N_SEGMENTS, M_SEGMENTS)
angle_x, angle_y, angle_z = 0, 0, 0
position = [0, 0, 0]
scale_factor = [1, 1, 1]
running = True

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    keys = pygame.key.get_pressed()
    if keys[pygame.K_w]:
        position[1] += 5
        logging.debug("Движение вверх по оси Y")
    if keys[pygame.K_s]:
        position[1] -= 5
        logging.debug("Движение вниз по оси Y")
    if keys[pygame.K_a]:
        position[0] -= 5
        logging.debug("Движение влево по оси X")
    if keys[pygame.K_d]:
        position[0] += 5
        logging.debug("Движение вправо по оси X")
    if keys[pygame.K_r]:
        position[2] += 5
        logging.debug("Движение вперед по оси Z")
    if keys[pygame.K_f]:
        position[2] -= 5
        logging.debug("Движение назад по оси Z")
    if keys[pygame.K_y]:
        scale_factor = [sf * 1.05 for sf in scale_factor]
        logging.debug("Масштабирование объекта (увеличение)")
    if keys[pygame.K_x]:
        scale_factor = [sf * 0.95 for sf in scale_factor]
        logging.debug("Масштабирование объекта (уменьшение)")
    if keys[pygame.K_LEFT]:
        angle_y -= 0.05
        logging.debug("Поворот объекта по оси Y влево")
    if keys[pygame.K_RIGHT]:
        angle_y += 0.05
        logging.debug("Поворот объекта по оси Y вправо")
    if keys[pygame.K_UP]:
        angle_x -= 0.05
        logging.debug("Поворот объекта по оси X вверх")
    if keys[pygame.K_DOWN]:
        angle_x += 0.05
        logging.debug("Поворот объекта по оси X вниз")
    if keys[pygame.K_q]:
        angle_z -= 0.05
        logging.debug("Поворот объекта по оси Z влево")
    if keys[pygame.K_e]:
        angle_z += 0.05
        logging.debug("Поворот объекта по оси Z вправо")

    screen.fill(WHITE)

    transformed_vertices = translate(vertices, *position)
    transformed_vertices = scale(transformed_vertices, *scale_factor)
    transformed_vertices = rotate_x(transformed_vertices, angle_x)
    transformed_vertices = rotate_y(transformed_vertices, angle_y)
    transformed_vertices = rotate_z(transformed_vertices, angle_z)

    projected_points = [project_point(x, y, z) for x, y, z in transformed_vertices]

    for poly in polygons:
        points = [projected_points[i] for i in poly]
        pygame.draw.polygon(screen, CYAN, points, 1)

    for edge in edges:
        p1, p2 = edge
        pygame.draw.line(screen, BLACK, projected_points[p1], projected_points[p2], 1)

    pygame.display.flip()
    clock.tick(FPS)

logging.info("Программа завершена")
pygame.quit()
