import pygame, sys


CELL_SIZE, CELL_NUMBER = 100, 8


class Cell:
    def __init__(self, x, y, screen, color):
        self.x = x
        self.y = y
        self.screen = screen
        self.color = color

    def draw(self):
        if self.color == 0:
            obj = pygame.Rect(int(self.x * CELL_SIZE), int(self.y * CELL_SIZE), CELL_SIZE, CELL_SIZE)
            pygame.draw.rect(self.screen, (255, 255, 255), obj)
        elif self.color == 1:
            obj = pygame.Rect(int(self.x * CELL_SIZE), int(self.y * CELL_SIZE), CELL_SIZE, CELL_SIZE)
            pygame.draw.rect(self.screen, (0, 0, 0), obj)


class MainController:
    def __init__(self, screen):
        self.screen = screen
        self.grid = []
        self.spawn_grid()

    def spawn_grid(self):
        number_of_color_sequence = ()
        counter = 0
        row_counter = -1
        bool_ = None
        r = range(CELL_NUMBER)
        for _ in r:
            self.grid.append([])
        for y in r:
            row_counter += 1
            if int(row_counter/2) == float(row_counter/2):
                print(row_counter/2)
                counter = 0
                number_of_color_sequence = (0, 1)
                bool_ = True
            elif int(row_counter/2) != float(row_counter/2):
                print(row_counter/2)
                number_of_color_sequence = (1, 0)
                counter = 2
                bool_ = False
            for x in r:
                if bool_:
                    counter += 1
                    if counter == 2:
                        counter = 0
                    print(counter)
                else:
                    counter -= 1
                    if counter == -1:
                        counter = 1
                    print(counter)

                self.grid[y].append(Cell(x, y, self.screen, number_of_color_sequence[counter]))

    def update(self):
        self.draw()

    def draw(self):
        for row in self.grid:
            for block in row:
                block.draw()


def main():
    screen = pygame.display.set_mode((CELL_SIZE * CELL_NUMBER, CELL_SIZE * CELL_NUMBER))
    fpsClock = pygame.time.Clock()
    main_controller = MainController(screen)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                pass

        screen.fill((255, 255, 255))
        main_controller.update()
        pygame.display.update()
        fpsClock.tick(10)


if __name__ == '__main__':
    main()

