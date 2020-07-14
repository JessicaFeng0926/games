# 翻转棋

import random
import sys
from typing import List, Optional, Tuple, Dict

# 棋盘宽度
WIDTH = 8
# 棋盘高度
HEIGHT = 8

def draw_board(board: List[List[str]]) -> None:
    '''绘制棋盘'''
    print('  12345678')
    print(' +--------+')
    for y in range(HEIGHT):
        print(f'{y+1}|{"".join(board[y])}|{y+1}')
    print(' +--------+')
    print('  12345678')

def get_new_board() -> List[List[str]]:
    '''创建一个空的新棋盘'''
    return [[' ' for _ in range(WIDTH)] for _ in range(HEIGHT)]

def is_valid_move(board: List[List[str]], tile: str, 
                  xstart: int, ystart: int) -> Optional[List]:
    '''判断一个棋步是否有效,无效返回False，有效返回一个列表'''
    # 格子被占了，或者格子不在棋盘上，返回False
    if board[ystart][xstart] != ' ' or not is_on_board(xstart,ystart):
        return False

    if tile == 'X':
        other_tile = 'O'
    else:
        other_tile = 'X'

    tiles_to_flip: List[Tuple[int,int]] = []
    
    # 分别判断这个格子周围的八个方向上是否有可以翻转的棋子
    for x_direction, y_direction in [(0,1),(1,1),(1,0),(1,-1),(0,-1),(-1,-1),(-1,0),(-1,1)]:
        x, y = xstart, ystart
        x += x_direction
        y += y_direction
        # 只要当前方向上相邻的棋子是对方的，就一直往那个方向走
        while is_on_board(x,y) and board[y][x] == other_tile:
            x += x_direction
            y += y_direction
            # 遇到第一个自己的棋子，开始往回走，沿路收集需要翻转的棋子坐标
            if is_on_board(x,y) and board[y][x] == tile:
                while True:
                    x -= x_direction
                    y -= y_direction
                    # 回到原点就停下来，这个方向的坐标收集结束了
                    if x == xstart and y== ystart:
                        break
                    tiles_to_flip.append((x,y))
    
    # 游戏规则是每步必吃，所以如果没有可以翻转的棋子，这步也是无效的
    if not tiles_to_flip:
        return False
    return tiles_to_flip

def is_on_board(x: int, y: int) -> bool:
    '''判断坐标是否在棋盘上'''
    return x>=0 and x<WIDTH and y>=0 and y<HEIGHT

def get_board_with_valid_moves(board: List[List[str]], 
                               tile: str) -> List[List[str]]:
    '''返回带有提示的棋盘，提示用圆点表示'''
    board_copy = get_board_copy(board)
    valid_moves = get_valid_moves(board_copy,tile)
    for x,y in valid_moves:
        board_copy[y][x] = '·'
    return board_copy

def get_valid_moves(board: List[List[str]], 
                    tile: str) -> List[Tuple[int,int]]:
    '''根据当前棋盘状态返回下一步可以走的坐标'''
    valid_moves: List[Tuple[int,int]] = []
    for y in range(HEIGHT):
        for x in range(WIDTH):
            if is_valid_move(board, tile, x, y) != False:
                valid_moves.append((x,y))
    return valid_moves

def get_score_of_board(board: List[List[str]]) -> Dict[str,int]:
    '''以字典的形式返回两名选手的得分'''
    xscore: int = 0
    oscore: int = 0
    for y in range(HEIGHT):
        for x in range(WIDTH):
            if board[y][x] == 'X':
                xscore += 1
            elif board[y][x] == 'O':
                oscore += 1
    return {'X':xscore,'O':oscore}

def enter_player_tile() -> Tuple[str,str]:
    '''获取用户选择的棋子'''
    tile = ''
    while not (tile=='X' or tile=='O'):
        tile = input('Do you want to be X or O?>>>').upper()
    # 返回玩家和电脑的棋子
    if tile == 'X':
        return 'X','O'
    return 'O','X'

def who_goes_first() -> str:
    '''随机决定谁先开始'''
    if random.randrange(2) == 0:
        return 'computer'
    return 'player'

def make_move(board: List[List[str]],
              tile: str,
              xstart: int,
              ystart: int) -> bool:
    '''把棋子放到指定的格子上，如果是无效的格子就返回False'''
    tiles_to_flip: List[Tuple[int,int]] = is_valid_move(board,tile,xstart,ystart)
    
    if tiles_to_flip == False:
        return False

    board[ystart][xstart] = tile
    for x,y in tiles_to_flip:
        board[y][x] = tile
    return True

def get_board_copy(board: List[List[str]]) -> List[List[str]]:
    '''返回棋盘的副本'''
    board_copy: List[List[str]] = get_new_board()
    for y in range(HEIGHT):
        for x in range(WIDTH):
            board_copy[y][x] = board[y][x]

    return board_copy

