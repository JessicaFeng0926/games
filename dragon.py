import random
import time

def display_intro():
    print('''You are in a land full of dragons. In front of you,
you see two caves. In one cave, the dragon is friendly
and will share his treasure with you. The other dragon
is greedy and hungry, and will eat you on sight.\n''')

def choose_cave() -> str:
    '''获取并返回用户输入的洞口号码'''
    while True:
        cave = input('Which cave will you go into?(1 or 2)>>>')
        if cave == '1' or cave == '2':
            return cave

def check_cave(chosen_cave: str) -> None:
    '''根据用户选择的洞口打印个性化的信息'''
    print('You approach the cave...')
    time.sleep(2)
    print('It is dark and spooky...')
    time.sleep(2)
    print('A large dragon jumps out in front of you! He opens his jaws and...\n')
    time.sleep(2)

    friendly_cave = str(random.randrange(1,3))

    if chosen_cave == friendly_cave:
        print('Gives you his treasure!')
    else:
        print('Gobbles you down in one bite!')

if __name__ == '__main__':
    while True:
        display_intro()
        chosen_cave = choose_cave()
        check_cave(chosen_cave)
        play_again = input('Do you want to paly again?(yes or no)>>>').lower()
        if play_again != 'yes' and play_again != 'y':
            break


