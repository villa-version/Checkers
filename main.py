import pygame, sys

CELL_SIZE, CELL_NUMBER = 100, 8


class Cell:
    def __init__(self, x, y, screen, color, size_of_borders, occupied):
        self.x = x
        self.y = y
        self.screen = screen
        self.color = color
        self.last_color = color
        self.size_of_borders = size_of_borders
        self.occupied = occupied

    def draw(self):
        if self.color == 0:
            obj = pygame.Rect(int(self.x * CELL_SIZE), int(self.y * CELL_SIZE), CELL_SIZE, CELL_SIZE)
            pygame.draw.rect(self.screen, (0, 255, 0), obj)
            obj = pygame.Rect(int(self.x * CELL_SIZE), int(self.y * CELL_SIZE),
                              CELL_SIZE - self.size_of_borders,
                              CELL_SIZE - self.size_of_borders)
            pygame.draw.rect(self.screen, (255, 255, 255), obj)
        elif self.color == 1:
            obj = pygame.Rect(int(self.x * CELL_SIZE), int(self.y * CELL_SIZE), CELL_SIZE, CELL_SIZE)
            pygame.draw.rect(self.screen, (0, 255, 0), obj)
            obj = pygame.Rect(int(self.x * CELL_SIZE), int(self.y * CELL_SIZE),
                              CELL_SIZE - self.size_of_borders,
                              CELL_SIZE - self.size_of_borders)
            pygame.draw.rect(self.screen, (0, 0, 0), obj)
        elif self.color == 2:
            self.color = self.last_color
            obj = pygame.Rect(int(self.x * CELL_SIZE), int(self.y * CELL_SIZE),
                              CELL_SIZE,
                              CELL_SIZE)
            pygame.draw.rect(self.screen, (0, 255, 0), obj)
        self.size_of_borders = 0


class Checker:
    def __init__(self, x, y, screen, side_of_the_team):
        self.x = x
        self.y = y
        self.screen = screen
        self.side_of_the_team = side_of_the_team

    def draw(self):
        if self.side_of_the_team == 'WHITE':
            pygame.draw.circle(self.screen, (255, 255, 200),
                            (int((self.x + 0.5) * CELL_SIZE), int((self.y + 0.5) * CELL_SIZE)), 50)
        elif self.side_of_the_team == 'BLACK':
            pygame.draw.circle(self.screen, (218, 160, 109),
                               (int((self.x + 0.5) * CELL_SIZE), int((self.y + 0.5) * CELL_SIZE)), 50)

    def pressed(self, mx, my):
        return self.x * CELL_SIZE < mx < (self.x + 1) * CELL_SIZE and self.y * CELL_SIZE < my < (self.y + 1) * CELL_SIZE

    def move_by_dir(self, direction, grid, prog):
        if prog:
            if direction == 'LEFT':
                if self.x != 0 and self.y != CELL_NUMBER - 1:
                    if grid[self.y + 1][self.x - 1].occupied is None:
                        grid[self.y][self.x].occupied = None
                        self.x, self.y = grid[self.y + 1][self.x - 1].x, grid[self.y + 1][self.x - 1].y
                        return True
            elif direction == 'RIGHT':
                if self.x != CELL_NUMBER-1 and self.y != CELL_NUMBER - 1:
                    if grid[self.y + 1][self.x + 1].occupied is None:
                        grid[self.y][self.x].occupied = None
                        self.x, self.y = grid[self.y + 1][self.x + 1].x, grid[self.y + 1][self.x + 1].y
                        return True
                return False
        elif not prog:
            if direction == 'LEFT':
                if self.x != 0 and self.y != 0:
                    if grid[self.y - 1][self.x - 1].occupied is None:
                        grid[self.y][self.x].occupied = None
                        self.x, self.y = grid[self.y - 1][self.x - 1].x, grid[self.y - 1][self.x - 1].y
                        return True
            elif direction == 'RIGHT':
                if self.x != CELL_NUMBER - 1 and self.y != 0:
                    if grid[self.y - 1][self.x + 1].occupied is None:
                        grid[self.y][self.x].occupied = None
                        self.x, self.y = grid[self.y - 1][self.x + 1].x, grid[self.y - 1][self.x + 1].y
                        return True
                return False