def is_on_corner(x: int, y: int) -> bool:
    '''判断一个坐标是否在角落'''
    return (x==0 or x== WIDTH-1) and (y==0 or y==HEIGHT-1)

def get_player_move(board, player_tile) -> Optional[Tuple[int,int]]:
    '''获取用户要下棋的坐标'''
    DIGITS1TO8 = '1 2 3 4 5 6 7 8'.split()
    while True:
        move: str = input('Enter your move, "quit" to end the game, or "hints" to toggle hints.>>>').lower()
        if move == 'quit' or move == 'hints':
            return move

        if len(move) == 2 and move[0] in DIGITS1TO8 and move[1] in DIGITS1TO8:
            x: int = int(move[0])-1
            y: int = int(move[1])-1
            if is_valid_move(board,player_tile,x,y) != False:
                break
        else:
            print('That is not a valid move. Enter the column(1-8) and then the row(1-8).')
            print('For example, 81 will move on the top-right corner.')
    return x,y

def get_computer_move(board: List[List[str]], computer_tile) -> Tuple[int,int]:
    '''获取电脑要下棋的格子坐标'''
    possible_moves: List[Tuple[int,int]] = get_valid_moves(board,computer_tile)
    random.shuffle(possible_moves)

    # 尽量占个角
    for x,y in possible_moves:
        if is_on_corner(x,y):
            return x,y
    
    # 占不了角，就选择一个分数最高的格子
    best_score = -1
    for x,y in possible_moves:
        # 在棋盘副本上试着走，然后看看得分是否更高了
        board_copy = get_board_copy(board)
        make_move(board_copy,computer_tile,x,y)
        score = get_score_of_board(board_copy)[computer_tile]
        if score > best_score:
            best_move = (x,y)
            best_score = score
    return best_move
        
def print_score(board: List[List[str]],
                player_tile: str,
                computer_tile: str) -> None:
    '''打印成绩'''
    scores: Dict[str,int] = get_score_of_board(board)
    print(f'You: {scores[player_tile]} points. Computer: {scores[computer_tile]} points.')

def play_game(player_tile: str, computer_tile: str) -> List[List[str]]:
    '''根据用户的输入下棋，结束的时候返回最终的棋盘'''
    show_hints: bool = False
    turn: str = who_goes_first()
    print(f'The {turn} will go first.')

    # 初始化棋盘
    board: List[List[str]] = get_new_board()
    board[3][3]='X'
    board[3][4]='O'
    board[4][3]='O'
    board[4][4]='X'

    while True:
        player_valid_moves: List[Tuple[int,int]] = get_valid_moves(board,player_tile)
        computer_valid_moves: List[Tuple[int,int]] = get_valid_moves(board,computer_tile)
        # 都没有地方下了，返回棋盘
        if player_valid_moves == [] and computer_valid_moves == []:
            return board
        elif turn == 'player':
            if player_valid_moves:
                if show_hints:
                    valid_moves_board = get_board_with_valid_moves(board,player_tile)
                    draw_board(valid_moves_board)
                else:
                    draw_board(board)
                print_score(board,player_tile,computer_tile)
                move = get_player_move(board,player_tile)
                if move == 'quit':
                    print('Thanks for playing!')
                    sys.exit()
                elif move == 'hints':
                    show_hints = not show_hints
                    continue
                else:
                    make_move(board,player_tile,move[0],move[1])
            # 不论这次玩家走没走，都要把出牌权交给电脑
            turn = 'computer'
        elif turn == 'computer':
            if computer_valid_moves:
                draw_board(board)
                print_score(board,player_tile,computer_tile)
                input('Press Enter to see the computer\'s move.')
                move = get_computer_move(board,computer_tile)
                make_move(board,computer_tile,move[0],move[1])
            # 不论这次电脑走没走，都要把出牌权交给玩家
            turn = 'player'
        

if __name__ == '__main__':
    print('Welcome to Reversegam!')

    player_tile, computer_tile = enter_player_tile()

    while True:
        final_board = play_game(player_tile,computer_tile)
        # 展示最终的棋盘
        draw_board(final_board)
        # 获取最终的得分
        scores: Tuple[int,int] = get_score_of_board(final_board)
        print(f'X scored {scores["X"]} points. O scored {scores["O"]} points.')
        if scores[player_tile] > scores[computer_tile]:
            print(f'You beat the computer by {scores[player_tile]-scores[computer_tile]} points! Congratulations!')
        elif scores[player_tile] < scores[computer_tile]:
            print(f'You losts. The computer beat you by {scores[computer_tile]-scores[player_tile]} points.')
        else:
            print('The game was a tie!')

        if not input('Do you want to play again?(yes or no)>>>').lower().startswith('y'):
            break  








