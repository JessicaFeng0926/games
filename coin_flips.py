import random

input('''I will flip a coin 1000 times. 
Guess how many times it will come up heads.
(Press enter to begin)''')

flips = 0
heads = 0

while flips < 1000:
    if random.randrange(0,2) == 1:
        heads += 1
    flips += 1
    
    if flips == 100:
        print(f'At 100 tosses, heads has come up {heads} times so far.')
    elif flips == 500:
        print(f'Halfway down, and heads has come up {heads} times.')
    elif flips == 900:
        print(f'900 flips and there have been {heads} heads.')
    
print(f'\nOut of 1000 coin tosses, heads come up {heads} times!')
print('Were you close?')