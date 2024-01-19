import base64
from nltk.corpus import words
word_list = words.words()

def xor_decrypt(cipher_text,key):
    num_list = [ord(char) ^ key for char in cipher_text]
    return ''.join([num.to_bytes((num.bit_length()+7) // 8, 'big').decode() for num in num_list])


file = open('file.txt', 'r')
file = file.readlines()
truc = 0
chars=['E', 'T', 'A', 'O', 'I', 'N', 'S', 'H', 'R', 'D', 'L', 'U', 'e', 't', 'a', 'o', 'i', 'n', 's', 'h', 'r', 'd', 'l', 'u']

for line in file:
    truc += 1
    fafa = False
    try:
        for n in range(250):
            decrypt_word = xor_decrypt(line,n)
            if decrypt_word.isprintable:
                if '%' in decrypt_word or '|' in decrypt_word or 'É' in decrypt_word or ':' in decrypt_word or '?' in decrypt_word or 'ö' in decrypt_word or ';' in decrypt_word:
                    continue
                for item in chars:
                    if item in decrypt_word:
                        # print('------------------------------------------------------------------------------------')
                        # print('\n')
                        # print(f'line: {truc}\niteration: {n}\n')
                        print(decrypt_word)
                        # print('\n')
            else:
                continue
    except Exception as e:
        print(e)
        continue