class MainController:
    def __init__(self, screen):
        self.screen = screen
        self.grid = []
        self.spawn_grid()
        self.checkers = [[], []]  # black and white
        self.spawn_checkers()
        self.dir = None
        self.pressed_on_a_checker = None
        self.progress = True

    def spawn_checkers(self):
        white_indent = [1, 0, 1]
        black_indent = [0, 1, 0]
        # WHITE TEAM
        for j in range(len(white_indent)):
            for i in range(white_indent[j], 8, 2):
                self.checkers[0].append(Checker(1 * i, j, self.screen, 'WHITE'))

        # BLACK TEAM
        for j in range(len(black_indent)):
            for i in range(black_indent[j], 8, 2):
                self.checkers[1].append(Checker(1 * i, CELL_NUMBER - 1 - j, self.screen, 'BLACK'))

    def spawn_grid(self):
        number_of_color_sequence = ()
        counter = 0
        row_counter = -1
        state_color_sequence = None
        r = range(CELL_NUMBER)
        for _ in r:
            self.grid.append([])
        for y in r:
            row_counter += 1
            if int(row_counter / 2) == float(row_counter / 2):
                counter = 2
                number_of_color_sequence = (1, 0)
                state_color_sequence = False
            elif int(row_counter / 2) != float(row_counter / 2):
                number_of_color_sequence = (0, 1)
                counter = 0
                state_color_sequence = True
            for x in r:
                if state_color_sequence:
                    counter += 1
                    if counter == 2:
                        counter = 0
                else:
                    counter -= 1
                    if counter == -1:
                        counter = 1

                self.grid[y].append(Cell(x, y, self.screen, number_of_color_sequence[counter], 0, None))

    def update(self):
        self.add_info_of_occupied_blocks()
        self.draw()
        self.check_ways_to_beat_enemy()
        self.move()

    def add_info_of_occupied_blocks(self):
        for team in self.checkers:
            for checker in team:
                self.grid[checker.y][checker.x].occupied = checker.side_of_the_team

    def check_ways_to_beat_enemy(self):
        try:
            if self.progress:
                if self.dir == 'LEFT':
                    if 3 <= self.pressed_on_a_checker.x:
                        if (self.grid[self.pressed_on_a_checker.y + 1][
                            self.pressed_on_a_checker.x - 1].occupied == 'BLACK' and
                                self.grid[self.pressed_on_a_checker.y + 2][
                                    self.pressed_on_a_checker.x - 2].occupied is None):
                            print(1)
                elif self.dir == 'RIGHT':
                    if self.pressed_on_a_checker.y <= CELL_NUMBER - 3:
                        if (self.grid[self.pressed_on_a_checker.y + 1][
                            self.pressed_on_a_checker.x + 1].occupied == 'BLACK' and
                                self.grid[self.pressed_on_a_checker.y + 2][
                                    self.pressed_on_a_checker.x + 2].occupied is None):
                            print(2)

            elif not self.progress:
                pass
        except AttributeError:
            pass

    def draw(self):
        for row in self.grid:
            for block in row:
                block.draw()
        for team in self.checkers:
            for checker in team:
                checker.draw()

    def check_neighbors(self, checker):
        if checker.x == 0:
            return 'LEFT'
        elif checker.x == CELL_NUMBER - 1:
            return 'RIGHT'
        else:
            return 'LEFT-RIGHT'

    def move(self):
        try:
            if self.pressed_on_a_checker.move_by_dir(self.dir, self.grid, self.progress):
                self.dir = 'NOTHING'
                self.pressed_on_a_checker = None
                self.progress = not self.progress
        except AttributeError:
            pass

    def excretion(self):
        if self.progress:
            for checker in self.checkers[0]:
                mx, my = pygame.mouse.get_pos()
                bx, by = checker.x, checker.y
                if checker.pressed(mx, my):
                    self.pressed_on_a_checker = checker
                    self.grid[by][bx].size_of_borders = 5
                    if self.check_neighbors(checker) == 'LEFT-RIGHT':
                        self.grid[checker.y + 1][checker.x + 1].color = 2
                        self.grid[checker.y + 1][checker.x - 1].color = 2
                    elif self.check_neighbors(checker) == 'LEFT':
                        self.grid[checker.y + 1][checker.x + 1].color = 2
                    elif self.check_neighbors(checker) == 'RIGHT':
                        self.grid[checker.y + 1][checker.x - 1].color = 2

        elif not self.progress:
            for checker in self.checkers[1]:
                mx, my = pygame.mouse.get_pos()
                bx, by = checker.x, checker.y
                if checker.pressed(mx, my):
                    self.pressed_on_a_checker = checker
                    self.grid[by][bx].size_of_borders = 5
                    if self.check_neighbors(checker) == 'LEFT-RIGHT':
                        self.grid[checker.y - 1][checker.x + 1].color = 2
                        self.grid[checker.y - 1][checker.x - 1].color = 2
                    elif self.check_neighbors(checker) == 'LEFT':
                        self.grid[checker.y - 1][checker.x + 1].color = 2
                    elif self.check_neighbors(checker) == 'RIGHT':
                        self.grid[checker.y - 1][checker.x - 1].color = 2


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
                main_controller.excretion()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_a:
                    main_controller.dir = 'LEFT'
                elif event.key == pygame.K_d:
                    main_controller.dir = 'RIGHT'
                else:
                    main_controller.dir = 'NOTHING'

        screen.fill((255, 255, 255))
        main_controller.update()
        pygame.display.update()
        fpsClock.tick(10)


if __name__ == '__main__':
    main()
