import pygame, random

pygame.init()

# Constants
BOARD_WIDTH = 4
BOARD_HEIGHT = 4

DISPLAY_HEIGHT = 600
DISPLAY_WIDTH = 800

FPS = 60
BLANK = None

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
BEIGE = (245, 245, 220)
GREEN = (114, 179, 131)
BRIGHTER_GREEN = (119, 189, 137)
RED = (176, 111, 137)
BRIGHTER_RED = (191, 120, 149)
BLANK_COLOR = (247, 232, 188)
BLUE = (153, 174, 247)

TEXT_COLOR = BLACK
BG_COLOR = BEIGE
BORDER_COLOR = WHITE
BUTTON_COLOR = GREEN
HOVER_BUTTON = BRIGHTER_GREEN
BUTTON_TEXT_COLOR = WHITE
HOVER_COLOR = BLUE

FONT_SIZE = 20

UP = 'up'
DOWN = 'down'
LEFT = 'left'
RIGHT = 'right'

EASY = 'easy'
MED = 'medium'
HARD = 'hard'

X_BORDER = 1
Y_BORDER = 1

pygame.display.set_caption('Slide Puzzle')
gameDisplay = pygame.display.set_mode((DISPLAY_WIDTH, DISPLAY_HEIGHT))
clock = pygame.time.Clock()

tile_len = 117

smallText = pygame.font.Font("freesansbold.ttf", FONT_SIZE)
largeText = pygame.font.Font('freesansbold.ttf', 115)

images = ['large_wave', 'chopper', 'pompom', 'cinna']
random.shuffle(images)

# load pieces of image
one = pygame.image.load('./' + images[0] + '/16.jpg')
two = pygame.image.load('./' + images[0] + '/15.jpg')
three = pygame.image.load('./' + images[0] + '/14.jpg')
four = pygame.image.load('./' + images[0] + '/13.jpg')
five = pygame.image.load('./' + images[0] + '/12.jpg')
six = pygame.image.load('./' + images[0] + '/11.jpg')
seven = pygame.image.load('./' + images[0] + '/10.jpg')
eight = pygame.image.load('./' + images[0] + '/9.jpg')
nine = pygame.image.load('./' + images[0] + '/8.jpg')
ten = pygame.image.load('./' + images[0] + '/7.jpg')
eleven = pygame.image.load('./' + images[0] + '/6.jpg')
twelve = pygame.image.load('./' + images[0] + '/5.jpg')
thirteen = pygame.image.load('./' + images[0] + '/4.jpg')
fourteen = pygame.image.load('./' + images[0] + '/3.jpg')
fifteen = pygame.image.load('./' + images[0] + '/2.jpg')
pic = pygame.image.load('./' + images[0] + '/pic.jpg')

empty_star = pygame.image.load('./empty_star.png')
star = pygame.image.load('./star.png')

solvedPositions = {one: (103, 63), two: (221, 63), three: (339, 63),
                   four: (457, 63),
                   five: (103, 181), six: (221, 181), seven: (339, 181),
                   eight: (457, 181),
                   nine: (103, 299), ten: (221, 299), eleven: (339, 299),
                   twelve: (457, 299),
                   thirteen: (103, 417), fourteen: (221, 417),
                   fifteen: (339, 417), BLANK: (457, 417)}

currentPositions = solvedPositions.copy()
currentPuzzle = {}
currentBlock = None
prevBlock = None
curr_move = None
moves = 0
times_shuffled = 0
mode = None
solution = False


