import random
from typing import List

# 要猜的是3个数字
NUM_DIGITS: int = 3
# 最多猜10次
MAX_GUESS: int = 10

def get_secret_num() -> str:
    '''返回要猜的三个数字'''
    numbers: List[str] = [str(num) for num in range(10)]
    return ''.join(random.sample(numbers,NUM_DIGITS))

def get_clues(guess: str, secret_num: str) -> str:
    '''获取提示'''
    if guess == secret_num:
        return 'You got it!'
    clues: List[str] = []
    for i, digit in enumerate(guess):
        if digit == secret_num[i]:
            clues.append('Fermi')
        elif digit in secret_num:
            clues.append('Pico')
    
    # 如果clues是空的，就说明猜的一点都不沾边
    if not clues:
        return 'Bagels'
    
    # 按照字母顺序排序
    clues.sort()

    return ' '.join(clues)

def is_only_digits(num: str) -> bool:
    '''检测是否是纯数字'''
    if num == '':
        return False
    
    digits: List[str] = [str(d) for d in range(10)]
    # 只要有一个字符不是数字，就返回False
    for n in num:
        if n not in digits:
            return False
    return True

def get_guess(guesses_taken: int) -> str:
    '''获取用户输入'''
    guess: str = ''
    # 检测用户输入的数字个数，还要检测是否是纯数字
    while len(guess) != NUM_DIGITS or not is_only_digits(guess):
        guess: str = input(f'Guess #{guesses_taken}>>>')
    return guess

if __name__ == '__main__':
    print(f'I am thinking of a {NUM_DIGITS}-digit number.'
          f' Try to guess what it is.')
    print('The clues I give are...')
    print('When I say:    That means:')
    print('  Bagels       None of the digits is correct.')
    print('  Pico         One digit is correct but in the wrong position.')
    print('  Fermi        One digit is correct and in the right position.')
    
    # 如果用户不退出，会一次次地玩儿
    while True:
        secret_num: str = get_secret_num()
        print(f'I have thought up a number.'
              f' You have {MAX_GUESS} guessess to get it.')
        
        guesses_taken:int = 1

        # 一次游戏的主体
        while guesses_taken <= MAX_GUESS:
            guess: str = get_guess(guesses_taken)
            print(get_clues(guess,secret_num))
            guesses_taken += 1

            if guess == secret_num:
                break
        else:
            print(f'You ran out of guesses. The answer was {secret_num}.')
        
        if not input('Do you want to player again?(yes or no)>>>').lower().startswith('y'):
            break
            


