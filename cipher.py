# Caesar Cipher

SYMBOLS = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz'
MAX_KEY_SIZE = len(SYMBOLS)

def get_mode() -> str:
    '''获取用户想要使用的模式，是加密还是解密还是暴力破解'''
    while True:
        print('Do you wish to encrypt or decrypt  or brute-force a message?(e or d or b)')
        mode: str = input('>>>').lower()
        if mode in ['encrypt','e','decrypt','d','brute-force','b']:
            return mode
        print('Enter either "encrypt" or "e" or "decrypt" or "d" or "brute-force" or "b".')

def get_message() -> str:
    '''获取用户输入的文本'''
    return input('Enter your message:')

def get_key() -> int:
    '''获取用户的密钥'''
    while True:
        key: str = input(F'Enter the key number (1-{MAX_KEY_SIZE})>>>')
        if key.isdigit():
            key = int(key)
            if key >=1 and key<=MAX_KEY_SIZE:
                return key

def get_translated_message(mode: str, message: str, key:int) -> str:
    '''根据用户的指示加密或者解密'''
    if mode[0] == 'd':
        # 加上key是1，MAX_KEY_SIZE是52，往左走一步和往右,51步是等效的
        # 这样不管是加密还是解密，我们都统一为往右走（加法运算）
        key = MAX_KEY_SIZE-key
    translated: str = ''
    for symbol in message:
        symbol_index: int = SYMBOLS.find(symbol)
        if symbol_index == -1:
            translated += symbol
        else:
            # 为了不越界，这里要取模
            symbol_index = (symbol_index+key)%MAX_KEY_SIZE
            translated += SYMBOLS[symbol_index]

    return translated

if __name__ == '__main__':
    # 获取加密或者解密模式
    mode: str = get_mode()
    # 获取用户要加密或者解密的文本
    message:str = get_message()
    # 如果是暴力破解，就不需要密钥
    if mode[0] != 'b':
        # 获取密钥
        key: int = get_key()
    print('Your translated text is:')

    if mode[0] != 'b':
        # 展示加密或解密后的结果
        print(get_translated_message(mode,message,key)) 
    else:
        # 暴力破解就是尝试所有的Key,让用户自己判断哪一个是正确的结果
        for key in range(1,MAX_KEY_SIZE+1):
            print(key,get_translated_message('decrypt',message,key))







