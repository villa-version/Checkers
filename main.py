import pygame, sys


CELL_SIZE, CELL_NUMBER = 100, 8


class Cell:
    def __init__(self, x, y, screen, color, size_of_borders):
        self.x = x
        self.y = y
        self.screen = screen
        self.color = color
        self.last_color = color
        self.size_of_borders = size_of_borders

    def draw(self):
        if self.color == 0:
            obj = pygame.Rect(int(self.x * CELL_SIZE), int(self.y * CELL_SIZE), CELL_SIZE, CELL_SIZE)
            pygame.draw.rect(self.screen, (255, 0, 255), obj)
            obj = pygame.Rect(int(self.x * CELL_SIZE), int(self.y * CELL_SIZE),
                              CELL_SIZE - self.size_of_borders,
                              CELL_SIZE - self.size_of_borders)
            pygame.draw.rect(self.screen, (255, 255, 255), obj)
        elif self.color == 1:
            obj = pygame.Rect(int(self.x * CELL_SIZE), int(self.y * CELL_SIZE), CELL_SIZE, CELL_SIZE)
            pygame.draw.rect(self.screen, (255, 0, 255), obj)
            obj = pygame.Rect(int(self.x * CELL_SIZE), int(self.y * CELL_SIZE),
                              CELL_SIZE - self.size_of_borders,
                              CELL_SIZE - self.size_of_borders)
            pygame.draw.rect(self.screen, (0, 0, 0), obj)
        elif self.color == 2:
            self.color = self.last_color
            obj = pygame.Rect(int(self.x * CELL_SIZE), int(self.y * CELL_SIZE),
                              CELL_SIZE,
                              CELL_SIZE)
            pygame.draw.rect(self.screen, (255, 0, 255), obj)


class Checker:
    def __init__(self, x, y, screen):
        self.x = x
        self.y = y
        self.screen = screen

    def draw(self):
        pygame.draw.circle(self.screen, (255, 255, 0), (int((self.x + 0.5) * CELL_SIZE), int((self.y + 0.5) * CELL_SIZE)), 50)

    def pressed(self, mx, my):
        if self.x * CELL_SIZE < mx < (self.x + 1) * CELL_SIZE and self.y * CELL_SIZE < my < (self.y + 1) * CELL_SIZE:
            return True
        else:
            return False


class MainController:
    def __init__(self, screen):
        self.screen = screen
        self.grid = []
        self.spawn_grid()
        self.checkers = [[], []]  # black and white
        self.spawn_checkers()
        self.click_state = False

    def spawn_checkers(self):
        for i in range(1, 8, 2):
            self.checkers[0].append(Checker(1*i, 0, self.screen))
        for i in range(0, 8, 2):
            self.checkers[0].append(Checker(1*i, 1, self.screen))
        for i in range(1, 8, 2):
            self.checkers[0].append(Checker(1*i, 2, self.screen))

        for i in range(0, 8, 2):
            self.checkers[1].append(Checker(1*i, CELL_NUMBER-1, self.screen))
        for i in range(1, 8, 2):
            self.checkers[1].append(Checker(1*i, CELL_NUMBER-2, self.screen))
        for i in range(0, 8, 2):
            self.checkers[1].append(Checker(1*i, CELL_NUMBER-3, self.screen))

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
                counter = 2
                number_of_color_sequence = (1, 0)
                bool_ = False
            elif int(row_counter/2) != float(row_counter/2):
                number_of_color_sequence = (0, 1)
                counter = 0
                bool_ = True
            for x in r:
                if bool_:
                    counter += 1
                    if counter == 2:
                        counter = 0
                else:
                    counter -= 1
                    if counter == -1:
                        counter = 1

                self.grid[y].append(Cell(x, y, self.screen, number_of_color_sequence[counter], 0))

    def update(self):
        self.draw()
        self.move()

    def draw(self):
        for row in self.grid:
            for block in row:
                block.draw()
        for team in self.checkers:
            for checker in team:
                checker.draw()

    def chek_neighbors(self, checker):
        if checker.x == 0:
            return 'LEFT'
        elif checker.x == CELL_NUMBER-1:
            return 'RIGHT'
        else:
            return 'LEFT-RIGHT'

    def move(self):
        for team in self.checkers:
            for checker in team:
                mx, my = pygame.mouse.get_pos()
                bx, by = checker.x, checker.y
                if checker.pressed(mx, my):
                    if self.click_state:
                        self.click_state = False
                        self.grid[by][bx].size_of_borders = 5
                        if self.chek_neighbors(checker) == 'LEFT-RIGHT':
                            self.grid[checker.y + 1][checker.x + 1].color = 2
                            self.grid[checker.y + 1][checker.x - 1].color = 2
                        elif self.chek_neighbors(checker) == 'LEFT':
                            self.grid[checker.y + 1][checker.x + 1].color = 2
                        elif self.chek_neighbors(checker) == 'RIGHT':
                            self.grid[checker.y + 1][checker.x - 1].color = 2

                else:
                    self.grid[by][bx].size_of_borders = 0


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
                main_controller.click_state = True

        screen.fill((255, 255, 255))
        main_controller.update()
        pygame.display.update()
        fpsClock.tick(10)


if __name__ == '__main__':
    main()