def main():
    game_exit = False
    newPuzzle()
    global moves
    while not game_exit:
        gameDisplay.fill(BG_COLOR)
        pygame.draw.rect(gameDisplay, WHITE, (100, 60, 477, 477))
        displayMessage('Click a tile and press arrow keys to slide.', 5, 5)
        if currentPositions == solvedPositions:
            displayImage()
        button("RESET", 650, 400, 100, 50, BUTTON_COLOR, HOVER_BUTTON, reset)
        button("SHUFFLE", 650, 460, 125, 50, BUTTON_COLOR, HOVER_BUTTON,
               newPuzzle)
        button("SOLVE", 650, 520, 100, 50, BUTTON_COLOR, HOVER_BUTTON, solve)
        displayMessage('Number of moves: ' + str(moves), 600, 60)

        mouse_pos = pygame.mouse.get_pos()
        checkTile(currentBlock, mouse_pos[0], mouse_pos[1])
        if prevBlock is not None:
            deselectTile(prevBlock)
        if currentBlock is not None:
            selectTile(currentBlock)

        # display board
        for key in currentPositions:
            if key != BLANK:
                displayTile(key, currentPositions[key][0],
                            currentPositions[key][1])
            else:
                blankTile(currentPositions[key][0], currentPositions[key][1])
        global curr_move
        for event in pygame.event.get():  # gets list of events per fps
            if event.type == pygame.QUIT:
                quitGame()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT or event.key == pygame.K_a:
                    curr_move = LEFT
                elif event.key == pygame.K_RIGHT or event.key == pygame.K_d:
                    curr_move = RIGHT
                elif event.key == pygame.K_UP or event.key == pygame.K_w:
                    curr_move = UP
                elif event.key == pygame.K_DOWN or event.key == pygame.K_s:
                    curr_move = DOWN
                else:
                    curr_move = None
            else:
                curr_move = None

            if isValidMove(currentBlock, curr_move):
                moves += 1
                moveTile(currentBlock)
                deselectTile(BLANK)

        pygame.display.update()
        clock.tick(FPS)


def reset():
    # go back to original puzzle
    print('reset')
    global currentPositions
    currentPositions = currentPuzzle.copy()
    global moves
    moves = 0


def newPuzzle():
    # generate new puzzle
    print('new')
    print(mode)

    possible_moves = [UP, DOWN, LEFT, RIGHT]
    blocks = [one, two, three, four, five, six, seven, eight, nine, ten, eleven,
              twelve, thirteen, fourteen, fifteen, BLANK]
    global currentPuzzle
    global currentPositions
    global times_shuffled

    currentPositions = solvedPositions.copy()
    # reset number of moves
    i = 0
    if mode == EASY:
        i = 5
    elif mode == MED:
        i = 15
    elif mode == HARD:
        i = 30
    while i != 0:
        # select a random block to move
        random.shuffle(blocks)
        block = blocks[0]
        # select a random move
        random.shuffle(possible_moves)
        move = possible_moves[0]
        # check if move is valid
        if isValidMove(block, move):
            # move block
            moveTile(block)
            i -= 1

    currentPuzzle = currentPositions.copy()
    times_shuffled += 1


def solve():
    # give answer to puzzle
    print('solve')
    global currentPositions
    currentPositions = solvedPositions
    global solution
    solution = True


def retry():
    initializePuzzle()
    modeScreen()


def isValidMove(curr, move):
    if curr is None:
        return False

    blank_x = currentPositions[BLANK][0]
    blank_y = currentPositions[BLANK][1]
    curr_x = currentPositions[curr][0]
    curr_y = currentPositions[curr][1]

    if move == UP:
        return (curr_x == blank_x) and (curr_y - (tile_len + 1) == blank_y)
    elif move == DOWN:
        return (curr_x == blank_x) and (curr_y + (tile_len + 1) == blank_y)
    elif move == LEFT:
        return (curr_x - (tile_len + 1) == blank_x) and (curr_y == blank_y)
    elif move == RIGHT:
        return (curr_x + (tile_len + 1) == blank_x) and (curr_y == blank_y)
    else:
        return False


def moveTile(curr):
    currentPositions[BLANK], currentPositions[curr] = currentPositions[curr], \
                                                      currentPositions[BLANK]


def displayTile(img, x, y):
    gameDisplay.blit(img, (x, y))


def blankTile(x, y):
    pygame.draw.rect(gameDisplay, BLANK_COLOR, (x, y, 117, 117))


