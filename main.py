import pygame
import random

from classes.Board import Board
from classes.Square import Square
from classes.Knight import Knight
from classes.Pawn import Pawn

pygame.init()

knight = pygame.image.load('knight.png')
width, height = 800, 800
screen = pygame.display.set_mode((width + 200, height))
pygame.display.set_caption("Skoczek Szachowy")
pygame.display.set_icon(knight)


board = Board(width,height)
running = True
clock = pygame.time.Clock()
searching = False
knight_pos = None
next_move = 0

def are_all_squares_filled(board):
    for square in board.squares:
        if not square.highlight and not square.occupying_piece:
            return False
    return True

def are_squares_filled(board):
    count = 0
    for square in board.squares:
        if not square.highlight and not square.occupying_piece:
            count += 1
    if count >= 5:
        return False
    else:
        return True

visited_squares = []
banned_routes = []
imagined_visited_squares = []
counter = 0


while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if 800 < event.pos[0] < 1000 and 0 < event.pos[1] < 100:
                if not searching:
                    searching = True
                    if knight_pos is None:
                        knight_pos = board.knight.pos
                        visited_squares.append(knight_pos)  # Dodaj pole początkowe do odwiedzonych

    if searching:
        # Warnsdorff's algorythm with Backtracking
        def get_valid_moves(pos):
            moves = []
            for dx, dy in [(-1, -2), (-2, -1), (-2, 1), (-1, 2), (1, -2), (2, -1), (2, 1), (1, 2)]:
                new_x, new_y = pos[0] + dx, pos[1] + dy
                point = new_x, new_y
                imagined_visited_squares = visited_squares.copy()
                imagined_visited_squares.append(point)
                if 0 <= new_x < 8 and 0 <= new_y < 8 and \
                    (new_x, new_y) not in visited_squares and \
                    board.get_piece_from_position((new_x, new_y)) is False:
                        if all(route != imagined_visited_squares for route in banned_routes):
                            moves.append((new_x, new_y))
            return moves

        if knight_pos is not None:
            # searching for possible moves and highlighting current position
            board.get_square_from_pos(knight_pos).highlight = True  # Zaznacz obecną pozycję
            possible_moves = get_valid_moves(knight_pos)

            # 3 possibilities of the end of program
            if not possible_moves and are_all_squares_filled(board) != False:
                searching = False  # Brak możliwych ruchów, kończ wyszukiwanie
                print('Nie ma rozwiązania')
                print(f'Droga pokonana przez skoczka: {visited_squares}')
                print(f'Skoczek pokrył {len(visited_squares)} z 52 potrzebnych pól')
            # additional functionality
            elif not possible_moves and are_squares_filled(board) != False:
                print('Koniec szukania, najlepszy wynik ')
                print(f'Droga pokonana przez skoczka: {visited_squares}')
                print(f'Skoczek pokrył {len(visited_squares)} z 52 potrzebnych pól')
            elif are_all_squares_filled(board):
                searching = False  # Wszystkie pola są zajęte, kończ wyszukiwanie
                print('Wszystkie pola są zajęte, udało się')
                print(f'Droga pokonana przez skoczka: {visited_squares}')
                print(f'Skoczek pokrył {len(visited_squares)} z 52 potrzebnych pól')
            else:
                if possible_moves:
                    # Choosing next step with Warnsdorff's algorythm
                    next_move = min(possible_moves, key=lambda pos: len(get_valid_moves(pos)))
                    knight_pos = next_move
                    visited_squares.append(next_move)
                    board.get_square_from_pos(visited_squares[-1]).highlight = False
                else:
                    # Wrong path, going back + current track getting on the banned list
                    counter += 1
                    board.get_square_from_pos(knight_pos).highlight = False
                    board.get_square_from_pos(visited_squares[-1]).highlight = False
                    banned_routes.append(visited_squares.copy())
                    visited_squares.pop()
                    next_move = visited_squares[-1]
                    knight_pos = next_move



    #drawing/updating board
    screen.fill((132,118,118))
    board.draw(screen, next_move)
    pygame.time.delay(1)


    # right side pannel
    button_color = (0, 255, 0) if not searching else (255, 0, 0)
    pygame.draw.rect(screen, button_color, pygame.Rect(820, 40, 160, 60), border_radius=10)
    button_text = "Start Search" if not searching else "Stop Search"
    font = pygame.font.Font(None, 36)
    text_surface = font.render(button_text, True, (0, 0, 0))
    text_rect = text_surface.get_rect(center=(900, 70))
    screen.blit(text_surface, text_rect)
    pygame.display.flip()
    clock.tick(60)

pygame.quit()
