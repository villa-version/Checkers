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

    def move_by_dir(self, grid, prog, last_area_to_move, last_pressed_checker):
        if prog:
            if (last_area_to_move.x - last_pressed_checker.x == 1 and
                    last_area_to_move.y - last_pressed_checker.y == 1):
                if self.x != CELL_NUMBER - 1 and self.y != CELL_NUMBER - 1:
                    if last_area_to_move.occupied is None:
                        grid[self.y][self.x].occupied = None
                        self.x, self.y = last_area_to_move.x, last_area_to_move.y
                        return True
            elif (last_area_to_move.x - last_pressed_checker.x == -1 and
                  last_area_to_move.y - last_pressed_checker.y == 1):
                if self.x != 0 and self.y != CELL_NUMBER - 1:
                    if last_area_to_move.occupied is None:
                        grid[self.y][self.x].occupied = None
                        self.x, self.y = last_area_to_move.x, last_area_to_move.y
                        return True
                return False
        elif not prog:
            if (last_area_to_move.x - last_pressed_checker.x == -1 and
                    last_area_to_move.y - last_pressed_checker.y == -1):
                if self.x != 0 and self.y != 0:
                    if last_area_to_move.occupied is None:
                        grid[self.y][self.x].occupied = None
                        self.x, self.y = last_area_to_move.x, last_area_to_move.y
                        return True
            elif (last_area_to_move.x - last_pressed_checker.x == 1 and
                  last_area_to_move.y - last_pressed_checker.y == -1):
                if self.x != CELL_NUMBER - 1 and self.y != 0:
                    if last_area_to_move.occupied is None:
                        grid[self.y][self.x].occupied = None
                        self.x, self.y = last_area_to_move.x, last_area_to_move.y
                        return True
                return False


