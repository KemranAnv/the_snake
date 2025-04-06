from random import choice, randint

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
pygame.display.set_caption('Змейка')

# Настройка времени:
clock = pygame.time.Clock()


# Тут опишите все классы игры.
class GameObject:
    """Базовый класс для игровых объектов."""

    def __init__(self, position=((SCREEN_WIDTH // 2), (SCREEN_HEIGHT // 2))):
        self.position = position
        self.body_color = None

    def draw(self):
        """Абстрактный метод для отрисовки объекта на экране."""
        pass


class Apple(GameObject):
    """Класс, представляющий яблоко в игре."""

    def __init__(self):
        super().__init__()
        self.body_color = APPLE_COLOR  # (255, 0, 0)
        self.randomize_position()

    def randomize_position(self):
        """устанавливает случайное положение яблока"""
        self.position = (
            randint(0, GRID_WIDTH - 1) * GRID_SIZE,
            randint(0, GRID_HEIGHT - 1) * GRID_SIZE
        )

    def draw(self):
        """Отрисовывает яблоко"""
        rect = pygame.Rect(self.position, (GRID_SIZE, GRID_SIZE))
        pygame.draw.rect(screen, self.body_color, rect)
        pygame.draw.rect(screen, BORDER_COLOR, rect, 1)


class Snake(GameObject):
    """описывающий змейку и её поведение."""

    def __init__(self):
        super().__init__()
        self.length = 1
        self.positions = [self.position]
        self.direction = RIGHT
        self.next_direction = None
        self.body_color = SNAKE_COLOR  # (0, 255, 0)
        self.last = None

    def update_direction(self):
        """Обновление направления движения змейки."""
        if self.next_direction:
            self.direction = self.next_direction
            self.next_direction = None

    def move(self):
        """Обновление позиции змейки."""
        head_x, head_y = self.get_head_position()
        dx, dy = self.direction

        # Новая позиция головы с учётом перехода через границы.
        new_x = (head_x + (dx * GRID_SIZE)) % SCREEN_WIDTH
        new_y = (head_y + (dy * GRID_SIZE)) % SCREEN_HEIGHT
        new_head = (new_x, new_y)

        # Проверка столкновения с собой.
        if new_head in self.positions[2:]:
            self.reset()
            return

        self.positions.insert(0, new_head)

        # Сохранение последнего сегмента перед удалением.
        if len(self.positions) > self.length:
            self.last = self.positions.pop()
        else:
            self.last = None

    def draw(self):
        """отрисовывает змейку на экране"""
        for position in self.positions[:-1]:
            rect = (pygame.Rect(position, (GRID_SIZE, GRID_SIZE)))
            pygame.draw.rect(screen, self.body_color, rect)
            pygame.draw.rect(screen, BORDER_COLOR, rect, 1)

        # Отрисовка головы змеи.
        head_rect = pygame.Rect(self.positions[0], (GRID_SIZE, GRID_SIZE))
        pygame.draw.rect(screen, self.body_color, head_rect)
        pygame.draw.rect(screen, BORDER_COLOR, head_rect, 1)

        # Затирание последнего сегмента.
        if self.last:
            last_rect = pygame.Rect(self.last, (GRID_SIZE, GRID_SIZE))
            pygame.draw.rect(screen, BOARD_BACKGROUND_COLOR, last_rect)

    def get_head_position(self):
        """возвращает позицию головы змейки"""
        return self.positions[0]

    def reset(self):
        """сбрасывает змейку после столкновения с собой."""
        self.length = 1
        self.positions = [((SCREEN_WIDTH // 2), (SCREEN_HEIGHT // 2))]
        self.direction = choice([UP, DOWN, LEFT, RIGHT])
        self.next_direction = None
        self.last = None


def handle_keys(game_object):
    """обрабатывает нажатия клавиш"""
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
    """Основной игровой цикл"""
    # Инициализация PyGame:
    pygame.init()

    # Тут нужно создать экземпляры классов.
    snake = Snake()
    apple = Apple()

    while True:
        clock.tick(SPEED)
        # Тут опишите основную логику игры.
        # Обработка событий.
        handle_keys(snake)
        snake.update_direction()
        snake.move()

        # Проверка на съеденное яблоко.
        if snake.get_head_position() == apple.position:
            snake.length += 1
            apple.randomize_position()

        # Отрисовка
        screen.fill(BOARD_BACKGROUND_COLOR)
        snake.draw()
        apple.draw()
        pygame.display.update()


if __name__ == '__main__':
    main()
