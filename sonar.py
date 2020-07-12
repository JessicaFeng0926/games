# 声呐寻宝

import random
import sys
import math
from typing import List, Tuple

def get_new_board() -> List[List[str]]:
    '''生成由~和`组成的海洋'''
    # 15行，60列
    board = [['~' if random.randrange(2) else '`' for _ in range(60)] for _ in range(15) ]
    return board

def draw_board(board: List[List[str]]) -> None:
    '''打印海水'''
    tens_digits_line = '    '
    for i in range(1,6):
        tens_digits_line += (" "*9)+str(i)
    # 打印头部的刻度
    print(tens_digits_line)
    print('   '+('0123456789'*6))
    print()
    
    # 打印海水和行号
    for row in range(15):
        extra_space = ' ' if row<10 else ''
        board_row = ''.join(board[row])
        print(f'{extra_space}{row} {board_row} {row}')
    
    # 打印尾部刻度
    print()
    print('   '+('0123456789'*6))
    print(tens_digits_line)

def get_random_chests(num_chests: int) -> List[Tuple[int,int]]:
    '''生成一系列宝箱的坐标'''
    chests: List[Tuple[int,int]] = []
    while len(chests) < num_chests:
        new_chest: Tuple[int,int] = (random.randrange(60),random.randrange(15))
        if new_chest not in chests:
            chests.append(new_chest)
    return chests


def is_on_board(x: int, y: int) -> bool:
    '''判断给定的坐标是否在坐标系里'''
    return x>=0 and x<=59 and y>=0 and y<=14

def make_move(board: List[List[str]], 
              chests: List[Tuple[int,int]], 
              x: int, y: int) -> str:
    '''放置声呐探测仪或者取走宝箱,返回描述字符串'''
    # 只探测距离在10以内的宝箱
    # 如果没有宝箱，min函数会报错，所以这里需要有一个判断
    if chests:
        smallest_distance: float = min(math.sqrt((cx-x)**2+(cy-y)**2) for cx,cy in chests)
        smallest_distance: int = round(smallest_distance)
    else:
        smallest_distance: int = 10
    if smallest_distance == 0:
        chests.remove((x,y))
        return 'You have found a sunken treasure chest!'
    elif smallest_distance < 10:
        board[y][x] = str(smallest_distance)
        return f'Treasure detected at a distance of {smallest_distance} from the sonar device.'
    else:
        board[y][x] = 'X'
        return 'Solar did not detect anything. All treasure chests out of range.'

def enter_player_move(previous_moves: List[Tuple[int,int]]) -> Tuple[int,int]:
    '''获取用户输入的坐标'''
    print('Where do you want to drop the next sonar device? (0-59 0-14)(or type quit)')
    while True:
        move: str = input('>>>')
        if move.lower() == 'quit':
            print('Thanks for playing!')
            sys.exit()
        
        move: List[str] = move.split()
        if len(move) == 2 and move[0].isdigit() and move[1].isdigit() and is_on_board(int(move[0]),int(move[1])):
            if (int(move[0]),int(move[1])) in previous_moves:
                print('You alreday moved there.')
                continue
            return int(move[0]),int(move[1])
        print('Enter a number from 0 to 59, a space, then a number from 0 to 14.')


def show_instructions():
    '''打印给玩家看的游戏说明'''
    print('''Instructions:
You are the caption of the Simon, a treasure-hunting ship. Your current mission
is to user sonar devices to find three suken treasure chests at the bottom of
the ocean. But you only have cheap sonar that finds distance, not direction.

Enter the coordinates to drop a sonar device. The ocean map will be marked with
how far away the nearest chest is, or an X if it is beyond the sonar device's
range. For example, the C marks are where chests are. The sonar device shows a
3 because the closest chest is 3 spaces away.
                    1         2         3
          012345678901234567890123456789012
        0 ~```````~~~~~`~~~~~`````~~~`````` 0
        1 `~~~~````~~````````~`~```````~~~~ 1
        2 `~`C``3``````C~~~````~~~~~`````~~ 2
        3 ~````~~~~~````~~~~`````~~~~~```~~ 3
        4 ~````~`````~`C``~~~~~~```````~~~` 4
          012345678901234567890123456789012 
                    1         2         3
(In the real game, the chests are not visible in the ocean.)

Press enter to continue...
''')
    input()
    print('''When you drop a sonar device directly on the chest, you retrieve it and the other
sonar devices update to show how far away the next nearest chest is. The chests
are beyond the range of the sonar device on the left, so it shows an X.
                    1         2         3
          012345678901234567890123456789012
        0 ~```````~~~~~`~~~~~`````~~~`````` 0
        1 `~~~~````~~````````~`~```````~~~~ 1
        2 `~`X``7``````C~~~````~~~~~`````~~ 2
        3 ~````~~~~~````~~~~`````~~~~~```~~ 3
        4 ~````~`````~`C``~~~~~~```````~~~` 4
          012345678901234567890123456789012 
                    1         2         3

The treasure chests don't move around. Sonar devices can detect treasure chests
up to a distance of 9 spaces. Try to collect all 3 chests before running out of
sonar devices. Good luck!

Press enter to continue...
'''
)
    input()

if __name__ == '__main__':
    print('S O N A R !\n')
    if input('Would you like to view the instructions?(yes or no)>>>').lower().startswith('y'):
        show_instructions()

while True:
    # 初始化设置
    sonar_devices: int = 20
    board: List[List[str]] = get_new_board()
    chests: List[Tuple[int,int]] = get_random_chests(3)
    draw_board(board)
    previous_moves: List[Tuple[int,int]] = []

    while sonar_devices > 0:
        # 展示声呐和宝箱的情况
        print(f'You have {sonar_devices} device(s) left. {len(chests)} treasure chest(s) remaining.')

        x, y = enter_player_move(previous_moves)
        previous_moves.append((x,y))

        move_result: str = make_move(board,chests,x,y)

        if move_result == 'You have found a sunken treasure chest!':
            # 更新所有声呐的探测情况
            for x,y in previous_moves:
                make_move(board,chests,x,y)
        
        draw_board(board)
        print(move_result)
        
        # 宝箱都找到了，游戏胜利
        if len(chests) == 0:
            print('You have found all the sunken treasure chests! Congratulations and good game!')
            break
        
        # 更新声呐设备数量
        sonar_devices -= 1

    else:
        print('We have run out of sonar devices! Now we have to turn the ship around'
              ' and head for home with treasure chests still out there!'
              ' Game over.')
        print('    The remaining chests were here:')
        for x,y in chests:
            print(f'    {x}, {y}')
    
    # 是否再玩儿一局
    if not input('Do you want to play again?(yes or no)>>>').lower().startswith('y'):
        break



