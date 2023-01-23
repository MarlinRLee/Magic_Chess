def valid_move(board, x, y, color = None):
    return board.inbound(x, y) and board.squares[x][y].occupying_piece is None

def valid_attack(board, x, y, color):
    ret = False
    if not board.inbound(x, y) or board.squares[x][y].occupying_piece is None:
        ret = False
    elif board.squares[x][y].occupying_piece.color != color:
        ret = True
    return ret

def add_options(options, square, for_attack):
    store = [square]
    if for_attack:
        store.append(store[0].occupying_piece)
        options.append(store)
    else:
        options.append(store[0])

def Bishop_gen(Piece, add_condition, quit_condition, for_attack = False):
    options = []
    for X,Y in [(1,1), (1,-1), (-1,1), (-1,-1)]:
        next_x = Piece.x
        next_y = Piece.y
        valid = True
        while valid:
            next_x = next_x + X
            next_y = next_y + Y
            if add_condition(Piece.board, next_x, next_y, Piece.color):
                add_options(options, Piece.board.squares[next_x][next_y], for_attack)
            valid = quit_condition(Piece.board, next_x, next_y, Piece.color)
    return options

def Bishop_Move(Piece):
    return Bishop_gen(Piece, valid_move, valid_move, for_attack = False)

def Bishop_Attack(Piece):
    return Bishop_gen(Piece, valid_attack, valid_move, for_attack = True)

def King_gen(Piece, add_condition, for_attack = False):
    options = []
    for X in [1, 0, -1]:
        for Y in [1, 0, -1]:
            if X == 0 and Y == 0:
                continue
            next_x = Piece.x + X
            next_y = Piece.y + Y
            if add_condition(Piece.board, next_x, next_y, Piece.color):
                add_options(options, Piece.board.squares[next_x][next_y], for_attack)
    return options

def King_Move(Piece):
    return King_gen(Piece, valid_move, for_attack = False)

def King_Attack(Piece):
    return King_gen(Piece, valid_attack, for_attack = True)

def Knight_gen(Piece, add_condition, for_attack = False):
    options = []
    for X,Y in [(2, 1),(1, 2),(-1, 2),(-2, 1), (-1, -2),(-2, -1),(1,-2),(2,- 1)]:
        next_x = Piece.x + X
        next_y = Piece.y + Y
        if add_condition(Piece.board, next_x, next_y, Piece.color):
            add_options(options, Piece.board.squares[next_x][next_y], for_attack)
    return options

def Knight_Move(Piece):
    return Knight_gen(Piece, valid_move, for_attack = False)

def Knight_Attack(Piece):
    return Knight_gen(Piece, valid_attack, for_attack = True)


def Rook_gen(Piece, add_condition, quit_condition, for_attack = False):
    options = []
    for X,Y in [(1,0), (0,1), (-1,0), (0,-1)]:
        next_x = Piece.x
        next_y = Piece.y
        valid = True
        while valid:
            next_x = next_x + X
            next_y = next_y + Y
            if add_condition(Piece.board, next_x, next_y, Piece.color):
                add_options(options, Piece.board.squares[next_x][next_y], for_attack)
            valid = quit_condition(Piece.board, next_x, next_y, Piece.color)
    return options

def Rook_Move(Piece):
    return Rook_gen(Piece, valid_move, valid_move, for_attack = False)

def Rook_Attack(Piece):
    return Rook_gen(Piece, valid_attack, valid_move, for_attack = True)
def Pawn_Move(Piece):
    options = []
    direct = 1 if Piece.color == "White" else -1

    test_loc_y = Piece.y + direct

    if valid_move(Piece.board, Piece.x, test_loc_y):
        options.append(Piece.board.squares[Piece.x][test_loc_y])
        test_loc_y += direct
        if not Piece.has_moved and valid_move(Piece.board, Piece.x, test_loc_y):
            options.append(Piece.board.squares[Piece.x][test_loc_y])

    return options

def Pawn_Attack(Piece):
    options = []
    direct = 1 if Piece.color == "White" else -1
    test_loc_y = Piece.y + direct
    sides = [-1, 1]
    for dir in sides:
        test_loc_x = Piece.x + dir
        if (valid_attack(Piece.board, test_loc_x, test_loc_y, Piece.color)):
            store = [Piece.board.squares[test_loc_x][test_loc_y]]
            store.append(store[0].occupying_piece)
            options.append(store)
    #check unpesant
    last_move = Piece.board.History[-1]
    if last_move[0] == "P" and abs(last_move[2][1] - last_move[1][1]) == 2:
        last_move_square = Piece.board.squares[last_move[2][0]][last_move[2][1]]
        chec_x, chec_y = last_move[2]
        chec_y = chec_y + direct
        if chec_y == test_loc_y and 1 == abs(chec_x - Piece.x):
            store = [Piece.board.squares[last_move[2][0]][last_move[2][1] + direct]]
            store.append(last_move_square.occupying_piece)
            options.append(store)
    return options

def Summon_move(Card):
    options = []
    for square_list in Card.board.squares:
        iter = square_list if Card.team_color == "White" else reversed(square_list)
        temp_options = []
        for square in iter:
            if valid_move(Card.board, square.x, square.y):
                temp_options.append(square)
            if (square.occupying_piece is not None and 
                square.occupying_piece.name == "P"):
                if square.occupying_piece.color == Card.team_color:
                    options += temp_options
                    break
    return options

def Promotion_Attack(Card):
    options = []
    color = 'White' if Card.team_color == 'Black' else 'Black'
    for square_list in Card.board.squares:
        for square in square_list:
            if valid_attack(Card.board, square.x, square.y, color):
                options.append([square, square.occupying_piece])
    return options


def Destroy_Attack(Card):
    options = []
    for square_list in Card.board.squares:
        for square in square_list:
            if valid_attack(Card.board, square.x, square.y, Card.team_color):
                if square.occupying_piece.name != "K":
                    options.append([square, square.occupying_piece])
    return options