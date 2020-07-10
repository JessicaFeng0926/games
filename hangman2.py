import random 
from typing import List, Dict, Tuple

HANGMAN_PICS = [
'''
 +---+
     |
     |
     |
    ===
''',
'''
 +---+
 O   |
     |
     |
    ===
''',
'''
 +---+
 O   |
 |   |
     |
    ===
''',
'''
 +---+
 O   |
/|   |
     |
    ===
''',
'''
 +---+
 O   |
/|\  |
     |
    ===
''',
'''
 +---+
 O   |
/|\  |
/    |
    ===
''',
'''
 +---+
 O   |
/|\  |
/ \  |
    ===
''',
'''
 +---+
[O   |
/|\  |
/ \  |
    ===
''',
'''
 +---+
[O]  |
/|\  |
/ \  |
    ===
'''  
]

words = {
'Colors':'''red orange yellow green blue indigo 
violet white black brown'''.split(),

'Shapes':'''square triangle rectangle circle ellipse 
rhombus trapezoid chevron pentagon hexagon septagon 
octagon'''.split(),

'Fruits':'''apple orange lemon lime pear watermelon 
grape grapefruit cherry banana cantaloupe mango 
strawberry tomato'''.split(),

'Animals':'''bat bear beaver cat cougar crab deer dog 
donkey duck eagle fish frog goat leech lion lizard 
monkey moose mouse otter owl panda python rabbit rat 
shark sheep skunk squid tiger turkey turtle weasel 
whale wolf wombat zebra'''.split()
}


def get_random_word(word_dict: Dict[str, List[str]]) -> Tuple[str, str]:
    '''返回要猜的单词，和这个单词所属的类别'''
    # 从字典里随机选取一个键
    word_key: str = random.choice(list(word_dict.keys()))
    # 从这个键对应的单词列表里随机选取一个单词
    word: str = random.choice(word_dict[word_key])
    return word,word_key

def choose_difficulty() -> List[str]:
    '''根据用户选择的难度返回相应的图形组合
    越难，图形越少'''
    hangman_pics_copy: List[str] = HANGMAN_PICS.copy()
    # 这里一定要初始化为空格而不是空串，因为空串在任何字符串里
    difficulty: str = ' '
    while difficulty not in 'EMH':
        difficulty = input('Enter difficulty: E-Easy, M-Medium, H-Hard>>>').upper()
    if difficulty == 'M':
        del hangman_pics_copy[8]
        del hangman_pics_copy[7]
    elif difficulty == 'H':
        del hangman_pics_copy[8]
        del hangman_pics_copy[7]
        del hangman_pics_copy[5]
        del hangman_pics_copy[3]
    return hangman_pics_copy



def display_board(missed_letters: str, 
                  correct_letters: str,
                  secret_word: str,
                  hangman_pics: List[str]) -> None:
    '''这是给玩家展示信息的部分'''
    # 猜错的字母的数量正好对应要显示的图形的索引
    print(hangman_pics[len(missed_letters)])
    print(f'Missed letters: {missed_letters}')
    blanks = ['_']*len(secret_word)
    for i,letter in enumerate(secret_word):
        if letter in correct_letters:
            blanks[i] = letter
    print(' '.join(blanks))

def get_guess(already_guessed: str) -> str:
    '''获取用户输入的合法猜测'''
    while True:
        guess: str = input('Guess a letter>>>').lower()
        if len(guess) != 1:
            print('Please enter a single letter.')
        elif guess in already_guessed:
            print('You have already guessed that letter. Choose again.')
        elif guess not in 'abcdefghijklmnopqrstuvwxyz':
            print('Please enter a LETTER.')
        else:
            return guess
        
def play_again() -> bool:
    '''询问用户是否要再玩一次'''
    return input('Do you want to play again? (yes or no)').lower().startswith('y')


if __name__ == '__main__':
    print('H A N G M A N')
    # 选择游戏难度
    hangman_pics: List[str] = choose_difficulty()
    # 猜错的字母
    missed_letters: str = ''
    # 猜对的字母
    correct_letters: str = ''
    # 要猜的单词和单词所属的类别
    secret_word, secret_set = get_random_word(words)
    # 这轮游戏是否完成了（包括胜利和失败）
    game_is_done: bool = False

    while True:
        # 提醒用户要猜的单词所属的类别、
        print(f'The secret word is in the set: {secret_set}')

        # 展示信息
        display_board(missed_letters,correct_letters,secret_word,hangman_pics)
        
        # 获取用户输入
        guess = get_guess(missed_letters+correct_letters)

        if guess in secret_word:
            correct_letters += guess
            if set(correct_letters) == set(secret_word):
                print(f'Yes! The secret word is "{secret_word}" ! '
                      f'You have won!')
                game_is_done = True
        else:
            missed_letters += guess
            if len(missed_letters) == len(hangman_pics)-1:
                display_board(missed_letters,correct_letters,secret_word,hangman_pics)
                print(f'You have run out of guesses!\n'
                      f'After {len(missed_letters)} missed guess and '
                      f'{len(correct_letters)} correct guesses,'
                      f'the word was "{secret_word}".')
                game_is_done = True
        
        # 仅当一轮游戏完成了才会询问是否要再玩儿一次
        if game_is_done:
            # 如果用户选择再玩一次，就重置所有变量
            if play_again():
                missed_letters: str = ''
                correct_letters: str = ''
                secret_word, secret_set = get_random_word(words)
                game_is_done: bool = False
            else:
                break 