import random 
from typing import List

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
'''
]


words = '''ant baboon badger bat bear beaver camel cat clam cobra cougar 
 coyote crow deer dog donkey duck eagle ferret fox frog goat goose hawk 
 lion lizard llama mole monkey moose mouse mule newt otter owl panda 
 parrot pigeon python rabbit ram rat raven rhino salmon seal shark sheep 
 skunk sloth snake spider stork swan tiger toad trout turkey turtle 
 weasel whale wolf wombat zebra'''.split()

def get_random_word(word_list: List[str]) -> str:
    '''生成要猜的单词'''
    return random.choice(word_list)

def display_board(missed_letters: str, 
                  correct_letters: str,
                  secret_word: str) -> None:
    '''这是给玩家展示信息的部分'''
    # 猜错的字母的数量正好对应要显示的图形的索引
    print(HANGMAN_PICS[len(missed_letters)])
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
    # 猜错的字母
    missed_letters: str = ''
    # 猜对的字母
    correct_letters: str = ''
    # 答案
    secret_word: str = get_random_word(words)
    # 这轮游戏是否完成了（包括胜利和失败）
    game_is_done: bool = False

    while True:
        # 展示信息
        display_board(missed_letters,correct_letters,secret_word)
        
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
            if len(missed_letters) == len(HANGMAN_PICS)-1:
                display_board(missed_letters,correct_letters,secret_word)
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
                secret_word: str = get_random_word(words)
                game_is_done: bool = False
            else:
                break 


    
