from random import randint

import pygame

# Константы для размеров поля и сетки:
SCREEN_WIDTH, SCREEN_HEIGHT = 640, 480
GRID_SIZE = 20
GRID_WIDTH = SCREEN_WIDTH // GRID_SIZE
GRID_HEIGHT = SCREEN_HEIGHT // GRID_SIZE

# Направления движения:
UP = (0, -1)
DOWN = (0, 1)
LEFT = (-1, 0)
RIGHT = (1, 0)

# Цвет фона - черный:
BOARD_BACKGROUND_COLOR = (0, 0, 0)

# Цвет границы ячейки
BORDER_COLOR = (93, 216, 228)

# Цвет яблока
APPLE_COLOR = (255, 0, 0)

# Цвет змейки
SNAKE_COLOR = (0, 255, 0)

# Скорость движения змейки:
SPEED = 20

# Настройка игрового окна:
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), 0, 32)

# Заголовок окна игрового поля:
pygame.display.set_caption("Змейка")

# Настройка времени:
clock = pygame.time.Clock()


# Классы игры:
class GameObject:
    def __init__(self, body_color=None):  # Инициализирует базовые атрибуты.
        self.position = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)
        self.body_color = body_color

    def draw(self):  # Определяет, как объект будет отрисовываться на экране.
        pass


class Apple(GameObject):
    def __init__(self):  # Инициализирует яблоко со случайной позицией.
        self.randomize_position()
        super().__init__(APPLE_COLOR)

    def randomize_position(self):  # Устанавливает начальную позицию яблока.
        x = randint(0, GRID_WIDTH - 1) * GRID_SIZE
        y = randint(0, GRID_HEIGHT - 1) * GRID_SIZE
        self.position = (x, y)

    def draw(self):  # Отрисовывает яблоко на игровой поверхности.
        apple_rectangle = pygame.Rect(self.position, (GRID_SIZE, GRID_SIZE))
        pygame.draw.rect(screen, self.body_color, apple_rectangle)
        pygame.draw.rect(screen, BORDER_COLOR, apple_rectangle, 1)


class Snake(GameObject):
    def __init__(self):  # Инициализирует змейку с начальными параметрами.
        super().__init__(SNAKE_COLOR)
        self.reset()

    def reset(self):  # Сбрасывает змейку в начальное состояние.
        self.length = 1
        self.positions = [(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)]
        self.direction = RIGHT
        self.next_direction = None
        self.last = None

    def update_direction(self):  # Обновляет направление движения змейки.
        if self.next_direction:
            self.direction = self.next_direction
            self.next_direction = None

    def get_head_position(self):  # Возвращает позицию головы змейки.
        return self.positions[0]

    def move(self):  # Обновляет позицию змейки.
        head_x, head_y = self.get_head_position()
        dir_x, dir_y = self.direction
        new_x = (head_x + dir_x * GRID_SIZE) % SCREEN_WIDTH
        new_y = (head_y + dir_y * GRID_SIZE) % SCREEN_HEIGHT
        new_position = (new_x, new_y)

        self.last = self.positions[-1] if len(self.positions) > 1 else None

        self.positions.insert(0, new_position)

        if len(self.positions) > self.length:
            self.positions.pop()

    def draw(self):  # Отрисовывает змейку на экране, затирая след.
        for position in self.positions[:-1]:
            snake_rectangle = pygame.Rect(position, (GRID_SIZE, GRID_SIZE))
            pygame.draw.rect(screen, self.body_color, snake_rectangle)
            pygame.draw.rect(screen, BORDER_COLOR, snake_rectangle, 1)

        snake_head_rectangle = pygame.Rect(self.positions[0], 
                                           (GRID_SIZE, GRID_SIZE))
        pygame.draw.rect(screen, self.body_color, snake_head_rectangle)
        pygame.draw.rect(screen, BORDER_COLOR, snake_head_rectangle, 1)

        if self.last:
            last_snale_rectangle = pygame.Rect(self.last, 
                                               (GRID_SIZE, GRID_SIZE))
            pygame.draw.rect(screen, BOARD_BACKGROUND_COLOR, 
                             last_snale_rectangle)


# Функция обработки действий пользователя:
def handle_keys(game_object):
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            raise SystemExit
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP and game_object.direction != DOWN:
                game_object.next_direction = UP
            elif event.key == pygame.K_DOWN and game_object.direction != UP:
                game_object.next_direction = DOWN
            elif event.key == pygame.K_LEFT and game_object.direction != RIGHT:
                game_object.next_direction = LEFT
            elif event.key == pygame.K_RIGHT and game_object.direction != LEFT:
                game_object.next_direction = RIGHT


def main():
    # Инициализация PyGame:
    pygame.init()
    # Экземпляры классов:
    snake = Snake()
    apple = Apple()

    while True:
        clock.tick(SPEED)

        # Основная логика игры:
        handle_keys(snake)  # Обработка события клавиш.

        snake.update_direction()  # Обновление направления движения змейки.

        snake.move()  # Перемещение змейки.

        # Проверка, съела ли змейка яблоко:
        if snake.get_head_position() == apple.position:
            snake.length += 1
            apple.randomize_position()

            while apple.position in snake.positions:
                apple.randomize_position()

        # Проверка столкновения змейки с собой:
        if snake.get_head_position() in snake.positions[1:]:
            snake.reset()
            apple.randomize_position()

        # Отрисовка игрового поля:
        screen.fill(BOARD_BACKGROUND_COLOR)
        # Отрисовка змейки и яблока:
        apple.draw()
        snake.draw()

        pygame.display.update()  # Обновление экрана.


if __name__ == "__main__":
    main()
