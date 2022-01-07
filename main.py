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
            obj = pygame.Rect(int(self.x * CELL_SIZE), int(self.y * CELL_SIZE),
                              CELL_SIZE,
                              CELL_SIZE)
            pygame.draw.rect(self.screen, (0, 255, 0), obj)
        elif self.color == 3:
            obj = pygame.Rect(int(self.x * CELL_SIZE), int(self.y * CELL_SIZE),
                              CELL_SIZE,
                              CELL_SIZE)
            pygame.draw.rect(self.screen, (255, 0, 0), obj)
        self.size_of_borders = 0


class Checker:
    def __init__(self, x, y, screen, side_of_the_team):
        self.x = x
        self.y = y
        self.screen = screen
        self.side_of_the_team = side_of_the_team
        self.beat_state = False
        self.beat_dir = None

    def draw(self):
        if self.side_of_the_team == 'WHITE':
            pygame.draw.circle(self.screen, (255, 255, 200),
                               (int((self.x + 0.5) * CELL_SIZE), int((self.y + 0.5) * CELL_SIZE)), 50)
        elif self.side_of_the_team == 'BLACK':
            pygame.draw.circle(self.screen, (218, 160, 109),
                               (int((self.x + 0.5) * CELL_SIZE), int((self.y + 0.5) * CELL_SIZE)), 50)

    def pressed(self, mx, my):
        return self.x * CELL_SIZE < mx < (self.x + 1) * CELL_SIZE and self.y * CELL_SIZE < my < (self.y + 1) * CELL_SIZE

    def move_by_dir(self, grid, progress, last_area_to_move, last_pressed_checker):
        if progress:
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
        else:
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
        self.last_block = []

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
        self.beat_an_enemy()
        self.check_win()
        self.draw()
        self.move()

    def add_info_of_occupied_blocks(self):
        for team in self.checkers:
            for checker in team:
                self.grid[checker.y][checker.x].occupied = checker

    def beat_an_enemy(self):
        if self.progress:
            dist_array_x = (2, -2)
            dist_array_y = (2, -2)
            for x in dist_array_x:
                for y in dist_array_y:
                    if self.last_pressed_checker is not None:
                        if self.last_pressed_checker.x <= 2:
                            x = 2
                        elif self.last_pressed_checker.x >= CELL_NUMBER - 2:
                            x = -2
                        if self.last_pressed_checker.y <= 2:
                            y = 2
                        elif self.last_pressed_checker.y >= CELL_NUMBER - 2:
                            y = -2
                        dx = x + 1 if x == -2 else x - 1
                        dy = y + 1 if y == -2 else y - 1
                        if self.сheck_out_ways_to_beat(dx, dy, x, y):
                            if self.last_area_to_move is not None:
                                dist_x = self.last_area_to_move.x - self.last_pressed_checker.x
                                dist_y = self.last_area_to_move.y - self.last_pressed_checker.y
                                if x == dist_x and y == dist_y:
                                    self.progress = not self.progress
                                    self.score_white_team += 5
                                    self.checkers[1].remove(self.grid[self.last_pressed_checker.y +
                                                                      dy]
                                                            [self.last_pressed_checker.x +
                                                             dx].occupied)
                                    self.last_pressed_checker.x, self.last_pressed_checker.y = \
                                        (self.last_pressed_checker.x + x,
                                         self.last_pressed_checker.y + y)
                                    self.grid[self.last_pressed_checker.y - y
                                              ][self.last_pressed_checker.x - x].occupied = None
                                    self.grid[self.last_pressed_checker.y - dy
                                              ][self.last_pressed_checker.x - dx].occupied = None
                                    self.last_pressed_checker.beat_state = False
                                    self.last_pressed_checker.beat_dir = []
                                    self.last_pressed_checker = None
                                    self.last_area_to_move = None
        else:
            dist_array_x = (2, -2)
            dist_array_y = (2, -2)
            for x in dist_array_x:
                for y in dist_array_y:
                    if self.last_pressed_checker is not None:
                        if self.last_pressed_checker.x <= 2:
                            x = 2
                        elif self.last_pressed_checker.x >= CELL_NUMBER - 2:
                            x = -2
                        if self.last_pressed_checker.y <= 2:
                            y = 2
                        elif self.last_pressed_checker.y >= CELL_NUMBER - 2:
                            y = -2
                        dx = x + 1 if x == -2 else x - 1
                        dy = y + 1 if y == -2 else y - 1
                        if self.сheck_out_ways_to_beat(dx, dy, x, y):
                            if self.last_area_to_move is not None:
                                dist_x = self.last_area_to_move.x - self.last_pressed_checker.x
                                dist_y = self.last_area_to_move.y - self.last_pressed_checker.y
                                if x == dist_x and y == dist_y:
                                    self.progress = not self.progress
                                    self.score_white_team += 5
                                    self.checkers[0].remove(self.grid[self.last_pressed_checker.y +
                                                                      dy]
                                                            [self.last_pressed_checker.x +
                                                             dx].occupied)
                                    self.last_pressed_checker.x, self.last_pressed_checker.y = \
                                        (self.last_pressed_checker.x + x,
                                         self.last_pressed_checker.y + y)
                                    self.grid[self.last_pressed_checker.y - y
                                              ][self.last_pressed_checker.x - x].occupied = None
                                    self.grid[self.last_pressed_checker.y - dy
                                              ][self.last_pressed_checker.x - dx].occupied = None
                                    self.last_pressed_checker.beat_state = False
                                    self.last_pressed_checker.beat_dir = []
                                    self.last_pressed_checker = None
                                    self.last_area_to_move = None

    def сheck_out_ways_to_beat(self, dist_to_the_occupied_block_x, dist_to_the_occupied_block_y, dist_x, dist_y):
        dir_x = ['RIGHT', 'LEFT']
        dir_y = ['UP', 'DOWN']
        if self.progress:
            if dist_x == -2:
                ind_for_dir_x = 0
            else:
                ind_for_dir_x = 1
            if dist_x == -2:
                ind_for_dir_y = 0
            else:
                ind_for_dir_y = 1
            middle_dist_x = self.last_pressed_checker.x + dist_to_the_occupied_block_x
            middle_dist_y = self.last_pressed_checker.y + dist_to_the_occupied_block_y
            full_dist_x = self.last_pressed_checker.x + dist_x
            full_dist_y = self.last_pressed_checker.y + dist_y
            occupied_block = self.grid[full_dist_y][full_dist_x].occupied
            if self.grid[middle_dist_y][middle_dist_x].occupied is not None:
                side_of_the_team = self.grid[middle_dist_y][middle_dist_x].occupied.side_of_the_team
                if side_of_the_team == 'BLACK' and occupied_block is None:
                    self.last_pressed_checker.beat_state = True
                    self.last_pressed_checker.beat_dir = [(dir_x[ind_for_dir_x], dir_y[ind_for_dir_y]), (dist_x, dist_y)]
                    return True
            return False
        else:
            if dist_x == -2:
                ind_for_dir_x = 0
            else:
                ind_for_dir_x = 1
            if dist_x == -2:
                ind_for_dir_y = 0
            else:
                ind_for_dir_y = 1
            middle_dist_x = self.last_pressed_checker.x + dist_to_the_occupied_block_x
            middle_dist_y = self.last_pressed_checker.y + dist_to_the_occupied_block_y
            full_dist_x = self.last_pressed_checker.x + dist_x
            full_dist_y = self.last_pressed_checker.y + dist_y
            if self.grid[middle_dist_y][middle_dist_x].occupied is not None:
                side_of_the_team = self.grid[middle_dist_y][middle_dist_x].occupied.side_of_the_team
                occupied_block = self.grid[full_dist_y][full_dist_x].occupied
                if side_of_the_team == 'WHITE' and occupied_block is None:
                    self.last_pressed_checker.beat_state = True
                    self.last_pressed_checker.beat_dir = [(dir_x[ind_for_dir_x], dir_y[ind_for_dir_y]), (dist_x, dist_y)]
                    return True
            return False

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
                    if self.last_block:
                        if not self.last_pressed_checker.beat_state:
                            if len(self.last_block) == 1:
                                self.last_block[0].color = self.last_block[0].last_color
                                self.last_block = []
                            else:
                                self.last_block[0].color = self.last_block[0].last_color
                                self.last_block[1].color = self.last_block[1].last_color
                                self.last_block = []
                        else:
                            for i in range(len(self.last_block)):
                                self.last_block[i].color = self.last_block[i].last_color
                            self.last_block = []
                    if not self.last_pressed_checker.beat_state:
                        if self.check_ways(checker, self.progress) == 'LEFT-RIGHT-DOWN':
                            self.last_block.append(self.grid[checker.y + 1][checker.x + 1])
                            self.last_block.append(self.grid[checker.y + 1][checker.x - 1])
                            self.grid[checker.y + 1][checker.x + 1].color = 2
                            self.grid[checker.y + 1][checker.x - 1].color = 2
                        elif self.check_ways(checker, self.progress) == 'LEFT-DOWN':
                            self.last_block.append(self.grid[checker.y + 1][checker.x + 1])
                            self.grid[checker.y + 1][checker.x + 1].color = 2
                        elif self.check_ways(checker, self.progress) == 'RIGHT-DOWN':
                            self.last_block.append(self.grid[checker.y + 1][checker.x - 1])
                            self.grid[checker.y + 1][checker.x - 1].color = 2
                    else:
                        if self.last_pressed_checker.beat_dir[1][0] == -2:
                            dist_to_the_occupied_block_x = self.last_pressed_checker.beat_dir[1][0] + 1
                        else:
                            dist_to_the_occupied_block_x = self.last_pressed_checker.beat_dir[1][0] - 1
                        if self.last_pressed_checker.beat_dir[1][1] == -2:
                            dist_to_the_occupied_block_y = self.last_pressed_checker.beat_dir[1][1] + 1
                        else:
                            dist_to_the_occupied_block_y = self.last_pressed_checker.beat_dir[1][1] - 1
                        self.last_block.append(self.grid[checker.y][checker.x])
                        self.last_block.append(self.grid[checker.y + dist_to_the_occupied_block_y]
                                                        [checker.x + dist_to_the_occupied_block_x])
                        self.last_block.append(self.grid[checker.y + self.last_pressed_checker.beat_dir[1][1]][
                                                         checker.x + self.last_pressed_checker.beat_dir[1][0]])
                        self.grid[checker.y][checker.x].color = 2
                        self.grid[checker.y + dist_to_the_occupied_block_y][
                                  checker.x + dist_to_the_occupied_block_x].color = 3
                        self.grid[checker.y + self.last_pressed_checker.beat_dir[1][1]][checker.x + self.last_pressed_checker.beat_dir[1][0]].color = 2
        else:
            for checker in self.checkers[1]:
                mx, my = pygame.mouse.get_pos()
                bx, by = checker.x, checker.y
                if checker.pressed(mx, my):
                    if self.last_block:
                        self.last_pressed_checker = checker
                        self.grid[by][bx].size_of_borders = 5
                        if len(self.last_block) == 1:
                            self.last_block[0].color = self.last_block[0].last_color
                            self.last_block = []
                        else:
                            self.last_block[0].color = self.last_block[0].last_color
                            self.last_block[1].color = self.last_block[1].last_color
                            self.last_block = []
                    if not self.last_pressed_checker.beat_state:
                        if self.check_ways(checker, self.progress) == 'LEFT-RIGHT-UP':
                            self.last_block.append(self.grid[checker.y - 1][checker.x + 1])
                            self.last_block.append(self.grid[checker.y - 1][checker.x - 1])
                            self.grid[checker.y - 1][checker.x + 1].color = 2
                            self.grid[checker.y - 1][checker.x - 1].color = 2
                        elif self.check_ways(checker, self.progress) == 'LEFT-UP':
                            self.last_block.append(self.grid[checker.y - 1][checker.x + 1])
                            self.grid[checker.y - 1][checker.x + 1].color = 2
                        elif self.check_ways(checker, self.progress) == 'RIGHT-UP':
                            self.last_block.append(self.grid[checker.y - 1][checker.x - 1])
                            self.grid[checker.y - 1][checker.x - 1].color = 2
                    else:
                        if self.last_pressed_checker.beat_dir[1][0] == -2:
                            dist_to_the_occupied_block_x = self.last_pressed_checker.beat_dir[1][0] + 1
                        else:
                            dist_to_the_occupied_block_x = self.last_pressed_checker.beat_dir[1][0] - 1
                        if self.last_pressed_checker.beat_dir[1][1] == -2:
                            dist_to_the_occupied_block_y = self.last_pressed_checker.beat_dir[1][1] + 1
                        else:
                            dist_to_the_occupied_block_y = self.last_pressed_checker.beat_dir[1][1] - 1
                        self.last_block.append(self.grid[checker.y][checker.x])
                        self.last_block.append(self.grid[checker.y + dist_to_the_occupied_block_y]
                                                        [checker.x + dist_to_the_occupied_block_x])
                        self.last_block.append(self.grid[checker.y + self.last_pressed_checker.beat_dir[1][1]][
                                                         checker.x + self.last_pressed_checker.beat_dir[1][0]])
                        self.grid[checker.y][checker.x].color = 2
                        self.grid[checker.y + dist_to_the_occupied_block_y][
                                  checker.x + dist_to_the_occupied_block_x].color = 3
                        self.grid[checker.y + self.last_pressed_checker.beat_dir[1][1]][checker.x + self.last_pressed_checker.beat_dir[1][0]].color = 2


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
