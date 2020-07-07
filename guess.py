# 猜数字游戏
import random

# 获取玩家姓名
my_name = input('Hello! What is your name? >>>')
# 生成一个随机数
number = random.randrange(1,21)

print(f'Well, {my_name},'
      f' I am thinking of a number between 1 and 20.')

# 最多猜六次
for guesses_taken in range(6):
    guess = int(input('Take a guess. >>>'))
    
    if guess < number:
        print('Your guess is too low.')
    elif guess > number:
        print('Your guess is too high.')
    else:
        # 处理单位的单复数
        unit = 'time' if guesses_taken == 0 else 'times'
        print(f'Good job, {my_name}!'
              f' You guessed my number in {guesses_taken+1} {unit}!')
        break
else:
    print(f'Nope. The number I was thinking of was {number}.')