def checkTile(curr, x, y):
    global currentBlock
    global prevBlock
    click = pygame.mouse.get_pressed()
    if click[0] == 1:
        for key in currentPositions:
            if currentPositions[key][0] <= x <= currentPositions[key][0] + \
                    tile_len:
                if currentPositions[key][1] <= y <= currentPositions[key][1] + \
                        tile_len:
                    currentBlock = key
                    prevBlock = curr


def selectTile(block):
    x = currentPositions[block][0] - 1
    y = currentPositions[block][1] - 1

    pygame.draw.rect(gameDisplay, HOVER_COLOR, (x, y, 120, 120))


def deselectTile(block):
    x = currentPositions[block][0] - 1
    y = currentPositions[block][1] - 1

    pygame.draw.rect(gameDisplay, WHITE, (x, y, 120, 120))


def quitGame():
    pygame.quit()
    quit()


def text_objects(text, font, color):
    textSurface = font.render(text, True, color)
    return textSurface, textSurface.get_rect()


def button(msg, x, y, w, h, ic, ac, action=None):
    mouse = pygame.mouse.get_pos()
    click = pygame.mouse.get_pressed()
    if x + w >= mouse[0] >= x and y + h >= mouse[1] >= y:
        pygame.draw.rect(gameDisplay, ac, (x, y, w, h))
        if click[0] == 1 and action is not None:
            action()
    else:
        pygame.draw.rect(gameDisplay, ic, (x, y, w, h))

    textSurf, textRect = text_objects(msg, smallText, BUTTON_TEXT_COLOR)
    textRect.center = ((x + (w // 2)), (y + (h // 2)))
    gameDisplay.blit(textSurf, textRect)


def displayMessage(msg, x, y):
    font = pygame.font.SysFont(None, 25)
    textSurf, textRect = text_objects(msg, font, TEXT_COLOR)
    textRect.topleft = (x, y)
    gameDisplay.blit(textSurf, textRect)


def introScreen():
    intro = True
    while intro:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quitGame()
        gameDisplay.fill(BG_COLOR)
        TextSurf, TextRect = text_objects("Slide Puzzle", largeText, TEXT_COLOR)
        TextRect.center = ((DISPLAY_WIDTH // 2), (DISPLAY_HEIGHT // 2))
        gameDisplay.blit(TextSurf, TextRect)  # in background

        button("START", 150, 450, 100, 50, GREEN, BRIGHTER_GREEN, modeScreen)
        button("QUIT", 550, 450, 100, 50, RED, BRIGHTER_RED, quitGame)

        pygame.display.update()
        clock.tick(FPS)


def modeScreen():
    modeSelect = True
    while modeSelect:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quitGame()
        gameDisplay.fill(BG_COLOR)
        displayMessage('Select a mode:', 340, 120)

        button("EASY", 350, 200, 100, 50, GREEN, BRIGHTER_GREEN, easy)
        button("MEDIUM", 350, 300, 100, 50, GREEN, BRIGHTER_GREEN, medium)
        button("HARD", 350, 400, 100, 50, GREEN, BRIGHTER_GREEN, hard)

        pygame.display.update()
        clock.tick(FPS)


def easy():
    global mode
    mode = EASY
    main()


def medium():
    global mode
    mode = MED
    main()


def hard():
    global mode
    mode = HARD
    main()


def displayImage():
    display = True
    star1 = (640, 100)
    star2 = (640, 196)
    star3 = (640, 292)

    while display:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quitGame()
        gameDisplay.fill(BG_COLOR)
        displayMessage('You solved it!', 290, 30)
        displayMessage('Number of moves: ' + str(moves), 600, 60)
        gameDisplay.blit(pic, (103, 63))
        total = moves + (times_shuffled - 1 * 2)
        if mode == EASY:
            if solution:
                gameDisplay.blit(empty_star, star1)
                gameDisplay.blit(empty_star, star2)
                gameDisplay.blit(empty_star, star3)
            elif total <= 5:
                gameDisplay.blit(star, star1)
                gameDisplay.blit(star, star2)
                gameDisplay.blit(star, star3)
            elif 6 <= total <= 9:
                gameDisplay.blit(star, star1)
                gameDisplay.blit(star, star2)
                gameDisplay.blit(empty_star, star3)
            else:
                gameDisplay.blit(star, star1)
                gameDisplay.blit(empty_star, star2)
                gameDisplay.blit(empty_star, star3)
        elif mode == MED:
            if solution:
                gameDisplay.blit(empty_star, star1)
                gameDisplay.blit(empty_star, star2)
                gameDisplay.blit(empty_star, star3)
            elif total <= 15:
                gameDisplay.blit(star, star1)
                gameDisplay.blit(star, star2)
                gameDisplay.blit(star, star3)
            elif 16 <= total <= 19:
                gameDisplay.blit(star, star1)
                gameDisplay.blit(star, star2)
                gameDisplay.blit(empty_star, star3)
            else:
                gameDisplay.blit(star, star1)
                gameDisplay.blit(empty_star, star2)
                gameDisplay.blit(empty_star, star3)
        elif mode == HARD:
            if solution:
                gameDisplay.blit(empty_star, star1)
                gameDisplay.blit(empty_star, star2)
                gameDisplay.blit(empty_star, star3)
            elif total <= 30:
                gameDisplay.blit(star, star1)
                gameDisplay.blit(star, star2)
                gameDisplay.blit(star, star3)
            elif 31 <= total <= 39:
                gameDisplay.blit(star, star1)
                gameDisplay.blit(star, star2)
                gameDisplay.blit(empty_star, star3)
            else:
                gameDisplay.blit(star, star1)
                gameDisplay.blit(empty_star, star2)
                gameDisplay.blit(empty_star, star3)

        button("RETRY", 585, 420, 100, 50, GREEN, BRIGHTER_GREEN, retry)
        button("QUIT", 685, 420, 100, 50, RED, BRIGHTER_RED, quitGame)
        pygame.display.update()
        clock.tick(FPS)


def initializePuzzle():
    global one, two, three, four, five, six, seven, eight, nine, ten, eleven, \
        twelve, thirteen, fourteen, fifteen, pic, solvedPositions, \
        currentPositions, currentBlock, curr_move, prevBlock, moves, \
        currentPuzzle, mode, solution, times_shuffled
    random.shuffle(images)

    # load pieces of image
    one = pygame.image.load('./' + images[0] + '/16.jpg')
    two = pygame.image.load('./' + images[0] + '/15.jpg')
    three = pygame.image.load('./' + images[0] + '/14.jpg')
    four = pygame.image.load('./' + images[0] + '/13.jpg')
    five = pygame.image.load('./' + images[0] + '/12.jpg')
    six = pygame.image.load('./' + images[0] + '/11.jpg')
    seven = pygame.image.load('./' + images[0] + '/10.jpg')
    eight = pygame.image.load('./' + images[0] + '/9.jpg')
    nine = pygame.image.load('./' + images[0] + '/8.jpg')
    ten = pygame.image.load('./' + images[0] + '/7.jpg')
    eleven = pygame.image.load('./' + images[0] + '/6.jpg')
    twelve = pygame.image.load('./' + images[0] + '/5.jpg')
    thirteen = pygame.image.load('./' + images[0] + '/4.jpg')
    fourteen = pygame.image.load('./' + images[0] + '/3.jpg')
    fifteen = pygame.image.load('./' + images[0] + '/2.jpg')
    pic = pygame.image.load('./' + images[0] + '/pic.jpg')

    solvedPositions = {one: (103, 63), two: (221, 63), three: (339, 63),
                       four: (457, 63),
                       five: (103, 181), six: (221, 181), seven: (339, 181),
                       eight: (457, 181),
                       nine: (103, 299), ten: (221, 299), eleven: (339, 299),
                       twelve: (457, 299),
                       thirteen: (103, 417), fourteen: (221, 417),
                       fifteen: (339, 417), BLANK: (457, 417)}

    currentPositions = solvedPositions.copy()
    currentPuzzle = None
    currentBlock = None
    prevBlock = None
    curr_move = None
    moves = 0
    times_shuffled = 0
    mode = None
    solution = False


introScreen()