class MainController:

    def __init__(self, screen):
        self.screen = screen
        self.grid = []
        self.spawn_grid()
        self.checkers = [[], []]  # black and white
        self.spawn_checkers()
        self.last_pressed_checker = None
        self.last_area_to_move = None
        self.progress = True
        self.score_white_team = 0
        self.score_black_team = 0
        self.text_score_teams = pygame.font.Font(None, 48)

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
        self.check_win()
        self.draw()
        self.move()
        self.check_ways_to_beat_enemy()

    def add_info_of_occupied_blocks(self):
        for team in self.checkers:
            for checker in team:
                self.grid[checker.y][checker.x].occupied = checker

    def check_ways_to_beat_enemy(self):
        try:
            if self.progress:
                dist_array_x, dist_array_y = (2, -2), (2, -2)
                for i in range(len(dist_array_x)):
                    for j in range(len(dist_array_y)):
                        if (self.last_area_to_move.x - self.last_pressed_checker.x == dist_array_x[i] and
                                self.last_area_to_move.y - self.last_pressed_checker.y == dist_array_y[j]):

                            if dist_array_x[i] == -2:
                                dist_to_the_occupied_block_x = dist_array_x[i] + 1
                            else:
                                dist_to_the_occupied_block_x = dist_array_x[i] - 1
                            if dist_array_y[j] == -2:
                                dist_to_the_occupied_block_y = dist_array_y[j] + 1
                            else:
                                dist_to_the_occupied_block_y = dist_array_y[j] - 1

                            if (self.grid[self.last_pressed_checker.y + dist_to_the_occupied_block_y][
                                self.last_pressed_checker.x + dist_to_the_occupied_block_x
                                ].occupied.side_of_the_team == 'BLACK' and
                                    self.grid[self.last_pressed_checker.y + dist_array_y[j]][
                                        self.last_pressed_checker.x + dist_array_x[i]].occupied is None):
                                self.progress = not self.progress
                                self.score_white_team += 5
                                self.checkers[1].remove(self.grid[self.last_pressed_checker.y +
                                                                  dist_to_the_occupied_block_y]
                                                        [self.last_pressed_checker.x +
                                                         dist_to_the_occupied_block_x].occupied)
                                self.last_pressed_checker.x, self.last_pressed_checker.y = \
                                                            (self.last_pressed_checker.x + dist_array_x[i],
                                                            self.last_pressed_checker.y + dist_array_y[j])
                                self.grid[self.last_pressed_checker.y - dist_array_y[j]
                                ][self.last_pressed_checker.x - dist_array_x[i]].occupied = None
                                self.grid[self.last_pressed_checker.y - dist_to_the_occupied_block_y
                                ][self.last_pressed_checker.x - dist_to_the_occupied_block_x].occupied = None
                                self.last_pressed_checker = None
                                self.last_area_to_move = None

            elif not self.progress:
                dist_array_x, dist_array_y = (2, -2), (2, -2)
                for i in range(len(dist_array_x)):
                    for j in range(len(dist_array_y)):
                        if (self.last_area_to_move.x - self.last_pressed_checker.x == dist_array_x[i] and
                                self.last_area_to_move.y - self.last_pressed_checker.y == dist_array_y[j]):

                            if dist_array_x[i] == -2:
                                dist_to_the_occupied_block_x = dist_array_x[i] + 1
                            else:
                                dist_to_the_occupied_block_x = dist_array_x[i] - 1
                            if dist_array_y[j] == -2:
                                dist_to_the_occupied_block_y = dist_array_y[j] + 1
                            else:
                                dist_to_the_occupied_block_y = dist_array_y[j] - 1

                            if (self.grid[self.last_pressed_checker.y + dist_to_the_occupied_block_y][
                                self.last_pressed_checker.x + dist_to_the_occupied_block_x
                            ].occupied.side_of_the_team == 'WHITE' and
                                    self.grid[self.last_pressed_checker.y + dist_array_y[j]][
                                        self.last_pressed_checker.x + dist_array_x[i]].occupied is None):
                                self.progress = not self.progress
                                self.score_black_team += 5
                                self.checkers[0].remove(self.grid[self.last_pressed_checker.y +
                                                                  dist_to_the_occupied_block_y]
                                                        [self.last_pressed_checker.x +
                                                         dist_to_the_occupied_block_x].occupied)
                                self.last_pressed_checker.x, self.last_pressed_checker.y = \
                                    (self.last_pressed_checker.x + dist_array_x[i],
                                     self.last_pressed_checker.y + dist_array_y[j])
                                self.grid[self.last_pressed_checker.y - dist_array_y[j]
                                          ][self.last_pressed_checker.x - dist_array_x[i]].occupied = None
                                self.grid[self.last_pressed_checker.y - dist_to_the_occupied_block_y
                                          ][self.last_pressed_checker.x - dist_to_the_occupied_block_x].occupied = None
                                self.last_pressed_checker = None
                                self.last_area_to_move = None
        except AttributeError:
            pass

    def check_win(self):
        if len(self.checkers[0]) == 0:
            print('BLACK TEAM WON')
        elif len(self.checkers[1]) == 0:
            print('WHITE TEAM WON')

    def draw(self):
        for row in self.grid:
            for block in row:
                 block.draw()
        for team in self.checkers:
            for checker in team:
                checker.draw()

        text_score = self.text_score_teams.render(str(self.score_white_team), True, (0, 0, 0))
        self.screen.blit(text_score, (25, 25))
        text_score = self.text_score_teams.render(str(self.score_black_team), True, (0, 0, 0))
        self.screen.blit(text_score, (CELL_NUMBER * CELL_SIZE - 45, CELL_NUMBER * CELL_SIZE - 45))

    @staticmethod
    def check_ways(checker, progress):
        if progress:
            if checker.x == 0:
                if checker.y != CELL_NUMBER - 1:
                    return 'LEFT-DOWN'
            elif checker.x == CELL_NUMBER - 1:
                if checker.y != CELL_NUMBER - 1:
                    return 'RIGHT-DOWN'
            else:
                if checker.y != CELL_NUMBER - 1:
                    return 'LEFT-RIGHT-DOWN'
                else:
                    return None
        else:
            if checker.x == 0:
                if checker.y != CELL_NUMBER - 1:
                    return 'LEFT-UP'
            elif checker.x == CELL_NUMBER - 1:
                if checker.y != CELL_NUMBER - 1:
                    return 'RIGHT-UP'
            else:
                if checker.y != CELL_NUMBER - 1:
                    return 'LEFT-RIGHT-UP'
                else:
                    return None

    def click_to_area(self, mx, my):
        for row in self.grid:
            for block in row:
                if block.occupied is None:
                    if (block.x * CELL_SIZE < mx < (block.x + 1) * CELL_SIZE and
                            block.y * CELL_SIZE < my < (block.y + 1) * CELL_SIZE):
                        self.last_area_to_move = block

    def move(self):
        if self.last_pressed_checker is not None and self.last_area_to_move is not None:
            if self.last_pressed_checker.move_by_dir(self.grid, self.progress, self.last_area_to_move,
                                                     self.last_pressed_checker):
                self.last_area_to_move = None
                self.last_pressed_checker = None
                self.progress = not self.progress

    def excretion(self):
        if self.progress:
            for checker in self.checkers[0]:
                mx, my = pygame.mouse.get_pos()
                bx, by = checker.x, checker.y
                if checker.pressed(mx, my):
                    self.last_pressed_checker = checker
                    self.grid[by][bx].size_of_borders = 5
                    if self.check_ways(checker, self.progress) == 'LEFT-RIGHT-DOWN':
                        self.grid[checker.y + 1][checker.x + 1].color = 2
                        self.grid[checker.y + 1][checker.x - 1].color = 2
                    elif self.check_ways(checker, self.progress) == 'LEFT-DOWN':
                        self.grid[checker.y + 1][checker.x + 1].color = 2
                    elif self.check_ways(checker, self.progress) == 'RIGHT-DOWN':
                        self.grid[checker.y + 1][checker.x - 1].color = 2

        elif not self.progress:
            for checker in self.checkers[1]:
                mx, my = pygame.mouse.get_pos()
                bx, by = checker.x, checker.y
                if checker.pressed(mx, my):
                    self.last_pressed_checker = checker
                    self.grid[by][bx].size_of_borders = 5
                    if self.check_ways(checker, self.progress) == 'LEFT-RIGHT-UP':
                        self.grid[checker.y - 1][checker.x + 1].color = 2
                        self.grid[checker.y - 1][checker.x - 1].color = 2
                    elif self.check_ways(checker, self.progress) == 'LEFT-UP':
                        self.grid[checker.y - 1][checker.x + 1].color = 2
                    elif self.check_ways(checker, self.progress) == 'RIGHT-UP':
                        self.grid[checker.y - 1][checker.x - 1].color = 2


def main():
    project_name = 'Checkers'
    screen = pygame.display.set_mode((CELL_SIZE * CELL_NUMBER, CELL_SIZE * CELL_NUMBER))
    pygame.display.set_caption(project_name)
    pygame.font.init()
    fpsClock = pygame.time.Clock()
    main_controller = MainController(screen)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                main_controller.excretion()
                mx, my = pygame.mouse.get_pos()
                main_controller.click_to_area(mx, my)

        screen.fill((255, 255, 255))
        main_controller.update()
        pygame.display.update()
        fpsClock.tick(10)


if __name__ == '__main__':
    main()
