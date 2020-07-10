# 井字棋游戏

import random
from typing import List, Tuple, Optional

def draw_board(board: List[str]) -> None:
    '''根据电脑和玩家选择的位置绘制棋盘'''
    print(board[7]+'|'+board[8]+'|'+board[9])
    print('-+-+-')
    print(board[4]+'|'+board[5]+'|'+board[6])
    print('-+-+-')
    print(board[1]+'|'+board[2]+'|'+board[3])


def input_player_letter() -> Tuple[str, str]:
    '''返回玩家和电脑的棋子'''
    letter: str = ''
    while not (letter=='X' or letter=='O'):
        letter: str = input('Do you want to be X or O?>>>').upper()
    if letter == 'X':
        return 'X', 'O'
    else:
        return 'O', 'X'

def who_goes_first() -> str:
    '''随机选择谁先开始'''
    if random.randrange(0,2) == 0:
        return 'computer'
    else:
        return 'player'

def make_move(board: List[str], letter: str, move: int):
    '''根据指定的位置放下棋子'''
    board[move] = letter

def is_winner(board: List[str], letter: str) -> bool:
    '''判断一个选手是否赢了'''
    return (board[7]==letter and board[8]==letter and board[9]==letter) or\
    (board[4]==letter and board[5]==letter and board[6]==letter) or\
    (board[1]==letter and board[2]==letter and board[3]==letter) or\
    (board[7]==letter and board[4]==letter and board[1]==letter) or\
    (board[8]==letter and board[5]==letter and board[2]==letter) or\
    (board[9]==letter and board[6]==letter and board[3]==letter) or\
    (board[7]==letter and board[5]==letter and board[3]==letter) or\
    (board[9]==letter and board[5]==letter and board[1]==letter)


def get_board_copy(board: List[str]) -> List[str]:
    '''返回棋盘的副本'''
    return board.copy()

def is_space_free(board: List[str], move: int) -> bool:
    '''判断指定的格子是否为空'''
    return board[move] == ' '

def get_player_move(board: List[str]) -> int:
    '''获取用户输入的格子号码'''
    move: str = ' '
    # 用户的输入必须是1到9之间的一个数字
    # 并且这个格子必须是空的才行
    while move not in '1 2 3 4 5 6 7 8 9'.split() or \
        not is_space_free(board, int(move)):
        move: str = input('What is your next move? (1-9)>>>')
    return int(move)

def choose_random_move_from_list(board: List[str], move_list: List[int]) -> Optional[int]:
    '''在给定的号码列表中随机选择一个可行的格子'''
    possible_moves: List[int] = [move for move in move_list if is_space_free(board, move)]
    if possible_moves:
        return random.choice(possible_moves)
    # 如果没有空格，返回None
    return None

def get_computer_move(board: List[str], computer_letter: str) -> int:
    '''返回电脑要下棋的格子号码'''
    if computer_letter == 'X':
        player_letter = 'O'
    else:
        player_letter = 'X'
    
    # 先检查一下下一步电脑有没有可能赢
    # 如果电脑有可能赢，就往可以赢的格子下棋
    for move in range(1,10):
        board_copy = get_board_copy(board)
        if is_space_free(board_copy, move):
            make_move(board_copy,computer_letter,move)
            if is_winner(board_copy,computer_letter):
                return move

    # 如果下一步电脑无法赢，就检查一下玩家是不是要赢了
    # 如果玩家要赢了，就阻碍他
    for move in range(1,10):
        board_copy = get_board_copy(board)
        if is_space_free(board_copy,move):
            make_move(board_copy,player_letter,move)
            if is_winner(board_copy,player_letter):
                return move

    # 如果还没有到赛点，那就按照格子的重要程度抢占
    # 先看看能不能占一个角
    if (move := choose_random_move_from_list(board,[1,3,7,9])) is not None:
        return move
    
    # 占不到角，就试着占中心
    if is_space_free(board,5):
        return 5

    # 实在不行就往边上下
    return choose_random_move_from_list(board,[2,4,6,8])

def is_board_full(board: List[str]) -> bool:
    '''判断棋盘是否已经下满了'''
    for move in range(1,10):
        if is_space_free(board,move):
            return False
    return True

    
if __name__ == '__main__':
    print('Welcome to Tic-Tac-Toe!')
    
    # 这个循环可以在整得玩家同意的前提下
    # 一盘接一盘地下棋
    while True:
        # 初始化空棋盘
        board: List[str] = [' ']*10
        player_letter, computer_letter = input_player_letter()
        turn: str = who_goes_first()
        print(f'The {turn} will go first.')
        
        # 下面是一盘棋的主体
        while True:
            if turn == 'player':
                draw_board(board)
                move: int = get_player_move(board)
                make_move(board,player_letter,move)
                
                if is_winner(board,player_letter):
                    draw_board(board)
                    print('Hooray! You have won the game!')
                    break
                else:
                    if is_board_full(board):
                        draw_board(board)
                        print('The game is a tie!')
                        break
                    else:
                        turn: str = 'computer'
            else:
                move: int = get_computer_move(board,computer_letter)
                make_move(board,computer_letter,move)

                if is_winner(board,computer_letter):
                    draw_board(board)
                    print('The computer has beaten you! You lose.')
                    break
                else:
                    if is_board_full(board):
                        draw_board(board)
                        print('The game is a tie!')
                        break
                    else:
                        turn: str = 'player'
        if not input('Do you want to play again? (yes or no)>>>').lower().startswith('y'):
            break


    

    





